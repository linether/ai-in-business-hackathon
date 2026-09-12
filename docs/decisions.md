# Decisions

One line per decision, newest at the bottom. If it was argued about, it goes here.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-09-10 | Repo starts private on GitHub | ⚠️ Submission requires a **public** repo — must flip before Mon 12pm |
| 2026-09-12 | ⏳ *under review until 21:00* — **Project: ComplaintGuard** ([@Genicayyy's proposal](proposals/genicayyy-complaintguard.md), 17/18) | Highest-scoring proposal, and the only one where an author has done the job being automated. Spec: [spec.md](spec.md) |
| 2026-09-12 | **Track 1 + ElevenLabs special track** | Improving an existing capability (complaint QA). ElevenLabs is core — TTS builds the corpus, Scribe transcribes it |
| 2026-09-12 | Data: **100% synthetic**, generated from scripts we write | No real employer data, ever. Writing the scripts also gives us free ground truth |
| 2026-09-12 | Replay first, **live mic last** | The 80-point preliminary round is scored from a video; a video only needs replay |
| 2026-09-12 | Stack: **Python + FastAPI**, minimal server-rendered frontend | Audio/LLM pipeline lives in Python. No React — judges look at the evidence panel, not our frontend |
| 2026-09-12 | Hosting: **Railway or Render** | Fastest path to the live URL the rubric explicitly rewards |
| 2026-09-12 | ✅ Google Form 队伍登记已完成 | 那个周六 12:00 的软截止，已交 |
| 2026-09-12 | Devpost 上 Requirements / Rules / Judges / Judging Criteria 全是 **TBC** | 权威规则只有 onyx wiki，提交前必须再看一遍 |
| 2026-09-12 | Devpost 奖项列表**没有 ElevenLabs 赛道** | 与 wiki 不符，需在 Discord 向主办方确认怎么参加 |
| 2026-09-12 | 部署：**自建阿里云 ECS（马来西亚）+ DuckDNS + Caddy**，不买域名 | 详见 [deploy.md](deploy.md)。DuckDNS 在公共后缀列表里，证书配额独立，不会像 nip.io/sslip.io 那样被别人耗尽 |
| 2026-09-12 | ✅ **技术栈通过评审** —— Python + FastAPI + 最小服务端渲染前端 + 阿里云 ECS | @Genicayyy 确认，并指出因 1.6 GB 内存约束不跑本地模型，转录与语言判断用外部 API |
| 2026-09-12 | ✅ **「明确不做」清单通过** | 不做实时麦克风、真实电话线路、用户账号、聚合根因看板、移动端适配 |
| 2026-09-12 | ✅ **证据校验环通过，但改为分层** | 硬事实用确定性字符串校验（优先），语义判断的蕴含校验延后；证据不足标记 `uncertain` 不进评分。定位是风险评分前的安全门，不是升级判别标准 |
| 2026-09-12 | 风险信号补充 **无人负责 / 答复矛盾 / 问题影响 / 信任变化** | 来自 @Genicayyy 的行业经验；情绪保持为**弱信号**，不能单独触发高风险 |
| 2026-09-12 | 实现优先级：**主链路端到端 > 引文校验+核心信号 > 蕴含校验 > 声学情绪** | 时间不足时按此顺序砍 |

