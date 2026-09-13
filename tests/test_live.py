"""Offline tests for the "paste a transcript" path. No API key, no network.

Two things matter here and they are tested separately:

    the limits actually bind      — length, lines, per-visitor rate, daily cap
    a failure stays contained     — every bad input returns the form, never a 500,
                                    and the twelve prepared pages keep working

The second is the whole reason this feature is in its own module. A demo that
takes the site down on the one afternoon judges look at it is worse than no demo.

Run:  PYTHONPATH=src .venv/bin/python -m pytest tests -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from complaintguard import live  # noqa: E402
from complaintguard.app import app  # noqa: E402
from complaintguard.llm import FakeLLM  # noqa: E402
from complaintguard.models import Speaker  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean_state():
    """Module-level counters are shared; a test must not inherit another's."""
    live._ip_hits.clear()
    live._cache.clear()
    live._cache_order.clear()
    live._day = ("", 0)
    yield
    live._ip_hits.clear()
    live._cache.clear()
    live._cache_order.clear()
    live._day = ("", 0)


# ------------------------------------------------------------------- parsing

def test_parses_speakers_and_keeps_order():
    case = live.parse_transcript(live.SAMPLE)
    utts = case.contacts[0].transcript.utterances
    assert len(utts) == 7
    assert utts[0].speaker == Speaker.CUSTOMER
    assert utts[1].speaker == Speaker.AGENT
    assert utts[-1].text.endswith("once the contract is up.")


@pytest.mark.parametrize("line", [
    "Customer: hello",
    "  agent - hello",
    "[Agent] hello",
    "REP: hello",
    "caller — hello",
])
def test_accepts_the_ways_people_actually_paste(line):
    case = live.parse_transcript(line + "\nagent: right\ncustomer: ok")
    assert case.contacts[0].transcript.utterances[0].text == "hello"


def test_refuses_to_guess_who_is_speaking():
    """The one thing this project exists to avoid is attributing words to the
    wrong person, so an unlabelled line is an error, not a coin flip."""
    with pytest.raises(live.LiveError) as e:
        live.parse_transcript("customer: hello\nI never agreed to this\nagent: I see")
    assert "who is speaking" in str(e.value)


def test_rejects_empty_and_single_line_pastes():
    for bad in ["", "   ", "customer: hello"]:
        with pytest.raises(live.LiveError):
            live.parse_transcript(bad)


def test_length_cap_binds():
    with pytest.raises(live.LiveError) as e:
        live.parse_transcript("customer: " + "a" * live.MAX_CHARS)
    assert "limit" in str(e.value)


def test_line_cap_binds():
    long = "\n".join("customer: line {}".format(i) for i in range(live.MAX_LINES + 5))
    with pytest.raises(live.LiveError) as e:
        live.parse_transcript(long)
    assert str(live.MAX_LINES) in str(e.value)


# -------------------------------------------------------------------- limits

def test_per_visitor_rate_limit_binds_and_is_per_visitor():
    for _ in range(live.PER_IP_PER_HOUR):
        live.check_budget("1.2.3.4")
        live.spend("1.2.3.4")
    with pytest.raises(live.LiveError):
        live.check_budget("1.2.3.4")
    live.check_budget("5.6.7.8")   # somebody else is unaffected


def test_daily_cap_binds_across_everyone():
    for i in range(live.GLOBAL_PER_DAY):
        live.spend("ip-{}".format(i))
    with pytest.raises(live.LiveError) as e:
        live.check_budget("brand-new-visitor")
    assert "prepared cases" in str(e.value), "must point somewhere that still works"


def test_identical_text_hits_the_cache_regardless_of_whitespace_and_case():
    a = live.cache_key("customer: Hello\nagent: Hi")
    b = live.cache_key("  CUSTOMER:  hello \n\n agent:   hi  ")
    assert a == b


def test_cache_does_not_grow_without_bound():
    for i in range(live.CACHE_MAX + 25):
        live.remember("key-{}".format(i), object())
    assert len(live._cache) <= live.CACHE_MAX


# -------------------------------------------------------------------- routes

def _fake_llm():
    """One extraction response, then one resolution response."""
    return FakeLLM([
        json.dumps({
            "needs": [{"summary": "Reverse a charge never agreed to", "utterance_index": 0,
                       "quote": "I rang last Tuesday about a charge I never signed up for"}],
            "promises": [], "actions": [],
        }),
        json.dumps({"needs": [], "promises": []}),
    ])


def test_form_renders():
    r = client.get("/try")
    assert r.status_code == 200
    assert "customer:" in r.text


def test_a_bad_paste_returns_the_form_not_an_error(monkeypatch):
    monkeypatch.setattr(live, "client", _fake_llm)
    r = client.post("/try", data={"transcript": "no speaker labels here at all"})
    assert r.status_code == 200
    assert "who is speaking" in r.text
    assert "<textarea" in r.text, "the visitor must be able to fix it and retry"


def test_a_bad_paste_costs_nothing():
    before = live._day[1]
    client.post("/try", data={"transcript": "nonsense"})
    assert live._day[1] == before


def test_a_good_paste_runs_the_pipeline_and_renders_the_case_view(monkeypatch):
    monkeypatch.setattr(live, "client", _fake_llm)
    r = client.post("/try", data={"transcript": live.SAMPLE})
    assert r.status_code == 200
    assert "This one was not prepared" in r.text
    assert "Escalation risk" in r.text
    assert live._day[1] == 1, "a real run should be charged against the daily cap"


def test_a_repeat_paste_is_served_from_cache_and_is_not_charged(monkeypatch):
    monkeypatch.setattr(live, "client", _fake_llm)
    client.post("/try", data={"transcript": live.SAMPLE})
    client.post("/try", data={"transcript": live.SAMPLE})
    assert live._day[1] == 1, "the second run must not spend anything"


def test_a_provider_failure_degrades_to_a_message(monkeypatch):
    def explode():
        class Boom:
            name = "boom"

            def complete(self, *a, **k):
                raise RuntimeError("upstream is down")
        return Boom()

    monkeypatch.setattr(live, "client", explode)
    r = client.post("/try", data={"transcript": live.SAMPLE})
    assert r.status_code == 200
    assert "prepared cases" in r.text
    assert live._day[1] == 0, "a failed run must not be charged"


def test_an_unconfigured_deployment_says_so_instead_of_crashing(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    r = client.post("/try", data={"transcript": live.SAMPLE})
    assert r.status_code == 200
    assert "not configured" in r.text


# ------------------------------------------------------ the rest of the site

def test_every_existing_route_is_untouched_when_the_live_path_is_exhausted():
    """The point of the isolation. Burn the whole daily budget, then check that
    the twelve prepared cases and the API still behave exactly as before."""
    for i in range(live.GLOBAL_PER_DAY):
        live.spend("ip-{}".format(i))

    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
    ids = [p.stem for p in __import__("complaintguard.scenarios", fromlist=["x"]).list_scenarios()]
    assert len(ids) == 12
    for scenario_id in ids:
        assert client.get("/case/{}".format(scenario_id)).status_code == 200
        assert client.get("/api/case/{}".format(scenario_id)).json()["telemetry"]["llm_calls"] == 0

    # And the form itself degrades rather than erroring.
    r = client.get("/try")
    assert r.status_code == 200 and "Closed for now" in r.text
