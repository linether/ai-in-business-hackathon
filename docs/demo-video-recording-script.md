# 正式视频录制稿（人声版，目标 4:00）

> ## 🔴 这是 09-14 04:15 AEST 的**新版**。上一版作废。
>
> **@lillianguo1031-cyber 你手上录好的那一版不要删。** 它是我们唯一确定能交的东西。
> 下面是在它之上**怎么补**，以及为什么要补。

---

## 为什么要改

你录的时候，站点只有 12 个预置案例。**之后加了两个页面，而且把整个卖点往前推了一大步：**

| 新增 | 它是什么 |
| --- | --- |
| **`/live`** | **可以按住麦克风真的打一通电话。** ElevenLabs Scribe 转写你说的话，一个 AI 客服用 ElevenLabs 的声音回你，ComplaintGuard 实时读这通电话、对照写好的公司政策检查客服，**判断到需要人工介入时把电话叫停** |
| **`/try`** | 粘贴任意一段通话记录，真的跑模型分析 |

**更要紧的是：旧稿里有三句话现在会让我们掉分**，因为它们低估了自己的系统：

- ❌ 旧稿结尾："there's no upload route yet, and no live microphone" —— **两个都有了**
- ❌ 旧稿"绝对不能说"第 1 条："站点不实时调用 LLM" —— **`/live` 和 `/try` 都真调用**
- ❌ 旧稿"绝对不能说"第 2 条："评委不能自己输入" —— **现在可以**

**照旧稿念 = 主动认领一个我们已经不再有的短板。**

---

## 两个选择，你定

### 选择 A：只补 100 秒（省时间）

录一段 `/live`（下面 **0:30–2:10** 那一格），剪进你现有那版最前面，把结尾那句
"no upload route, no live microphone" 剪掉或重配。**大约 20 分钟。**

### 选择 B：按下面整篇重录（效果最好）

**大约 40 分钟**，但叙事重心对：从"看着它被叫停"开头，比从"我们分析了 12 个案例"开头强得多。

> 不管选哪个：**现有那版留着**，存成 `assets/demo-lillian-v1.mp4`。

---

## 录之前

- 浏览器**干净窗口**，关书签栏和插件图标，缩放 100%，宽度 ~1280
- **地址栏必须可见** —— 评委要看到这是线上的，不是 localhost
- **声音打开** —— 客服会用 ElevenLabs 的声音回话，这是 ElevenLabs 赛道的抓手，一定要录进去
- 录屏：`Cmd + Shift + 5` → **「选项」里把麦克风选上** → 录制
- **先不出声完整走一遍**，确认 `/live` 那通电话跑得顺
- 🔴 **开录前先点一次 🎙 把麦克风权限授权掉。** 浏览器第一次会弹权限框，
  不先清掉它就会被录进视频 —— 那在评委眼里就是一个可见瑕疵
- 旁白**用英文**，语速比平时慢

> ⚠️ **`/live` 有额度：每通 8 轮、每人每小时 6 通、全站每天 25 通。**
> 彩排 + 正式录，一小时内别超过 6 通。真超了就等一会儿，或者先录别的段落。

---

## 0:00–0:30 · 问题（画面：线上首页，边说边慢慢往下滚）

> ⚠️ **不要停在静止页面上念。** 官方原文排除 "narration over static screens"。一边说一边滚。

**画面**：打开 https://bizalchemists.duckdns.org ，**立刻开始缓慢下滚**，让案例列表一路划过。

> Last financial year, fifty-seven thousand five hundred and ninety-two telecommunications
> complaints reached the Australian Telecommunications Industry Ombudsman.
>
> The single biggest issue — sixty per cent of them — was "no or delayed action by provider."
> Not a bad product. A complaint that was handled, and then dropped.
>
> Every one of those had a moment where it could still have been stopped. We built the thing
> that finds that moment — **while the call is still happening.**

---

## 0:30–2:10 · `/live` 实录 ★★★ 全片主角

> ⚠️ **这 100 秒是整支视频的理由。** 不要压缩，不要加速。

**画面**：点首页最上面那张红色卡片 **"Hold a call and watch it get stopped →"**

**先把定位说清楚**（这句话值 17 分，见下方"为什么这句必须说"）：

> You're about to talk to an AI support agent. **The agent is the demo. What we built is the
> thing watching it.**
>
> Observe.AI scores a call after it ends. CallMiner aggregates a quarter of them.
> **Neither one interrupts a call in progress.**

**画面**：点 **Start the call** → 点 🎙 → **对着麦克风说**：

> "I rang last week about a charge I never signed up for, and nobody called me back."

**画面**：再点 ■ 发送。等客服**用声音回话**（会有两三秒，让它播完，别剪掉）。

**画面**：右边 ComplaintGuard 面板会动起来 —— 分数出现，下面列出依据，**带政策条号**。

> It transcribed that with ElevenLabs Scribe, the agent answered in its own ElevenLabs
> voice — and the panel on the right just read the call.
>
> It's already found something: the policy that governs this, and whether the agent
> did what the policy requires. **That number is not a model's opinion** — it's fixed
> weights, and every point below it quotes a line that was actually said.

**画面**：点 🎙，**说第二句**：

> "This is the third time I've rung about this. I want to speak to your boss."

**画面**：点 ■。**警报会弹出来** —— 红框，标题 **"The customer asked for a human"**，客服被停掉。

> **There it is.**
>
> Policy five-point-two — our own written policy — says a customer who asks for a supervisor
> must be given one, and that it is **not the agent's call to make.** So it isn't ours either.
> The moment they asked, we stopped the agent and called a person.
>
> And notice: **the agent said the right thing.** It said it would find a team leader.
> Saying one will be found is not the same as one arriving — and that gap is the entire
> failure mode this project exists to catch.

---

## 2:10–2:50 · 不是情绪分析 ★★ 最有说服力的 40 秒

> ⚠️ **不要压缩这一段。** 这是我们证明"不是在做语气分析"的唯一证据。

**画面**：**← all cases** → 点 **demo-002** → 停在 **THE CHAIN**（六环**全 ✓**）
→ 展开 transcript 让评委看到客户在咆哮 → 滚到分数 **0**。

> This customer is furious about a double charge. They're shouting, they interrupt.
>
> But every link in the chain holds. Risk score: **zero.** The agent reversed the charge
> during the call. Nothing is outstanding.

**画面**：回首页 → 点 **demo-003** → 停在 **THE CHAIN**（**四个 ✕**）→ 展开 transcript
（客户全程礼貌）→ 滚到分数 **100**。

> This one never raises their voice. Completely polite, the whole way through.
> Risk score: **one hundred.**
>
> They asked the same question twice and got two different answers, and on the third call
> they mention — calmly — that they've lodged with the Ombudsman.
>
> **Any system built on sentiment gets both of these backwards.**
> We track unresolved needs and unmet commitments, not tone.

---

## 2:50–3:25 · 架构与评测（画面：滚到案例页底部 RUN 区块）

**画面**：留在 demo-003，滚到最底部的 **RUN** 区块，让 `extractor` 和 `llm calls` 被看到。

> Models read language. Code makes decisions.
>
> These twelve cases run the deterministic half only — the site prints it, right here:
> **zero model calls.** Same case, same number, every time. The live call you just saw
> reports **two.** What you see is what actually ran.

**画面**：（可选，很加分）点任意一条依据里的**政策条号**，跳到政策原文页。

> When we say the agent broke a rule, **you can open the rule.**

> 📌 下面这些数字是 **09-14 04:10 AEST 真实跑出来的**（`notebooks/evaluate.py --llm`，
> 12 个案例，模型只看到对话原文，没有任何预置答案）。**只念这一版。**

> On the two decisions that matter, against the real model:
> **escalation, eighty-six per cent F1. The intervention point, eighty-three per cent —
> ten out of twelve.**
>
> And hallucination isn't one number, so we report three separately.
> **Citation failures: zero. Across eighty-seven quotes, the model never once invented
> a line.** That was the failure mode that could blame a real agent, and it didn't happen.
>
> The other two we report because they're real: **grounding sixty-two per cent,
> reasoning twenty-nine.** The extraction over-produces. We'd rather show you that
> than a single number that hides it.

---

## 3:25–4:00 · 诚实收尾（画面：回首页顶部黄色横幅）

**画面**：**← all cases** → 滚到顶部那条 "All data on this site is synthetic"。

> Everything here is synthetic. We wrote the call scripts and voiced them with ElevenLabs,
> which is also why we have exact ground truth — we know what was promised because we
> wrote it. **No real customer recordings are used anywhere.**
>
> What's real: the pipeline, the scoring, the evaluation, and the call you just held.
> What isn't: the phone network. **We don't connect to a real telco line** — you speak into
> a browser.
>
> Built for Track One, and entered in Built With ElevenLabs — **Scribe transcribes the call,
> and the agent's voice is theirs.**

**停止录制。**

---

## 为什么"对话是道具"这句必须说

评分表两条，一共 **17 分**：

- **Originality（10 分）**：明写 **"克隆知名产品给 0–4 分"**。会说话的客服机器人，
  Observe.AI、NiCE、Salesforce 全都有。**在通话进行中把电话叫停的，没有人做。**
- **Differentiation（7 分）**：**"说不出竞品给 0–2 分"**。

**如果视频看起来像"我们做了个客服机器人"，这 17 分就没了。**
所以开头那句 "The agent is the demo. What we built is the thing watching it." 不能省。

---

## ⛔ 三句绝对不能说

1. ❌ **"12 个预置案例是实时调用模型的"** —— 它们不是，RUN 区块写着 `llm calls: 0`。
   要说清楚：**预置案例是确定性的，`/live` 和 `/try` 才真调用。**
2. ❌ **"它会自动帮客户解决问题"** —— 我们不是 chatbot，我们是**判断何时该叫人**的那一层。
   说成前者直接毁掉差异化那 7 分。
3. ❌ **任何没跑出来的数字** —— 只念上面 04:10 那一版。旧稿的 88% / 75% / 0-of-83 **全部作废**。

---

## 录完

1. 存成 `assets/demo-narrated.mp4`（**别覆盖** `assets/demo.mp4` 和你的 v1）
2. 传 YouTube，**选 Unlisted（不公开列出）**，🔴 **不要选 Private —— 评委点进去是空白**
3. 确认时长在 **3–5 分钟**之间（硬要求）
4. 把链接贴到 BOARD.md 或 Issue #3，我填进 Devpost
