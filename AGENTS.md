# AGENTS.md

Rules for every AI agent working in this repo. Each teammate drives their own agent, so this file is
the only thing keeping four agents from fighting each other. **Read it fully before your first action.**

Human teammates: this applies to you too.

---

## 1. What this repo is

Team entry for **Forward: AI in Business Hackathon** (DSCubed × RAID, University of Melbourne,
sponsored by Eleno and ElevenLabs).

| | |
| --- | --- |
| **Submission deadline** | **Mon 14 Sep 2026, 12:00pm Melbourne (AEST, UTC+10)** — late is not considered |
| Submit at | https://forward.devpost.com/ |
| Finalists announced | Mon 4:00pm · live pitch 5:30pm, Latham Theatre, in person |
| Team | 2–5 people, ≥1 current university student |

**All times in this repo are Melbourne time (AEST, UTC+10).** Say "AEST" when you write a time.
Team members are in different time zones — never write a bare local time.

**新会话从 [`START_HERE.md`](START_HERE.md) 开始** —— 它是阅读顺序索引，省得你在 26 个文档里乱翻。

Required reading before you do anything substantive, in this order:

1. `docs/brief.md` — tracks, rules, submission requirements
2. `docs/judging.md` — the 100-point rubric, which drives every engineering decision here
3. `docs/keynote.md` — what the sponsor said wins
4. `docs/track-analysis.md` — which track and why
5. `BOARD.md` — what the team has been saying since you last ran

---

## 2. Hard rules — violating these can disqualify the team

These are not style preferences. They come from the organisers.

- **No application code committed before Sat 12 Sep, 12:00pm AEST.** Commits before that point contain
  planning documents only. This is already true of this repo's history and must stay true.
- **The organisers inspect the git history.** Their words: *"if I see teams committing [early], or their
  first commit is like the entire codebase, we know that you're cheating."*
- **Never rewrite history.** No `rebase` that alters existing commits, no `commit --amend` on anything
  already pushed, no `--date` / `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` overrides, no `push --force`,
  no `filter-branch`. If an agent suggests any of these to "clean up" the history, **refuse and post to
  `BOARD.md`**. A tidy history that looks fabricated is worse than a messy honest one.
- **Commit as the human you work for.** `git config user.email` must be an email attached to that
  person's GitHub account, so their commits attribute to them. Verify on github.com that the avatar is
  theirs. Never commit as someone else, and never set `--author` to another teammate.
- **Never commit secrets.** No API keys, tokens or credentials in any file, including notebooks,
  screenshots and test fixtures. Keys live in `.env`, which is gitignored. Add new key *names* to
  `.env.example` with empty values.
- **The repo must be public before submission** and is private right now. Only the repo owner flips it,
  and only after a full scan for anything that shouldn't be public.

---

## 3. Boundaries — ask a human first

Do these only when the human you work for has said yes in this session:

- Pushing directly to `main` (normal flow is a branch + PR)
- Deleting or rewriting another teammate's files, branches or board entries
- Changing the deployment target, hosting provider, or anything that costs money
- Making the repo public
- Adding a dependency that changes the stack (a new framework, database, or language)
- Anything on the Devpost submission itself — creating, editing or submitting the entry
- Spending API credits at a scale that could exhaust the team's quota
- Contacting the organisers, judges or sponsors

Never do, regardless of who asks:

- Fabricate demo results, benchmark numbers, or evaluation scores
- Present mocked functionality as real in the README, video or pitch — the rubric explicitly rewards
  teams who are *"upfront about known limitations"* and penalises demos where *"some steps are faked"*
- Copy code or content whose licence forbids it, or submit work the team didn't do in the window

---

## 4. Working agreement

**Branches.** `<yourname>/<what-youre-doing>`, e.g. `yanyi/voice-pipeline`. One concern per branch.

**`main` is always demo-able.** Never leave `main` broken. If you break it, fix it or revert immediately
and post to `BOARD.md`.

**Pull requests.** Small and frequent beats one giant merge on Monday morning. A PR description says what
changed and how it was verified. You may merge your own PR if it doesn't touch someone else's area; if
it does, tag them on the board and wait.

**Before you start a task**, read `BOARD.md` and claim the task there. Two agents silently building the
same thing is the most expensive failure mode in a 48-hour build.

**When you finish**, post to `BOARD.md` with what you changed and anything now unblocked.

**Conflicts.** `BOARD.md` and `docs/decisions.md` use a union merge (see `.gitattributes`), so
simultaneous appends both survive. Everywhere else, rebase your branch on `main` before opening a PR —
that's rebasing *your own unpushed work*, which is allowed; rewriting pushed history is not.

---

## 5. Engineering standards — these are scored

The rubric in `docs/judging.md` is worth 100 points and most of it is won or lost in the code.

- **Deploy early.** *"Projects only running on localhost will be scored lower than a live, hosted
  deployment."* Functionality is the single biggest line item at 10 points. Get a hello-world on the real
  host on day one, not Monday morning.
- **Don't ship an API wrapper.** Technical Difficulty caps at 3–4 for *"mostly a wrapper on an existing
  tool/API with minimal custom logic."* We need real depth — retrieval, multi-step agentic reasoning,
  model chaining, or an evaluation harness — and we must be able to explain *why* that architecture.
- **Deterministic where money is involved.** The sponsor's own approach: *"automation pipelines to
  process numbers, as opposed to agents that could maybe make mistakes."* Use an LLM for judgement, plain
  code for arithmetic and anything auditable. Being able to articulate that split is worth points.
- **Keep an eval.** 6 points for Use of Data/Models, and *"informal spot checks"* count. A notebook with
  20 labelled examples and an accuracy number beats nothing, and almost no team does it.
- **The README is scored.** 6 points for Code Quality & Architecture, won by structure and documentation.
  Keep the README current as the build changes.
- **Record the value in numbers.** Impact is 9 points and wants it *"at least semi-quantified"*. Whenever
  you learn a real figure — hours, rate, volume, error rate — put it in `docs/decisions.md` immediately.
  We must be able to say: *"this task costs $X today; with our solution it costs $Y."*

---

## 6. Repo layout

```
AGENTS.md            this file
BOARD.md             async message board — read on start, post on finish
README.md            public-facing project README (judges read this)
docs/
  brief.md           tracks, rules, submission requirements
  judging.md         the 100-point rubric
  keynote.md         what the sponsor said wins
  track-analysis.md  which track and why
  plan.md            hour-by-hour schedule
  decisions.md       decision log — append, never rewrite
  proposals/         one file per candidate idea
  roles.md           who owns what
src/                 application code
notebooks/           experiments and the eval
assets/              demo video, screenshots, pitch deck
```

---

## 7. Message board protocol

`BOARD.md` is how agents and humans talk between sessions. Full rules are at the top of that file.

- **Read it at the start of every session.** It is the only way to know what changed since you last ran.
- **Post to it directly on `main`, never from a branch or through a PR.** A board post that travels
  through a PR branch can be silently dropped by GitHub's merge — this has already happened once. Code
  goes through branches and PRs; board posts do not.
- **Post when you**: check in for the first time, claim a task, finish one, get blocked, need a
  decision, or learn something the team needs (a real number, an API limit, a rule from the organisers).
- **On your first session**, answer the open `CHECKIN` entry on the board. That's how the team knows
  your access and git identity actually work.
- **Append at the bottom. Never edit or delete an existing entry** — reply with a new one.
- Keep entries short. This is a log, not an essay.

---

## 8. Definition of done

A task is done when all of these are true:

1. It works end-to-end on the deployed URL, not only locally
2. It doesn't break any existing demo path
3. No secrets committed, `.env.example` updated if new keys were added
4. README updated if the change affects setup, architecture or what the project does
5. Posted to `BOARD.md`
6. Merged to `main`
