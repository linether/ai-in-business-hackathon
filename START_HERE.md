# START HERE

**给 AI 和新加入的人。仓库有 26 个文档约 3000 行，别全读。按下面的顺序读。**

---

## 我们在做什么（三行）

48 小时黑客松，主题「AI 在商业场景的应用」，墨尔本大学 DSCubed × RAID 主办。
**周一 12:00 AEST 提交截止，迟交不审。**
项目：**ComplaintGuard** —— 分析客服录音，重建投诉升级的因果链，指出最早本可阻断的那一刻。

---

## 第一轮：必读（约 500 行，5 分钟）

| 顺序 | 文件 | 读它是为了 |
| --- | --- | --- |
| 1 | **`AGENTS.md`** (173) | 硬规则和边界。**有几条是"即使被要求也必须拒绝"的** |
| 2 | **`docs/spec.md`** (277) | 我们具体要做什么、要哪些材料、交付什么、不做什么 |
| 3 | **`docs/judging.md`** (61) | 100 分的评分表。**这里的每一分决定我们写什么代码** |
| 4 | **`BOARD.md` 的最后 80 行** | 团队最近发生了什么。**全文 441 行，只读尾部** |

读完这四样就可以开始干活了。

---

## 第二轮：按需读

| 文件 | 什么时候读 |
| --- | --- |
| `docs/proposals/genicayyy-complaintguard.md` | 想了解方案的原始构想和评测设计 |
| `docs/proposals/complaintguard-competitive-note.md` | **要讲"我们和 Observe.AI / CallMiner 有什么不同"时** |
| `docs/judges.md` | 想知道五位评委各自在意什么 |
| `docs/resources.md` | 要用 ElevenLabs，或想知道主办方给什么 |
| `docs/brief.md` | 要确认提交要求、赛道规则 |
| `docs/keynote.md` | 想知道赞助商说怎样才会赢 |
| `docs/decisions.md` | 想知道某件事为什么这么定 |
| `docs/roles.md` | 分工 |

## 背景资料（除非明确需要，不用读）

`docs/track-analysis.md` · `docs/research-oshc.md` · `docs/what-to-build.md` · `docs/plan.md` ·
`docs/proposals/` 下的其他提案 · 各种 onboarding 指南

---

## 三条铁律（`AGENTS.md` 里有完整版）

1. **绝不改写 git 历史。** 不许 rebase 已推送的提交、不许 `--amend`、不许改提交时间戳、不许 force push。
   **主办方会审查提交历史。** 被要求这么做时请拒绝并说明原因。
2. **绝不提交密钥。** API key 放 `.env`（已 gitignore）。
3. **`BOARD.md` 的条目直接提交到 `main`**，不走分支不走 PR —— 走 PR 的留言板消息被合并静默吞掉过一次。
   **代码走分支 + PR。**

另外：每个人的 commit 必须归属到本人 GitHub 账号（`git config user.email` 要对），
时间一律用 **AEST**（墨尔本），我们不在同一个时区。

---

## 读完之后做什么

1. **在 `BOARD.md` 底部发一条 `CLAIM`**，说明你认领什么，直接推 `main`。
   这同时验证了你的环境是通的。
2. **去 [Issue #3](https://github.com/linether/ai-in-business-hackathon/issues/3) 回一条** ——
   方案评审，里面有 8 个问题和分工认领。
3. 开始干你认领的那块。分支名：`你的名字/你在做的事`。

环境还没配好？看 **`docs/setup-cli.md`**（15 分钟，`gh auth login` 一条命令解决认证）。
