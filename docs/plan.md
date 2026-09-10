# 48-hour plan

Build window: **Sat 12 Sep 12:00pm → Mon 14 Sep 12:00pm.** Everything below is Melbourne time.

The tracks are only revealed at kick-off, so this plan is about *tempo*, not about the idea. Adjust the
idea, keep the tempo.

## Before Saturday

- [ ] Attend opening night, take notes into [brief.md](brief.md), get the open questions answered.
- [ ] Lock the team (2–5, at least one current uni student, all able to attend in person Monday night).
- [ ] Everyone accepts the GitHub invite and pushes one commit so we know access works.
- [ ] Decide the default stack so Saturday isn't spent on setup — see [decisions.md](decisions.md).
- [ ] Get API keys sorted ahead of time (Anthropic, ElevenLabs, whatever else) and put them in `.env`.
- [ ] Fill [ideas.md](ideas.md) with a few AI-in-business ideas so we have something to bend to the tracks.

## Saturday

| Time | Goal |
| --- | --- |
| 12:00–13:00 | Tracks revealed. Read them properly. Don't fall in love with the first idea. |
| 13:00–14:00 | Pick a track and one idea. Write down the demo we want the judges to see on Monday. |
| 14:00–15:00 | Split the work. Skeleton repo running end-to-end with fake data. |
| 15:00–20:00 | Build the core loop — the one thing that makes the demo impressive. |
| 20:00–22:00 | First end-to-end run. Ugly is fine. It has to run. |
| 22:00 | Stop. Sleep. Tired judgement on Sunday costs more than the hours gained. |

**Rule for Saturday: the demo path works before anything gets polished.**

## Sunday

| Time | Goal |
| --- | --- |
| Morning | Fix what broke overnight. Talk to a mentor — they know what the judges reward. |
| Midday | Feature freeze target. Anything not started by now probably doesn't ship. |
| Afternoon | Polish the demo path, real data, real UI. Start the deck and demo script. |
| Evening | Record the demo video (do not leave this to Monday). Rehearse the pitch out loud. |
| Night | Full dry run of the submission: repo public if required, README, video, deck. |

## Monday

| Time | Goal |
| --- | --- |
| 08:00–10:00 | Bug fixes only. No new features. |
| 10:00–11:00 | **Submit.** An hour of buffer is the whole point. |
| 11:00–12:00 | Buffer for the thing that always goes wrong. |
| 12:00 | Submissions close. |
| 16:00 | Finalists announced. |
| 17:30–20:30 | Pitches and awards — be there in person. |

## What judges at a business-AI hackathon actually reward

- A **real business problem** with a named user and a number attached to the pain.
- A demo that runs **live**, on the judge's own input if possible.
- Honesty about limits — "here's what's real, here's what's mocked" beats overselling.
- Some responsible-AI story. The organiser is literally called Responsible AI Development: know your
  failure modes, what you do about hallucination, what data you'd need and where it comes from.
- A clear "what we'd do with another month".
