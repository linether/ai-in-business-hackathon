# 正式视频录制稿（人声版，目标 4:00）

> **给 @lillianguo1031-cyber 录制用。** 仓库里已有 `assets/demo.mp4`（自动生成版，3:37）兜底，
> 所以这一版是**升级，不是救火** —— 录砸了不影响提交。
>
> 与 `docs/demo-video.md` 的区别：①旁白按 09-13 22:07 的 RISK 改过，不再声称站点实时调用 LLM
> ②加入了站点 22:44 新增的 **THE CHAIN** 区块 ③所有数字已逐条核对来源。
>
> 画面在 **https://bizalchemists.duckdns.org** 线上站点上走，全部于 09-14 01:10 AEST 复核。

---

## 录之前

- 浏览器**干净窗口**，关书签栏和插件图标，缩放 100%，宽度 ~1280
- **地址栏必须可见** —— 评委要看到这是线上的，不是 localhost
- 录屏：`Cmd + Shift + 5` → **「选项」里把麦克风选上** → 录制
- 先不出声完整走一遍，确认没有加载一半或错位
- 旁白**用英文**，语速比平时慢

---

## 0:00–0:35 · 问题（画面：首页）

**画面**：打开线上首页，鼠标不动两秒，让地址栏和黄色横幅都被看到。

> Last financial year, fifty-seven thousand five hundred and ninety-two telecommunications
> complaints reached the Australian Telecommunications Industry Ombudsman.
>
> The single biggest issue — sixty per cent of them — was "no or delayed action by provider."
>
> Sixteen thousand two hundred and seventy-nine came back to the Ombudsman **after** being
> referred to the telco, because the referral still didn't fix it. That's up thirty-seven per cent
> in a year.
>
> Inside a contact centre, the people who work out why are quality-assurance analysts.
> They listen to recordings and try to reconstruct which earlier failure let an ordinary
> complaint escalate. They can only ever sample a fraction.

> 📌 数字来源 `docs/market-evidence.md`（TIO 官方年报）：57,592 · 60.4% · 16,279 · +36.9%

---

## 0:35–1:05 · 因果链（画面：点 demo-001，停在 THE CHAIN）

**画面**：点 **demo-001** → 页面顶部就是 **THE CHAIN** → **停住三秒**，让评委读完六个环节。

> ComplaintGuard reads a customer's calls alongside their earlier contacts, and reconstructs
> the chain.
>
> The need was raised. The agent acted. But it was never resolved, the promise was never kept,
> the customer came back, and it escalated.
>
> Each link is drawn from what the pipeline found — where it shows as broken, the evidence
> is right below.

**画面**：往下滚到大号分数。

> Escalation risk: one hundred, up from eighty-nine on the previous contact.
> But the score isn't the point. **This is.**

---

## 1:05–1:45 · 最早阻断点 ★ 主角

**画面**：滚到红色的 **EARLIEST POINT THIS COULD HAVE BEEN STOPPED**，停住。

> On the third of September, the agent promised a callback within twenty-four hours
> to confirm a refund. It never happened.
>
> The customer rang twice more, and by the third call they'd mentioned the Ombudsman
> and porting out.
>
> **The earliest point this could have been stopped was that deadline — the fourth of
> September, before the customer ever rang back.**
>
> Every existing product gives you a risk score, or a chart of root causes across the quarter.
> None of them tells an operator when **this one** could still have been caught.

---

## 1:45–2:20 · 证据可回溯（画面：点引文 → 跳转高亮）

**画面**：滚到 **WHY — 7 SIGNALS**，**点 REGULATOR MENTION 下面那句灰色引文**。
页面会跳到对话原文，**折叠的 transcript 自动展开，那一行淡黄高亮**。再点一条。

> Every reason carries the line it came from. Click it, and you land on the words
> the agent actually said.
>
> That matters because this system can say an agent promised something.
> If it's wrong about that, it blames a real person.
>
> So nothing reaches the score without a verbatim quote that we check against the
> transcript — **a plain string comparison, no model involved.**
>
> A claim whose quote doesn't hold up is marked **uncertain**: still shown, excluded
> from the score. Saying "I'm not sure" is more useful than guessing.

---

## 2:20–3:05 · 不是情绪分析 ★★ 全片最有说服力的 45 秒

> ⚠️ **不要压缩这一段。**

**画面**：**← all cases** 回首页 → 点 **demo-002** → 停在 **THE CHAIN**（六个环节**全是 ✓**）
→ 展开 transcript 让评委看到客户在咆哮 → 滚到分数 **0**。

> This customer is furious about a double charge. Listen to them — they're shouting,
> they interrupt.
>
> But look at the chain: **every link holds.** Risk score: **zero.**
> The agent reversed the charge during the call and removed the duplicate entry.
> Nothing is outstanding.

**画面**：回首页 → 点 **demo-003** → 停在 **THE CHAIN**（**四个 ✕**）→ 展开 transcript
（客户全程礼貌）→ 滚到分数 **100**。

> This customer never raises their voice once. Completely polite, the whole way through.
>
> Risk score: **one hundred.** They asked the same question twice and got two different
> answers, and on the third call they mention, calmly, that they've already lodged with
> the Ombudsman.
>
> **Any system built on sentiment gets both of these backwards.**
> We track unresolved needs and unmet commitments, not tone.

---

## 3:05–3:40 · 架构与评测（画面：留在案例页，滚到底部 RUN 区块）

> ⚠️ **这段旁白是改过的。** 旧稿说 "an LLM does it"，而屏幕上 RUN 区块显示
> `llm calls: 0` —— 那是评分表说的 "some steps are faked"。**按下面这版念。**

**画面**：滚到案例页最底部的 **RUN** 区块，让 `extractor` 和 `llm calls` 被看到。

> Models read language. Code makes decisions.
>
> What you're seeing on this site is the deterministic half: scoring, deadlines and the
> intervention point are plain code with fixed weights. The same case always gives the
> same number, and every point traces to a line someone said. The site tells you so —
> it prints which extractor ran and how many model calls it made.
>
> The language extraction runs in our evaluation harness, against the same twelve
> scenarios. **Escalation judgement: eighty-eight per cent precision, one hundred per cent
> recall. Intervention point: seventy-five per cent.**
>
> And hallucination isn't one number, so we report three. **Citation failures: zero —
> across eighty-three quotes, the model never once invented a line.**
> That was the failure mode that could blame a real agent, and it didn't happen.

> 📌 数字来自 @linether 09-13 18:00 板上报告的真实 DeepSeek 运行。
> **录之前如果能重跑 `notebooks/evaluate.py`，以当时输出为准。** 数字对不上就念新的，不要念旧的。

---

## 3:40–4:00 · 诚实收尾（画面：回首页顶部黄色横幅）

**画面**：**← all cases** → 滚到顶部那条 "All data on this site is synthetic"。

> Everything here is synthetic. We wrote the call scripts ourselves and voiced them with
> ElevenLabs, which is also why we have exact ground truth — we know what was promised
> because we wrote it. **No real customer recordings are used anywhere.**
>
> What's real: the pipeline, the scoring, the evaluation.
> What isn't: the phone network. This version replays voiced scripts — **there's no upload
> route yet, and no live microphone.**
>
> Built for Track One, and entered in Built With ElevenLabs.

**停止录制。**

---

## ⛔ 三句绝对不能说

评分表和 `AGENTS.md` 都明确扣分：

1. ❌ 站点**实时调用 LLM** —— RUN 区块写着 `llm calls: 0`
2. ❌ 评委可以**上传自己的音频** —— 站点只有 4 个 GET 路由
3. ❌ 任何**没跑出来的数字** —— 只念评测真实输出

---

## 录完

1. 存成 `assets/demo-narrated.mp4`（**别覆盖** `assets/demo.mp4`，那是兜底版）
2. 和自动版比一遍，**选更好的那个**提交 —— 自动版的优势是 ElevenLabs 旁白呼应特别赛道
3. `BOARD.md` 发 `DONE`
