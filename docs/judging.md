# Judging rubric

**100 points total: 80 preliminary + 20 finals.** Verbatim structure from the organisers' doc site.
This is the most useful document we have — it tells us exactly where the marks are.

## Preliminary · 80 points

Scored from: public codebase · production URL · 3–5 min demo video.

### Technical Excellence · 30

| Sub-criterion | Pts | What top marks look like |
| --- | --- | --- |
| Functionality & Execution | 10 | 9–10 = fully working, polished, handles edge cases, **no visible bugs in the video**. 5–6 if steps are faked/hardcoded or need a specific demo path. Explicitly: *"The team should have a live app rather than a local host."* |
| Technical Difficulty | 8 | 7–8 = sophisticated approach, team understands the *why* of the architecture. **3–4 if it's "mostly a wrapper on an existing tool/API with minimal custom logic."** They name: fine-tuning, RAG pipelines, agentic/multi-step reasoning, custom evaluation, model chaining, embedding/vector search. |
| Code Quality & Architecture | 6 | 5–6 = clean, modular, well-documented (README, comments), sensible separation of concerns, justified tool choices. 0–2 for one monolithic file. |
| Use of Data / Models | 6 | 5–6 = deliberate model choice with reasoning about size/cost/latency vs accuracy, thoughtful data-quality handling, **and some form of evaluation — "even informal spot checks."** |

### Innovation · 25

| Sub-criterion | Pts | What top marks look like |
| --- | --- | --- |
| Originality of Idea | 10 | 9–10 = genuinely fresh, or a known problem reframed surprisingly. 0–4 for a clone of a well-known product. |
| Creativity in Solution Design | 8 | 7–8 = creative, well-considered decisions; AI feels genuinely useful rather than bolted on. |
| Differentiation | 7 | 6–7 = **can name existing alternatives** and give a specific, credible reason ours is better. 0–2 if we show no awareness competitors exist. |

### Business Value & Application · 25

| Sub-criterion | Pts | What top marks look like |
| --- | --- | --- |
| Problem Significance | 8 | 7–8 = sharp, well-evidenced problem with a **specific named target user**. 5–6 if the audience is generic. |
| Feasibility & Viability | 8 | 7–8 = credible path to real deployment; **cost, data access, regulatory concerns and adoption path acknowledged**. |
| Impact & Value Proposition | 9 | 8–9 = compelling, specific, **at least semi-quantified** value (hours saved, cost cut, capability unlocked) and who benefits by how much. |

## Finals · 20 points — top 8 only, live on stage

| Sub-criterion | Pts | What top marks look like |
| --- | --- | --- |
| Clarity of Pitch | 6 | Clean arc: problem → solution → how it works → why it matters. Within time. No unexplained jargon. |
| Live Demo Quality | 8 | Rehearsed, leads with the most differentiating feature, **actually proves the claims made in the pitch**. 0–4 if the demo fails or is skipped. |
| Team Engagement & Q&A | 6 | Direct specific answers, **multiple team members can speak to the project**, honest about limitations when pressed. 3–4 if it all rests on one person. |

## What this rubric tells us to do

1. **Deploy it.** Functionality (10) explicitly rewards a live URL over localhost, and Submission
   Requirements lists a Production URL. Vercel/Railway/Fly — pick one on day one, not Monday morning.
2. **Don't ship an API wrapper.** Technical Difficulty caps at 3–4 for a thin wrapper. We need at least
   one of: a real RAG pipeline, multi-step agentic reasoning, an eval harness, or model chaining —
   and we need to be able to explain *why* that architecture.
3. **Run an eval, however scrappy.** 6 points for Use of Data/Models, and they accept "informal spot
   checks". Twenty labelled examples in a notebook with an accuracy number beats nothing. Most teams
   skip this entirely.
4. **Write the README properly.** 6 points for code quality is the cheapest scoring in the whole rubric
   and it's won by documentation and file structure, not by cleverness.
5. **Name our competitors out loud.** 7 points for Differentiation, 0–2 if we ignore them. One slide:
   "here's what exists, here's why ours is different."
6. **Quantify the value.** 9 points. "Saves an ops manager ~6 hrs/week, ~$18k/yr at loaded cost" scores;
   "improves efficiency" does not.
7. **No bugs in the video.** The prelim score comes from the *video*, not a live session — so we control
   exactly what the judges see. Re-record until it's clean.
8. **Everyone rehearses.** Q&A explicitly rewards multiple team members being able to speak to it.
