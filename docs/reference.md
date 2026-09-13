# 资料索引

所有官方链接、API 文档、调研来源和关键数字。**找东西先看这里。**

最后更新：2026-09-12 · 比赛期间持续补充

---

## 1. 官方渠道

| 什么 | 链接 |
| --- | --- |
| 🔴 **组织方 Wiki（唯一权威，会更新）** | [onyx.nuucognition.com](https://onyx.nuucognition.com/published/1ef30155-a5e8-4682-9904-aa0678519c59/doc/Homepage) |
| 🔴 **Devpost（提交入口）** | https://forward.devpost.com/ |
| **比赛 Discord** | https://discord.gg/KBq3tdZaF |
| 活动页（Luma） | https://luma.com/qmvfa2nk |
| 队伍登记表（已完成 ✅） | https://forms.gle/tUDRz7TwGGXUzKFZ9 |
| 主办人 Nathan Luo | 见 Luma 活动页 |
| Devpost 注册 | https://devpost.com/signup |

> ⚠️ **Devpost 上 Requirements / Rules / Judges / Judging Criteria 全是 "TBC"。**
> 权威规则只有 Wiki，而且主办方说会在赛中更新 —— **提交前务必重读一遍 Wiki。**

Wiki 上的子页面：Hackathon Description · Timeline · FAQ · Checklist · Tracks（含 4 条赛道）·
Submission Requirements · Final Pitch Requirements · Judging Criteria (Preliminary / Finals) ·
Judges Information · Important Links · ElevenLabs Guide · Contact Information

## 2. 主办方与赞助商

| | |
| --- | --- |
| DSCubed | https://www.dscubed.org.au/ · [Discord](https://discord.gg/Q3gZcPQV63) |
| RAID UniMelb | https://www.raidunimelb.com/ · [Agora Saturdays](https://luma.com/6v5vmm9h) |
| Eleno（赞助商，keynote） | https://www.eleno.com.au/ |
| RAID 其他活动 | [Atlassian: Careers in AI](https://luma.com/652yaf7e) |

---

## 3. ElevenLabs

| 什么 | 链接 |
| --- | --- |
| 🔴 **领免费额度的 Discord**（⚠️ 不是比赛那个） | https://discord.com/invite/VnBvbbcdEC |
| Hacker Guide 原文 | [Google Doc](https://docs.google.com/document/d/1mCh5MtOzBw0aJpurQVUmIVFfPMAHW3MjNemE-LNiMto/edit) |
| 领取教程视频 | https://youtu.be/S143_JtCtV8 |
| **STT（Scribe）能力说明** | https://elevenlabs.io/docs/capabilities/speech-to-text |
| **STT API 参考** | https://elevenlabs.io/docs/api-reference/speech-to-text/convert |
| 价格与额度 | https://elevenlabs.io/pricing |
| 官方项目展示（可提交拿周边） | https://showcase.elevenlabs.io/ |
| 反馈表（填了可拿周边） | https://forms.gle/gHs8mGFGSPt6Hrco9 |

### 领取步骤

1. 注册 https://elevenlabs.io/sign-up
2. 加上面那个 Discord → `#🎟️│coupon-codes` → **Start Redemption**
3. 选活动，**用你报名黑客松时的邮箱**填表 ← 最容易错的一步
4. 机器人私信发兑换码 → 回 ElevenLabs 订阅页兑换
5. 账号设置里生成 API key，放进各自的 `.env`

卡住了去 **`#hackathon-support`** 频道，赛期有技术 moderator 在线。

### STT 调用要点

```
POST https://api.elevenlabs.io/v1/speech-to-text
Header: xi-api-key
model_id=scribe_v2   diarize=true   num_speakers=2   timestamps_granularity=word
```

返回 `words[]`，每个词带 `text` / `start` / `end` / `speaker_id`。
⚠️ 返回的是**词**不是句子，需要自己按说话人聚成对话。
⚠️ `entity_detection` 有 **30% 费用附加**，我们用合成数据，**不要开**。

### 额度（Creator 档）

| 项 | 数值 |
| --- | --- |
| 每月 credits | **121,000** |
| 并发 | ~30 |
| TTS | **~1 credit / 字符** |
| STT | **~330 credits / 分钟**（全花在 STT 约 367 分钟） |

**两条纪律**：① 转录结果必须缓存成 JSON，开发时读缓存，**绝不重复转录**
② **评测集不需要音频**（评的是文字上的抽取和判断），只给 3–5 个 demo 场景生成音频，
TTS 开销直接砍掉约 85%

---

## 4. 竞品（差异化那 7 分要用）

我们必须能点名竞品并说清不同。**装作不知道竞品存在，这项给 0–2 分。**

| 产品 | 已有能力 |
| --- | --- |
| [Observe.AI](https://www.getmacha.com/blog/observe-ai-complete-guide) | 会后分析含情绪、意图、合规、**escalation risk**、CSAT 预测 |
| [CallMiner Eureka](https://callminer.com/compare/callminer-vs-observe-ai) | **root cause analysis** + 情绪检测 |
| NiCE CXone · Zendesk Intelligent Triage · Salesforce Service Cloud | 转录、话题/情绪、质检、路由 |
| [会话智能市场对比](https://www.miarec.com/conversation-intelligence-market-guide) | 全景 |
| [US Patent 11410181](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11410181) | contact center AI 的 **"prediction of promises"** |

**我们的差异化必须窄到这个程度**（见 [complaintguard-competitive-note.md](proposals/complaintguard-competitive-note.md)）：

> 它们输出**分数**或**聚合趋势**；我们输出**单个案例的因果时间线，并标出最早干预点**。

---

## 5. 技术文档

| 主题 | 链接 |
| --- | --- |
| FastAPI | https://fastapi.tiangolo.com/ |
| Pydantic v2 | https://docs.pydantic.dev/latest/ |
| Anthropic API | https://docs.anthropic.com/ |
| Caddy（自动 HTTPS） | https://caddyserver.com/docs/ |
| DuckDNS（免费子域名） | https://www.duckdns.org/ |
| Docker Compose | https://docs.docker.com/compose/ |
| GitHub CLI | https://cli.github.com/manual/ |

### 部署相关的调研结论

- [Let's Encrypt 6 天 + IP 证书已 GA](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability) ·
  [Certbot 支持](https://letsencrypt.org/2026/03/11/shorter-certs-certbot)
  —— 但 [Caddy 支持不完整](https://github.com/caddyserver/caddy/issues/7399)，所以我们不走 IP 证书
- [sslip.io 配额已耗尽](https://github.com/cunnie/sslip.io/issues/108) —— 所以不用 nip.io/sslip.io
- [公共后缀列表](https://publicsuffix.org/list/public_suffix_list.dat) ——
  `duckdns.org` **在**列表里（每个子域名独立配额），`nip.io`/`sslip.io` **不在**。这是我们选 DuckDNS 的根据

---

## 6. 架构与评测的理论依据

写在 [architecture-upgrade.md](architecture-upgrade.md) 里的结论，来源在这：

| 主题 | 来源 |
| --- | --- |
| Agent 设计模式（2026） | [Agentic Design Patterns](https://www.sitepoint.com/the-definitive-guide-to-agentic-design-patterns-in-2026/) · [Orchestration Patterns](https://thinking.inc/en/blue-ocean/agentic/agent-orchestration-patterns/) |
| 幻觉的四种失败模式 | [LLM Hallucination 2026 Deep Dive](https://futureagi.com/blog/llm-hallucination-deep-dive-2026/) |
| Groundedness 评测方法 | [RAG Groundedness Guide](https://www.openlayer.com/blog/measuring-rag-groundedness-complete-evaluation-guide) |
| 强制引证的生成 | [Grounded generation](https://zeroentropy.dev/concepts/grounded-generation/) |

**核心两句**（台上可直接引用的立场）：

> 能提前列出步骤的就用 **workflow**，不要用 agent。只在**某个具体失败模式要求时**才叠加新模式。

> 幻觉不是一个指标，是**四种失败模式**（factual / grounding / citation / reasoning），
> 每种需要不同的检测器 —— 所以我们报三个分开的失败率，而不是一个"准确率"。

---

## 7. 关键数字速查

### 截止时间（全部墨尔本 AEST）

| 时间 | 事项 |
| --- | --- |
| **周一 14 Sep 12:00** | 🔴 **提交截止，迟交不审** |
| 周一 16:00 | 公布决赛名单（**取前 8 队**） |
| 周一 17:30–20:30 | 决赛路演，**Latham Theatre，必须本人到场** |

### 提交物（四样，缺一不可）

1. Devpost 描述里**写明赛道** 2. **公开**仓库 3. **线上 URL** 4. **3–5 分钟视频**

### 奖金

1st **$2,000** · 2nd **$500** · 3rd **$200** · Track 1/2/3 各 **$100**
（⚠️ Devpost 奖项列表**没有** ElevenLabs 赛道，与 Wiki 不符，**需向主办方确认怎么参加**）

### 评分（100 分）

初赛 80：技术 30（功能 10 / 难度 8 / 代码质量 6 / 数据与模型 6）+
创新 25（原创 10 / 创意 8 / 差异化 7）+ 商业 25（问题 8 / 可行 8 / 影响 9）
决赛 20：清晰度 6 / 现场演示 8 / 团队答辩 6

**初赛 80 分全部由那段视频 + 仓库 + URL 评定。**

### 其他

| | |
| --- | --- |
| 参赛人数 | **32 人** → 约 7–16 队，**取 8 队进决赛（接近一半）** |
| 队伍规模 | 2–5 人，至少一名在读大学生，须达法定成年年龄 |
| 工具限制 | **无**（"any technology can be used"） |
| 主办方提供数据 | **无**，自己想办法 |
| 部署服务器 | Ubuntu 22.04 · **内存 1.6 GB（跑不了本地模型）** · 40G 磁盘 |

### 🔴 澳洲官方市场数据（可直接引用，评委可核实）

完整版见 [market-evidence.md](market-evidence.md)。

- **「No or delayed action by provider」占 TIO 全部投诉的 60.4%**，FY2024–25 共 **34,779 件**
- **16,279 件**投诉在转介给服务商后**又回到 TIO**，同比 **+36.9%**
- FY2024–25 总投诉 **57,592** 件；手机服务占 44.7%
- ⚠️「Resolution agreed but not met」FY25 **下降 29.1%** —— **不要说成在恶化**
- TIO 收费：会员费 + 按月案件费，**费用随升级层级上升**，但**精确金额不公开**（会员门户）

### 行业数据（来自 @Genicayyy 实习经验，用于价值测算）

- 每名分析员**每天复核 30+ 条**录音 → 每月约 **600–700 条**
- 录音长度差异大，少数超 20 分钟
- 香港同类岗位时薪 **HK$60 以上**
- ⚠️ **平均每条分析时长未知** —— 计划在评测中实测，**不编造**

---

## 8. 仓库文档索引

| 想知道什么 | 看哪个 |
| --- | --- |
| 我该从哪开始 | [`START_HERE.md`](../START_HERE.md) |
| 协作规则与硬约束 | [`AGENTS.md`](../AGENTS.md) |
| 团队近况 | [`BOARD.md`](../BOARD.md) |
| **我们要做什么** | [`spec.md`](spec.md) |
| **评分细则** | [`judging.md`](judging.md) |
| 评委是谁、各自在意什么 | [`judges.md`](judges.md) |
| 赞助商说怎样会赢 | [`keynote.md`](keynote.md) |
| 赛道与提交要求 | [`brief.md`](brief.md) |
| 赛道怎么选、为什么 | [`track-analysis.md`](track-analysis.md) |
| 主办方/赞助商给什么 | [`resources.md`](resources.md) |
| 到底交什么、怎么选题 | [`what-to-build.md`](what-to-build.md) |
| 架构升级提案 | [`architecture-upgrade.md`](architecture-upgrade.md) |
| 部署怎么做 | [`deploy.md`](deploy.md) |
| 本地环境配置 | [`setup-cli.md`](setup-cli.md) |
| 把 AI 接进项目 | [`ai-setup.md`](ai-setup.md) |
| 谁负责什么 | [`roles.md`](roles.md) |
| 决策记录 | [`decisions.md`](decisions.md) |
| 时间表 | [`plan.md`](plan.md) |
| 各份提案 | [`proposals/`](proposals/) |

---

## 9. ⚠️ 转公开之前要检查的

✅ **已于 09-14 04:35 AEST 转为 public**，匿名访问已验证。以下是转前逐条确认的记录：

- [ ] 全库搜一遍 API key / token / 密码（`git grep -iE "sk-|api[_-]?key|token|password"`）
- [ ] 没有服务器 IP、SSH 私钥、内网地址
- [ ] 没有任何真实客户数据、真实录音、雇主内部资料
- [ ] `.env` 确实被 gitignore（`.env.example` 里只有空值）
- [ ] README 说明白**哪些是合成数据、哪些功能是模拟的**
- [ ] 提交历史里没有误提交过密钥（历史也会一起公开）
