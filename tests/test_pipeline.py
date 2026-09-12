"""Offline tests. No API key, no network.

Everything that can go wrong between the model and the score is exercised here:
malformed JSON, out-of-range indexes, fabricated quotes, missing fields. The only
thing left untested is how a real model actually behaves, which needs a key.

Run:  PYTHONPATH=src .venv/bin/python -m pytest tests -q
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from complaintguard import pipeline, scenarios  # noqa: E402
from complaintguard.llm import FakeLLM, parse_json_object  # noqa: E402
from complaintguard.models import Confidence  # noqa: E402
from complaintguard.pipeline import citation  # noqa: E402
from complaintguard.pipeline.extract import LabelledExtractor, LLMExtractor  # noqa: E402

CASE = scenarios.SCENARIO_DIR / "demo-001.json"


# --------------------------------------------------------------------- parsing

def test_parses_bare_json():
    assert parse_json_object('{"a": 1}') == {"a": 1}


def test_parses_fenced_json():
    assert parse_json_object('here you go:\n```json\n{"a": 1}\n```\nhope that helps') == {"a": 1}


def test_parses_json_buried_in_prose():
    assert parse_json_object('Sure! {"a": 1} Let me know.') == {"a": 1}


def test_returns_none_on_garbage():
    assert parse_json_object("no json here at all") is None
    assert parse_json_object("") is None


# ------------------------------------------------------------------ extraction

def _extract(response: str):
    case = scenarios.load_case(CASE, with_labels=False)
    ex = LLMExtractor(client=FakeLLM([response])).extract(case, 1)
    return case, ex


def test_extracts_a_well_formed_promise():
    _, ex = _extract(json.dumps({
        "needs": [],
        "promises": [{"summary": "Call back within 24 hours", "utterance_index": 3,
                      "quote": "I'll have someone call you back within 24 hours",
                      "due_hours": 24}],
        "actions": [],
    }))
    assert len(ex.promises) == 1
    p = ex.promises[0]
    assert p.utterance_index == 3
    assert p.due_at == datetime(2026, 9, 4, 10, 12)
    assert p.fulfilled is None, "the extractor must not decide fulfilment — layer 5 does"
    assert p.evidence[0].utterance_index == 3


def test_malformed_response_yields_nothing_rather_than_guesses():
    _, ex = _extract("the model had a bad day")
    assert ex.needs == [] and ex.promises == [] and ex.actions == []


def test_drops_items_with_an_out_of_range_index():
    _, ex = _extract(json.dumps({
        "promises": [{"summary": "x", "utterance_index": 999, "quote": "x"}],
        "needs": [], "actions": [],
    }))
    assert ex.promises == []


def test_drops_items_missing_required_fields():
    _, ex = _extract(json.dumps({
        "promises": [
            {"summary": "no index", "quote": "x"},
            {"utterance_index": 0, "quote": "no summary"},
            {"summary": "no quote", "utterance_index": 0},
            {"summary": "", "utterance_index": 0, "quote": "blank summary"},
        ],
        "needs": [], "actions": [],
    }))
    assert ex.promises == []


def test_tolerates_wrong_types_throughout():
    _, ex = _extract(json.dumps({"needs": "not a list", "promises": [42, None], "actions": {}}))
    assert ex.needs == [] and ex.promises == [] and ex.actions == []


# -------------------------------------------------------------- citation check

def test_citation_accepts_a_verbatim_quote():
    case = scenarios.load_case(CASE)
    ev = case.contacts[0].extraction.promises[0].evidence[0]
    assert citation.check_evidence(case, ev) is True


def test_citation_rejects_an_invented_quote():
    """The failure that matters: a promise the agent never made."""
    case = scenarios.load_case(CASE)
    ev = case.contacts[0].extraction.promises[0].evidence[0]
    ev.quote = "I promise a full refund today, no questions asked"
    assert citation.check_evidence(case, ev) is False


def test_citation_rejects_a_quote_from_the_wrong_line():
    case = scenarios.load_case(CASE)
    ev = case.contacts[0].extraction.promises[0].evidence[0]
    ev.utterance_index = 0  # real words, wrong line
    assert citation.check_evidence(case, ev) is False


def test_citation_ignores_whitespace_and_curly_apostrophes():
    case = scenarios.load_case(CASE)
    ev = case.contacts[0].extraction.promises[0].evidence[0]
    ev.quote = "  I’ll   have someone call you back within 24 hours  "
    assert citation.check_evidence(case, ev) is True


def test_failed_citation_marks_the_claim_uncertain_and_keeps_it_out_of_the_score():
    case = scenarios.load_case(CASE)
    case.contacts[0].extraction.promises[0].evidence[0].quote = "words never spoken"

    analysis = pipeline.analyse(case)
    promise = analysis.case.contacts[0].extraction.promises[0]

    assert promise.confidence is Confidence.UNCERTAIN
    assert analysis.telemetry.claims_marked_uncertain >= 1
    assert not any(
        s.kind.value == "broken_promise" and promise.summary in s.detail
        for s in analysis.risk.signals
    ), "an unverified promise must never become a signal against an agent"


# ------------------------------------------------------- deterministic scoring

def test_every_scenario_matches_its_ground_truth():
    for path in scenarios.list_scenarios():
        case = scenarios.load_case(path)
        gt = scenarios.ground_truth(path)
        a = pipeline.analyse(case)

        assert (a.risk.score >= 40) is bool(gt["should_escalate"]), path.stem
        got = a.earliest_intervention.contact_seq if a.earliest_intervention else None
        assert got == gt["earliest_intervention_contact_seq"], path.stem


def test_scoring_is_deterministic():
    first = pipeline.analyse(scenarios.load_case(CASE)).risk.score
    for _ in range(3):
        assert pipeline.analyse(scenarios.load_case(CASE)).risk.score == first


def test_repeat_contact_needs_something_outstanding():
    """Two contacts about two resolved matters is a success, not a warning."""
    a = pipeline.analyse(scenarios.load_case(scenarios.SCENARIO_DIR / "demo-006.json"))
    assert a.risk.score == 0
    assert a.risk.signals == []


def test_a_kept_promise_with_an_unsolved_problem_still_escalates():
    """demo-004: the callback happened on time and nothing was ever assigned."""
    a = pipeline.analyse(scenarios.load_case(scenarios.SCENARIO_DIR / "demo-004.json"))
    assert a.risk.score >= 40
    assert any(s.kind.value == "no_owner" for s in a.risk.signals)


def test_fury_alone_does_not_escalate():
    """demo-002: the customer is shouting and everything was fixed on the call."""
    a = pipeline.analyse(scenarios.load_case(scenarios.SCENARIO_DIR / "demo-002.json"))
    assert a.risk.score == 0


def test_calm_plus_regulator_does_escalate():
    """demo-003: no raised voice anywhere, complaint already with the Ombudsman."""
    a = pipeline.analyse(scenarios.load_case(scenarios.SCENARIO_DIR / "demo-003.json"))
    assert a.risk.score >= 70
    assert any(s.kind.value == "regulator_mention" for s in a.risk.signals)


# ------------------------------------------------------------------- resolution

def test_resolution_applies_statuses():
    from complaintguard.pipeline import resolution

    case = scenarios.load_case(CASE)
    need_id = case.all_needs()[0].id
    promise_id = case.all_promises()[0].id

    client = FakeLLM([json.dumps({
        "needs": [{"id": need_id, "status": "resolved", "why": "handled on the call"}],
        "promises": [{"id": promise_id, "fulfilled": False, "why": "no callback recorded"}],
    })])
    assert resolution.resolve(case, client) == 1
    assert case.all_needs()[0].status.value == "resolved"
    assert case.all_promises()[0].fulfilled is False


def test_resolution_leaves_statuses_alone_on_a_bad_response():
    from complaintguard.pipeline import resolution

    case = scenarios.load_case(CASE)
    before = [n.status for n in case.all_needs()]
    resolution.resolve(case, FakeLLM(["not json"]))
    assert [n.status for n in case.all_needs()] == before


def test_resolution_keeps_unknown_promises_unknown():
    """Silence in the record is not evidence an agent failed."""
    from complaintguard.pipeline import resolution

    case = scenarios.load_case(CASE)
    pid = case.all_promises()[0].id
    resolution.resolve(case, FakeLLM([json.dumps({
        "needs": [], "promises": [{"id": pid, "fulfilled": None, "why": "nothing either way"}],
    })]))
    assert case.all_promises()[0].fulfilled is None


# ------------------------------------------------------------------- the stub

def test_labelled_stub_makes_no_llm_calls():
    a = pipeline.analyse(scenarios.load_case(CASE), extractor=LabelledExtractor())
    assert a.telemetry.llm_calls == 0
    assert a.telemetry.extractor == "labelled-stub"


# --------------------------------------------------------- scribe word folding

def test_scribe_words_fold_into_speaker_turns():
    """Scribe returns a word stream; a turn ends when the speaker changes."""
    from complaintguard.audio.stt import to_transcript

    payload = {
        "language_code": "en",
        "words": [
            {"type": "word", "text": "I", "start": 0.0, "end": 0.2, "speaker_id": "speaker_0"},
            {"type": "word", "text": "want", "start": 0.2, "end": 0.5, "speaker_id": "speaker_0"},
            {"type": "spacing", "text": " ", "start": 0.5, "end": 0.5},
            {"type": "word", "text": "a", "start": 0.5, "end": 0.6, "speaker_id": "speaker_0"},
            {"type": "word", "text": "refund", "start": 0.6, "end": 1.1, "speaker_id": "speaker_0"},
            {"type": "word", "text": "Certainly", "start": 1.4, "end": 2.0, "speaker_id": "speaker_1"},
        ],
    }
    t = to_transcript(payload)
    assert len(t.utterances) == 2
    assert t.utterances[0].speaker.value == "customer"
    assert t.utterances[0].text == "I want a refund"
    assert t.utterances[1].speaker.value == "agent"
    assert t.utterances[1].start_s == 1.4


def test_scribe_folding_survives_an_empty_response():
    from complaintguard.audio.stt import to_transcript

    assert to_transcript({"words": []}).utterances == []
