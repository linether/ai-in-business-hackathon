"""The "try it yourself" path: a pasted transcript, analysed live.

Isolated on purpose. Everything here is self-contained and every failure is
caught and returned as a message, so a broken model call, an exhausted budget or
a malformed paste can never take down the twelve prepared cases — those stay
deterministic, instant, and free.

Three limits, because this endpoint is public and it spends money:

    per request   characters capped, so one paste cannot be enormous
    per visitor   a handful of runs an hour, keyed by address
    per day       a hard ceiling for everyone, after which the form politely
                  closes and the prepared cases carry on working

Identical text is served from cache, so re-submitting costs nothing.
"""

from __future__ import annotations

import hashlib
import re
import time
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Optional, Tuple

from .models import Case, Channel, Contact, Speaker, Transcript, Utterance

MAX_CHARS = 6000
MAX_LINES = 60
PER_IP_PER_HOUR = 6
GLOBAL_PER_DAY = 80
CACHE_MAX = 200

# Be generous about how the label is written, strict about who is speaking.
# Two shapes, because the punctuation rules differ: a bracketed label stands on
# its own ("[Agent] hello"), a bare one needs a separator or "Agent smith called"
# would parse as the agent saying "smith called".
_NAMES = r"customer|caller|client|agent|rep|representative|advisor|operator"
_SPEAKER_PATTERNS = (
    re.compile(r"^\s*[\[\(]\s*(" + _NAMES + r")\s*[\]\)]\s*[:\-–—]?\s*(.+)$", re.I),
    re.compile(r"^\s*(" + _NAMES + r")\s*[:\-–—]\s*(.+)$", re.I),
)


def _speaker_line(raw: str):
    for pattern in _SPEAKER_PATTERNS:
        m = pattern.match(raw)
        if m:
            return m.group(1).lower(), m.group(2).strip()
    return None
_AGENT_WORDS = {"agent", "rep", "representative", "advisor", "operator"}

try:
    # So that a key sitting in .env works when someone runs uvicorn directly, the
    # way the README tells them to. In the container the key arrives through
    # env_file and this finds nothing, which is the correct no-op.
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover - python-dotenv is a listed dependency
    pass

_ip_hits: Dict[str, Deque[float]] = {}
_day: Tuple[str, int] = ("", 0)
_cache: Dict[str, object] = {}
_cache_order: Deque[str] = deque()


class LiveError(Exception):
    """Something the visitor should see, phrased for a visitor."""


def parse_transcript(text: str) -> Case:
    """Turn pasted dialogue into a one-contact Case.

    Deliberately forgiving about formatting and unforgiving about ambiguity: a
    line without a recognisable speaker is rejected with the line quoted back,
    rather than guessed at. Guessing who said something is exactly the mistake
    this whole project exists to avoid.
    """
    text = (text or "").strip()
    if not text:
        raise LiveError("Paste a short call transcript first.")
    if len(text) > MAX_CHARS:
        raise LiveError(
            "That is {:,} characters and the limit is {:,}. "
            "A few minutes of conversation is plenty.".format(len(text), MAX_CHARS)
        )

    utterances: List[Utterance] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        parsed = _speaker_line(raw)
        if parsed is None:
            raise LiveError(
                'Could not tell who is speaking on this line: "{}". '
                'Start each line with "customer:" or "agent:".'.format(raw.strip()[:70])
            )
        who, said = parsed
        if not said:
            continue
        speaker = Speaker.AGENT if who in _AGENT_WORDS else Speaker.CUSTOMER
        # Offsets are nominal — there is no audio here, but the evidence links
        # and the citation check both key off the utterance index, which is real.
        start = float(len(utterances) * 6)
        utterances.append(Utterance(start_s=start, end_s=start + 5.5, speaker=speaker, text=said))

    if len(utterances) < 2:
        raise LiveError("That is only one line. Paste at least a short exchange.")
    if len(utterances) > MAX_LINES:
        raise LiveError("That is {} lines; the limit is {}.".format(len(utterances), MAX_LINES))

    occurred = datetime(2026, 9, 8, 10, 0)
    return Case(
        case_id="live",
        customer_ref="pasted-by-visitor",
        contacts=[
            Contact(
                seq=1,
                occurred_at=occurred,
                channel=Channel.CALL,
                summary="Pasted by a visitor and analysed live.",
                transcript=Transcript(contact_seq=1, language="en", utterances=utterances),
            )
        ],
    )


def _today() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def check_budget(ip: str) -> None:
    """Raise LiveError if this request should not spend money."""
    global _day

    today = _today()
    if _day[0] != today:
        _day = (today, 0)
    if _day[1] >= GLOBAL_PER_DAY:
        raise LiveError(
            "The live demo has used its budget for today — it runs on a hackathon allowance. "
            "The twelve prepared cases below still work, and they show the same pipeline."
        )

    now = time.time()
    hits = _ip_hits.setdefault(ip, deque())
    while hits and now - hits[0] > 3600:
        hits.popleft()
    if len(hits) >= PER_IP_PER_HOUR:
        wait = int((3600 - (now - hits[0])) / 60) + 1
        raise LiveError(
            "That is {} runs in an hour from here, which is the limit. "
            "Try again in about {} minutes, or browse the prepared cases.".format(
                PER_IP_PER_HOUR, wait
            )
        )


def spend(ip: str) -> None:
    """Record a run that actually cost something."""
    global _day
    _day = (_today(), _day[1] + 1)
    _ip_hits.setdefault(ip, deque()).append(time.time())


def cache_key(text: str) -> str:
    return hashlib.sha256(" ".join(text.split()).lower().encode("utf-8")).hexdigest()[:24]


def cached(key: str):
    return _cache.get(key)


def remember(key: str, analysis) -> None:
    if key in _cache:
        return
    _cache[key] = analysis
    _cache_order.append(key)
    while len(_cache_order) > CACHE_MAX:
        _cache.pop(_cache_order.popleft(), None)


def budget_left() -> Tuple[int, int]:
    today = _today()
    used = _day[1] if _day[0] == today else 0
    return max(0, GLOBAL_PER_DAY - used), GLOBAL_PER_DAY


SAMPLE = """customer: I rang last Tuesday about a charge I never signed up for, and I was told someone would call me back within two days.
agent: I can see a note on the account, yes.
customer: Nobody called. That was a week ago.
agent: I'm sorry about that. I'll chase it up with the billing team and get back to you.
customer: That is what the last person said. I'd like to know who is actually dealing with it.
agent: It goes into the queue for them to review. I can't see an individual name from here.
customer: Then I'll take it to the Ombudsman, and I'll be moving my number once the contract is up."""


def client():
    """An LLM client tuned for a person waiting in front of a browser.

    45 seconds, not the harness's 180. Two calls run per analysis — extraction
    and resolution — so the worst case a visitor can wait is bounded, and a
    hung provider cannot sit on a worker thread the prepared pages also use.
    """
    import os

    from .llm import AnthropicClient, OpenAICompatClient

    if os.environ.get("DEEPSEEK_API_KEY"):
        return OpenAICompatClient(timeout=45)
    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicClient()
    raise LiveError(
        "Live analysis is not configured on this deployment — it needs a model key. "
        "The twelve prepared cases below run without one."
    )


def configured() -> bool:
    import os

    return bool(os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))
