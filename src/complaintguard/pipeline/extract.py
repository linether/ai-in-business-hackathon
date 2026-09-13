"""Layer 3 — structured extraction.

**Owner: @Genicayyy** (claimed on BOARD.md, 09-12 21:18). The LLM extractor is
hers to write; this file exists so the rest of the pipeline runs end to end from
the first hour rather than waiting for it.

Two implementations behind one interface:

- ``LabelledExtractor`` reads the extraction that already sits in the scenario
  file. It needs no API key and no network, so the app is demoable immediately
  and the deterministic layers downstream can be developed and tested on real
  shapes. **It is not a model — it cannot be evaluated, because it is reading
  the answers.**
- ``LLMExtractor`` is the real one. Stub for now.

Swap by passing a different extractor to ``pipeline.analyse``; nothing else in
the codebase needs to change.
"""

from __future__ import annotations

from datetime import timedelta
from typing import List, Optional, Protocol

from ..llm import LLMClient, default_client, parse_json_object
from ..models import Case, Extraction


class Extractor(Protocol):
    """Anything that can turn a contact's transcript into structured claims."""

    name: str

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        ...


class LabelledExtractor:
    """Reads the ground-truth extraction already loaded onto the case.

    Useful for building and demoing the rest of the system. Useless for
    measuring anything — see the docstring at the top of this file.
    """

    name = "labelled-stub"

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        contact = next((c for c in case.contacts if c.seq == contact_seq), None)
        return contact.extraction if contact else None


SYSTEM = """You read transcripts of telecommunications customer-service calls and pull out \
three things, exactly as they appear: what the customer asked for, what the agent \
committed to, and what the agent actually did.

You are part of a system that helps a quality-assurance analyst work out why a \
complaint escalated. A claim you make can end up attributed to a named agent, so \
accuracy matters more than coverage.

Rules, in order of importance:

1. Quote verbatim. Copy the words exactly as they appear in the transcript. Never \
   paraphrase, tidy up grammar, or merge two lines into one quote.
2. Cite the line. Every item must carry the utterance_index it came from — the \
   0-based position in the list you were given.
3. When in doubt, leave it out. A missed promise costs us recall. An invented \
   promise blames a person who did nothing wrong. Those are not equally bad.
4. A promise is a specific commitment to a future act — "I'll have someone call you \
   back within 24 hours", "I'll raise a ticket". Sympathy is not a promise. \
   "I understand how frustrating that is" commits to nothing.
5. Deadlines only when stated. "within 24 hours" is a deadline. "as soon as \
   possible" is not — leave due_at null.

Return one JSON object and nothing else:

{
  "needs":    [{"summary": str, "utterance_index": int, "quote": str}],
  "promises": [{"summary": str, "utterance_index": int, "quote": str,
                "due_hours": int or null}],
  "actions":  [{"summary": str, "utterance_index": int, "quote": str,
                "assigns_owner": true|false|null}]
}

assigns_owner is true when the action puts the matter into someone's queue — a \
ticket raised, a case assigned, an escalation made, or the thing itself done. It is \
false for a note on the account that nobody acts on. Null if you cannot tell."""


def _user_prompt(contact) -> str:
    lines = [
        "{}. [{}] {}".format(i, u.speaker.value, u.text)
        for i, u in enumerate(contact.transcript.utterances)
    ]
    return "Contact {} on {:%d %b %Y at %H:%M}.\n\n{}".format(
        contact.seq, contact.occurred_at, "\n".join(lines)
    )


class LLMExtractor:
    """The real extractor.

    ⚠️ **First pass. @Genicayyy owns layer 3** (claimed on BOARD.md 09-12 21:18)
    — written overnight so the pipeline is not blocked, explicitly hers to
    rewrite. The prompt above encodes guesses about telecom complaint handling
    that she has actually done; where her judgement differs, hers wins.

    ⚠️ **Never exercised against the live API** — no key was available when this
    was written. The parsing, validation and failure paths are covered by tests
    with FakeLLM; genuine model behaviour is not. Treat the first real call as a
    test rather than a demo.

    Contract it has to satisfy — the rest of the pipeline depends on all four:

    1. Return an ``Extraction`` for the contact: needs, promises, actions.
    2. **Every claim carries at least one ``Evidence`` with a verbatim ``quote``
       and the ``utterance_index`` it came from.** The citation check (3b) and
       the whole evaluation both key off that index; a claim without one cannot
       be verified and will be marked UNCERTAIN.
    3. Never paraphrase inside ``quote``. Copy the words exactly as transcribed.
    4. Prefer omitting a claim over inventing one. A missed promise costs recall;
       a fabricated promise blames a person.

    Suggested shape: ask the model for strict JSON keyed by utterance index, then
    validate against the models here before returning. See
    docs/spec.md §4 and docs/architecture-upgrade.md.
    """

    name = "llm"

    def __init__(self, client: Optional[LLMClient] = None) -> None:
        self.client = client or default_client()
        self.name = "llm:{}".format(self.client.name)

    def extract(self, case: Case, contact_seq: int) -> Optional[Extraction]:
        contact = next((c for c in case.contacts if c.seq == contact_seq), None)
        if contact is None or contact.transcript is None:
            return None

        raw = self.client.complete(SYSTEM, _user_prompt(contact))
        parsed = parse_json_object(raw)
        if parsed is None:
            # Malformed response: return nothing rather than guessing. An empty
            # extraction is visible downstream; a fabricated one is not.
            return Extraction(contact_seq=contact_seq)

        return _build(contact, parsed)


def _clean(items, contact, kind: str):
    """Keep only well-formed items whose index is in range.

    Anything the model returns that we cannot tie to a real line is dropped here,
    before it reaches the citation check. Two gates are better than one: this one
    catches structural nonsense, 3b catches plausible-looking fabrication.
    """
    n = len(contact.transcript.utterances)
    out = []
    for raw in items if isinstance(items, list) else []:
        if not isinstance(raw, dict):
            continue
        idx, quote, summary = raw.get("utterance_index"), raw.get("quote"), raw.get("summary")
        if not isinstance(idx, int) or not (0 <= idx < n):
            continue
        if not isinstance(quote, str) or not quote.strip():
            continue
        if not isinstance(summary, str) or not summary.strip():
            continue
        out.append((raw, idx, quote.strip(), summary.strip()))
    return out


def _build(contact, parsed: dict) -> Extraction:
    from ..models import Action, Evidence, Need, NeedStatus, Promise

    def ev(idx: int, quote: str) -> List[Evidence]:
        u = contact.transcript.utterances[idx]
        return [
            Evidence(
                contact_seq=contact.seq,
                utterance_index=idx,
                start_s=u.start_s,
                speaker=u.speaker.value,
                quote=quote,
            )
        ]

    needs = [
        Need(
            id="n{}-{}".format(contact.seq, i),
            utterance_index=idx,
            summary=summary,
            raised_at=contact.occurred_at,
            status=NeedStatus.UNKNOWN,  # layer 5 decides this, not the extractor
            evidence=ev(idx, quote),
        )
        for i, (_, idx, quote, summary) in enumerate(_clean(parsed.get("needs"), contact, "needs"))
    ]

    promises = []
    for i, (raw, idx, quote, summary) in enumerate(_clean(parsed.get("promises"), contact, "promises")):
        due = raw.get("due_hours")
        promises.append(
            Promise(
                id="p{}-{}".format(contact.seq, i),
                utterance_index=idx,
                summary=summary,
                made_at=contact.occurred_at,
                due_at=(contact.occurred_at + timedelta(hours=due)) if isinstance(due, int) else None,
                fulfilled=None,  # layer 5 / cross-contact state decides
                evidence=ev(idx, quote),
            )
        )

    actions = []
    for i, (raw, idx, quote, summary) in enumerate(_clean(parsed.get("actions"), contact, "actions")):
        owner = raw.get("assigns_owner")
        actions.append(
            Action(
                id="a{}-{}".format(contact.seq, i),
                utterance_index=idx,
                summary=summary,
                taken_at=contact.occurred_at,
                evidence=ev(idx, quote),
                assigns_owner=owner if isinstance(owner, bool) else None,
            )
        )

    return Extraction(contact_seq=contact.seq, needs=needs, promises=promises, actions=actions)
