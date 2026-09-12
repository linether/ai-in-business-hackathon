# 48-hour plan

Build window: **Sat 12 Sep 12:00pm → Mon 14 Sep 12:00pm.** All times Melbourne (AEST).

Written against the real rubric ([judging.md](judging.md)) and the real submission requirements
([brief.md](brief.md)), not guesses.

## The four things we hand in

Everything below exists to produce these, and the prelim score comes **only** from these:

1. Track name in the Devpost description
2. **Public** GitHub repo
3. **Live deployed URL** (localhost scores lower — this is explicit in the rubric)
4. **3–5 min video** of the app working end-to-end

## Saturday (started 12:00pm)

| Time | Goal |
| --- | --- |
| 12:00–13:00 | Pick the track. Pick the idea. Don't marry the first one. |
| 13:00–14:00 | Write down the exact demo the judges will watch on Monday. Work backwards from it. |
| 14:00–15:00 | Split the work. **Deploy a hello-world to the real host today** — deployment is never a Monday task. |
| 15:00–20:00 | Build the core loop — the one thing that makes the demo land. |
| 20:00–22:00 | First end-to-end run. Ugly is fine. It has to run. |
| 22:00 | Stop. Sleep. Tired judgement on Sunday costs more than the hours gained. |

**Saturday's rule: the demo path works before anything gets polished.**

## Sunday

| Time | Goal |
| --- | --- |
| Morning | Fix what broke overnight. **Talk to a mentor** — they know what the judges reward. |
| Midday | Feature freeze target. Not started by now = doesn't ship. |
| Afternoon | Polish the demo path. Real data. Write the README properly (6 rubric points, cheapest on the board). |
| Afternoon | **Run the eval** — 20 labelled examples in a notebook with a number. Worth 6 points and most teams skip it. |
| Evening | **Record the 3–5 min video.** Do not leave this to Monday. Re-record until there are no visible bugs. |
| Night | Full dry run of the submission: repo public, README, live URL, video, Devpost draft filled in. |

## Monday

| Time | Goal |
| --- | --- |
| 08:00–10:00 | Bug fixes only. No new features. |
| 10:00–11:00 | **Flip the repo to public. Submit on Devpost.** |
| 11:00–12:00 | Buffer for the thing that always goes wrong. |
| **12:00** | **Submissions close — late is not considered.** |
| 16:00 | Top 8 announced. |
| 17:30–20:30 | If we're in: **live** demo + pitch, 3–5 min. Pre-recorded video not accepted here. |

## Cheap points we should not leave on the table

- **Deploy it** — a live URL, not localhost.
- **Not a wrapper** — RAG, agentic multi-step reasoning, model chaining or an eval harness, and be able
  to explain *why* that architecture.
- **A number for the value** — "saves ~6 hrs/week, ~$18k/yr" beats "improves efficiency".
- **Name the competitors** — 7 points, and 0–2 if we act like none exist.
- **Everyone can pitch it** — Q&A rewards more than one person knowing the project.
- **ElevenLabs special track** — if voice can be *core* to the idea, we get a second $100 shot for free.
