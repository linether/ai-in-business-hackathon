# Devpost 提交清单

**逐字段可粘贴。** 提交页：https://forward.devpost.com/ → 右上角 **Submit a project**

⏰ **周一 12:00 AEST 截止，迟交不审。目标 10:00 提交，留两小时缓冲。**

> ⚠️ 所有内容都按**站点实际能做的**写过一遍，09-14 04:45 重新核对。
> **现在站点确实会实时调用模型**（`/live` 和 `/try`），但**预置案例不会**（`llm calls: 0`）——
> 描述里必须把这两条路径分开说，含糊其辞两头都不讨好。
> **仍然不能说**：可以上传音频文件（只能说话或粘贴文字）、接入了真实电话网络。

---

## 提交前必须先做完的两件事

- [ ] **视频传到 YouTube 或 Vimeo**（Devpost 只收**链接**，不收文件上传）
      → 设为 **Unlisted（不公开但有链接可看）**，不要设成 Private，评委打不开
- [x] ~~**仓库转为 public**~~ ✅ **09-14 04:35 已完成**，匿名访问已验证
      （两把真实 key 在工作区和全部 git 历史里均 0 命中；无服务器 IP；`.env` 从未被跟踪）

---

## 字段逐条

### Project name
```
ComplaintGuard
```

### Elevator pitch（一句话，Devpost 限 ~200 字符）
```
Talk to an AI support agent. ComplaintGuard watches the agent, checks it against written policy, and takes the call off it the moment a human is needed. Not a chatbot — the thing watching one.
```
（190 字符。旧版只讲"事后重建失败链条"，没提现在最强的实时叫停。）

### Built with（标签，逐个加）
```
python · fastapi · pydantic · elevenlabs · elevenlabs-scribe · deepseek · bm25 · docker · caddy · jinja · mediarecorder · web-audio · html · css · javascript · pytest
```

### Try it out（链接）
```
https://bizalchemists.duckdns.org/live
https://bizalchemists.duckdns.org
https://github.com/linether/ai-in-business-hackathon
```
⚠️ **`/live` 放第一个** —— 评委点进来第一眼应该看到会动的那个，不是案例列表。

### Video demo link
```
（视频上传后填这里）
```

### Team
```
BizAlchemists
```
把四个人都加进项目（他们各自需要 Devpost 账号并接受邀请）：
@linether · @Genicayyy · @RanchelWood · @lillianguo1031-cyber

⚠️ **没被加进项目的人，作品上不会有名字。**

### Prize categories / tracks
勾选 **Track 1**。并在描述开头写明也参加 **Built With ElevenLabs**
（Devpost 的奖项列表里没有这个赛道，与 wiki 不符 —— 描述里声明，必要时在 Discord 问主办方）

---

## Project description（整段粘贴）

> ⚠️ **这一版是 09-14 04:45 AEST 重写的。** 上一版有五处已经失效，其中最严重的是把
> 「通话进行中分析」写在 *What's next* 里 —— 那已经是我们的主功能了，留在那里等于把最强的
> 东西藏起来。评测数字也全部换成 04:10 重跑的真实输出。

---

> **Team: BizAlchemists**
> **Track: Track 1 — Improve an Existing Business Capability**
> **Also entered in: Built With ElevenLabs**
>
> ### In one paragraph
>
> **[Hold a call with an AI support agent](https://bizalchemists.duckdns.org/live) — out loud, into
> your microphone — and watch ComplaintGuard take the call off the agent the moment a human is
> needed.** It reads the conversation as it happens, checks what the agent said against written
> company policy, and cites the rule it broke. **The conversation is the demo; the judgement about
> when to interrupt it is the product.** Observe.AI scores a call after it ends and CallMiner
> aggregates a quarter of them — neither interrupts one in progress. Everything that scores is plain
> code with fixed weights, every claim quotes the line that proves it, and across 87 quotes the model
> never once invented one.
>
> ## Inspiration
>
> One of us spent an internship inside a telecommunications contact centre doing complaint quality
> assurance: listening to recordings, reconstructing a customer's history, and working out which
> earlier handling failure let an ordinary complaint turn into a formal one. It is slow, and you can
> only ever sample a fraction of the calls — and by the time you find the failure, the complaint is
> already at the Ombudsman.
>
> The Australian Telecommunications Industry Ombudsman received **57,592 complaints** last financial
> year. In **60.4%** of them — 34,779 — the issue was *"no or delayed action by provider."* Another
> **16,279** came back to the Ombudsman after being referred to the telco, because the referral still
> didn't resolve them: **up 36.9% in a year.**
>
> Those are not product failures. They are calls where something was promised and then dropped.
>
> ## What it does
>
> **Open [/live](https://bizalchemists.duckdns.org/live), hold the microphone, and complain about
> something.** ElevenLabs Scribe transcribes what you say, an AI support agent answers in its own
> ElevenLabs voice — and ComplaintGuard reads the call as it happens, checks what the agent said
> against written company policy, and **takes the call off them the moment a human is needed.**
>
> **The conversation is the demo. The product is the judgement about when to interrupt it.**
>
> That distinction is the entry. A customer-facing voice bot is a category with a dozen incumbents.
> **Observe.AI** ships escalation-risk scoring; **CallMiner Eureka** ships root-cause analysis;
> NiCE, Zendesk and Salesforce ship transcription, sentiment and routing. All of them produce a
> **score** (`escalation risk = 0.87`) or an **aggregate trend**, and all of them do it *after the
> call is over.* None of them interrupts one in progress.
>
> Say *"I want to speak to your boss"* and it stops the agent immediately — not because the score
> crossed a threshold, but because our own policy 5.2 says a customer who asks for a supervisor must
> be given one and that it is **not the agent's call to make.** If it isn't the agent's, it isn't
> ours. It fires even when the agent answers well: *"I'll see if I can get a team leader"* is not a
> team leader, and that gap is the entire failure mode this project exists to catch.
>
> It also works on finished cases. Twelve prepared complaints reconstruct the **failure chain** —
> what was asked for, what was committed to, what actually happened — and mark **the earliest point
> the escalation could still have been stopped**, every claim linked to the transcript line behind it.
>
> The clearest demonstration is two of them. In one the customer is shouting, and the risk score is
> **zero**, because the agent fixed everything during the call. In another the customer never raises
> their voice, and the score is **100**, because they have already lodged with the Ombudsman over an
> answer that contradicted one they got a week earlier. **Any system built on sentiment gets both
> backwards.** You can hear both on the site.
>
> ## How we built it
>
> **Models read language; code makes decisions.** Extraction and resolution matching use an LLM.
> Deadlines, signal detection, scoring and the intervention point are plain code with fixed weights —
> the same case always yields the same number, and every point traces to something someone said.
> Anything that scores or attributes blame has to be auditable, so none of it is a model's opinion.
>
> **Retrieval sits with the supervisor, not the agent — and finding out why was the most interesting
> hour of the build.** Our first version handed the retrieved policy to the demo agent, and the agent
> stopped making mistakes: it cited the ownership rule, escalated on the third contact, honoured the
> Ombudsman mention, all correctly. That is a real finding worth stating — *an agent holding the right
> paragraph at the right moment handles the call well.* Front-line agents do not hold it, and
> modelling that away made our own demo dishonest in the direction that flattered us. So the agent now
> works from memory under time pressure, and retrieval moved to where it is load-bearing: the policy
> says what was required, and deterministic predicates check whether the agent did it. Findings cite
> the rule by section number, and you can click through and read it.
>
> Retrieval is **BM25 over twelve documents, in plain Python — no vector store**, and that is a
> decision rather than a shortcut. Over a corpus this size, written in the same register as the
> questions, lexical matching finds the right rule with no index to build and no service to call
> mid-conversation. Past a few hundred documents the argument flips; it is one function behind one
> interface.
>
> **ElevenLabs is load-bearing rather than decorative.** Scribe transcribes each live turn and, with
> diarisation and word-level timestamps, the prepared corpus — the evidence links depend on those
> timestamps. Text-to-speech voices both the corpus and the live agent, which is what makes the whole
> thing demonstrable without touching a single real customer recording.
>
> One thing beyond the pipeline: a **citation check**. The system could claim an agent promised
> something they never promised, and that would blame a real person. The highest-stakes claim is also
> the one a string comparison settles exactly, so every quote is verified verbatim against the line it
> cites. A claim that fails is marked *uncertain* — shown in the interface, excluded from the score.
> Saying *"I am not sure"* is more trustworthy than guessing.
>
> ## Challenges
>
> Attribution, not detection. Strong emotion doesn't mean escalation, and a calm customer may go
> straight to the regulator. Building the evaluation set around that was harder than building the
> detector: without cases that should **not** escalate, a system that cries wolf every time scores
> perfectly.
>
> The live call brought a second one. Our rules were written for case files — several contacts, days
> apart, statuses already settled — and almost none of them can fire inside one call in progress.
> `repeat_contact` needs two contacts on file; `missed_deadline` needs a deadline that has passed.
> Watching a call as it happens is a different problem, so it got its own layer rather than a looser
> version of the existing one: what the customer *states* (recorded as stated, because we have no
> history to verify it against) and what the policy *required and did not get.*
>
> ## Accomplishments
>
> Twelve labelled scenarios across six root causes, seven that should escalate and five that should
> not. Hallucination reported as **three separate failure rates** rather than one accuracy number,
> because citation, grounding and reasoning failures need different detectors. **Matching is by
> utterance index — never a model grading another model's output.**
>
> Measured on the real extractor, with the pipeline seeing transcripts only and nothing pre-answered:
>
> - escalation decision — **precision 86%, recall 86%, F1 86%**
> - earliest intervention point — **83%** (10 of 12)
> - **citation failures: 0%** across 87 quotes
> - grounding 62%, reasoning 29%
>
> That citation number is the one we care about most: the failure mode that would put words in a real
> agent's mouth did not occur once in 87 opportunities. The grounding rate is not fabrication — with
> citations clean, every extracted claim has a real source; the model is simply finer-grained than our
> labels, and where one line raises two things our anchor cannot say which claim maps to which. We
> report all of it as it came out, including the numbers that do not flatter us.
>
> 112 tests. One of them burns the live room's entire daily budget and then asserts the twelve
> prepared cases, the JSON API and the health check all still answer, having called no model at all —
> because a demo that takes the site down on the one afternoon judges look at it is worse than no demo.
>
> ## What we learned
>
> Making it runnable before it was finished found five real faults in a morning — including a case
> where the callback was delivered exactly on time and nothing was ever assigned to anyone, which is
> invisible to a system watching only promises. One of those five was a label we had written wrong,
> and we corrected the label rather than the code.
>
> The other lesson is the retrieval one above: **the version of your system that performs best is not
> always the one that models the problem honestly.** We caught that on ourselves and wrote it down.
>
> ## Feasibility, cost and what would have to be true
>
> Per live turn this costs roughly one transcription and one short synthesis plus two small model
> calls; the deterministic layers are free and are where every scoring decision is made. Running the
> analysis on recorded calls overnight — the realistic first deployment — costs transcription only,
> because the supervisor layer needs no model at all once extraction has run.
>
> A contact centre already records calls and already has a QA function, so the data access and the
> consent basis exist. What would have to be true for real deployment: the policy corpus becomes the
> operator's actual policy rather than ours, the signal weights get calibrated against their own
> resolved complaints instead of our twelve, and **a score is never used on its own to judge an
> agent** — a constraint we wrote into the interface and the README, not just the pitch, because the
> obvious misuse of this tool is performance-managing people with it.
>
> ## What's next
>
> Calibration against a real operator's complaint history, and a coverage view across a whole service
> for someone facing an Ombudsman assessment. Live audio arrives over a browser today; a telephony
> integration is the step after that.
>
> ## ⚠️ What is real and what is not
>
> **All data is synthetic.** We wrote the call scripts ourselves and voiced them with ElevenLabs. The
> telco "Meridian Mobile" and its policy manual are fictional. **No real customer recordings,
> transcripts, or employer records are used anywhere in this project.**
>
> Three paths on the site, and they are deliberately different:
>
> - **The twelve prepared cases** run the deterministic layers only — a case always yields the same
>   result and **no page view spends a token.** Each page prints its `extractor` and `llm calls` in a
>   Run panel, so the page corroborates this rather than asking you to take our word: it reads **0**.
> - **`/try`** analyses a transcript you paste. Two model calls, and the Run panel says so.
> - **`/live`** is the call. Transcription, the agent's reply and its voice are all real API calls.
>
> `/live` spends real credits, so it is capped — 8 turns a call, 6 calls an hour per visitor, 25 a
> day — and has a manual switch we keep open for judging. When a limit binds, that page closes with a
> message and **everything else keeps working.** The English-only check is the same principle: the
> conversation layers handle other languages fine, but the policy checks are English and would score
> everything at zero, so we say so rather than returning a confident analysis that found nothing.
>
> We are not integrated with a phone network. You speak into a browser.

---

## 提交后立刻检查

- [ ] 描述里**写明了赛道**（Track 1 + ElevenLabs）
- [ ] 仓库链接能打开，且**已是 public**
- [ ] 线上 URL 能打开（**用手机流量试，不要用队里 wifi**）
- [ ] 视频链接**匿名窗口**能打开（验证不是 Private）
- [ ] 四个队员都在项目里
- [ ] 视频时长在 **3–5 分钟**之间

---

## 截图素材（Devpost 图库，可选但建议）

线上现成的，截这三张：

1. `/case/demo-003` 顶部 —— **100 分 + 红框「最早阻断点」**
2. `/case/demo-002` —— **0 分**，配 transcript 里客户在咆哮（那组对比）
3. `/case/demo-001` 展开 transcript —— **播放按钮 + 证据高亮**
