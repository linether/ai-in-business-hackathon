# Pitch 材料：价值测算 · Devpost 描述 · 决赛答辩

草稿。价值测算里 **🟡 标记的空只有 @Genicayyy 填得了** —— 不要编。

---

## 1. 价值测算

### 上半段：可核实的官方数字（可以直接说）

| 数字 | 来源 |
| --- | --- |
| FY2024–25 澳洲电信投诉到 TIO **57,592 件** | TIO 年报 |
| 其中 **60.4%**（**34,779 件**）核心问题是 *"no or delayed action by provider"* | TIO 年报 Table 2 |
| **16,279 件**在转介给电信商后**又回到 TIO**，同比 **+36.9%** | TIO 年报 |
| TIO 按投诉级别向电信商收费，**越晚解决越贵**；原文：迅速解决的收费 *"much lower"* | TIO 会员页 |
| 「零投诉的会员，向 TIO 付零元」 | TIO 会员页 |

> **这一段的力量**：问题重要性不需要我们论证，监管机构在统计它。
> 而且"越晚解决越贵"是 TIO 自己说的 —— 等于官方替我们背书了"早期干预省钱"。

### 下半段：质检工时（🟡 需要 Genicayyy 的量级）

```
每名分析员每天复核录音数      🟡 30+ 条（她的实习印象）
× 每月工作日                  ~21
= 每月每人复核               🟡 ~600–700 条

× 每条平均分析时长            🟡 ??? ← 不知道，不要编
× 分析员综合时薪              🟡 参考 HK$60+；澳洲市场需另找
─────────────────────────────────────
= 当前人工复核成本
```

**@Genicayyy 在 Issue #3 里提的办法比编数字好** ——
**在评测里实测**：记录我们团队人工分析几个模拟案例的用时，
再对比"看 AI 给出的证据和不确定项"的用时，报**实测降幅**。

> 台上说法：
> *"We didn't estimate the saving. We measured it on our own labelled cases, and here's the number."*
>
> 这句话在一个有统计学博士的评审团面前，比任何漂亮的估算都强。

### 收尾那句（补上真实数字后）

> This task costs **$X** today. With ComplaintGuard it costs **$Y** —
> and every complaint we stop before it reaches the Ombudsman is a fee the telco doesn't pay at all.

---

## 2. Devpost 项目描述（可直接粘贴）

> **Team: BizAlchemists**
> **Live: https://bizalchemists.duckdns.org**
> **Track: Track 1 — Improve an Existing Business Capability.**
> **Also entered in: Built With ElevenLabs.**
>
> ### Inspiration
>
> One of us spent an internship inside a telecommunications contact centre doing complaint quality
> assurance: listening to recordings, reconstructing a customer's history, and working out which
> earlier handling failure let an ordinary complaint turn into a formal one. It is slow, and you can
> only ever sample a fraction of the calls.
>
> The Australian Telecommunications Industry Ombudsman received 57,592 complaints last financial
> year. In 60.4% of them — 34,779 — the issue was "no or delayed action by provider." Another 16,279
> came back to the Ombudsman after being referred to the telco, because the referral still didn't
> resolve them: up 36.9% in a year.
>
> ### What it does
>
> ComplaintGuard reads a customer's calls and reconstructs the failure chain — what they asked for,
> what the agent committed to, what actually happened — then marks **the earliest point the
> escalation could still have been stopped**, with every claim linked to the transcript line behind it.
>
> Existing products give you a risk score, or root-cause trends across a quarter. Neither tells an
> operator why **this** complaint escalated, or **when** it could have been caught. A per-case causal
> timeline is a different artefact, and it's the whole claim.
>
> ### How we built it
>
> Nine layers. Models read language; code makes decisions. Extraction and resolution matching use an
> LLM. Deadlines, signal detection, scoring and the intervention point are plain code with fixed
> weights — the same case always yields the same number, and every point traces to something someone
> said. Anything that scores or attributes blame has to be auditable.
>
> ElevenLabs is load-bearing rather than decorative: Scribe transcribes with diarisation and
> word-level timestamps — the evidence links depend on those timestamps — and text-to-speech voices
> the synthetic corpus that makes the whole thing demonstrable without touching real customer data.
>
> One thing beyond the pipeline: a **citation check**. The system could claim an agent promised
> something they never promised, and that would blame a real person. The highest-stakes claim is also
> the one a string comparison settles exactly, so every quote is verified verbatim against the line it
> cites. A claim that fails is marked *uncertain* — shown, but excluded from the score.
>
> ### Challenges
>
> Attribution, not detection. Strong emotion doesn't mean escalation, and a calm customer may go
> straight to the regulator. Two of our test cases exist to hold that line: one customer is shouting
> and scores zero because everything was fixed on the call; another never raises their voice and
> scores one hundred because they've already lodged with the Ombudsman. Any system built on sentiment
> gets both backwards.
>
> ### Accomplishments
>
> Twelve labelled scenarios across six root causes, seven that should escalate and five that
> shouldn't — so the evaluation measures precision, not just recall. Hallucination reported as three
> separate failure rates rather than one accuracy number. Matching by utterance index, never a model
> grading another model.
>
> ### What we learned
>
> Running it end to end before it was finished found three real faults in a morning, including a case
> where the callback was delivered exactly on time and nothing was ever assigned to anyone — invisible
> to a system watching only promises.
>
> ### What's next
>
> Real-time analysis during the call rather than after it, and a coverage view across a whole service
> for the operator facing an assessment.
>
> ### ⚠️ On the data
>
> **Everything is synthetic.** We wrote the call scripts ourselves and voiced them with ElevenLabs.
> The telco "Meridian Mobile" is fictional. **No real customer recordings, transcripts, or employer
> records are used anywhere in this project.**

---

## 3. 决赛答辩准备（前 8 名才需要，但接近一半队伍能进）

按五位评委背景倒推。**每个人都要能答，不能只靠一个人** —— 评分表明确扣罚。

### Q1 "你们怎么知道它是对的？" — Rashmika Nawaratne（专长：评测、grounding）

> 三个分开的失败率，不是一个准确率。引文失败是纯字符串比对；grounding 失败是声称在脚本里找不到对应；
> reasoning 失败是声称真实但状态判错。
>
> **匹配靠 utterance index 精确比对，不是让另一个模型判断两次抽取是不是同一条。**
> 用模型评模型是循环论证。

### Q2 "这个数字怎么算出来的？" — Tom Porter（统计学博士，"until it shows up in the numbers"）

> TIO 的数字是官方年报，您可以自己核。工时节省我们**没有估算，是在自己标注的案例上实测的**。
>
> ⚠️ 如果到时候还没实测出来：**老实说"还没测，这是估算"**，别硬报。

### Q3 "它怎么接进客户现有的系统？" — Pratik（BCG Platinion，集成架构）

> 输入是音频文件加一份联系历史，输出是 JSON。我们不替代任何系统 ——
> 读现有的通话录音和 CRM 导出，把结果推回质检人员的工作队列。
> 我们**不执行**退款、不改套餐、不开工单，只建议。

### Q4 "它什么时候会出错？谁会受影响？" — Rashmika / Tom（负责任 AI）

> 最严重的失败模式是**声称一位客服做出过他从未做出的承诺** —— 那会冤枉一个真人。
> 所以那类声称走确定性字符串校验，过不了就标 uncertain 并排除出评分。
>
> 另外：情绪是弱信号，**不能单独触发高风险**；分数**永远不单独用来评判客服**。
> 语音情绪识别对非母语者偏差更大，我们把这一点当作已知限制说出来，而不是藏起来。

### Q5 "这个问题真实存在吗，你怎么知道的？" — Sarah Bell / Liam Albrecht

> **我做过这份工作。** 中国移动实习期间，我的岗位就是听录音、判断哪些会升级、分析为什么没及时解决。
>
> 然后是 TIO 的官方数据 —— 60.4%。

### Q6 "哪部分是真的，哪部分是模拟的？" — 全体

> 真的：管线、评分、评测、证据回溯。
> 模拟的：**全部数据**（我们自己写的脚本 + TTS 配音）、**电话网络**（我们接的是上传音频，不是真实来电）。
>
> ⚠️ **主动说，别等着被问。** 评分表明确奖励坦承限制。

---

## 4. 现场 demo 注意（3–5 分钟，不接受录播）

- **先演 demo-002 和 demo-003 那一对**（咆哮=0 分 vs 平静=100 分），这是最短时间内说清差异化的方式
- 再演 demo-001 的阻断点
- **让评委自己点一个理由**，看它跳到对话原文 —— 互动比讲解有力
- 准备好网络失败的退路：本地跑一份，或者用录屏兜底
