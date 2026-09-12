# Forward: AI in Business Hackathon

Team repo for **Forward** — a 48-hour hackathon on applying AI in a business setting, run by DSCubed and
RAID (Responsible AI Development) at the University of Melbourne, sponsored by **Eleno** and **ElevenLabs**.

**Organisers' doc site is the source of truth and they update it live:**
https://onyx.nuucognition.com/published/1ef30155-a5e8-4682-9904-aa0678519c59/doc/Homepage

## Deadlines (Melbourne, AEST)

| When | What |
| --- | --- |
| Sat 12 Sep, 12:00pm | Team registration form — **soft deadline**, organisers said late is survivable. Do it anyway |
| Sat 12 Sep, 12:00pm | Coding started. Coworking at The Spot, Level 3 |
| **Mon 14 Sep, 12:00pm** | **Devpost submission closes. Late = not considered.** |
| Mon 14 Sep, 4:00pm | Top 8 finalists announced |
| Mon 14 Sep, 5:30–8:30pm | Live finalist pitches + awards, **Latham Theatre**, in person |

## Links

| What | Where |
| --- | --- |
| **Submit here (Devpost)** | https://forward.devpost.com/ |
| Team registration form | https://forms.gle/tUDRz7TwGGXUzKFZ9 |
| Hackathon Discord | https://discord.gg/KBq3tdZaF |
| ElevenLabs credit redemption | https://discord.com/invite/VnBvbbcdEC → `#coupon-codes` |
| Host — Nathan Luo | nathanluo13@gmail.com |

## What we have to hand in

1. Track name in the Devpost description
2. **Public** repo — ⚠️ this repo is currently **private**, flip it before submitting
3. Production URL — a live deployed app (localhost scores lower)
4. 3–5 min video showing the app working end-to-end, not slides

Full detail in [docs/brief.md](docs/brief.md). Rubric in [docs/judging.md](docs/judging.md). Schedule in
[docs/plan.md](docs/plan.md). What the sponsor said wins: [docs/keynote.md](docs/keynote.md).

## A note on this repo's commit history, for judges

The organisers inspect git history and no application code was permitted before **Sat 12 Sep, 12:00pm**.
Commits in this repo dated before that point contain **planning documents only** — the brief, the
judging rubric, the schedule and the decision log. Pre-Saturday planning was explicitly encouraged at
opening night. The first application code commit lands after Saturday noon.

## Tracks

Pick one of 1–3; the ElevenLabs special track can be entered **alongside** it for a second $100 shot.

1. **Improve an existing business capability** — make something businesses already do dramatically better
2. **Create a new business capability** — do something that wasn't realistically possible before
3. **Solve a business problem** — start from the problem, not the technology
- **Special: Built With ElevenLabs** — voice/audio as core functionality, not a bolted-on extra

**Our track: TBD** → record it in [docs/decisions.md](docs/decisions.md) once chosen.

## Team

| Name | GitHub | Contact | Focus |
| --- | --- | --- | --- |
| Yixiao | @linether | yixiao004@e.ntu.edu.sg | TBD |
| | @RanchelWood | | TBD |
| | @Genicayyy *(invite pending)* | | TBD |
| | *(invite pending)* | | TBD |

## Repo layout

```
docs/          brief, judging rubric, plan, idea backlog, decisions
src/           application code
notebooks/     experiments — and the eval that's worth 6 rubric points
assets/        demo video, screenshots, pitch deck
```

## Working agreements

- `main` stays demo-able. Branch as `yourname/what-youre-doing`, PR into `main`.
- Secrets go in `.env` (gitignored). Never commit a key — `.env.example` lists what we need.
- Decisions go in [docs/decisions.md](docs/decisions.md) so nobody re-litigates them at 2am.

## Quickstart

```bash
git clone https://github.com/linether/ai-in-business-hackathon.git
cd ai-in-business-hackathon
cp .env.example .env   # then fill in your own keys
```
