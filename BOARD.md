# Message board

Async channel for the team and our agents. Everything below is append-only.

## Rules

- **Read the whole board at the start of every session.** It is how you learn what changed.
- **Append new entries at the bottom.** Never edit or delete an existing entry — reply with a new one.
- Use **AEST (Melbourne, UTC+10)** for every timestamp. We are not all in the same time zone.
- Keep entries to a few lines. This is a log, not an essay.
- `BOARD.md` uses a union merge (see `.gitattributes`), so two people appending at once both survive.
  If you do see conflict markers, keep **both** sides and delete only the `<<<<<<<` / `=======` /
  `>>>>>>>` lines.
- Post to the board when you: **claim** a task, **finish** one, get **blocked**, need a **decision**, or
  learn a fact the team needs (a real number, an API limit, a rule from the organisers).
- A decision that's actually made belongs in `docs/decisions.md` as well — the board is where it's
  argued, `decisions.md` is where it's settled.

## Entry format

```
### [MM-DD HH:MM AEST] @username · TAG
Body, a few lines.
```

Tags: `CHECKIN` · `CLAIM` · `DONE` · `BLOCKED` · `DECIDE` · `FYI` · `HANDOFF` · `RISK`

Quick reference:

| Tag | Use when |
| --- | --- |
| `CLAIM` | You're starting on something, so nobody duplicates it |
| `DONE` | You finished and merged it; say what's now unblocked |
| `BLOCKED` | You can't proceed; say exactly what you need and from whom |
| `DECIDE` | The team needs to choose; give the options and your recommendation |
| `FYI` | Something the team should know but needn't act on |
| `HANDOFF` | You're stopping mid-task; say where it stands and what's next |
| `RISK` | Something that could cost us the submission |
| `CHECKIN` | Roll call — you're online and your setup works |

---

### [09-12 17:00 AEST] @linether · FYI
Board is live, along with `AGENTS.md`. Every agent reads `AGENTS.md` first, then this board.

Repo state: docs only — brief, rubric, keynote notes, track analysis, plan. No application code yet,
which is correct, since code was not permitted before Sat 12:00pm.

### [09-12 17:00 AEST] @linether · RISK
Two of four invited teammates still haven't accepted the GitHub invite (sent 09-10). Only @RanchelWood
has joined so far. Nobody but me has pushed anything. Onboarding instructions are in
`docs/onboarding-prompt.md`; accept at
https://github.com/linether/ai-in-business-hackathon/invitations

### [09-12 17:00 AEST] @linether · DECIDE
**We have no idea yet and 43 hours left. This is the only thing that matters right now.**

Process is in `docs/proposals/README.md`: everyone writes one proposal, we score them against the
rubric, we pick one tonight. Proposals due **20:00 AEST tonight**, decision by **21:00**.

The single question each proposal must answer, per the sponsor: *"this task costs $X today; with our
solution it costs $Y."*

### [09-12 17:10 AEST] @linether · CHECKIN
**Roll call. Everyone reply by 19:00 AEST tonight.**

This is how we confirm four people are actually online and set up, rather than finding out at midnight
that someone's pushes don't work. **Do not reply here in chat — reply by appending an entry to this
file and pushing it.** Getting your reply into this file *is* the test.

Before you reply, your agent should have:

1. Accepted the GitHub invite → https://github.com/linether/ai-in-business-hackathon/invitations
2. Read `AGENTS.md` top to bottom
3. Cloned the repo and made one commit that **shows your own avatar on github.com**
   (if `git config user.email` doesn't match your GitHub account, it won't — fix it before replying)

Then append this, filled in, at the bottom of the board:

```
### [09-12 HH:MM AEST] @your-handle · CHECKIN
1. GitHub handle: @...
2. Commit shows my avatar on github.com: yes / no
3. From AGENTS.md — name one thing an agent must refuse to do even if asked:
4. Industries I actually know (part-time job, family business, internship, club I ran):
5. What I can own: frontend / backend / audio+ML / eval / video+pitch / deployment
6. My timezone, and the hours I'm genuinely available before Mon 12:00 AEST:
```

Question 3 is not a formality — it's how we know your agent read the rules rather than skimmed the
README. Question 4 matters because our idea lives or dies on someone having real domain contact.
Question 6 matters because we are not in the same time zone and there are 43 hours left.

If anything is broken, reply `BLOCKED` instead and say exactly what failed. A broken setup at 19:00 is
fine; a broken setup discovered at 02:00 is not.

### [09-12 17:10 AEST] @linether · FYI
Direction so far, so your replies have context: **an after-hours enrolment line for education SMEs**
(tutoring centres, language schools). The AI answers; our system scores urgency, buying intent and
parent distress from the caller's voice and decides whether to wake the owner or queue a morning
callback. Multilingual — an anxious Mandarin-speaking parent calling an Australian centre — which also
enters us in the ElevenLabs special track.

Not locked yet. If you think it's wrong, say so on the board tonight, not on Sunday.

### [09-12 17:15 AEST] @linether · FYI
@lillianguo1031-cyber is on an **iPad**, no laptop, and her GitHub account is new as of today — which
is also why the old email invite looked "expired": it was sent on 09-10 to an address that had no
GitHub account attached yet. Re-invited by username, so it should work now.

`docs/onboarding-ipad.md` is written for her. Short version:

- **Check in with zero setup** — open `BOARD.md` on github.com, tap the ✏️ pencil, append, Commit.
  Web-UI commits attribute correctly to her account automatically, so the `user.email` trap can't bite.
- Needs a terminal later → **GitHub Codespaces** (browser VS Code, nothing to install on the iPad).
- Don't assign her anything that needs a local dev server.

**Do assign her the Business Value block, the demo video and the pitch.** That's 25 rubric points plus
the artefact the entire 80-point preliminary round is judged from. iPad is a better video editing
machine than any of our laptops, and nobody should be treating this as the leftover work.

### [09-12 17:25 AEST] @linether · DECIDE
**Correcting my 17:10 entry.** I wrote up the education / after-hours-enrolment idea as though it were
our direction. It isn't. It came out of one conversation between two of us this afternoon, and it is
now sitting in `docs/proposals/linether-education-escalation.md` as **one candidate**, self-scored
**14/18 with a 0 on originality** — "customer support agent" is literally a Track 1 example and on our
own crowded-ideas list.

**It is in the pile to be beaten. Please don't converge on it by default.**

**What I need from each of you, by 20:00 AEST tonight: one proposal.**

- `docs/proposals/` → `_template.md` if you have time, or the **ten-minute version** in that folder's
  README if you don't
- On github.com: open `docs/proposals/` → **Add file** → **Create new file** → `yourname-idea.md` →
  **Commit changes**. No laptop or git needed — this works in Safari on an iPad
- There's a prompt in that README you can hand straight to your AI. It's written to interrogate *you*
  about what you've actually seen, rather than hand you generic ideas

The three questions that matter most, from the sponsor who is judging us:

1. **Who hurts** — a job title and a company size, not "businesses"
2. **What it costs them today** — hours × rate × volume
3. **Where you know this from** — a part-time job, a family business, an internship, a club you ran

That third line is worth more than the rest of the proposal. It is the only thing we have that no other
team here has, and the sponsor's advice was explicit: pick an industry you know first, then the
technology. Go where nobody is looking.

**20:00 proposals in · 21:00 decision · then we build and the idea is closed.** A 7/10 idea decided at
21:00 beats an 8/10 one decided at midnight.

### [09-12 17:30 AEST] @linether · FYI
Lowering the bar, because a good idea is hard to invent in two hours and a first-hand observation isn't.

**New: `docs/proposals/observations.md`.** If you have no idea, don't stall — go write down something
you have *watched someone do*. Who, doing what, how often, why it's painful. Three lines. Append
directly in the browser, union-merged so concurrent edits can't conflict.

> "行政老师每周三花四小时手工核对 200 个学生的课时余额，错了家长会投诉" is worth more than any
> polished proposal written from nothing.

**Hard filter for tonight, so we don't waste 21:00 arguing:** any proposal whose *"where I know this
from"* line is empty gets deprioritised. Not because it's a bad idea, but because an idea none of us has
first-hand contact with means we can't put real numbers on it — and Impact is 9 points that wants the
value "at least semi-quantified".

**@linether decides at 21:00** if we haven't converged. Committees at 21:00 with 43 hours left don't
converge, they adjourn.

### [09-12 17:35 AEST] @linether · FYI
Opened issue #1 and @-mentioned all three of you, because pushing to this board notifies nobody —
everything written here so far has had an audience of zero.

https://github.com/linether/ai-in-business-hackathon/issues/1

Same two asks: check in here by 19:00, and by 20:00 either a proposal in `docs/proposals/` or three
lines in `observations.md`. Reply to the issue if something's broken.

### [09-12 17:55 AEST] @linether · FYI
Pulled the full ElevenLabs Hacker Guide and the judge list. Two findings that change planning:

**1. ElevenLabs does not offer emotion recognition.** Their products are speech generation,
transcription, the Agents platform, dubbing, voices, music, SFX. Reading tone out of a caller's voice
is something we build ourselves. Not a blocker — it's precisely why it wouldn't count as a wrapper —
but nobody should assume it's one API call. Details in `docs/resources.md`.

Free tier is **one month of Creator ($22 value) per person**, redeemed through ElevenLabs' own Discord
(not the hackathon one). Credits are finite: cache TTS output during development.

**2. The judges are not a "cool demo" panel.** Two of five specialise in Responsible AI — Rashmika
Nawaratne's stated expertise is *"responsible AI, evaluation, knowledge retrieval, agentic
foundations"*, and Tom Porter co-authored MIT Sloan Management Review on Responsible AI and has a PhD
in statistics. Two more are BCG consultants (architecture, enterprise AI). One is a human-centred
design director.

So the eval notebook and an honest account of failure modes aren't garnish — they're aimed straight at
the majority of this panel. Full read in `docs/judges.md`.

Also: **Liam Albrecht (Eleno founder, the keynote speaker) co-founded an EdTech startup.** If we go
education, he needs no convincing that the industry is real.

### [09-12 18:05 AEST] @linether · DECIDE
**First real proposal is in — @lillianguo1031-cyber, four education directions.** Transcribed into
`docs/proposals/lillian-education-four-directions.md` (she sent it over chat; content unchanged, the
scoring section is mine). Lillian — commit your own work directly from here on, it matters for how the
history reads.

All four carry Australian specifics — CRT, VCAA, OSHC, MTOP. That's first-hand industry knowledge
rather than an LLM's prior, which is exactly what we were missing.

Scored against the nine-point checklist:

| 方向 | 分数 | |
| --- | :-: | --- |
| **三 · OSHC/MTOP 观察记录** | **17/18** | **领先** |
| 一 · CRT 备课 | 12 | 谁掏钱不清楚 |
| 二 · 多语言通知 | 12 | **技术深度 0** — 翻译 API + TTS 就是评分表说的 wrapper |
| 四 · AI 批改 | 12 | 拥挤赛道，原创性接近 0 |

**方向三 wins on almost every axis:** a paying SME operator, a genuine regulatory driver (NQF/ACECQA
ratings), a clean hours × rate × volume calculation, ground truth for an eval, and nobody else at this
hackathon will touch OSHC documentation. Voice is the *right* interface rather than a bolt-on — the
educator's hands are literally full of children, which is the same shape as **Orva**, the dental
voice-charting project in ElevenLabs' own 2025 showcase.

**Its one weakness, and it's fixable:** Lillian marked it 技术难度 低, and taken literally it *is* a
single prompt. Built as an expander it scores 3–4 on Technical Difficulty and dies in front of
Rashmika. Built as a **compliance checker** — retrieve the MTOP framework, map observations to
outcomes, then **validate whether the dictation actually evidences the outcome claimed**, and report
the gaps — it's a real system. A tool that refuses to over-claim about a child is a far stronger story
for this panel than one that writes nicer prose.

**@lillianguo1031-cyber — three things only you can answer:** OSHC educator hourly rate, what a real
observation record looks like, and what actually goes wrong when they're written badly.

@RanchelWood @Genicayyy — still nothing from either of you. Decision at 21:00. Post an observation in
`docs/proposals/observations.md` if nothing else; three lines is enough.

### [09-12 18:25 AEST] @linether · RISK
**Researched the OSHC direction. The differentiator I proposed already ships as a product.**

**StoryLoop** (storyloop.space) turns rough notes and **voice memos** into learning-story drafts, maps
them to framework outcomes "with evidence grounding", and has a **"Privacy + Evidence Guardian" that
flags unsupported claims** plus an "Observation Coach" for missing context. $19/month. That is the
refuse-to-over-claim feature, already built and sold.

And **One Child** already pairs "AI writing assistance on every plan" with **"MTOP V2.0 included by
default rather than as an upgrade"**, $10–79/month.

So "AI drafts MTOP observations and checks the evidence" is an occupied position, not a gap. Building
it gives us a 48-hour thin version of a shipping product — Originality lands in the 5–6 band.

**Finding this now is a win, not a loss.** Differentiation is 7 points and scores 0–2 for "no apparent
awareness of existing solutions". Whatever we build, we now cite these by name.

**Proposed pivot — move up a level.** Every existing product serves the same act: an educator writes
one story for one family. **None of them answers the operator's question:**

> *"The assessment visit is next week. Across this quarter, which children have no evidence at all for
> Outcome 4? Which educators' records are thin? Where will the assessor find the gap?"*

That changes the user (operator facing an ACECQA rating, not an educator writing), the act (coverage
analysis over a whole corpus, not single-document generation), and the output (a gap report: which
outcome, which child, which educator, which week). Technically it's retrieval + coverage statistics +
gap detection, which is a lot more interesting to a judge whose stated specialities are retrieval,
evaluation and agentic foundations. Voice input survives, so the ElevenLabs track survives.

**Numbers I dug up, all sourced in `docs/research-oshc.md`:** 5,077 subsidy-eligible OSHC services in
Australia · 566,600 children · Children's Services Award Level 3.1 casual **$32.73/hr** from Jul 2025
(⚠️ new FWC rates operative 1 Mar 2026 — verify before quoting) · only **30%** of educators' paid hours
are uninterrupted time with children · **91.5%** work unpaid overtime in a typical week.

⚠️ Caveat we must state honestly on stage: most of that workload research covers **early childhood
(0–5), not OSHC specifically**. Adjacent evidence, not direct. With two responsible-AI specialists and
a statistics PhD on the panel, blurring that will get caught.

**Good news:** the MTOP framework is a free public PDF from ACECQA, so our retrieval corpus is
already available.

@lillianguo1031-cyber — does the pivot match anything you've seen? Does anyone actually worry about
assessment & rating, or is that a paper problem?
