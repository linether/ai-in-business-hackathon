"""Layer 6 — deterministic timing and rule checks.

Owner: @linether

**No LLM output reaches this file.** Everything here is arithmetic and keyword
matching against a fixed list. That is deliberate and it is the answer to the
judges' "why this architecture" question: anything that affects a human
decision — scoring an agent, flagging a case, triggering a callback — has to be
auditable and reproducible. Models extract; code decides.

See docs/spec.md §4 and docs/judges.md (Rashmika Nawaratne, Tom Porter).
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from ..models import Case, Evidence, Signal, SignalKind

# Fixed weights. Tuned by hand, never learned, never model-generated, so that
# any score can be explained line by line on stage.
WEIGHTS = {
    SignalKind.REPEAT_CONTACT: 12,
    SignalKind.UNRESOLVED_NEED: 15,
    SignalKind.BROKEN_PROMISE: 22,
    SignalKind.MISSED_DEADLINE: 18,
    SignalKind.REGULATOR_MENTION: 25,
    SignalKind.CHURN_INTENT: 20,
    SignalKind.ESCALATION_REQUEST: 10,
}

# Deliberately small and inspectable. Extend from real scenario scripts, not
# from a model's imagination.
REGULATOR_TERMS = [
    "ombudsman", "tio", "regulator", "acma", "complaint to the",
    "工信部", "投诉到", "监管", "消协",
]
CHURN_TERMS = [
    "cancel my", "switch to", "port out", "leave you", "another provider",
    "close my account", "转网", "销户", "换运营商", "不用你们了",
]
ESCALATION_TERMS = [
    "supervisor", "manager", "escalate", "someone senior",
    "主管", "上级", "投诉你",
]


def _match(text: str, terms: List[str]) -> bool:
    lowered = text.lower()
    return any(t in lowered for t in terms)


def timing_signals(case: Case, now: datetime) -> List[Signal]:
    """Promises whose deadline has passed without being fulfilled.

    This is the single most important signal in the product. "You said you'd
    call back within 24 hours and you didn't" is concrete, checkable, and maps
    straight to an action — see docs/spec.md §3, step 4.
    """
    signals: List[Signal] = []
    for promise in case.all_promises():
        if promise.fulfilled:
            continue
        if promise.due_at is None:
            continue
        if promise.due_at >= now:
            continue

        overdue = (now - promise.due_at).total_seconds() / 3600.0
        promise.overdue_by_hours = round(overdue, 1)
        signals.append(
            Signal(
                kind=SignalKind.MISSED_DEADLINE,
                weight=WEIGHTS[SignalKind.MISSED_DEADLINE],
                detail=(
                    f"Promise \"{promise.summary}\" was due "
                    f"{promise.due_at:%-d %b %H:%M} and is {overdue:.0f}h overdue."
                ),
                evidence=promise.evidence,
            )
        )
    return signals


def promise_signals(case: Case) -> List[Signal]:
    """Promises explicitly known to be unfulfilled, deadline or not."""
    signals: List[Signal] = []
    for promise in case.all_promises():
        if promise.fulfilled is False:
            signals.append(
                Signal(
                    kind=SignalKind.BROKEN_PROMISE,
                    weight=WEIGHTS[SignalKind.BROKEN_PROMISE],
                    detail=f"Agent promised \"{promise.summary}\" and it did not happen.",
                    evidence=promise.evidence,
                )
            )
    return signals


def unresolved_signals(case: Case) -> List[Signal]:
    signals: List[Signal] = []
    for need in case.all_needs():
        if need.status.value in ("unresolved", "partial"):
            signals.append(
                Signal(
                    kind=SignalKind.UNRESOLVED_NEED,
                    weight=WEIGHTS[SignalKind.UNRESOLVED_NEED],
                    detail=f"Customer need \"{need.summary}\" is still {need.status.value}.",
                    evidence=need.evidence,
                )
            )
    return signals


def repeat_contact_signals(case: Case) -> List[Signal]:
    """Contacting three times about the same thing is a fact, not a feeling.

    Note this is counted from the case history, not inferred from tone. A calm
    customer on their third call is higher risk than an angry one on their
    first — see docs/proposals/genicayyy-complaintguard.md, "Hardest part".
    """
    count = len(case.contacts)
    if count < 2:
        return []
    return [
        Signal(
            kind=SignalKind.REPEAT_CONTACT,
            weight=WEIGHTS[SignalKind.REPEAT_CONTACT] * (count - 1),
            detail=f"{count} contacts about the same unresolved matter.",
            evidence=[],
        )
    ]


def language_signals(case: Case) -> List[Signal]:
    """Keyword matches on customer utterances only.

    Kept deterministic on purpose: a regulator mention is a hard fact about what
    was said, and we want the same input to produce the same flag every time.
    """
    signals: List[Signal] = []
    checks = [
        (SignalKind.REGULATOR_MENTION, REGULATOR_TERMS, "Customer referred to an external regulator."),
        (SignalKind.CHURN_INTENT, CHURN_TERMS, "Customer signalled intent to leave."),
        (SignalKind.ESCALATION_REQUEST, ESCALATION_TERMS, "Customer asked to escalate."),
    ]
    for contact in case.contacts:
        if contact.transcript is None:
            continue
        for utterance in contact.transcript.utterances:
            if utterance.speaker.value != "customer":
                continue
            for kind, terms, detail in checks:
                if _match(utterance.text, terms) and not any(s.kind == kind for s in signals):
                    signals.append(
                        Signal(
                            kind=kind,
                            weight=WEIGHTS[kind],
                            detail=detail,
                            evidence=[
                                Evidence(
                                    contact_seq=contact.seq,
                                    start_s=utterance.start_s,
                                    speaker=utterance.speaker.value,
                                    quote=utterance.text,
                                )
                            ],
                        )
                    )
    return signals


def all_signals(case: Case, now: datetime) -> List[Signal]:
    return (
        promise_signals(case)
        + timing_signals(case, now)
        + unresolved_signals(case)
        + repeat_contact_signals(case)
        + language_signals(case)
    )
