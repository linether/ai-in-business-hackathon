"""Signals that only make sense while a single call is still happening.

`rules.py` reads a case file: several contacts, days apart, with statuses already
settled. Almost none of it can fire on one live call — `repeat_contact` needs two
contacts in the file, `missed_deadline` needs a deadline that has passed. Watching
a call as it happens is a different problem, so it gets its own layer rather than
a looser version of the existing one.

Two things are detectable inside one call and both are deterministic:

**What the customer states.** "This is the third time I've rung" is a repeat
contact asserted in the room. We cannot verify it against a case history we do not
have, and we do not pretend to — it is recorded as *stated by the customer*, and
the interface says so.

**What the policy required and did not get.** This is where retrieval becomes
load-bearing. `knowledge.py` finds the rule that governs what the customer is
calling about; the check that it was honoured is a string predicate over what the
agent actually said. **The model reads the language, the code makes the call** —
the same division as everywhere else. Every finding cites the policy by section,
so a supervisor can disagree with us by opening the rule.

These predicates are blunt on purpose. They look for the thing the policy names —
a ticket number, a person's name, the words "team leader" — because that is what
an auditor would look for, and because a blunt check that a human can verify in
two seconds is worth more here than a subtle one they have to trust.
"""

from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional, Tuple

from .. import knowledge
from ..models import Case, Evidence, Signal, SignalKind
from .rules import WEIGHTS

# Weight for a breach of a written policy. Sits between a repeat contact and a
# broken promise: heavier than a soft indicator because a rule was written down
# and not followed, lighter than a promise broken to a customer's face.
POLICY_BREACH_WEIGHT = 18

STATED_REPEAT = [
    "second time", "third time", "fourth time", "twice now", "three times",
    "rang before", "called before", "phoned before", "rang about this",
    "called about this", "spoke to someone", "last time i rang", "last time i called",
    "every time i ring", "every time i call", "keep ringing", "keep calling",
    "again about", "still not", "still haven't", "still havent",
]

# What "an owner" looks like in speech: a person, or a handle to one.
OWNER_MARKERS = [
    "my name is", "i'm ", "ask for me", "i'll personally", "i will personally",
    "reference number", "case number", "direct line", "extension",
    "i'll call you", "i will call you", "i'll ring you", "i will ring you",
]
# What "no owner" looks like: a queue with nobody's name on it.
UNOWNED_MARKERS = [
    "the team will", "the billing team", "the network team", "another team",
    "goes into the queue", "in the queue", "someone will", "somebody will",
    "they'll get back", "they will get back", "they'll be in touch",
    "it gets passed", "i'll pass it", "i will pass it", "pass it on",
    "once it leaves us", "can't see what they", "cannot see what they",
    "i'll chase", "i will chase", "chase it up",
]
LEADER_MARKERS = [
    "team leader", "supervisor", "manager", "escalate", "escalating",
    "up the line", "senior", "complaints team",
]
TICKET_MARKERS = ["ticket", "reference", "job number", "fault number"]


def _said(text: str, terms: List[str]) -> bool:
    low = " " + re.sub(r"\s+", " ", text.lower()) + " "
    return any(t in low for t in terms)


def _lines(case: Case, speaker: str) -> List[Tuple[int, int, object]]:
    """(contact_seq, utterance_index, utterance) for one side of the call."""
    out = []
    for contact in case.contacts:
        if contact.transcript is None:
            continue
        for i, u in enumerate(contact.transcript.utterances):
            if u.speaker.value == speaker:
                out.append((contact.seq, i, u))
    return out


def _evidence(seq: int, index: int, u) -> Evidence:
    return Evidence(
        contact_seq=seq, utterance_index=index, start_s=u.start_s,
        speaker=u.speaker.value, quote=u.text,
    )


# ------------------------------------------------------- stated repeat contact

def stated_repeat_contact(case: Case) -> List[Signal]:
    """The customer says they have been here before.

    Recorded as an assertion, not a verified fact — we are watching one call and
    have no history to check it against. The detail line says "stated" for exactly
    that reason, and a supervisor reading it knows what it rests on.
    """
    for seq, index, u in _lines(case, "customer"):
        if _said(u.text, STATED_REPEAT):
            return [
                Signal(
                    kind=SignalKind.REPEAT_CONTACT,
                    weight=WEIGHTS[SignalKind.REPEAT_CONTACT],
                    detail="Customer stated this is not their first contact about this matter.",
                    evidence=[_evidence(seq, index, u)],
                )
            ]
    return []


# ------------------------------------------------------------ unowned handover

def unowned_handover(case: Case) -> List[Signal]:
    """The agent handed the matter somewhere without a name on it.

    Policy 2.2 is explicit that a queue is not an owner, and the reason is the
    whole thesis of this project: nobody is answerable for a deadline that belongs
    to a team. Fires only when the agent never names anyone anywhere in the call.
    """
    agent_lines = _lines(case, "agent")
    if any(_said(u.text, OWNER_MARKERS) for _, _, u in agent_lines):
        return []
    for seq, index, u in agent_lines:
        if _said(u.text, UNOWNED_MARKERS):
            return [
                Signal(
                    kind=SignalKind.NO_OWNER,
                    weight=WEIGHTS[SignalKind.NO_OWNER],
                    detail="The matter was handed to a team, not a person. Nobody on this call "
                           "became answerable for it.",
                    evidence=[_evidence(seq, index, u)],
                )
            ]
    return []


# --------------------------------------------------------- policy obligations

def _agent_ever(case: Case, terms: List[str]) -> bool:
    return any(_said(u.text, terms) for _, _, u in _lines(case, "agent"))


def _agent_gave_ticket(case: Case) -> bool:
    for _, _, u in _lines(case, "agent"):
        if _said(u.text, TICKET_MARKERS) and re.search(r"\d{3,}", u.text):
            return True
    return False


def _customer_line(case: Case, terms: List[str]) -> Optional[Tuple[int, int, object]]:
    for seq, index, u in _lines(case, "customer"):
        if _said(u.text, terms):
            return seq, index, u
    return None


# slug -> (trigger terms in the customer's words, requirement label, met?)
Obligation = Tuple[List[str], str, Callable[[Case], bool]]

OBLIGATIONS: Dict[str, Obligation] = {
    "ombudsman-referral": (
        ["ombudsman", "tio", "regulator", "acma", "formal complaint"],
        "escalate to a team leader before the call ends",
        lambda case: _agent_ever(case, LEADER_MARKERS),
    ),
    "repeat-contact": (
        ["third time", "three times", "fourth time", "every time i ring", "every time i call"],
        "escalate the third contact to a team leader",
        lambda case: _agent_ever(case, LEADER_MARKERS),
    ),
    "escalation-rights": (
        ["speak to a manager", "speak to your manager", "supervisor", "team leader",
         "someone higher", "make a complaint"],
        "put the customer through to a team leader, or take details for a callback",
        lambda case: _agent_ever(case, LEADER_MARKERS),
    ),
    "fault-ticket-sla": (
        ["dropping out", "drops out", "keeps cutting", "no internet", "internet is",
         "slow", "signal", "reception", "not working", "outage", "dropout"],
        "raise a fault ticket on the call and read the number out",
        _agent_gave_ticket,
    ),
    "unauthorised-add-on": (
        ["never signed up", "didn't sign up", "did not sign up", "never agreed",
         "didn't agree", "never authorised", "did not authorise", "unauthorised",
         "never asked for"],
        "remove the add-on on the call and refund every charge for it",
        lambda case: _agent_ever(case, ["removed it", "i've removed", "i have removed",
                                        "taken it off", "take it off now", "refund it",
                                        "refunding", "i'll refund", "i will refund"]),
    ),
    "case-ownership": (
        ["who is dealing", "who's dealing", "who is handling", "who's handling",
         "who is actually", "who do i", "whose name"],
        "give the customer a named owner before the call ends",
        lambda case: _agent_ever(case, OWNER_MARKERS),
    ),
    "service-loss": (
        ["no service", "cut off", "disconnected", "can't make calls", "cannot make calls",
         "nothing works", "completely down", "no signal at all"],
        "restore service or offer an interim arrangement before resolving the billing question",
        lambda case: _agent_ever(case, ["restore", "reconnect", "back on", "interim",
                                        "temporary", "credit your account"]),
    ),
}


def policy_breaches(case: Case) -> List[Signal]:
    """Rules the call triggered, and did not honour.

    Retrieval picks the governing policy from what the customer said; the check
    is a predicate over what the agent said. Both halves are inspectable, and the
    signal carries the policy section so the finding can be argued with.
    """
    signals: List[Signal] = []
    corpus = knowledge.corpus()

    for slug, (triggers, requirement, met) in OBLIGATIONS.items():
        hit = _customer_line(case, triggers)
        if hit is None:
            continue
        if met(case):
            continue
        chunk = corpus.by_slug(slug)
        if chunk is None:
            continue
        seq, index, u = hit
        signal = Signal(
            kind=SignalKind.UNRESOLVED_NEED,
            weight=POLICY_BREACH_WEIGHT,
            detail="Policy {} ({}) required the agent to {} — it did not happen on this call.".format(
                chunk.ref, chunk.title.lower(), requirement
            ),
            evidence=[_evidence(seq, index, u)],
        )
        # Carried for the interface; the model contract has no field for it and
        # widening the contract for one route would be the wrong trade.
        setattr(signal, "_policy", {"slug": slug, "ref": chunk.ref, "title": chunk.title})
        signals.append(signal)

    return signals


def all_live_signals(case: Case) -> List[Signal]:
    return stated_repeat_contact(case) + unowned_handover(case) + policy_breaches(case)
