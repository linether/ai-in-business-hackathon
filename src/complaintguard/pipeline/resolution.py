"""Layer 5 — resolution matching. Cross-contact. Uses an LLM.

⚠️ **First pass. Layer 5 sits inside @Genicayyy's claimed area** (main pipeline
+ extraction). Written overnight so nothing downstream is blocked; hers to change.

⚠️ **Never exercised against the live API.** Parsing and failure handling are
tested with FakeLLM; model behaviour is not.

The extractor works one contact at a time and cannot know whether a need raised
on Monday was dealt with on Thursday. This layer sees the whole case and decides
two things:

    need.status       resolved / partial / unresolved
    promise.fulfilled True / False / None

Why an LLM: matching "refund the two months I've already paid" against "the
credit went on this morning" is a reading-comprehension problem. Why not for the
rest: what those statuses *mean* for escalation is policy, and policy stays in
rules.py where it can be audited.

The third state matters here. A promise nobody mentioned again is **not** a
broken promise — it is an unknown one, and it stays None rather than counting
against an agent.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..llm import AnthropicClient, LLMClient, parse_json_object
from ..models import Case, Confidence, NeedStatus

SYSTEM = """You are given everything that happened across a customer's contacts with \
their telco: what they asked for, what agents committed to, and what agents did.

Decide, for each item, whether it actually got dealt with.

For each need, answer resolved, partial, or unresolved:
  resolved    the thing the customer wanted happened
  partial     some of it happened, or it happened for one of several requests
  unresolved  it did not happen, or it is still pending at the last contact

For each promise, answer true, false, or null:
  true   the committed act demonstrably happened
  false  the deadline passed, or a later contact shows it did not happen
  null   nothing in the record shows either way

Two things to hold on to:

Delivering a callback is not the same as solving the problem. If an agent promised \
to ring back and did ring back, the promise is true — even if the call itself \
changed nothing. Judge the promise and the need separately.

Never guess a promise into false. "False" means an agent failed to do something \
they said they would, and that gets attributed to a person. If the record is \
silent, the answer is null.

Return one JSON object and nothing else:

{
  "needs":    [{"id": str, "status": "resolved"|"partial"|"unresolved", "why": str}],
  "promises": [{"id": str, "fulfilled": true|false|null, "why": str}]
}"""


def _case_digest(case: Case) -> str:
    parts: List[str] = []
    for contact in sorted(case.contacts, key=lambda c: c.seq):
        parts.append(
            "--- Contact {} · {:%d %b %H:%M} ---".format(contact.seq, contact.occurred_at)
        )
        ex = contact.extraction
        if not ex:
            parts.append("(nothing extracted)")
            continue
        for n in ex.needs:
            parts.append('NEED {}: {}'.format(n.id, n.summary))
        for p in ex.promises:
            due = " (due {:%d %b %H:%M})".format(p.due_at) if p.due_at else ""
            parts.append('PROMISE {}: {}{}'.format(p.id, p.summary, due))
        for a in ex.actions:
            owner = "" if a.assigns_owner is None else (
                " [assigned]" if a.assigns_owner else " [no owner]"
            )
            parts.append('DID {}: {}{}'.format(a.id, a.summary, owner))
    return "\n".join(parts)


def resolve(case: Case, client: Optional[LLMClient] = None) -> int:
    """Fill in statuses across the case, in place. Returns the LLM call count."""
    if not any(c.extraction for c in case.contacts):
        return 0

    client = client or AnthropicClient()
    raw = client.complete(SYSTEM, _case_digest(case), max_tokens=1500)
    parsed = parse_json_object(raw)
    if parsed is None:
        # Leave every status as the extractor left it. Unknown is a safe default;
        # a guessed "unresolved" is not.
        return 1

    _apply(case, parsed)
    return 1


def _apply(case: Case, parsed: Dict[str, Any]) -> None:
    needs = {n.id: n for n in case.all_needs()}
    promises = {p.id: p for p in case.all_promises()}

    for row in parsed.get("needs") or []:
        if not isinstance(row, dict):
            continue
        need = needs.get(row.get("id"))
        if need is None:
            continue
        try:
            need.status = NeedStatus(row.get("status"))
        except ValueError:
            continue
        if isinstance(row.get("why"), str):
            need.resolution_note = row["why"].strip()

    for row in parsed.get("promises") or []:
        if not isinstance(row, dict):
            continue
        promise = promises.get(row.get("id"))
        if promise is None:
            continue
        value = row.get("fulfilled")
        if value is None or isinstance(value, bool):
            promise.fulfilled = value
        # A model that cannot say either way leaves the promise unknown, and an
        # unknown promise never becomes a broken-promise signal in rules.py.
        if value is None and promise.confidence is Confidence.CONFIRMED:
            pass
