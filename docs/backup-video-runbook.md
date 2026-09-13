# 备份视频录制清单（90 秒，一遍过）

> **这不是正式视频。** 目的只有一个：**先让我们有东西可交。**
> 粗糙、朴素、没有剪辑 —— 都可以。`assets/` 是空的，这比什么都糟。
>
> 下面每一个画面我都在线上站点亲眼验证过能用（09-13 22:07 AEST）。

---

## 录之前（2 分钟）

1. 浏览器开一个**干净窗口**，关掉书签栏和插件图标
2. 地址栏输入 **https://bizalchemists.duckdns.org**，让它**保持可见**（评委要看到这是线上的）
3. 缩放 100%
4. 试一句麦克风，语速比平时**慢一点**

**录屏工具**：Mac 自带，按 **`Cmd + Shift + 5`** → 选「录制整个屏幕」或「录制所选部分」
→ **点右下角「选项」，把「麦克风」选成你的麦克风**（不选就没声音）→ 点「录制」。
停止：再按 `Cmd + Shift + 5`，或点菜单栏的 ⏹ 图标。

---

## 分镜（每格念完再点下一步）

### ① 0:00–0:15 · 首页

**画面**：停在首页，鼠标不动两秒，让地址栏和黄色横幅都被看到。

> This is ComplaintGuard, running live. Everything on this site is synthetic —
> we wrote the call scripts ourselves and voiced them with ElevenLabs text to speech.
> No real customer recordings are used anywhere.

### ② 0:15–0:35 · 点开 demo-001

**画面**：点 **demo-001** → 页面加载 → 停在大号分数上。

> This customer asked to cancel an add-on they never authorised, and to be refunded.
> The escalation risk is one hundred, up from eighty-nine on the previous contact.
> But the score isn't the point.

### ③ 0:35–0:55 · 最早阻断点 ★ 主角

**画面**：慢慢往下滚，停在红色的 **EARLIEST POINT THIS COULD HAVE BEEN STOPPED**。

> The agent promised a callback within twenty-four hours. It never happened.
> The earliest point this could have been stopped was that deadline —
> on the fourth of September, before the customer ever rang back.

### ④ 0:55–1:10 · 点引文跳原文 ★

**画面**：滚到 **WHY — 7 SIGNALS**，**点任意一条理由下面那句灰色引文**
（推荐点 `REGULATOR MENTION` 那条）。页面会跳到对话原文，**那一行会淡黄色高亮**。

> Every reason carries the line it came from. Click it, and you land on the words
> the agent actually said. Nothing reaches the score without a verbatim quote
> that we check against the transcript.

### ⑤ 1:10–1:30 · 不是情绪分析 ★★ 最值钱的一段

**画面**：点左上角 **← all cases** 回首页 → 点 **demo-002** → 停在分数 **0**。

> This customer is furious about a double charge. Risk score: zero —
> because the agent fixed it during the call. Nothing is outstanding.

**画面**：回首页 → 点 **demo-003** → 停在分数 **100**。

> This customer never raises their voice. Risk score: one hundred —
> they got two contradictory answers and have already gone to the Ombudsman.
> Any system built on sentiment gets both of these backwards.

### ⑥ 1:30–1:45 · 诚实收尾

**画面**：留在 demo-003 页面，或滚回首页横幅。

> The scoring you just saw is deterministic code, not a model —
> the same case always gives the same number.
> The language extraction runs in our evaluation harness, where it scores
> eighty-eight percent precision, one hundred percent recall,
> and zero citation failures across eighty-three quotes.
> This is a backup recording; the full walkthrough is in our submission.

**停止录制。**

---

## ⚠️ 绝对不能说的两句话

这两条说了就是虚假陈述，评分表和 AGENTS.md 都明确扣分：

- ❌ **不要说** 站点在实时调用 LLM —— 案例页底部写着 `llm calls: 0`，它跑的是确定性层
- ❌ **不要说** 评委可以上传自己的音频 —— 站点只有 4 个 GET 路由，没有上传入口

---

## 录完立刻做

1. 文件存成 `assets/backup-demo.mp4`（或 .mov，不用转码）
2. 传到 Devpost 项目（描述直接粘 `docs/pitch.md` 第 2 节）
3. 在 `BOARD.md` 发一条 `DONE`

**做完这三步，我们就有一份合法完整的提交了。** 之后所有工作都是加分，不是保命。
