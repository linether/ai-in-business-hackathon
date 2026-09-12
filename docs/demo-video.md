# Demo 视频分镜脚本（草稿，需全队一起过一遍）

**初赛 80 分全部由这段视频 + 仓库 + 线上 URL 评定。** 它不是收尾杂活，它就是交付物。

**要求**：3–5 分钟 · 展示应用**真实运行** · 主办方原文：
*"not just slides or narration over static screens"* —— **不能是 PPT 配旁白**。

**目标时长 4:00**，留 1 分钟余量。

---

## 录之前

- [ ] 系统跑在**线上 URL** 上（不是 localhost），地址栏可见
- [ ] 浏览器缩放 100%，窗口 1280 宽左右，关掉书签栏和插件图标
- [ ] 先完整走一遍，确认**没有任何可见 bug**
- [ ] 麦克风试音，语速比平时慢一点
- [ ] **旁白用英文**（五位评委都是英语母语者）

---

## 分镜

### 0:00–0:30 · 问题（画面：线上首页）

**画面**：浏览器打开线上 URL，首页案例列表。鼠标不动，让地址栏和页面停留两秒。

**旁白**：

> Last financial year, fifty-seven thousand telecommunications complaints reached the Australian
> Telecommunications Industry Ombudsman. The single biggest issue, in sixty percent of them, was
> "no or delayed action by provider."
>
> Sixteen thousand of those came back to the Ombudsman **after** being referred to the telco —
> because the referral still didn't fix it. That number is up thirty-seven percent in a year.
>
> Inside a contact centre, the people who work out why are quality-assurance analysts. They listen
> to recordings and try to reconstruct which earlier failure let an ordinary complaint escalate.
> They can only ever sample a fraction.

> 💡 数字全部来自 TIO 官方年报，评委可自行核实。见 `docs/market-evidence.md`。

### 0:30–0:55 · 这是什么（画面：点开 demo-001）

**画面**：点击 demo-001，页面加载，停在风险分区域。

**旁白**：

> ComplaintGuard reads a customer's calls and reconstructs the chain: what they asked for, what the
> agent committed to, what actually happened, and where it went wrong.
>
> This case escalated. The score went from eighty-nine to one hundred on the latest contact.
> But the score isn't the point — **this is.**

### 0:55–1:40 · 核心：最早阻断点（画面：滚到 intervention 区块）

**画面**：慢慢滚到红色的 "Earliest point this could have been stopped"，停住。

**旁白**：

> On the third of September, the agent promised a callback within twenty-four hours to confirm a
> refund. It never happened. The customer rang twice more, and by the third call they'd mentioned
> the Ombudsman and porting out.
>
> **The earliest point this could have been stopped was the twenty-four hour mark on the fourth of
> September** — before the customer ever rang back.
>
> Every existing product I looked at gives you a risk score, or a chart of root causes across the
> quarter. None of them tells an operator when **this one** could still have been caught.

### 1:40–2:15 · 证据可回溯（画面：点击理由 → 跳转高亮）

**画面**：滚到 "Why — N signals"，**点击某条理由下的引文**，画面跳到对话原文并高亮那一行。再点一条。

**旁白**：

> Every reason carries the line it came from. Click it, and you land on the words the agent actually
> said.
>
> That matters because this system can say an agent promised something. If it's wrong about that,
> it blames a real person. So nothing reaches the score without a verbatim quote that we check
> against the transcript — **a plain string comparison, no model involved.**
>
> A claim whose quote doesn't hold up gets marked **uncertain**: still shown, excluded from the
> score. Saying "I'm not sure" is more useful than guessing.

### 2:15–3:00 · 关键一对：不是情绪分析（画面：demo-002 → demo-003）

> ⚠️ **这是整段视频最有说服力的 45 秒，不要压缩。**

**画面**：回首页 → 点 demo-002 → 展开 transcript 让评委看到客户在咆哮 → 画面停在分数 **0**。

**旁白**：

> This customer is furious. Listen to the transcript — they're shouting, they interrupt, they've
> been charged twice.
>
> Risk score: **zero.** Because the agent reversed the charge during the call and removed the
> duplicate billing entry. Nothing is outstanding.

**画面**：回首页 → 点 demo-003 → 展开 transcript → 画面停在 **100**。

**旁白**：

> This customer never raises their voice once. Completely polite, the whole way through.
>
> Risk score: **one hundred.** They asked the same question twice, got two different answers, were
> told to prove it themselves — and on the third call they mention, calmly, that they've already
> lodged with the Ombudsman.
>
> **Any system built on sentiment gets both of these backwards.** We track unresolved needs and
> unmet commitments, not tone.

### 3:00–3:35 · 架构与评测（画面：分屏或切到终端跑 evaluate.py）

**画面**：切到终端，跑 `python notebooks/evaluate.py`，让输出滚出来。

**旁白**：

> Models read language. Code makes decisions. Extraction is a language problem, so an LLM does it.
> Scoring, deadlines, and the intervention point are plain code with fixed weights — the same case
> always gives the same number, and every point traces to a line someone said.
>
> Hallucination isn't one number, so we report three: citation, grounding, and reasoning failures,
> each with its own detector. Across twelve scenarios — seven that should escalate, five that
> shouldn't — [**读出当时的真实数字**].

> ⚠️ **必须按录制当天的真实输出念，不要念这里写的数字。**
> 如果当时跑的还是 labelled stub，**必须说明这一点**，别让它听起来像真实测量。

### 3:35–4:00 · 诚实收尾（画面：回到首页顶部的黄色横幅）

**画面**：滚到首页顶部那条 "All data on this site is synthetic" 横幅。

**旁白**：

> Everything here is synthetic. We wrote the call scripts ourselves and voiced them with ElevenLabs,
> which is also why we have exact ground truth — we know what was promised because we wrote it.
> **No real customer recordings or employer records are used anywhere.**
>
> What's real: the pipeline, the scoring, the evaluation. What isn't: the phone network — we take
> uploaded audio, not live calls.
>
> Built for Track One, and entered in Built With ElevenLabs.

---

## 分工

| 角色 | 做什么 |
| --- | --- |
| 录屏 | 一个人操作鼠标，慢一点，每次点击后停半秒 |
| 旁白 | 另一个人念，**不要边操作边说**，两条轨后期对齐更稳 |
| 剪辑 | 第三个人。iPad 剪比笔记本顺手 |

**全队先一起把脚本过一遍**，确认每句话都对得上画面，再开录。

---

## 硬性检查

- [ ] 时长在 **3:00–5:00** 之间
- [ ] 全程是**真实应用**，没有静态截图、没有 PPT
- [ ] **没有可见 bug**（有就重录，这就是缓冲时间的用途）
- [ ] 明说了**哪些是合成的、哪些是模拟的**
- [ ] 地址栏显示的是**线上 URL**
- [ ] 评测数字念的是**当天真实输出**
- [ ] 文件放进 `assets/`
