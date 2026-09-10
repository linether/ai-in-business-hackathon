# Forward: AI in Business Hackathon

Team repo for **Forward** — a 48-hour hackathon on applying AI in a business setting, run by
[RAID (Responsible AI Development)](https://luma.com/qmvfa2nk) and DSCubed at the University of Melbourne,
sponsored by Eleno.

Event page: https://luma.com/qmvfa2nk

## Timeline (all times Melbourne, AEST / UTC+10)

| When | What | Where |
| --- | --- | --- |
| **Thu 10 Sep, 6:00–7:30pm** | Opening night — Eleno keynote + team formation | Elisabeth Murdoch Building, G06 Theatre |
| **Sat 12 Sep, 12:00pm** | Hack starts — **challenge tracks revealed** | — |
| **Mon 14 Sep, 12:00pm** | ⛔ **Submissions close** | — |
| **Mon 14 Sep, 4:00pm** | Finalists announced | — |
| **Mon 14 Sep, 5:30–8:30pm** | Finalist pitches + awards | — |

That is **48 hours of build time**, Sat noon → Mon noon. See [docs/plan.md](docs/plan.md) for the working plan.

## Rules that affect us

- Teams of **2–5 people**; at least one member must be a current university student (any institution).
- **In-person attendance is required** for finalists / prize eligibility.
- 3 challenge tracks, revealed at kick-off on Saturday. We pick one.

## Prizes

1st **$2,000** · 2nd **$500** · 3rd **$200** · each track winner **$100**.
Plus ElevenLabs credits (Creator tier for all participants, Pro/Scale for winners) and internship/job
conversations with Eleno.

## Team

| Name | GitHub | Contact | Focus |
| --- | --- | --- | --- |
| Yixiao | @linether | yixiao004@e.ntu.edu.sg | TBD |
| | | yangyanyi20020603@gmail.com | TBD |
| | | andrewsu412@gmail.com | TBD |
| | | lillianguo1031@gmail.com | TBD |

Fill in your GitHub handle and what you want to own once you accept the invite.

## Repo layout

```
docs/          brief, plan, idea backlog, decisions
src/           application code (stack decided after tracks drop on Saturday)
notebooks/     scratch experiments, data exploration
assets/        slides, demo video, screenshots
```

## Working agreements

- `main` stays demo-able. Branch as `yourname/what-youre-doing`, PR into `main`.
- Secrets go in `.env` (gitignored). Never commit an API key — `.env.example` documents the keys we need.
- Anything decided in a call goes into [docs/decisions.md](docs/decisions.md) so nobody re-litigates it at 2am.

## Quickstart

```bash
git clone https://github.com/linether/ai-in-business-hackathon.git
cd ai-in-business-hackathon
cp .env.example .env   # then fill in your own keys
```
