"""Layer 3b — citation check. Deterministic. Owner: @linether

The first of the three verification tiers agreed in review
(docs/decisions.md, 2026-09-12): **hard facts are checked by verbatim string
matching, with no LLM involved at all.**

The reasoning is worth stating on stage, because it is the whole point:

    The highest-stakes claim this system can make — that an agent promised
    something they never promised, which would blame a real person — is also
    the claim a string comparison can settle exactly.

So the safety guarantee that matters most costs one string search. The expensive
entailment check is reserved for the fuzzy claims and can wait.

A claim whose quote is not found verbatim is marked UNCERTAIN: still shown, but
excluded from scoring.
"""

from __future__ import annotations

import re
from typing import List, Tuple

from ..models import Case, Confidence, Evidence

_WS = re.compile(r"\s+")


def _norm(text: str) -> str:
    """Normalise for comparison without being permissive about content.

    Whitespace and the curly/straight apostrophe distinction are transcription
    noise. Wording is not — if the words differ, the citation fails.
    """
    return _WS.sub(" ", text.replace("’", "'").replace("‘", "'")).strip().lower()


def check_evidence(case: Case, ev: Evidence) -> bool:
    """Does this quote actually appear in the utterance it cites?"""
    contact = next((c for c in case.contacts if c.seq == ev.contact_seq), None)
    if contact is None or contact.transcript is None:
        return False

    quote = _norm(ev.quote)
    if not quote:
        return False

    if ev.utterance_index is not None:
        if not (0 <= ev.utterance_index < len(contact.transcript.utterances)):
            return False
        return quote in _norm(contact.transcript.utterances[ev.utterance_index].text)

    # No anchor given — fall back to searching the whole contact. Weaker, and the
    # extractor should always supply an index.
    return any(quote in _norm(u.text) for u in contact.transcript.utterances)


def verify(case: Case) -> Tuple[int, int, int]:
    """Check every citation on the case in place.

    Returns (claims_checked, citations_rejected, claims_marked_uncertain).
    """
    checked = rejected = uncertain = 0

    for contact in case.contacts:
        if contact.extraction is None:
            continue
        claims: List = (
            list(contact.extraction.needs)
            + list(contact.extraction.promises)
            + list(contact.extraction.actions)
        )
        for claim in claims:
            checked += 1
            evidence: List[Evidence] = list(getattr(claim, "evidence", []))
            evidence += list(getattr(claim, "resolution_evidence", []))
            if not evidence:
                # A claim with no citation at all cannot be verified, so it does
                # not get to influence the score.
                if hasattr(claim, "confidence"):
                    claim.confidence = Confidence.UNCERTAIN
                    uncertain += 1
                continue

            ok = True
            for ev in evidence:
                ev.citation_verified = check_evidence(case, ev)
                if not ev.citation_verified:
                    ok = False
                    rejected += 1
            if not ok and hasattr(claim, "confidence"):
                claim.confidence = Confidence.UNCERTAIN
                uncertain += 1

    return checked, rejected, uncertain
