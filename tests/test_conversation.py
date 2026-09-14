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


# -------------------------------------------------------------- the language

@pytest.mark.parametrize("text", [
    "I rang last week about a charge I never signed up for",
    "My name is Ruairí and the café was already closed",
    "naïve résumé Ångström",              # accented Latin is still English enough
])
def test_english_passes(text):
    assert cv.looks_english(text)


@pytest.mark.parametrize("text", [
    "我上周打过电话说有一笔费用",
    "こんにちは、料金について聞きたいです",
    "안녕하세요",
    "Здравствуйте, у меня вопрос",
    "I rang 上周 about a charge",          # mixed is still unreadable to the rules
])
def test_other_scripts_are_refused(text):
    assert not cv.looks_english(text)


def test_the_room_explains_itself_rather_than_failing_silently():
    """The whole point of the check.

    Scribe, the model and ElevenLabs all handle Chinese well, so without this a
    visitor gets a fluent agent and a supervisor frozen at zero — the product
    looking broken in exactly the place it is meant to be good.
    """
    session = cv.start("1.1.1.1")
    with pytest.raises(cv.RoomError) as e:
        cv.reply(session, "我上周打过电话，没有人回我", Scripted(["好的"]))
    assert "English only" in str(e.value)
    assert "supervisor" in str(e.value), "say which half cannot read it, not just 'unsupported'"
    assert session.turns == 0, "a refused turn must not be charged"


def test_the_paste_route_refuses_the_same_thing():
    from complaintguard import live as live_mod

    with pytest.raises(live_mod.LiveError) as e:
        live_mod.parse_transcript(
            "customer: 我上周打过电话说有一笔我没有同意过的费用\nagent: 我帮您查一下"
        )
    assert "English only" in str(e.value)


def test_both_pages_say_so_before_you_try_it():
    assert "In English" in client.get("/live").text
    assert "English only" in client.get("/try").text


# ------------------------------------------------ asking for a human

@pytest.mark.parametrize("said", [
    "I want to speak to your boss",
    "Can I talk to someone higher up",
    "put me through to a team leader",
    "Is there someone who can actually approve this",
    "I want to make a complaint",
    "get me your supervisor",
    "who is in charge there",
])
def test_asking_for_a_human_is_recognised_however_it_is_phrased(said):
    """The first list was written in the vocabulary of an org chart. People do
    not ask for "a supervisor", they ask for your boss."""
    from complaintguard.pipeline.rules import ESCALATION_TERMS, _match
    assert _match(said, ESCALATION_TERMS), said


def test_asking_for_a_human_calls_one_immediately(monkeypatch):
    """Policy 5.2 is ours and it is unambiguous: a customer who asks for a
    supervisor must be given one, and it is not the agent's call. A system whose
    whole claim is knowing when a human is needed cannot then demand sixty more
    points of evidence after the customer has said it out loud."""
    session = cv.start("1.1.1.1")
    cv.reply(session, "I want to speak to your boss about this.",
             Scripted(["I can put you through to a team leader."]))
    out = cv.watch(session, Scripted(['{"needs":[],"promises":[],"actions":[]}']))
    assert out["asked_for_human"] is True
    assert out["escalate"] is True
    assert out["score"] < out["threshold"], "it must fire on the request, not on the score"


def test_it_fires_even_when_the_agent_said_the_right_thing():
    """"I'll see if I can find a team leader" is not a team leader. The gap
    between what is said on a call and what happens after it is the entire
    failure mode this project exists to catch."""
    session = cv.start("2.2.2.2")
    cv.reply(session, "Get me your manager please.",
             Scripted(["Absolutely, I'll get a team leader on the line for you right now."]))
    out = cv.watch(session, Scripted(['{"needs":[],"promises":[],"actions":[]}']))
    assert out["escalate"] is True


def test_the_alarm_says_they_asked_rather_than_quoting_a_threshold():
    session = cv.start("3.3.3.3")
    cv.reply(session, "I'd like to speak to your boss.", Scripted(["Let me see."]))
    out = cv.watch(session, Scripted(['{"needs":[],"promises":[],"actions":[]}']))
    assert "asked for you by name" in out["intervention"]["what"]
    assert "5.2" in out["intervention"]["what"]


def test_an_ordinary_complaint_does_not_call_a_human_on_its_own():
    """The counterweight. If every call escalated the feature would be useless."""
    session = cv.start("4.4.4.4")
    cv.reply(session, "My bill looks higher than I expected this month.",
             Scripted(["Let me take a look at that for you now."]))
    out = cv.watch(session, Scripted(['{"needs":[],"promises":[],"actions":[]}']))
    assert out["asked_for_human"] is False
    assert out["escalate"] is False


def test_the_panel_tells_you_how_far_off_it_is():
    """The original panel showed a number with no scale, so a visitor who said
    something serious and saw 40 had no way to know whether that was close."""
    page = client.get("/live").text
    assert 'id="gap"' in page
    assert "A human is called at" in page


# --------------------------------------------------- behind a reverse proxy

class _Req:
    def __init__(self, headers=None, host="172.18.0.3"):
        self.headers = headers or {}
        self.client = type("C", (), {"host": host})()


def test_the_visitor_ip_comes_from_the_proxy_header_not_the_socket():
    """Caught in production during judging.

    Behind Caddy every request arrives from one Docker-internal address, so a
    per-visitor rate limit keyed on request.client.host is really a site-wide
    one — the seventh judge to open /live would be told they had already made
    six calls this hour, having made none.
    """
    from complaintguard import live as live_mod
    r = _Req({"x-forwarded-for": "203.0.113.7"})
    assert live_mod.visitor_ip(r) == "203.0.113.7"


def test_the_leftmost_entry_wins_when_there_is_a_chain():
    from complaintguard import live as live_mod
    r = _Req({"x-forwarded-for": "203.0.113.7, 70.41.3.18, 172.18.0.3"})
    assert live_mod.visitor_ip(r) == "203.0.113.7"


def test_it_falls_back_sensibly():
    from complaintguard import live as live_mod
    assert live_mod.visitor_ip(_Req({"x-real-ip": "198.51.100.4"})) == "198.51.100.4"
    assert live_mod.visitor_ip(_Req({})) == "172.18.0.3"          # direct, no proxy
    assert live_mod.visitor_ip(_Req({"x-forwarded-for": "  "})) == "172.18.0.3"


def test_two_visitors_behind_the_proxy_get_their_own_budgets():
    """The actual consequence, asserted end to end."""
    for _ in range(cv.PER_IP_PER_HOUR):
        cv.start("203.0.113.7")
    with pytest.raises(cv.RoomError):
        cv.start("203.0.113.7")
    cv.start("198.51.100.4")   # a different judge, unaffected
