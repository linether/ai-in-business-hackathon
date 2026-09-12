"""Layer 7 — risk fusion. Deterministic. Owner: @linether

The score is a capped sum of fixed signal weights. No model, no learned
parameters, no randomness: the same case always produces the same number, and
every point is traceable to a signal that carries transcript evidence.

That is the claim we make on stage, so it has to stay true.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from ..models import Case, RiskAssessment, Signal
from .rules import all_signals

BANDS = [(70, "high"), (40, "medium"), (0, "low")]


def _band(score: int) -> str:
    for threshold, label in BANDS:
        if score >= threshold:
            return label
    return "low"


def _score(signals: List[Signal]) -> int:
    return min(100, sum(s.weight for s in signals))


def assess(case: Case, now: Optional[datetime] = None) -> RiskAssessment:
    """Score the case as it stands, and as it stood before the latest contact.

    The pair matters more than the number. A demo that shows 34 → 89 tells the
    judge *what the latest contact changed*; a bare 89 tells them nothing.
    See docs/spec.md §3, step 7.
    """
    now = now or datetime.utcnow()

    signals = all_signals(case, now)
    score = _score(signals)

    prior: Optional[int] = None
    if len(case.contacts) > 1:
        latest_seq = case.latest.seq
        earlier = case.model_copy(deep=True)
        earlier.contacts = [c for c in earlier.contacts if c.seq < latest_seq]
        prior = _score(all_signals(earlier, now))

    signals.sort(key=lambda s: s.weight, reverse=True)
    return RiskAssessment(score=score, prior_score=prior, signals=signals, band=_band(score))
