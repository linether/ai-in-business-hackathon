# Decisions

One line per decision, newest at the bottom. If it was argued about, it goes here.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-09-10 | Repo starts private on GitHub | ⚠️ Submission requires a **public** repo — must flip before Mon 12pm |
| 2026-09-12 | **Project: ComplaintGuard** ([@Genicayyy's proposal](proposals/genicayyy-complaintguard.md), 17/18) | Highest-scoring proposal, and the only one where an author has done the job being automated. Spec: [spec.md](spec.md) |
| 2026-09-12 | **Track 1 + ElevenLabs special track** | Improving an existing capability (complaint QA). ElevenLabs is core — TTS builds the corpus, Scribe transcribes it |
| 2026-09-12 | Data: **100% synthetic**, generated from scripts we write | No real employer data, ever. Writing the scripts also gives us free ground truth |
| 2026-09-12 | Replay first, **live mic last** | The 80-point preliminary round is scored from a video; a video only needs replay |
| 2026-09-12 | Stack: **Python + FastAPI**, minimal server-rendered frontend | Audio/LLM pipeline lives in Python. No React — judges look at the evidence panel, not our frontend |
| 2026-09-12 | Hosting: **Railway or Render** | Fastest path to the live URL the rubric explicitly rewards |
