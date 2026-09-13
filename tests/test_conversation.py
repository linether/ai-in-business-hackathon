"""Offline tests for the live room. No API key, no network.

The room is the only part of the site that both spends money and talks to a
model on every interaction, so what is tested here is mostly *what happens when
things go wrong*: a dead provider, an expired call, an exhausted budget, a
visitor who will not stop. A live demo that breaks on camera costs more than a
feature that was never built, and the last test in this file is the one that
matters — burn the room's entire budget and assert the rest of the site does not
notice.

Run:  PYTHONPATH=src .venv/bin/python -m pytest tests -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from complaintguard import conversation as cv, knowledge  # noqa: E402
from complaintguard.app import app  # noqa: E402
from complaintguard.llm import FakeLLM  # noqa: E402
from complaintguard.models import Speaker  # noqa: E402
from complaintguard.pipeline import live_rules  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean():
    cv._ip_hits.clear()
    cv._sessions.clear()
    cv._day = ("", 0)
    yield
    cv._ip_hits.clear()
    cv._sessions.clear()
    cv._day = ("", 0)


class Scripted:
    """An agent that says what we tell it to, so the rules can be tested alone."""

    name = "scripted"

    def __init__(self, lines):
        self.lines = list(lines)

    def complete(self, system, user, max_tokens=2000):
        return self.lines.pop(0) if self.lines else "Right."


def _call(customer_lines, agent_lines):
    session = cv.start("test-ip")
    llm = Scripted(agent_lines)
    for line in customer_lines:
        cv.reply(session, line, llm)
    return session


# ------------------------------------------------------------------ retrieval

def test_corpus_loads_and_excludes_the_readme():
    chunks = knowledge.corpus().chunks
    assert len(chunks) == 12
    assert all(c.ref for c in chunks), "every policy needs a section number to cite"
    assert not any(c.slug == "README" for c in chunks)


@pytest.mark.parametrize("question,slug", [
    ("I never signed up for this add-on and I want my money back", "unauthorised-add-on"),
    ("nobody called me back like they promised", "callback-commitment"),
    ("my internet keeps dropping out every night", "fault-ticket-sla"),
    ("I want to speak to a manager", "escalation-rights"),
    ("I'm taking this to the ombudsman", "ombudsman-referral"),
    ("who is actually dealing with my case", "case-ownership"),
    ("the last person told me something completely different", "contradictory-answers"),
    ("I want to cancel and move to another provider", "churn-intent"),
])
def test_retrieval_finds_the_governing_policy(question, slug):
    assert knowledge.search(question)[0].slug == slug


def test_retrieval_returns_nothing_rather_than_the_least_irrelevant_document():
    """The floor is the point. Handing back a near-miss is how a retrieval layer
    teaches a model to be confidently wrong."""
    assert knowledge.search("what is the weather in Perth tomorrow") == []
    assert knowledge.search("can you recommend a restaurant") == []


# ---------------------------------------------------------------- live rules

def test_a_stated_repeat_contact_is_recorded_as_stated():
    session = _call(["This is the third time I've rung about this."], ["Right."])
    signals = live_rules.stated_repeat_contact(session.case())
    assert len(signals) == 1
    assert "stated" in signals[0].detail.lower(), "we cannot verify it, so we must not claim it"


def test_a_queue_is_not_an_owner():
    session = _call(
        ["Who is dealing with it?"],
        ["I'll pass it to the billing team and they'll get back to you."],
    )
    assert live_rules.unowned_handover(session.case())


def test_naming_someone_clears_the_owner_finding():
    session = _call(
        ["Who is dealing with it?"],
        ["I'll chase it up with the billing team myself — my name is Sam and I'll call you back."],
    )
    assert live_rules.unowned_handover(session.case()) == []


def test_an_ombudsman_mention_not_escalated_breaches_policy_and_cites_it():
    session = _call(["I'm taking this to the Ombudsman."], ["That's your right."])
    breaches = live_rules.policy_breaches(session.case())
    refs = {getattr(b, "_policy")["ref"] for b in breaches}
    assert "7.1" in refs


def test_the_breach_lifts_when_the_agent_actually_complies():
    session = _call(
        ["I'm taking this to the Ombudsman."],
        ["Let me get a team leader on the line for you now."],
    )
    refs = {getattr(b, "_policy")["ref"] for b in live_rules.policy_breaches(session.case())}
    assert "7.1" not in refs, "a finding that cannot clear is not a check, it is an accusation"


def test_a_reported_fault_without_a_ticket_number_breaches_the_sla_policy():
    session = _call(
        ["My internet keeps dropping out every night."],
        ["I've logged that on your account for you."],
    )
    refs = {getattr(b, "_policy")["ref"] for b in live_rules.policy_breaches(session.case())}
    assert "3.1" in refs


def test_a_ticket_number_clears_it():
    session = _call(
        ["My internet keeps dropping out every night."],
        ["I've raised a fault ticket, the reference is 884231."],
    )
    refs = {getattr(b, "_policy")["ref"] for b in live_rules.policy_breaches(session.case())}
    assert "3.1" not in refs


# --------------------------------------------------------------------- limits

def test_the_turn_cap_binds():
    session = _call(["hello"] * cv.MAX_TURNS, ["ok"] * cv.MAX_TURNS)
    with pytest.raises(cv.RoomError) as e:
        cv.reply(session, "one more", Scripted(["ok"]))
    assert str(cv.MAX_TURNS) in str(e.value)


def test_the_per_visitor_call_limit_binds_and_is_per_visitor():
    for _ in range(cv.PER_IP_PER_HOUR):
        cv.start("9.9.9.9")
    with pytest.raises(cv.RoomError):
        cv.start("9.9.9.9")
    cv.start("8.8.8.8")


def test_the_daily_ceiling_binds_and_points_somewhere_that_still_works():
    for i in range(cv.GLOBAL_PER_DAY):
        cv.start("ip-{}".format(i))
    with pytest.raises(cv.RoomError) as e:
        cv.start("someone-new")
    assert "/try" in str(e.value) or "prepared" in str(e.value)


def test_the_manual_switch_closes_the_room(monkeypatch):
    monkeypatch.setenv("LIVE_ROOM", "off")
    assert cv.room_open() is False
    with pytest.raises(cv.RoomError) as e:
        cv.start("1.1.1.1")
    assert "closed" in str(e.value).lower()
    monkeypatch.setenv("LIVE_ROOM", "on")
    assert cv.room_open() is True


def test_an_over_long_turn_is_trimmed_rather_than_refused():
    session = cv.start("1.1.1.1")
    cv.reply(session, "a " * 2000, Scripted(["ok"]))
    assert len(session.utterances[0].text) <= cv.MAX_CHARS_PER_TURN + 2


def test_sessions_do_not_accumulate_without_bound():
    for i in range(cv.MAX_SESSIONS + 30):
        cv._sessions[str(i)] = cv.Session("x")
    cv._sweep()
    assert len(cv._sessions) <= cv.MAX_SESSIONS


# --------------------------------------------------------------------- routes

def test_the_room_renders_and_costs_nothing_to_look_at():
    before = cv._day[1]
    r = client.get("/live")
    assert r.status_code == 200
    assert "watches the agent" in r.text
    assert cv._day[1] == before, "a page view must not spend a call"


def test_the_room_says_what_it_is_not():
    """The framing is load-bearing: the conversation is the demo, the supervisor
    is the submission. If this line goes missing the page reads as a chatbot."""
    r = client.get("/live")
    assert "Observe.AI" in r.text and "interrupts one in progress" in r.text


def test_starting_a_call_spends_exactly_one():
    r = client.post("/live/start").json()
    assert r["ok"] and r["session"]
    assert cv._day[1] == 1


def test_an_expired_call_is_told_so_rather_than_crashing():
    r = client.post("/live/turn", data={"session": "nope", "text": "hello"}).json()
    assert r["ok"] is False and "expired" in r["error"]


def test_a_dead_provider_does_not_end_the_call(monkeypatch):
    def explode(*a, **k):
        class Boom:
            name = "boom"

            def complete(self, *args, **kwargs):
                raise RuntimeError("upstream is down")
        return Boom()

    monkeypatch.setattr("complaintguard.live.client", explode)
    sid = client.post("/live/start").json()["session"]
    r = client.post("/live/turn", data={"session": sid, "text": "hello"}).json()
    assert r["ok"] is False
    assert "not counted" in r["error"], "a failed turn must not be charged to the visitor"
    assert cv._sessions[sid].turns == 0


def test_a_failing_supervisor_never_takes_the_call_down(monkeypatch):
    def explode(*a, **k):
        raise RuntimeError("no")

    monkeypatch.setattr("complaintguard.conversation.watch", explode)
    sid = client.post("/live/start").json()["session"]
    r = client.post("/live/watch", data={"session": sid})
    assert r.status_code == 200 and r.json()["ok"] is False


def test_the_watcher_says_nothing_until_there_is_something_to_read():
    sid = client.post("/live/start").json()["session"]
    out = client.post("/live/watch", data={"session": sid}).json()
    assert out["ready"] is False


def test_the_policy_behind_a_finding_can_be_opened():
    r = client.get("/policy/ombudsman-referral")
    assert r.status_code == 200 and "10 business days" in r.text
    assert client.get("/policy/not-a-policy").status_code == 404


def test_the_policy_page_never_shows_the_alias_line():
    """`also:` is an indexing device. Showing it would look like keyword stuffing
    in a document we are asking a supervisor to trust."""
    r = client.get("/policy/fault-ticket-sla")
    assert "wifi" not in r.text.lower()


# ------------------------------------------------ the rest of the site, again

def test_burning_the_rooms_entire_budget_changes_nothing_else():
    """The isolation guarantee, asserted rather than asserted-about.

    Spend every call the room has for the day, then check that the twelve
    prepared cases, the JSON API, /health and /try all behave exactly as before —
    and that none of them called a model to do it.
    """
    for i in range(cv.GLOBAL_PER_DAY):
        cv.start("ip-{}".format(i))

    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/try").status_code == 200

    from complaintguard import scenarios
    ids = [p.stem for p in scenarios.list_scenarios()]
    assert len(ids) == 12
    for scenario_id in ids:
        assert client.get("/case/{}".format(scenario_id)).status_code == 200
        assert client.get("/api/case/{}".format(scenario_id)).json()["telemetry"]["llm_calls"] == 0

    r = client.get("/live")
    assert r.status_code == 200 and "room is closed" in r.text


# ----------------------------------------------------------------- the voice

def test_speech_is_skipped_when_the_voice_switch_is_off(monkeypatch):
    monkeypatch.setenv("LIVE_VOICE", "off")
    assert cv.voice_enabled() is False
    assert cv.speak("anything at all") is None


def test_speech_is_skipped_when_there_is_no_elevenlabs_key(monkeypatch):
    monkeypatch.setenv("LIVE_VOICE", "on")
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    assert cv.speak("anything at all") is None, "no key means no audio, not a crash"


def test_a_turn_still_completes_when_speech_fails(monkeypatch):
    """Audio is never load-bearing. If ElevenLabs is down the line is still on
    screen and the call goes on."""
    monkeypatch.setenv("LIVE_VOICE", "on")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "not-a-real-key")

    def explode(*a, **k):
        raise RuntimeError("elevenlabs is down")

    monkeypatch.setattr("complaintguard.audio.tts.synth", explode)
    session = cv.start("1.1.1.1")
    out = cv.reply(session, "hello", Scripted(["Hi there."]))
    assert out["agent_text"] == "Hi there."
    assert out["audio"] is None


def test_a_made_up_audio_id_is_refused_rather_than_resolved():
    """The digest comes back from the browser, so it is checked, not trusted."""
    for bad in ["../../etc/passwd", "nope", "", "a" * 64, "abc/def"]:
        assert cv.voice_path(bad) is None
    assert client.get("/live/say/deadbeef").status_code == 404
