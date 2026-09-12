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
