"""Data contract for the whole pipeline.

Typing note: Optional[...] / List[...] rather than `` X | None ``, because not
everyone on this team is on Python 3.11. Runs on 3.9+.

Everyone codes against these types. If you need to change one, post to BOARD.md
first — the frontend, the extractor and the scorer all depend on this shape.

Layer numbering matches docs/spec.md section 4.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# Evidence — layer 9. Every claim the system makes must carry one of these.
# Nothing reaches the UI without a citation back to what was actually said.
# --------------------------------------------------------------------------

class Evidence(BaseModel):
    contact_seq: int = Field(description="Which contact in the case this came from, 1-based")
    utterance_index: Optional[int] = Field(
        default=None,
        description=(
            "Index into that contact's utterances, 0-based. This is the anchor the evaluation "
            "matches on — exact integer comparison, never an LLM judging whether two extractions "
            "are 'the same'. See data/scenarios/README.md."
        ),
    )
    start_s: Optional[float] = Field(default=None, description="Offset into the audio, seconds")
    speaker: Optional[str] = None
    quote: str = Field(description="Verbatim line from the transcript. Never paraphrase.")

    # Set by the citation check (layer 3b). None means the check has not run.
    citation_verified: Optional[bool] = None


# --------------------------------------------------------------------------
# Layer 2 — transcription
# --------------------------------------------------------------------------

class Speaker(str, Enum):
    CUSTOMER = "customer"
    AGENT = "agent"
    UNKNOWN = "unknown"


class Utterance(BaseModel):
    start_s: float
    end_s: float
    speaker: Speaker
    text: str


class Transcript(BaseModel):
    contact_seq: int
    language: str = "en"
    utterances: List[Utterance] = []

    def line(self, index: int) -> Utterance:
        return self.utterances[index]


# --------------------------------------------------------------------------
# Layer 3 — structured extraction (LLM)
# --------------------------------------------------------------------------

class NeedStatus(str, Enum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


class Confidence(str, Enum):
    """Third state agreed in review (docs/decisions.md, 2026-09-12).

    A claim whose evidence does not hold up is marked UNCERTAIN: it is shown in
    the UI but excluded from scoring. Saying "I am not sure" is more trustworthy
    than guessing, and it keeps a fabricated promise from ever blaming a person.
    """

    CONFIRMED = "confirmed"
    UNCERTAIN = "uncertain"


class Need(BaseModel):
    """Something the customer asked to have happen."""

    id: str
    utterance_index: Optional[int] = None
    summary: str
    raised_at: datetime
    status: NeedStatus = NeedStatus.UNKNOWN
    evidence: List[Evidence] = []
    confidence: Confidence = Confidence.CONFIRMED
    # filled by layer 5
    resolution_note: Optional[str] = None
    resolution_evidence: List[Evidence] = []


class Promise(BaseModel):
    """Something the agent said would happen. The hero of the demo — see spec §3."""

    id: str
    utterance_index: Optional[int] = None
    summary: str
    made_at: datetime
    due_at: Optional[datetime] = Field(default=None, description="Deadline, if the agent gave one")
    fulfilled: Optional[bool] = Field(default=None, description="None means we could not tell")
    evidence: List[Evidence] = []
    confidence: Confidence = Confidence.CONFIRMED
    # filled by layer 6, deterministic
    overdue_by_hours: Optional[float] = None


class Action(BaseModel):
    """Something the agent actually did during the contact.

    ``assigns_owner`` and ``contradicts`` exist so the model extracts a *fact*
    and the deterministic layer decides what it *means*. "Did this action put the
    matter in someone's queue?" is a reading-comprehension question. "Does an
    unresolved need with no owner across three contacts warrant escalation?" is a
    policy question, and policy belongs in code that can be audited.
    """

    id: str
    utterance_index: Optional[int] = None
    summary: str
    taken_at: datetime
    evidence: List[Evidence] = []
    assigns_owner: Optional[bool] = Field(
        default=None,
        description="True if this action put the matter into someone's queue (ticket, assignment, "
        "escalation). False for a note that nobody acts on. None if not determined.",
    )
    contradicts: Optional[str] = Field(
        default=None,
        description="Id of an earlier action this one contradicts — the same question answered "
        "differently. Drives the 答复矛盾 signal.",
    )


class Extraction(BaseModel):
    contact_seq: int
    needs: List[Need] = []
    promises: List[Promise] = []
    actions: List[Action] = []


# --------------------------------------------------------------------------
# Layer 4 — the case: this contact plus its history
# --------------------------------------------------------------------------

class Channel(str, Enum):
    CALL = "call"
    CHAT = "chat"
    EMAIL = "email"
    STORE = "store"


class Contact(BaseModel):
    seq: int
    occurred_at: datetime
    channel: Channel = Channel.CALL
    summary: str = ""
    transcript: Optional[Transcript] = None
    extraction: Optional[Extraction] = None


class Case(BaseModel):
    case_id: str
    customer_ref: str = "synthetic-customer"
    contacts: List[Contact] = []

    @property
    def latest(self) -> Contact:
        return max(self.contacts, key=lambda c: c.seq)

    def all_needs(self) -> List[Need]:
        return [n for c in self.contacts if c.extraction for n in c.extraction.needs]

    def all_promises(self) -> List[Promise]:
        return [p for c in self.contacts if c.extraction for p in c.extraction.promises]


# --------------------------------------------------------------------------
# Layers 6-8 — deterministic. No LLM touches anything below this line.
# Judges will ask why; the answer is that consequential decisions must be
# auditable and reproducible. See spec §4.
# --------------------------------------------------------------------------

class SignalKind(str, Enum):
    REPEAT_CONTACT = "repeat_contact"
    NO_OWNER = "no_owner"
    CONTRADICTORY_ANSWER = "contradictory_answer"
    UNRESOLVED_NEED = "unresolved_need"
    BROKEN_PROMISE = "broken_promise"
    MISSED_DEADLINE = "missed_deadline"
    REGULATOR_MENTION = "regulator_mention"
    CHURN_INTENT = "churn_intent"
    ESCALATION_REQUEST = "escalation_request"


class Signal(BaseModel):
    """One reason the risk score is what it is. Always carries evidence."""

    kind: SignalKind
    weight: int = Field(description="Points this contributes. Fixed in rules.py, never model output.")
    detail: str
    evidence: List[Evidence] = []


class RiskAssessment(BaseModel):
    score: int = Field(ge=0, le=100)
    prior_score: Optional[int] = Field(default=None, description="Score before the latest contact")
    signals: List[Signal] = []
    band: str = "low"


class InterventionPoint(BaseModel):
    """Layer 8. The climax of the demo — spec §3 step 8."""

    contact_seq: int
    at: datetime
    what_should_have_happened: str
    why_it_was_missed: str
    evidence: List[Evidence] = []


class RecommendedAction(BaseModel):
    label: str
    rationale: str
    urgency: str = "normal"


class CaseAnalysis(BaseModel):
    """What the API returns and the UI renders."""

    case: Case
    risk: RiskAssessment
    earliest_intervention: Optional[InterventionPoint] = None
    recommended_actions: List[RecommendedAction] = []
    synthetic: bool = Field(
        default=True,
        description="Always true this weekend. Surfaced in the UI so nobody mistakes it for real data.",
    )
    telemetry: "Telemetry" = Field(default_factory=lambda: Telemetry())


class Telemetry(BaseModel):
    """Instrumentation. Cheap, and the 2026 agent-architecture guidance is explicit
    that every pattern's health should be measurable from day one."""

    llm_calls: int = 0
    elapsed_ms: int = 0
    claims_extracted: int = 0
    claims_rejected_by_citation_check: int = 0
    claims_marked_uncertain: int = 0
    extractor: str = "unknown"


CaseAnalysis.model_rebuild()
