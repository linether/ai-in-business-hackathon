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

Tags: `CLAIM` · `DONE` · `BLOCKED` · `DECIDE` · `FYI` · `HANDOFF` · `RISK`

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
