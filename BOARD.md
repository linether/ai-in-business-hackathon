# Message board

Async channel for the team and our agents. Everything below is append-only.

## Rules

- **Read the whole board at the start of every session.** It is how you learn what changed.
- **Append new entries at the bottom.** Never edit or delete an existing entry — reply with a new one.
- Use **AEST (Melbourne, UTC+10)** for every timestamp. We are not all in the same time zone.
- Keep entries to a few lines. This is a log, not an essay.
- ⚠️ **Post board entries straight to `main`. Never on a branch, never through a PR.** The easiest way
  is the pencil ✏️ on github.com — a web edit commits directly to `main`, so no merge can ever happen
  to it. We have already lost one message this way (see 19:35).
- The `merge=union` setting in `.gitattributes` only protects *local* merges. GitHub's server-side
  merge does not honour it, so a board post that travels through a PR branch can be dropped silently.
- If you ever do see conflict markers here, keep **both** sides and delete only the `<<<<<<<` /
  `=======` / `>>>>>>>` lines.
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

### [09-12 17:36 AEST] @Genicayyy · FYI

Submitted ComplaintGuard, based on first-hand China Mobile complaint-review work: AI tracks unresolved needs and broken promises across calls, predicts escalation, and identifies the earliest preventable intervention. Proposal and discussion are in PR #2: https://github.com/linether/ai-in-business-hackathon/pull/2

> ↑ Restored by @linether at 19:35. @Genicayyy posted this at 17:36 in commit `f82693b` and it was
> silently dropped when main was merged into her branch at 17:46. See the RISK entry at 19:35 below.

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

### [09-12 18:45 AEST] @linether · DECIDE
**Second proposal in: ComplaintGuard** — complaint-escalation analysis for contact centres, from
whoever's internship at China Mobile this was. @RanchelWood / @Genicayyy, one of you claim it here so
I can put your handle on the file. Written up at `docs/proposals/complaintguard.md`.

**It's the sharpest framing anyone has put on the table.** Not "is the customer angry" — every product
does that — but *"why did this escalate, and what was the earliest moment it could have been stopped."*

I ran the same competitor check that caught StoryLoop. **Observe.AI already ships escalation risk
scoring. CallMiner Eureka already does root cause analysis. There's a US patent on "prediction of
promises" in contact-centre AI.** So we cannot stand up and say "we predict escalation" — that gets us
caught.

**But the gap is real and narrow:** those products output a *score* (`escalation risk = 0.87`) or an
aggregate trend. This outputs a **causal timeline for one case with an intervention point marked** —
"the agent promised a callback within 24h on 3 Sep, it never happened, the customer redialled twice,
and the earliest block point was the 24h mark on 4 Sep." A timeline is a different artefact from a
score. Whether Differentiation scores 6–7 depends entirely on how precisely we say that.

**Scored 16/18 — dead level with the OSHC direction**, which dropped from 17 to 16 once research showed
StoryLoop and One Child occupy its position.

⚠️ **One hard rule if we take this:** no real recordings, transcripts or customer data from that
internship. Ever. That's an employer's confidential data and it has nothing to do with hackathon rules.
Industry knowledge yes, data no — everything synthetic, and stated as synthetic in the video and README.

**What I think breaks the tie:** Sarah Bell and Liam Albrecht will both ask "how do you know this
problem is real". *"I did this job"* is a better answer than anything else we have.

Decision at 21:00.

### [09-12 18:15 AEST] @linether · FYI
**@Genicayyy shipped PR #2 and it's merged.** Her ComplaintGuard write-up is better than the version I
transcribed from chat, so hers is canonical and I've deleted my duplicate.

She'd already covered, unprompted: naming the incumbents (NiCE CXone, CallMiner, Observe.AI, Zendesk,
Salesforce), splitting LLM judgement from deterministic scoring so decisions stay auditable, treating
emotion as a *weak* signal rather than the decision, evaluating Mandarin wording separately, refusing to
let the score auto-punish an agent, a build order that leaves live mic until last, and an eval harness
with need-extraction recall, unresolved-need F1, escalation precision/recall and evidence-grounding
accuracy. Also ruled out using any real China Mobile data before I raised it.

Her line *"the key metric is not sentiment accuracy — it is whether the system finds a materially
unresolved need early enough for a human to prevent escalation"* is the sharpest sentence in this repo.

**@RanchelWood is in too** — merged main into her branch at 17:46. Both of your commits attribute
correctly to your own accounts, so the `user.email` trap didn't catch anyone.

**One thing I've added** (`complaintguard-competitive-note.md`): the named incumbents already ship two
of the things we'd be claiming. **Observe.AI already scores escalation risk. CallMiner Eureka already
does root cause analysis.** So "our difference is not generic sentiment analysis" isn't narrow enough —
we'd get caught. The defensible claim is that they output a *score* or an *aggregate trend*, and we
output a **per-case causal timeline with the earliest intervention point marked**. Different artefact.

**Standing: ComplaintGuard 17/18 (self-scored) vs the OSHC direction 16/18** after research knocked it
down. Decision at 21:00 — 2h45m.

Nobody bothered with the check-in, and honestly that's the right call: @Genicayyy answered it by
opening a PR instead, which proves more than a roll-call reply ever would.

### [09-12 19:35 AEST] @linether · RISK
**We lost a message and I only caught it by auditing commits. Fixed, and the protocol has changed.**

@Genicayyy posted here at 17:36 (commit `f82693b`, +5 lines) announcing ComplaintGuard. When main was
merged into her branch at 17:46, **her entry was silently deleted** — that merge shows `-5` on
`BOARD.md`, which is exactly her five lines. It never reached `main`. I've restored it above, in place.

**Why the safeguard didn't work:** I set `BOARD.md merge=union` in `.gitattributes` so simultaneous
appends would both survive. That driver only applies to **local** merges. GitHub's server-side merge
(the "Update branch" button, and `gh pr merge`) does not honour it. So the one place I'd designed
against conflicts was the one place the protection didn't reach.

**New rule, effective now:**

> **Board posts go straight to `main`. Never on a branch, never through a PR.**
> The pencil ✏️ on github.com commits directly to `main` — no branch, no merge, nothing to drop.
> Code still goes through branches and PRs. The board does not.

`AGENTS.md` and the rules at the top of this file are updated.

**@Genicayyy — sorry, that was my setup's fault, not yours.** You followed the protocol exactly as
written: branch, PR, board post, template, self-score, AEST timestamps, the lot. The protocol was wrong.

### [09-12 19:45 AEST] @linether · DECIDE
**Calling it: we're building ComplaintGuard.** Full spec is now at **[docs/spec.md](docs/spec.md)** —
read it before you write anything.

Reasons, briefly: 17/18 was the top score, @Genicayyy actually did this job so *"how do you know the
problem is real"* has an unbeatable answer, and the proposal was already thought through to a build
order. Waiting until 21:00 buys us nothing and costs us tonight's only build hours. If you disagree,
say so on this board in the next hour and I'll reopen it — after that the idea is closed.

**Decisions recorded in `decisions.md`:** Track 1 + ElevenLabs special · Python/FastAPI + minimal
server-rendered frontend · Railway or Render · 100% synthetic data · replay path first, live mic last.

**The one idea in the spec worth reading twice:** we write the call scripts, then use **ElevenLabs TTS
with two voices to turn them into audio**, then our own pipeline transcribes that audio back. Because
we wrote the scripts, we already know exactly what was promised and what went unresolved — **the
ground truth comes free, with no labelling pass and no privacy risk.** It also makes ElevenLabs core to
the system rather than decorative, which is what the special track asks for.

**Claim a role here by replying `CLAIM`.** Suggested split in §9 of the spec:

- **@Genicayyy** — main pipeline + extraction (needs, promises, resolution matching). You know the
  semantics better than any of us.
- **@RanchelWood** — frontend and the evidence panel: the timeline, and clicking a reason to jump to
  the transcript line that justifies it.
- **@lillianguo1031-cyber** — scenario scripts + audio generation + labels, then the demo video and the
  value numbers. Scripts are the foundation of everything; the video is what the entire 80-point
  preliminary round is scored from. Both work fine on an iPad.
- **@linether** — deterministic rules, scoring, intervention-point detection, deployment.

**Post board entries straight to `main`** (pencil ✏️ on github.com), never through a PR — that's how
@Genicayyy's 17:36 message got eaten.

Next from me: hello-world deployed to a real URL tonight.

### [09-12 19:50 AEST] @linether · DECIDE
**Correcting my 19:45 entry — I moved faster than I should have.** I wrote "calling it" and gave an
hour to object. That's backwards: a spec nobody has read isn't a decision, it's a draft with my
assumptions baked in.

**`docs/spec.md` is now marked as a draft under review. Review is [issue #3](https://github.com/linether/ai-in-business-hackathon/issues/3), open until 21:00 AEST.**
The issue is the channel because pushing here notifies nobody — the same reason @Genicayyy's 17:36
message sat unread until I audited the commits.

It asks **8 specific questions rather than "any thoughts?"**, because a vague ask at 8pm gets a vague
answer. Five are for @Genicayyy alone — nobody else can answer them:

1. **Mandarin or English calls?** All five judges are English speakers, but your experience is a
   Mandarin-language operation. I lean bilingual, making it a feature — you'd know if that's honest.
2. **The three numbers** — recordings reviewed per month, minutes each, analyst loaded rate. Order of
   magnitude from memory only; **do not look anything up.** These three drive 9 points of Impact.
3. **What fields does a real contact record carry?** The JSON in §5.3 is my guess.
4. **Is the complaint taxonomy in §5.4 right?** I built it from your summary.
5. **Is the demo climax right?** I bet on the *earliest intervention point*. The *broken promise* might
   hit harder. You've done the job; I haven't.

And for everyone: **object to the stack now if you're going to** (I picked Python/FastAPI, minimal
server-rendered frontend, Railway/Render), say whether anything on the not-doing list is actually
essential, and — most important — **how many hours you can genuinely put in on Sunday, and your
timezone.** Roles get assigned on real availability, not willingness.

If you think the whole direction is wrong, say that too. @lillianguo1031-cyber's OSHC direction scored
16/18 and is still on the table.

**21:00 we lock it and start building.** Silence counts as agreement.

### [09-12 20:25 AEST] @linether · FYI
**Withdrawing the role assignments I posted at 19:45 and 19:50, and the ones in issue #3.**

I put names next to jobs — main pipeline to @Genicayyy, frontend to @RanchelWood, scripts and video to
@lillianguo1031-cyber — and none of you agreed to any of it. That was me deciding for you. Ignore it.

`docs/spec.md` §9 is now a **list of areas that need an owner**, with no names against them. Claim what
you actually want: a `CLAIM` entry at the bottom of this file, or a reply on issue #3.

The only thing I've claimed is what I've already written — `pipeline/rules.py`, `risk.py`,
`intervention.py` (the deterministic scoring layers) and deployment. Those carry my name because the
code is on disk, not because anyone assigned it.

### [09-12 21:15 AEST] @linether · FYI
**Looked at the Devpost page properly for the first time. Three things worth knowing.**

**1. Devpost is essentially unconfigured.** Requirements, Rules, Judges and Judging Criteria all say
**"TBC"**. The onyx wiki is the only source of truth, and the organisers said it changes during the
event — **re-read it before we submit**. It also means the submission form probably won't prompt us for
the four deliverables, so we have to remember them ourselves: track name in the description, public
repo, live URL, 3–5 min video.

**2. 32 participants are registered.** Teams are 2–5, so that's roughly 7–16 teams, and **8 make the
finals.** Somewhere near half the field gets to pitch. Making finals is very achievable; the work is in
being top 3 of those 8.

**3. The prize list on Devpost has no ElevenLabs track.** It lists 1st/2nd/3rd plus Track 1 / Track 2 /
Track 3 at $100 each — and nothing else. The wiki says the best ElevenLabs project "will have their own
track and their own special prize". The two don't match. **Someone should ask on Discord how to enter
it**, because we're planning to build for it and "declare it in the description" is currently our only
instruction.

Also, one eligibility line that's on Devpost but not the wiki: participants must be **above the legal
age of majority in their country of residence**.

### [09-12 21:15 AEST] @linether · DECIDE
**Devpost accounts — everyone needs one, today.**

@Genicayyy @RanchelWood @lillianguo1031-cyber — two minutes each:

1. Create a Devpost account: https://devpost.com/signup (GitHub login works)
2. Open https://forward.devpost.com/ and click the blue **Join hackathon** button
3. Reply here (or on issue #3) with the email or username you used

@linether will then create the project and add you as teammates. **You have to be on the Devpost
project to be credited on the submission** — if you're not added, your name isn't on the work.

Doing this now rather than Monday: a teammate discovering at 10am Monday that they have no Devpost
account is an entirely avoidable way to lose people from the submission.

**Google Form team registration is done** ✅ (confirmed by @linether). That was the one with the
Saturday noon soft deadline.

### [09-12 20:54 AEST] @Ranchelwood · CLAIM
我认领 前端 + 证据面板。本地环境已配好。
### [09-12 21:18 AEST] @Genicayyy · CLAIM
我认领 主链路 + 抽取层。本地环境已配好。

### [09-12 21:30 AEST] @linether · FYI
两个认领收到并记进 `docs/roles.md` 了：**前端 + 证据面板 → Ranchelwood**，
**主链路 + 抽取层 → Genicayyy**。两位都说本地环境配好了，而且都是直接推 `main`，
留言板这次没丢消息。

**Lillian 现在有 Mac 了**，所以不用走 iPad 那条路了 —— 直接看 `docs/setup-cli.md`
（15 分钟，`gh auth login` 一条命令解决认证）。`docs/onboarding-ipad.md` 可以忽略。

**还有三块没人碰，而且全是非代码的活**：场景脚本 + 标注、评测 notebook、
Demo 视频 + Pitch + 价值数字。

经讨论，这三块**全队一起做，不指派单一负责人**。理由是视频本来就该一起商量一起录 ——
决赛 Q&A 明确奖励"多个队员都能讲清楚项目"，而且**初赛 80 分完全由那段视频评定**，
它不该是某个人的收尾杂活。

但共同承担有个风险：**最后谁都没动手**。所以每一块都需要有人先在这里起个头，
比如"我先写 5 个场景"或"我起个 notebook 框架"，别默认别人会开始。

### [09-12 21:45 AEST] @linether · DECIDE
架构升级提案放在 `docs/architecture-upgrade.md`，Issue #3 上也贴了摘要。**是提案，不是决定。**

调研完 2026 年的 agent 架构实践，结论跟直觉相反：**只应该加一样东西，不是五样。**
业界共识是"能提前列出步骤的就用 workflow，只在某个具体失败模式要求时才叠加新模式"。
我们的流程能完整列出来，所以改成自主 agent 是降级。

加的那一样是**抽取之后的蕴含校验环**，因为确实有一个失败模式要求它：
**系统可能声称一位客服做出过他从未做出的承诺，而这会冤枉一个真人。**
这也正是让"绝不用分数自动惩罚客服"那条规矩在技术上成立的机制。

配套的评测改动是**报三个分开的失败率**（grounding / citation / reasoning），
而不是一个笼统的准确率。

这块落在抽取层里，所以主要请认领那块的人判断 —— 尤其第三个问题：
**时间上吃不吃得下。主链路跑通的优先级高于这个升级**，会挤时间就降级成纯字符串的
citation 校验，零额外调用，一样能报真实数字。

### [09-12 22:45 AEST] @linether · DECIDE
**时间表改了，`docs/plan.md` 已更新。核心是给测试和迭代留出真正的缓冲。**

**先说一个容易被忽略的事实：真正决定成绩的截止时间不是周一 12:00，是周日傍晚。**
因为那段 3–5 分钟视频必须从一个**稳定**的系统上录出来，而初赛 80 分全部由它评定。
系统周日傍晚就要能演示，不是周一早上。

上一版计划实际只留了约 2 小时给测试和录制。新版：

| 周日 AEST | |
| --- | --- |
| **12:00** | 🔵 **检查点：端到端在线上 URL 跑通一个场景。做不到就当场砍范围。** |
| **16:00** | 🔴 **功能冻结。此后不加任何新功能，没做完的直接砍。** |
| 16:00–18:00 | 只修 bug，只打磨 demo 路径 |
| 18:00–20:00 | 跑评测 + **录视频** |
| 20:00–22:00 | 缓冲：重录、提交彩排 |

周一 10:00 提交，**10:00–12:00 是纯缓冲**。

**16:00 冻结这条现在就说死，到时候就不用争。** 砍单顺序已经定好了：
主链路端到端 > 引文校验 + 核心信号 > 蕴含校验 > 声学情绪。

---

**🔴 今晚唯一还值得做的事：写场景脚本。**

它是整条链路的输入 —— **没有它，明早抽取层开工就没东西可测。**
而且不需要任何环境配置，写文字而已，任何设备都能写。

> **明早 09:00 如果仓库里有 5 个场景，抽取层可以立刻开始；没有的话，上午就废了。**

要求见 `spec.md` §5.1。特别注意**必须有反例**：该升级 vs 不该升级大致 6:4，
要有承诺兑现了的案例，还要有两种硬样本 ——
**情绪平静但直接找监管的**、**情绪激动但问题已解决的**。
那两类是我们证明"不是情绪分析"的关键样本。

谁能今晚或明早开工写几个，在这里说一声，避免撞车。

### [09-12 23:30 AEST] @linether · DONE
**场景脚本起了个头：4 个，都带标准答案，`data/scenarios/` 里。**
`data/scenarios/README.md` 写了格式规范和配比要求。**明早可以直接接着写或改。**

| 场景 | 通话 | 语言 | 该升级 | 根因 | 用来测什么 |
| --- | :-: | :-: | :-: | --- | --- |
| 001 | 3 | en | ✅ | 回电未兑现 | 基准场景，demo 主线 |
| **002** | 1 | en | ❌ | 无 | **硬样本**：情绪激动，但问题当场解决 |
| **003** | 3 | **zh** | ✅ | **答复矛盾** | **硬样本**：全程平静，已投诉监管 |
| **004** | 3 | en | ✅ | **无人负责** | 承诺**兑现了**，但问题没解决 |

**002 和 003 是一对镜像**，它们回答的是"你们和 Observe.AI 那些情绪分析产品有什么不同"：
002 情绪极高而风险低，003 情绪极低而风险极高。**任何依赖情绪的系统都会把这两单判反。**

**004 测一个容易被漏掉的区分**：回电准时打了（承诺兑现），但只是说"还在处理"——
真正的根因是**没有任何人被指派去解决问题，只有人被指派去打电话**。
如果系统把"有无未兑现承诺"当作升级的唯一依据，这单会被判低风险。

**003 是普通话的**，按评审结论把双语基线立起来了。

### 一个设计决定，写脚本的人请照做

**每条标注都带 `utterance_index`（那通电话里第几句，从 0 开始）。**

评测时判断"系统抽出的承诺和标注的是不是同一条"，靠 **index 精确匹配**，
**不是让另一个 LLM 去判断**。用模型评模型是循环论证，而评委里有一位统计学博士和
一位评测专家，**他们一定会问"你怎么判断一次抽取是对的"**。

四个场景的 index 都已校验通过。

### 还缺什么

**最缺「不该升级」的反例** —— 现在是 3:1，目标 6:4。
如果全是"承诺未兑现 + 该升级"，我们只能测召回测不了精确率，
系统无脑说"有未兑现承诺"就 100% 正确，那评测没有意义。

明早目标 5 个，周日下午扩到 15–20 个。**接着往下写的人从 `demo-005` 开始。**
