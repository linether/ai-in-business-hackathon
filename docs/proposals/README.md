# Proposals

One file per candidate idea. Copy `_template.md`, name it `<your-name>-<short-slug>.md`, fill it in,
commit it. One file per idea means nobody hits a merge conflict.

**Everyone writes one. Including you.** There is one proposal in here already
(`linether-education-escalation.md`) and it is *not* the plan — it came out of one conversation between
two people and it self-scores 0 on originality. It is in the pile to be beaten, not to be agreed with.

**No laptop needed.** On github.com: open this folder → **Add file** → **Create new file** → name it
`yourname-idea.md` → paste → **Commit changes**. Works fine in Safari on an iPad.

## The process, and it is time-boxed

| When (AEST) | What |
| --- | --- |
| **Sat 20:00** | Proposals in. Everyone writes at least one. A thin proposal beats no proposal |
| **Sat 20:00–21:00** | Score them against the checklist below, argue it out on `BOARD.md` |
| **Sat 21:00** | **Decision.** Record it in `../decisions.md`, split the work in `../roles.md` |
| Sat 21:00 → | Build. The idea is closed from here — reopening it on Sunday is how teams lose |

**The deadline matters more than the quality of any single proposal.** A decision at 21:00 on a
7/10 idea beats a decision at midnight on an 8/10 one.

## If you have no idea at all

**Go to [observations.md](observations.md) instead and write down something you've watched someone do.**
Not a product idea — an observation. Who, doing what, how often, why it's painful.

That file is the highest-value thing anyone can contribute tonight. A proposal invented in two hours is
usually an LLM's prior dressed up; a first-hand observation is something no other team here has.

## If you only have ten minutes

Don't let the template stop you. Open a file and answer just these three, which are the sponsor's own
three tests. We can fill in the rest together:

1. **Who hurts?** A specific person — a job title and a company size, not "businesses".
2. **What does it cost them today?** Hours × rate × volume. A rough guess with a stated source beats
   nothing.
3. **What do we build?** One sentence.

Then add one line: **where you know this from.** A part-time job, a family business, an internship, a
club you ran. That line is worth more than the rest of the proposal, because it's the thing no other
team at this hackathon has.

## Prompt for your AI

Paste this, then talk to it:

```
我在参加一个 48 小时黑客松，主题是「AI 在商业场景的应用」，
我需要在两小时内提出一个参赛点子并写成提案。

请先访问并读完这两个文件，再开始跟我讨论：
https://github.com/linether/ai-in-business-hackathon/blob/main/docs/judging.md
https://github.com/linether/ai-in-business-hackathon/blob/main/docs/keynote.md
（如果打不开，就告诉我，我把内容贴给你）

【最重要的一点】
不要直接给我一堆点子。先反过来问我：
- 我做过什么兼职、实习，家里有没有生意，我管过什么社团或组织
- 在那些地方，我亲眼见过谁在重复做什么又烦又蠢的事
赞助商（也是评委）的原话是：先选你懂的行业，再选技术；
去找那些枯燥重复的活；把能省下的钱算出来。

【然后帮我把它压成一个提案】，必须能回答：
1. 谁在痛（具体到职位和公司规模，不能是"企业"）
2. 这件事今天花他们多少钱（工时 × 时薪 × 频次）
3. 我们建什么（一句话）
4. 评委会看到的 3-5 分钟 demo 是什么样
5. 为什么这不是「套壳现有 API」——真正的技术含量在哪
6. 现有竞品是谁，我们凭什么不同

【请帮我避开这些】
这些点子几乎肯定会被多支队伍交上去，评分表会当成"知名产品的克隆"打低分：
公司文档 RAG 问答、发票/合同信息抽取、客服 agent、会议纪要同步 CRM、
简历筛选、"能解释你数据的 AI 仪表盘"。

【约束】
48 小时、4 个人、必须能部署成公开可访问的网站、必须能录一段 3-5 分钟
真实运行的演示视频。别给我 48 小时做不完的东西。

最后把提案输出成 Markdown，我要提交到 GitHub 上。
```

## Where ideas should come from

The sponsor — who is judging — was explicit about this:

> Pick an **industry you know** first, then the technology. Find the **tedious work**. Name the
> **dollar amount**. **Shrink the job down.** Go where nobody is looking.

So the useful question is not "what's a cool AI product" but: *what unglamorous, repetitive process have
I actually watched someone do?* A family business, a part-time job, an internship, a club you
administer, a lab, a student society's admin. That's where the proposals should come from.

Ties break toward Eleno's own verticals — financial services and non-bank lending, professional
services, real estate and auction houses, logistics, creative industries — because the sponsor judge
already knows the pain there is real and expensive.

## Scoring checklist

Score each proposal 0–2 on each line. This mirrors `../judging.md`, so it predicts the real score.

| # | Question | Why it matters |
| --- | --- | --- |
| 1 | Can we name the **specific person** with this problem? | Problem Significance · 8 pts; 0–4 for "unclear who actually has this problem" |
| 2 | Can we put **hours × rate × volume** on it? | Impact · 9 pts, wants it "at least semi-quantified" |
| 3 | Is there **real technical depth** — retrieval, multi-step agents, chaining, an eval? | Technical Difficulty · 8 pts; 3–4 for "mostly a wrapper on an existing API" |
| 4 | Can we **finish the demo path** in the hours left? | Functionality · 10 pts, the biggest single item |
| 5 | Can we **name existing alternatives** and say why we're different? | Differentiation · 7 pts; 0–2 if we act like none exist |
| 6 | Is it **off the obvious list** (see below)? | Originality · 10 pts; 0–4 for a clone of a known product |
| 7 | Can we **deploy** it publicly? | Explicitly scored; localhost loses marks |
| 8 | Is there **ground truth** to evaluate against? | Use of Data/Models · 6 pts |
| 9 | Would it survive *"what about cost, data access, regulation?"* | Feasibility · 8 pts |

**Anything scoring 0 on #1, #2 or #4 is out**, however exciting it is.

## The crowded list — avoid unless we have a sharp reason

Near-certain to be submitted many times over, and all sit in the rubric's "direct clone" band:

RAG chatbot over company docs · invoice / receipt / contract extraction · customer support agent ·
meeting notes → CRM · resume screening · "AI dashboard that explains your data"

## Status

| Proposal | Author | Self-score | Verdict |
| --- | --- | --- | --- |
| [ComplaintGuard 投诉升级预警](genicayyy-complaintguard.md) （+[竞品补充](complaintguard-competitive-note.md)） | @Genicayyy | **17/18**（自评） | **领先** — 提案人做过这个岗位 |
| [四个教育行业方向](lillian-education-four-directions.md) — 方向三 OSHC/MTOP | @lillianguo1031-cyber | **16/18** | **并列领先** — 调研后从 17 降，StoryLoop/One Child 占位 |
| 同上 — 方向一 CRT 备课 | @lillianguo1031-cyber | 12/18 | 付费方不清晰 |
| 同上 — 方向二 多语言通知 | @lillianguo1031-cyber | 12/18 | 技术深度 0，对这个评审团风险最高 |
| 同上 — 方向四 AI 批改 | @lillianguo1031-cyber | 12/18 | 拥挤赛道 |
| [After-hours enrolment line](linether-education-escalation.md) | @linether | 14/18 | 原创性 0 |
| _yours here_ | | | |
