"""The live room: a call a visitor can hold, and the supervisor watching it.

**The conversation is the demo. The product is the judgement about when a human
must step in.** The agent on the other end exists so there is a call to watch;
ComplaintGuard watches it and stops it. Those are not the same thing and the page
says so, because a bot that talks to customers is the most cloned product in this
category and the supervisor is not.

Two speeds, because they have different deadlines:

    fast   /live/turn    retrieve -> reply -> (speak)      the visitor waits on this
    slow   /live/watch   extract -> rules -> intervention   arrives a beat later

Running the pipeline inside the reply would put every turn past ten seconds,
which is not a conversation. Splitting them is also how a real deployment would
be built: a supervisor reacting one beat behind the call is what a human one
does.

### Why the agent does not get the policy, and the supervisor does

The first build handed the retrieved policy to the agent, and the agent stopped
making mistakes — it cited the ownership rule, escalated on the third contact and
honoured the Ombudsman mention, all correctly. That is a real finding and it is
worth stating plainly: **an agent holding the right paragraph at the right moment
handles the call well.** Front-line agents do not hold it. That gap is the whole
problem, and modelling it away made the demo dishonest in the specific direction
that flattered us.

So the agent here works from memory, under time pressure, on call thirty-seven of
forty — and retrieval moved to where it belongs, the supervisor. ComplaintGuard
looks up what the policy actually requires and checks the call against it. That
is also the right place architecturally: retrieval now serves the product rather
than decorating the prop.

**Nothing instructs the agent to fail.** Read SYSTEM below — it is the whole of
what it is told. Whatever goes wrong emerges from the constraints, and the
constraints are the ones the job really has.
"""

from __future__ import annotations

import hashlib
import os
import tempfile
import time
import uuid
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from . import knowledge
from .models import Case, Channel, Contact, SignalKind, Speaker, Transcript, Utterance

MAX_TURNS = 8
MAX_CHARS_PER_TURN = 600
# Six, not three. Judges share a campus network, so several of them arrive from
# one address and a tight per-address limit has them knocking each other out.
# The daily ceiling is the real protection; this one only stops a single visitor
# sitting on it. (It also caught me testing, which is how the number got looked at.)
PER_IP_PER_HOUR = 6
GLOBAL_PER_DAY = 25
SESSION_TTL_S = 3600
MAX_SESSIONS = 60

# Pinned so a live call has the same "now" as the prepared cases. Promises made
# during the call are therefore not instantly overdue, which would be a lie.
CALL_STARTED = datetime(2026, 9, 10, 11, 0)

_ip_hits: Dict[str, Deque[float]] = {}
_day: Tuple[str, int] = ("", 0)
_sessions: "Dict[str, Session]" = {}


class RoomError(Exception):
    """Something the visitor should see, phrased for a visitor."""


# ---------------------------------------------------------------- the switch

def room_open() -> bool:
    """The manual switch.

    Open during judging and while we are testing; closed otherwise, because every
    turn spends real transcription and speech credits and the room is a public
    URL. Flipped with ``LIVE_ROOM=on|off`` on the server — see scripts/room.sh —
    and it is checked per request, so closing it takes a restart and not a
    redeploy. Closing the room never touches /try or the twelve prepared cases.
    """
    return os.environ.get("LIVE_ROOM", "on").strip().lower() not in ("off", "0", "false", "no")


def voice_enabled() -> bool:
    """Audio can be switched off on its own, leaving the room open as text.

    Speech is ~200 credits a turn against transcription and synthesis; the text
    room is a fraction of that. If credits run low this is the thing to turn off
    first, and the room keeps working.
    """
    return os.environ.get("LIVE_VOICE", "on").strip().lower() not in ("off", "0", "false", "no")


# ---------------------------------------------------------------- the agent

SYSTEM = """You are a front-line customer service agent at Meridian Mobile, an Australian mobile \
and internet provider. You are on a live call. Reply with what you would say next, and nothing else \
— no stage directions, no labels, no quotation marks.

Your situation, which is the ordinary one for this job:

- This is call thirty-seven of about forty today and you are measured on how long each one takes.
- **You are working from memory.** You do not have the policy manual in front of you and there is no \
time to look anything up mid-call. You know roughly how things work here because you have done the \
job for a year.
- You can remove an add-on and raise a fault ticket yourself.
- You cannot approve a refund above $200, waive an exit fee, or credit an account without a team \
leader, and team leaders are usually busy.
- You can see notes on the account but not what the billing or network teams are doing with a case \
once it leaves you.
- You are Australian. Speak the way an Australian call centre agent speaks: plain, warm, brief.

How to reply:

- One or two sentences. Never more. This is speech, not an email.
- Never invent an account detail, a charge, a date, a ticket number or a name. If you would need to \
look something up, say what you would do rather than stating a fact you do not have.
- Be helpful and mean it. Do not stall, and do not be rude.
- Do not narrate your own limitations unprompted and do not apologise more than once."""


def _history(session: "Session") -> str:
    lines = []
    for u in session.utterances:
        who = "CUSTOMER" if u.speaker is Speaker.CUSTOMER else "YOU"
        lines.append("{}: {}".format(who, u.text))
    return "\n".join(lines)


# ---------------------------------------------------------------- sessions

class Session:
    def __init__(self, ip: str) -> None:
        self.id = uuid.uuid4().hex[:16]
        self.ip = ip
        self.created = time.time()
        self.utterances: List[Utterance] = []
        self.citations: Dict[int, List[str]] = {}   # agent utterance index -> policy labels
        self.turns = 0
        self.escalated = False
        self.analysis: Optional[Any] = None
        self.escalated_at_turn: Optional[int] = None

    # Offsets are nominal — there is no single audio file for a live call, but
    # every evidence link and the citation check key off the utterance index,
    # which is real.
    def add(self, speaker: Speaker, text: str) -> int:
        start = float(len(self.utterances) * 8)
        self.utterances.append(
            Utterance(start_s=start, end_s=start + 7.0, speaker=speaker, text=text.strip())
        )
        return len(self.utterances) - 1

    def case(self) -> Case:
        return Case(
            case_id="live-" + self.id,
            customer_ref="live-visitor",
            contacts=[
                Contact(
                    seq=1,
                    occurred_at=CALL_STARTED,
                    channel=Channel.CALL,
                    summary="A call held live on the site and watched as it happened.",
                    transcript=Transcript(
                        contact_seq=1, language="en", utterances=list(self.utterances)
                    ),
                )
            ],
        )

    @property
    def turns_left(self) -> int:
        return max(0, MAX_TURNS - self.turns)


def _sweep() -> None:
    now = time.time()
    for sid in [s for s, sess in _sessions.items() if now - sess.created > SESSION_TTL_S]:
        _sessions.pop(sid, None)
    while len(_sessions) > MAX_SESSIONS:
        oldest = min(_sessions, key=lambda s: _sessions[s].created)
        _sessions.pop(oldest, None)


def get(session_id: str) -> "Session":
    _sweep()
    session = _sessions.get(session_id)
    if session is None:
        raise RoomError("That call has expired. Start a new one.")
    return session


# ---------------------------------------------------------------- the budget

def _today() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def budget_left() -> Tuple[int, int]:
    today = _today()
    used = _day[1] if _day[0] == today else 0
    return max(0, GLOBAL_PER_DAY - used), GLOBAL_PER_DAY


def start(ip: str) -> Session:
    """Open a call, or explain why not. Charged at the start, not per turn."""
    global _day

    if not room_open():
        raise RoomError(
            "The live room is closed right now — it spends real transcription and speech credits "
            "and we open it for judging and testing. Everything else on the site still works: "
            "paste a transcript at /try, or open any of the twelve prepared cases."
        )

    today = _today()
    if _day[0] != today:
        _day = (today, 0)
    if _day[1] >= GLOBAL_PER_DAY:
        raise RoomError(
            "The live room has used its budget for today — it runs on a hackathon allowance. "
            "/try and the twelve prepared cases are unaffected and show the same pipeline."
        )

    now = time.time()
    hits = _ip_hits.setdefault(ip, deque())
    while hits and now - hits[0] > 3600:
        hits.popleft()
    if len(hits) >= PER_IP_PER_HOUR:
        wait = int((3600 - (now - hits[0])) / 60) + 1
        raise RoomError(
            "That is {} calls in an hour from this address, which is the limit. Another one frees "
            "up in about {} minutes. In the meantime you can paste a transcript at /try, or open "
            "any of the twelve prepared cases.".format(PER_IP_PER_HOUR, wait)
        )

    hits.append(now)
    _day = (today, _day[1] + 1)
    _sweep()
    session = Session(ip)
    _sessions[session.id] = session
    return session


# ---------------------------------------------------------------- the turn

def reply(session: Session, customer_text: str, llm) -> Dict[str, Any]:
    """One turn of the call: the visitor speaks, the agent answers.

    Deliberately does no analysis. The supervisor runs separately and arrives a
    beat later — see the module docstring.
    """
    text = (customer_text or "").strip()
    if not text:
        raise RoomError("Nothing came through. Say that again?")
    if len(text) > MAX_CHARS_PER_TURN:
        text = text[:MAX_CHARS_PER_TURN].rsplit(" ", 1)[0] + "…"
    if session.turns >= MAX_TURNS:
        raise RoomError(
            "That is {} turns, which is as long as a demo call runs. Start a new call, or open "
            "one of the prepared cases to see a whole complaint.".format(MAX_TURNS)
        )
    if session.escalated:
        raise RoomError("This call has been handed to a human. Start a new one to go again.")
    if not looks_english(text):
        raise RoomError(ENGLISH_ONLY)

    session.add(Speaker.CUSTOMER, text)

    agent_text = llm.complete(
        SYSTEM,
        _history(session) + "\n\nYOU:",
        max_tokens=160,
    ).strip()

    # Models like to prefix a label however firmly you ask them not to.
    for prefix in ("YOU:", "AGENT:", "Agent:", "You:"):
        if agent_text.startswith(prefix):
            agent_text = agent_text[len(prefix):].strip()
    agent_text = agent_text.strip('"').strip()
    if not agent_text:
        raise RoomError("The agent did not answer. Try that turn again.")

    session.add(Speaker.AGENT, agent_text)
    session.turns += 1

    return {
        "customer_text": text,
        "agent_text": agent_text,
        "audio": speak(agent_text),
        "turn": session.turns,
        "turns_left": session.turns_left,
    }


# ---------------------------------------------------------------- the watcher

def watch(session: Session, llm) -> Dict[str, Any]:
    """The supervisor. Runs the real pipeline over the call so far.

    Layer 5 is skipped: it reconciles a need on one contact against an action on
    another, and a live call is one contact. Everything that scores is the same
    deterministic code the twelve prepared cases run.
    """
    from . import pipeline
    from .pipeline import live_rules, risk as risk_layer
    from .pipeline.extract import LLMExtractor

    if len(session.utterances) < 2:
        return {"ready": False}

    case = session.case()
    analysis = pipeline.analyse(
        case,
        extractor=LLMExtractor(llm),
        now=CALL_STARTED,
        resolve=False,
    )

    # Layer 6b — the signals that only exist inside a live call, including the
    # policy checks. Merged here rather than inside risk.assess() so the twelve
    # prepared cases and the evaluation harness run exactly the code they always
    # ran; nothing in this route can change a published number.
    extra = live_rules.all_live_signals(analysis.case)
    existing = {s.kind for s in analysis.risk.signals}
    for signal in extra:
        # A live signal never displaces one the case-file rules already found.
        if signal.kind in existing and signal.kind is not SignalKind.UNRESOLVED_NEED:
            continue
        analysis.risk.signals.append(signal)

    analysis.risk.score = min(100, sum(s.weight for s in analysis.risk.signals))
    analysis.risk.band = risk_layer._band(analysis.risk.score)
    session.analysis = analysis

    point = analysis.earliest_intervention
    escalate = point is not None or analysis.risk.score >= 70
    if escalate and not session.escalated:
        session.escalated = True
        session.escalated_at_turn = session.turns

    signals = [
        {
            "kind": s.kind.value.replace("_", " "),
            "weight": s.weight,
            "detail": s.detail,
            "policy": getattr(s, "_policy", None),
            "quotes": [
                {"index": e.utterance_index, "speaker": e.speaker, "quote": e.quote}
                for e in s.evidence
                if e.utterance_index is not None
            ],
        }
        for s in analysis.risk.signals
    ]

    # When no intervention point exists — it needs a contradiction or an overdue
    # promise, and a five-minute call may have neither — say what actually took
    # the call over instead of quoting a threshold at the supervisor. The heaviest
    # signal is the honest answer: it is the one that moved the number most.
    if point is None and session.escalated and analysis.risk.signals:
        top = max(analysis.risk.signals, key=lambda s: s.weight)
        fallback = {
            "what": _WHAT_TO_DO.get(
                top.kind.value,
                "Take this call from the agent and deal with the outstanding matter directly.",
            ),
            "why": top.detail,
            "quotes": [
                {"index": e.utterance_index, "speaker": e.speaker, "quote": e.quote}
                for e in top.evidence
                if e.utterance_index is not None
            ],
        }
    else:
        fallback = None

    return {
        "ready": True,
        "score": analysis.risk.score,
        "band": analysis.risk.band,
        "signals": signals,
        "escalate": session.escalated,
        "escalated_at_turn": session.escalated_at_turn,
        "turn": session.turns,
        "telemetry": {
            "llm_calls": analysis.telemetry.llm_calls,
            "claims": analysis.telemetry.claims_extracted,
            "rejected": analysis.telemetry.claims_rejected_by_citation_check,
            "uncertain": analysis.telemetry.claims_marked_uncertain,
            "elapsed_ms": analysis.telemetry.elapsed_ms,
        },
        "intervention": fallback if point is None else {
            "what": point.what_should_have_happened,
            "why": point.why_it_was_missed,
            "quotes": [
                {"index": e.utterance_index, "speaker": e.speaker, "quote": e.quote}
                for e in point.evidence
                if e.utterance_index is not None
            ],
        },
    }


# What a supervisor should actually do, per signal. Plain instructions, written
# once, because "risk is high" is not an action and a supervisor taking the call
# needs to know what they are taking it for.
_WHAT_TO_DO = {
    "regulator_mention": "Take the call now. The customer has named the Ombudsman, which starts a "
                         "clock we cannot stop later — a team leader has to speak to them on this call.",
    "churn_intent": "Take the call now. The customer has said they are leaving, and the matter they "
                    "rang about is still open — resolve that before anyone discusses the contract.",
    "no_owner": "Take the call and put your name on it. The matter has been handed to a team and "
                "nobody on this call became answerable for it.",
    "repeat_contact": "Take the call. The customer says they have been here before and the matter is "
                      "still not resolved, which is the pattern that ends at the Ombudsman.",
    "unresolved_need": "Take the call. What the policy required has not happened, and the customer "
                       "is still waiting for it.",
    "broken_promise": "Take the call. A commitment made to this customer was not kept.",
    "missed_deadline": "Take the call. A deadline we set ourselves has passed without contact.",
    "service_loss": "Take the call. The customer is paying for a service they cannot currently use.",
    "contradictory_answer": "Take the call. This customer has been told two different things and is "
                            "being asked to prove which.",
    "escalation_request": "Take the call. The customer asked for a team leader, which is not a "
                          "request the agent gets to assess.",
}


def text_hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()[:20]


OPENERS = [
    "I rang last week about a charge I never signed up for and nobody has called me back.",
    "My internet has been dropping out every night for two weeks and nothing has been done.",
    "I was told my add-on would be removed and refunded. It is still on my bill.",
]


# ---------------------------------------------------------------- the voice

VOICE_DIR = Path(tempfile.gettempdir()) / "complaintguard-voice"
_voice_seen: Deque[str] = deque()
MAX_VOICE_FILES = 400


def speak(text: str) -> Optional[str]:
    """Synthesise the agent's line. Returns a URL, or None — never raises.

    Cached by the text itself, so a reply the agent has given before costs
    nothing: the demo scripts get repeated a great many times before a judge sees
    them, and speech is the expensive half of this route at roughly a credit a
    character.

    Failure is silent on purpose. If ElevenLabs is slow, out of credits, or
    simply down, the visitor reads the reply instead of hearing it and the call
    carries on. Losing the audio is a worse demo; losing the call is a broken one.
    """
    if not voice_enabled():
        return None
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return None

    digest = text_hash(text)
    path = VOICE_DIR / (digest + ".mp3")
    if path.exists():
        return "/live/say/" + digest

    try:
        from .audio import tts

        VOICE_DIR.mkdir(parents=True, exist_ok=True)
        tts.synth(text, "agent", path, key)
    except Exception:  # noqa: BLE001 — any failure means "no audio", not "no call"
        return None

    _voice_seen.append(digest)
    while len(_voice_seen) > MAX_VOICE_FILES:
        old = _voice_seen.popleft()
        try:
            (VOICE_DIR / (old + ".mp3")).unlink()
        except OSError:
            pass
    return "/live/say/" + digest


def voice_path(digest: str) -> Optional[Path]:
    """Resolve a digest to a file, refusing anything that is not one.

    The digest comes back from the browser, so it is checked rather than trusted:
    32 hex characters at most and no path separators, resolved inside VOICE_DIR.
    """
    if not digest or len(digest) > 32 or not all(c in "0123456789abcdef" for c in digest):
        return None
    path = VOICE_DIR / (digest + ".mp3")
    return path if path.exists() else None


# ---------------------------------------------------------------- the ear

MAX_AUDIO_BYTES = 2_000_000   # roughly 20 seconds of Opus at browser defaults


def hear(blob: bytes, filename: str = "turn.webm") -> str:
    """Transcribe one spoken turn. One voice, so no diarisation is needed.

    `audio/stt.py` is reused unchanged — it already caches by file digest and
    already knows Scribe's word-stream format. Diarisation is off here because a
    turn is one person speaking; asking for two speakers on a single voice
    produces a second speaker that does not exist.
    """
    if not blob:
        raise RoomError("Nothing was recorded. Hold the button while you speak.")
    if len(blob) > MAX_AUDIO_BYTES:
        raise RoomError("That was too long. Keep a turn under about twenty seconds.")
    if not os.environ.get("ELEVENLABS_API_KEY"):
        raise RoomError("Speech input is not configured on this deployment. Type instead.")

    import httpx

    resp = httpx.post(
        "https://api.elevenlabs.io/v1/speech-to-text",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
        data={"model_id": os.environ.get("EL_STT_MODEL", "scribe_v2"), "diarize": "false"},
        files={"file": (filename, blob, "application/octet-stream")},
        timeout=45,
    )
    resp.raise_for_status()
    text = (resp.json().get("text") or "").strip()
    if not text:
        raise RoomError("Nothing came through clearly. Try that again, or type it.")
    return text


# ---------------------------------------------------------------- language

# Scripts the supervisor cannot read. Not an exhaustive list of the world's
# writing systems — just the ones a visitor to this site is likely to type.
_NON_LATIN = (
    (0x4E00, 0x9FFF),    # CJK unified ideographs
    (0x3400, 0x4DBF),    # CJK extension A
    (0x3040, 0x30FF),    # hiragana + katakana
    (0xAC00, 0xD7AF),    # hangul syllables
    (0x0400, 0x04FF),    # cyrillic
    (0x0590, 0x05FF),    # hebrew
    (0x0600, 0x06FF),    # arabic
    (0x0E00, 0x0E7F),    # thai
)


def non_latin_count(text: str) -> int:
    total = 0
    for ch in text:
        code = ord(ch)
        for lo, hi in _NON_LATIN:
            if lo <= code <= hi:
                total += 1
                break
    return total


def looks_english(text: str) -> bool:
    """Whether the supervisor can actually read this.

    Counts characters in scripts the rules cannot match, rather than anything
    cleverer — accented Latin is fine (``café``, a name like ``Ruairí``), two
    CJK characters are not.

    The check exists because failing silently here would be worse than not
    supporting the language at all. The three layers of the *conversation* —
    Scribe, the model, ElevenLabs — all handle Chinese perfectly well, so a
    visitor typing Chinese gets a fluent agent and a supervisor panel frozen at
    zero: the product looks broken in exactly the place it is meant to be good.
    Saying so plainly costs one sentence and is the honest answer.
    """
    return non_latin_count(text) < 2


ENGLISH_ONLY = (
    "This demo reads English only. The agent would answer you in any language — but the part "
    "we built, the supervisor, matches against English policy wording and would sit at zero "
    "and tell you nothing, which would be worse than saying this. Try:  "
    "“I rang last week about a charge I never signed up for and nobody called me back.”"
)
