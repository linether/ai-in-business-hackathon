"""Pipeline orchestrator — wires layers 1-9 together.

Control flow is defined here in code, not by a model. That is deliberate and it
is the answer to "is this an agent?": if the steps can be listed in advance, a
workflow beats an agent — predictable, testable, cost-bounded. See
docs/architecture-upgrade.md.

    1  audio ingest          (deferred — replay path first, see decisions.md)
    2  transcribe + diarize  (ElevenLabs Scribe; scenarios ship transcripts)
    3  structured extraction                                    <- LLM
    3b citation check        verbatim string match, no LLM      <- deterministic
    4  cross-contact state
    5  resolution matching                                      <- LLM
    6  rules and timing                                         <- deterministic
    7  risk fusion                                              <- deterministic
    8  earliest intervention                                    <- deterministic
    9  evidence binding
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

from ..models import Case, CaseAnalysis, Telemetry
from . import citation, intervention, risk
from .extract import Extractor, LabelledExtractor

# The scenarios are dated early September; scoring "now" against the real clock
# would make every promise wildly overdue and flatten the demo. Pin it just past
# the last contact instead.
DEMO_NOW = datetime(2026, 9, 10, 12, 0)


def analyse(
    case: Case,
    extractor: Optional[Extractor] = None,
    now: Optional[datetime] = None,
) -> CaseAnalysis:
    started = time.time()
    extractor = extractor or LabelledExtractor()
    now = now or DEMO_NOW

    # 3 — extraction
    for contact in case.contacts:
        extracted = extractor.extract(case, contact.seq)
        if extracted is not None:
            contact.extraction = extracted

    # 3b — citation check, deterministic
    checked, rejected, uncertain = citation.verify(case)

    # 6, 7 — rules and risk fusion
    assessment = risk.assess(case, now)

    # 8 — earliest preventable intervention
    point = intervention.find(case)
    actions = intervention.recommend(case, point)

    return CaseAnalysis(
        case=case,
        risk=assessment,
        earliest_intervention=point,
        recommended_actions=actions,
        synthetic=True,
        telemetry=Telemetry(
            llm_calls=0 if extractor.name == "labelled-stub" else len(case.contacts),
            elapsed_ms=int((time.time() - started) * 1000),
            claims_extracted=checked,
            claims_rejected_by_citation_check=rejected,
            claims_marked_uncertain=uncertain,
            extractor=extractor.name,
        ),
    )
