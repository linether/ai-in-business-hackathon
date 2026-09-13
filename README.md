# ComplaintGuard

**Why a complaint escalated — and the earliest point it could have been stopped.**

### 🟢 Live: **https://bizalchemists.duckdns.org**
### 🎬 Demo video (4:52): **https://youtu.be/JalowEQSETY**

By **BizAlchemists** · built for [Forward: AI in Business Hackathon](https://forward.devpost.com/) ·
DSCubed × RAID, University of Melbourne · September 2026
**Track 1 — Improve an Existing Business Capability** · also entered in **Built With ElevenLabs**

---

## The problem

Last financial year **57,592** telecommunications complaints reached the Australian
[Telecommunications Industry Ombudsman](https://www.tio.com.au/). The single largest issue, present in
**60.4%** of them — **34,779 complaints** — was *"no or delayed action by provider."*
A further **16,279** came back to the Ombudsman **after** being referred to the telco, because the
referral still didn't resolve them: **up 36.9% in one year.**

Quality-assurance analysts inside contact centres are the people who work out why. They listen to
recordings, reconstruct the customer's history, and try to explain which earlier handling failure let
an ordinary complaint turn into a formal one. They can only sample a fraction of the calls.

Sources and the full table: [`docs/market-evidence.md`](docs/market-evidence.md).
The problem was brought to the team by [@Genicayyy](https://github.com/Genicayyy), who did this job
during an internship at a large telecommunications contact centre.

## What it does

Pick a case — or paste one of your own at **[/try](https://bizalchemists.duckdns.org/try)** — and
ComplaintGuard reads it alongside the customer's earlier contacts and reconstructs
the failure chain:

```
customer need → agent response → unresolved item → service promise
             → follow-through → repeat contact → escalation
```

It answers the question a risk score cannot:

> The agent promised a callback within 24 hours on 3 September. It never happened. The customer rang
> twice more. **The earliest point this could have been stopped was the 24-hour mark on 4 September.**

Every claim links back to the transcript line that justifies it.

### What it is not

**Not a chatbot.** There is a bot at `/live`, and it is the *prop*, not the product: it exists so a
visitor has a call to watch. What we built is the thing watching it. The distinction matters because
a customer-facing voice bot is a category with a dozen incumbents, and a supervisor that reads a call
in progress and interrupts it is not.

Not an autonomous agent — see *Architecture*. It does not issue refunds, change plans or open
tickets; it recommends, and a person decides. **A score is never used on its own to judge an agent.**

## How it is different

| | |
| --- | --- |
| **Observe.AI** | ships escalation-risk scoring |
| **CallMiner Eureka** | ships root-cause analysis |
| NiCE CXone, Zendesk, Salesforce | transcription, topic and sentiment, QA, routing |

Those produce a **score** (`escalation risk = 0.87`) or an **aggregate trend** ("top three drivers this
quarter"), both of them *after the call is over*. Neither tells an operator why **this one** escalated,
or **when it could still have been caught** — and neither interrupts a call in progress.

ComplaintGuard outputs a **per-case causal timeline with the intervention point marked**. That is a
different artefact, and it is the whole claim.

## Architecture

Control flow is defined in code, not by a model. If the steps can be listed in advance, a workflow
beats an agent — predictable, testable, cost-bounded.

```
1   input                    prepared cases · a transcript pasted at /try · a call held at /live
2   transcribe + diarize     ElevenLabs Scribe — word-level offline, per-turn live at /live
3   structured extraction    needs · promises · deadlines · actions        ← LLM
3b  citation check           verbatim string match                        ← deterministic
4   cross-contact state      merge this call with the case history
5   resolution matching      was each need actually dealt with            ← LLM
6   rules and timing         deadlines, repeat contact, contradictions    ← deterministic
7   risk fusion              fixed weights, fixed thresholds              ← deterministic
8   earliest intervention    walk the timeline to the first unmet duty    ← deterministic
6b  live-call signals        stated repeat · unowned handover · policy breach  ← deterministic
9   evidence binding         every claim carries the line behind it
```

**Models read language. Code makes decisions.** Anything that scores, attributes blame or triggers an
action has to be auditable and reproducible, so it is plain code with fixed weights — the same case
always yields the same number, and every point traces to something someone said.

### The one thing added beyond the pipeline

A **citation check** after extraction, because one failure mode demanded it:

> The system could claim an agent promised something they never promised — and that would blame a real
> person.

The highest-stakes claim is also the one a string comparison settles exactly, so the guarantee that
matters most costs almost nothing. A claim whose quote is not found verbatim where it says it is gets
marked **uncertain**: shown in the interface, excluded from the score. Saying *"I am not sure"* is more
trustworthy than guessing.

Rationale and the patterns deliberately **not** used: [`docs/architecture-upgrade.md`](docs/architecture-upgrade.md).

## Evaluation

Hallucination is not one number. We report three failure modes separately, because each needs its own
detector:

```
PYTHONPATH=src python notebooks/evaluate.py
```

| | |
| --- | --- |
| **citation** | the quote is not in the line it cites — pure string comparison |
| **grounding** | the claim has no counterpart in the script — so it was invented |
| **reasoning** | the claim is real, its status was judged wrong |

plus the two decisions a user cares about: **should this have escalated**, and **which contact was the
last chance**.

**Matching is by utterance index — never a model judging another model's output.** Every label is
anchored to the line it came from, so correctness is an integer comparison.

### The numbers

Run against the real extractor — the pipeline saw transcripts only, with nothing pre-answered:

| | |
| --- | --- |
| escalation decision | precision **86%** · recall **86%** · F1 **86%** |
| earliest intervention point | **83%** — 10 of 12 |
| **citation failures** | **0%** — 0 of 87 quotes |
| grounding failures | 62% — 40 of 64 claims |
| reasoning failures | 29% — 7 of 24 claims |

**The citation number is the one that matters most.** It is the failure mode that would put words in a
real agent's mouth, and across 87 opportunities it did not happen once.

The grounding figure is not fabrication — with citations clean, every extracted claim has a real
source. The model is simply finer-grained than our labels, and where one line raises two things the
anchor cannot say which extracted claim maps to which labelled one, so it matches greedily and counts
the leftovers as errors. Resolving that properly would need a model grading a model, which is the
circularity the anchor exists to avoid. **We report it as it came out**, including the two figures
that do not flatter us.

Reproduce with `PYTHONPATH=src python notebooks/evaluate.py --llm` and one LLM key.
Without `--llm` the harness runs the labelled stub and measures the deterministic layers only —
useful for catching regressions, useless for measuring the system.

## Data

**Everything is synthetic.** Call scripts are written by the team, carry their own ground truth because
we wrote them, and are voiced with ElevenLabs text-to-speech. The telco *Meridian Mobile* is fictional.
**No real customer recordings, transcripts, or employer records are used anywhere in this project.**

Format and the scenario inventory: [`data/scenarios/README.md`](data/scenarios/README.md).

## Run it

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
PYTHONPATH=src .venv/bin/uvicorn complaintguard.app:app --reload
```

Then open http://localhost:8000. **No API key is needed** to run the prepared cases.

⚠️ **What the deployed site does and does not do.** Three paths, deliberately different:

| | |
| --- | --- |
| `/` and `/case/…` | **Twelve prepared cases**, audio on three. Deterministic layers only. A case always yields the same result and **no page view spends a token or calls a model.** |
| `/try` | **Paste your own transcript.** Extraction (3) and resolution (5) genuinely run against it — two model calls — then the same deterministic code scores it. |
| `/live` | **Hold a call — out loud if you like.** Hold the microphone and speak; ElevenLabs Scribe transcribes the turn, an AI support agent answers in its own ElevenLabs voice, and ComplaintGuard reads the call as it happens, checks it against the written policy, and stops it when a human is needed. Typing does the same thing if you have no microphone. |

Every case page reports `extractor` and `llm calls` in its Run panel: `0` on the prepared cases,
`2` on a pasted one. There is **no audio upload route** — `/try` takes text.

`/try` and `/live` are the only routes that spend anything, and each is capped independently: length
and line limits, a per-visitor rate limit, a global daily ceiling, and caching. `/live` additionally
has a **manual switch** (`LIVE_ROOM=on|off`, flipped with `scripts/room.sh`) because it costs the most
per interaction — it is opened for judging and while we test, closed otherwise.

When any of those limits bind, the page in question closes with a sentence and **everything else
keeps working.** Each lives in its own module (`live.py`, `conversation.py`) behind its own routes
precisely so a model outage, a bad paste or an exhausted budget cannot take the site down. There is a
test that burns the entire daily budget and then asserts all twelve case pages, the JSON API and
`/health` still answer with `llm_calls=0`.

For a real extraction run, put one LLM key in `.env` — either `DEEPSEEK_API_KEY` or
`ANTHROPIC_API_KEY`; the first one present is used. The pipeline talks to an
`LLMClient` protocol, so swapping providers is a class, not a refactor.

**Deployed at https://bizalchemists.duckdns.org** — Docker + Caddy with automatic HTTPS on our own server.
Redeploy with `SITE_DOMAIN=bizalchemists.duckdns.org ./deploy.sh`.
Details: [`docs/deploy.md`](docs/deploy.md)

## Layout

```
src/complaintguard/
  models.py            the data contract everything shares
  scenarios.py         load scenario files into the model
  app.py               FastAPI routes
  live.py              the /try path — parsing, limits, cache; isolated on purpose
  conversation.py      the /live room — the call, the watcher, the switch
  knowledge.py         BM25 retrieval over the policy corpus
  templates/           server-rendered views
  pipeline/
    extract.py         layer 3   — LLM extraction (interface + stub)
    citation.py        layer 3b  — deterministic citation check
    rules.py           layer 6   — timing and signal detection
    live_rules.py      layer 6b  — signals that only exist inside a live call
    risk.py            layer 7   — fixed-weight fusion
    intervention.py    layer 8   — earliest preventable point
data/scenarios/        synthetic cases with ground truth
data/policy/           the fictional telco's written policy — what /live checks against
notebooks/evaluate.py  the evaluation harness
docs/                  spec, judging rubric, research, deployment
```

## Team — BizAlchemists

| | | |
| --- | --- | --- |
| Yan Yi | [@Genicayyy](https://github.com/Genicayyy) | main pipeline + extraction · brought the problem |
| Andrew | [@Ranchelwood](https://github.com/RanchelWood) | frontend + evidence panel |
| Yixiao | [@linether](https://github.com/linether) | rules, scoring, intervention, deployment |
| Lillian | [@lillianguo1031-cyber](https://github.com/lillianguo1031-cyber) | — |

Working agreements and the rules every contributor follows: [`AGENTS.md`](AGENTS.md).
New here? [`START_HERE.md`](START_HERE.md).

## A note on the commit history

The organisers inspect git history, and no application code was permitted before **Sat 12 Sep,
12:00 AEST**. Commits before that point contain **planning documents only** — the brief, the rubric,
research and the decision log. Planning ahead of Saturday was explicitly encouraged at opening night.
No history has been rewritten.
