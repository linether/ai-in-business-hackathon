"""Layer 8 — earliest preventable intervention. Deterministic. Owner: @linether

This is the climax of the demo (docs/spec.md §3, step 8) and the thing no
competitor outputs. Observe.AI gives a risk score; CallMiner gives aggregate
root-cause trends. Neither says *"this one could have been stopped here."*

The rule is deliberately simple and explainable: walk the case forwards and
stop at the first moment where something was owed to the customer and not
delivered. That moment is where a human could still have acted.
"""

from __future__ import annotations

from typing import List, Optional

from ..models import Case, InterventionPoint, Promise


def _earliest_broken_promise(case: Case) -> Optional[Promise]:
    broken = [
        p
        for p in case.all_promises()
        if p.fulfilled is False or (p.overdue_by_hours or 0) > 0
    ]
    if not broken:
        return None
    return min(broken, key=lambda p: p.made_at)


def find(case: Case) -> Optional[InterventionPoint]:
    promise = _earliest_broken_promise(case)
    if promise is not None:
        contact_seq = promise.evidence[0].contact_seq if promise.evidence else case.contacts[0].seq
        due = f" by {promise.due_at:%-d %b %H:%M}" if promise.due_at else ""
        return InterventionPoint(
            contact_seq=contact_seq,
            at=promise.made_at,
            what_should_have_happened=f"Deliver \"{promise.summary}\"{due}.",
            why_it_was_missed=(
                "The commitment was made on the call but no follow-through was recorded "
                "against the case before the customer made contact again."
            ),
            evidence=promise.evidence,
        )

    # Fall back to the first need that was raised and never closed.
    unresolved = [n for n in case.all_needs() if n.status.value in ("unresolved", "partial")]
    if not unresolved:
        return None
    need = min(unresolved, key=lambda n: n.raised_at)
    contact_seq = need.evidence[0].contact_seq if need.evidence else case.contacts[0].seq
    return InterventionPoint(
        contact_seq=contact_seq,
        at=need.raised_at,
        what_should_have_happened=f"Open and assign a case for \"{need.summary}\".",
        why_it_was_missed=(
            "The need was stated clearly but nothing was raised against it, so it did not "
            "reappear in anyone's queue."
        ),
        evidence=need.evidence,
    )


def recommend(case: Case, point: Optional[InterventionPoint]) -> List[dict]:
    """Suggestions only. We never execute a refund, plan change or ticket.

    Stated plainly because docs/spec.md §7 rules it out of scope and the video
    has to be honest about what is real.
    """
    from ..models import RecommendedAction

    actions: List[RecommendedAction] = []
    if point is not None:
        actions.append(
            RecommendedAction(
                label="Call the customer back within 2 hours",
                rationale=f"Owed since {point.at:%-d %b %H:%M} and still outstanding.",
                urgency="high",
            )
        )
    if any(n.status.value in ("unresolved", "partial") for n in case.all_needs()):
        actions.append(
            RecommendedAction(
                label="Raise and assign a case for the outstanding request",
                rationale="An unresolved need with no owner is what produced the repeat contact.",
                urgency="high",
            )
        )
    if len(case.contacts) >= 3:
        actions.append(
            RecommendedAction(
                label="Route to a supervisor rather than the general queue",
                rationale="Third contact on the same matter.",
                urgency="normal",
            )
        )
    return actions
