# After-hours enrolment line for education SMEs

**Author:** @linether · **Date:** 09-12 17:25 AEST · **Track:** 1 (+ ElevenLabs special)

> **Status: one candidate among several.** This came out of a two-person conversation on Saturday
> afternoon. It is not the team's decision and it has a real weakness (see Self-score). Write your own
> proposal rather than converging on this one by default.

## Who hurts

The owner or centre manager of a small tutoring centre or language school — one to three sites,
5–20 tutors, no receptionist after 6pm.

## What it costs them today

**Not yet validated — this is the calculation shape, not an answer.**

```
after-hours enquiry calls per week   × ?
share that go unanswered             × ?
enquiry → enrolment conversion       × ?
annual fee per enrolled student      × ?
────────────────────────────────────────
= revenue lost per year
```

**How to validate it by Sunday morning:** call three real centres as a prospective parent — one during
business hours, two after 6pm — and record who picks up and how fast. That is a number we can say on
stage and nobody can argue with. The sponsor explicitly told us to validate against real market data
before building.

## What we build

An AI that answers the after-hours line, and scores urgency, buying intent and caller distress from the
voice itself to decide whether to wake the owner now or queue a callback for the morning.

## The demo the judges watch

1. A call comes in at 21:00. A parent calmly asks about class times → system logs it, queues a morning
   callback. No one is woken.
2. A second call. The parent's child has just failed a practice exam; they're anxious and want to
   enrol this week. Voice shows it before the words do — rising pitch, faster speech, self-interruption.
3. The escalation score crosses the threshold live on screen, with the contributing signals broken out:
   prosody, wording, conversational dynamics.
4. The owner's phone rings.
5. The same call again in Mandarin — same decision, same score.

## What it costs with our solution

The other half of the sentence, once the numbers above are real:
*"This centre loses $X a year in unanswered after-hours enquiries; this costs $Y a month to run."*

## Why this isn't a wrapper

The conversational layer is deliberately delegated — that part *is* commodity. Our engineering is the
escalation scorer:

- **Prosody features** from the audio (pitch contour, energy, speech rate, jitter)
- **Lexical signal** from the transcript
- **Conversational dynamics** — interruptions, repeated questions, silences, talk-over
- **Fusion layer** producing one escalation score, with the contributions visible
- **Deterministic policy layer** on top of the score — thresholds and rules, not an LLM deciding whether
  to wake a human at midnight

That last split is the sponsor's own architecture principle: automation pipelines for the consequential
decision, models for the judgement.

## Existing alternatives

Observe.AI, CallMiner, Cogito, Uniphore, AWS Contact Lens. All are enterprise contact-centre analytics,
priced and shaped for large teams, and mostly **post-call** — QA and agent coaching after the fact.

Our claim, narrow enough to defend: **real-time, acting during the call, for a business with no contact
centre at all and no agent to coach.** Plus Mandarin, which none of them prioritise for SMEs.

## Hardest part

Speech emotion recognition is genuinely unreliable and biased against non-native speakers. If the score
looks random on stage, the pitch collapses.

Mitigations: claim **escalation risk**, not emotion categories, so there's objective ground truth. Fuse
multiple signals so no single weak one dominates. Measure the non-native-speaker gap and say it out loud
— this is a Responsible AI Development event and the rubric rewards being upfront about limitations.

## What we'd fake, and admit to

The phone network. Browser mic and uploaded audio, not a real inbound PSTN number. Say so plainly in the
video rather than implying a phone integration exists.

## How we'd evaluate it

20–30 scenario calls we record ourselves, labelled binary: should this have been escalated? Report
precision and recall plus a confusion matrix, and report the non-native-speaker subset separately.

## Can we deploy it?

Yes. Process audio in 2–3 second chunks rather than true streaming. **Build the replay path first** —
uploaded audio through the full pipeline — because the 80-point preliminary round is scored from a
video, and replay is enough for a video. Live mic is a finals upgrade.

## Self-score

| # | Question | Score |
| --- | --- | --- |
| 1 | Specific person named? | 2 |
| 2 | Hours × rate × volume? | 1 — shape is clear, numbers not yet real |
| 3 | Real technical depth? | 2 |
| 4 | Demo path finishable? | 1 — audio pipelines are where hackathon projects die |
| 5 | Can name alternatives? | 2 |
| 6 | Off the obvious list? | **0 — "customer support agent" is literally a Track 1 example and on our own crowded list** |
| 7 | Deployable? | 2 |
| 8 | Ground truth to evaluate? | 2 |
| 9 | Survives cost/data/regulation? | 2 |
| | **Total** | **14 / 18** |

**The honest weakness is #6.** The education framing, the after-hours constraint and the multilingual
angle pull it out of the clone band, but the first ten seconds of the pitch still sound like everyone
else's project. **A proposal that scores lower overall but beats this on originality is worth taking
seriously.**
