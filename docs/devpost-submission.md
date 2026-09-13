# Devpost 提交清单

**逐字段可粘贴。** 提交页：https://forward.devpost.com/ → 右上角 **Submit a project**

⏰ **周一 12:00 AEST 截止，迟交不审。目标 10:00 提交，留两小时缓冲。**

> ⚠️ 所有内容都按**站点实际能做的**写过一遍。**不要加上传、不要说站点实时跑 LLM** ——
> 那两条都不成立，写了就是虚假陈述。

---

## 提交前必须先做完的两件事

- [ ] **视频传到 YouTube 或 Vimeo**（Devpost 只收**链接**，不收文件上传）
      → 设为 **Unlisted（不公开但有链接可看）**，不要设成 Private，评委打不开
- [ ] **仓库转为 public** → `gh repo edit linether/ai-in-business-hackathon --visibility public`
      转之前过一遍 `docs/reference.md` §9 的检查清单（密钥已扫过，干净）

---

## 字段逐条

### Project name
```
ComplaintGuard
```

### Elevator pitch（一句话，Devpost 限 ~200 字符）
```
Reconstructs why a telecom complaint escalated — and marks the earliest point it could have been stopped, with every claim linked to the line that proves it.
```

### Built with（标签，逐个加）
```
python · fastapi · pydantic · elevenlabs · deepseek · docker · caddy · jinja · html · css · javascript
```

### Try it out（链接）
```
https://bizalchemists.duckdns.org
https://github.com/linether/ai-in-business-hackathon
```

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

> **Team: BizAlchemists**
> **Track: Track 1 — Improve an Existing Business Capability**
> **Also entered in: Built With ElevenLabs**
>
> ## Inspiration
>
> One of us spent an internship inside a telecommunications contact centre doing complaint quality
> assurance: listening to recordings, reconstructing a customer's history, and working out which
> earlier handling failure let an ordinary complaint turn into a formal one. It is slow, and you can
> only ever sample a fraction of the calls.
>
> The Australian Telecommunications Industry Ombudsman received **57,592 complaints** last financial
> year. In **60.4%** of them — 34,779 — the issue was *"no or delayed action by provider."* Another
> **16,279** came back to the Ombudsman after being referred to the telco, because the referral still
> didn't resolve them: **up 36.9% in a year.**
>
> ## What it does
>
> ComplaintGuard reads a customer's calls and reconstructs the failure chain — what they asked for,
> what the agent committed to, what actually happened — then marks **the earliest point the escalation
> could still have been stopped**, with every claim linked to the transcript line behind it.
>
> Existing tools give you a risk score, or root-cause trends across a quarter. Neither tells an
> operator why **this** complaint escalated, or **when** it could have been caught. A per-case causal
> timeline is a different artefact, and it is the whole claim.
>
> The clearest way to see the difference is two of our cases. In one, the customer is shouting — and
> the risk score is **zero**, because the agent fixed everything during the call. In another, the
> customer never raises their voice — and the score is **100**, because they have already lodged with
> the Ombudsman over an answer that contradicted the one they got a week earlier. Any system built on
> sentiment gets both backwards. You can hear both on the site.
>
> ## How we built it
>
> Nine layers. **Models read language; code makes decisions.** Extraction and resolution matching use
> an LLM. Deadlines, signal detection, scoring and the intervention point are plain code with fixed
> weights — the same case always yields the same number, and every point traces to something someone
> said. Anything that scores or attributes blame has to be auditable.
>
> ElevenLabs is load-bearing rather than decorative. Text-to-speech voiced our synthetic call corpus
> in two voices, which is what makes the system demonstrable without touching real customer data, and
> Scribe provides transcription with diarisation and word-level timestamps — the evidence links depend
> on those timestamps.
>
> One thing beyond the pipeline: a **citation check**. The system could claim an agent promised
> something they never promised, and that would blame a real person. The highest-stakes claim is also
> the one a string comparison settles exactly, so every quote is verified verbatim against the line it
> cites. A claim that fails is marked *uncertain* — shown, but excluded from the score.
>
> ## Challenges
>
> Attribution, not detection. Strong emotion doesn't mean escalation, and a calm customer may go
> straight to the regulator. Building the evaluation set around that was harder than building the
> detector: without cases that should **not** escalate, a system that cries wolf every time scores
> perfectly.
>
> ## Accomplishments
>
> Twelve labelled scenarios across six root causes, seven that should escalate and five that should
> not. Hallucination reported as **three separate failure rates** rather than one accuracy number,
> because citation, grounding and reasoning failures need different detectors. Matching is by
> utterance index — never a model grading another model's output.
>
> Measured on the real extractor, with the pipeline seeing transcripts only and nothing pre-answered:
>
> - escalation decision — **precision 88%, recall 100%, F1 93%**
> - earliest intervention point — **75%** (9 of 12)
> - **citation failures: 0%** across 83 quotes
> - grounding 60%, reasoning 33%
>
> That citation number is the one we care about most: the failure mode that would put words in a real
> agent's mouth did not occur once. The 60% grounding rate is not fabrication — with citations clean,
> every extracted claim has a real source; the model is simply finer-grained than our labels. We
> report it as it came out.
>
> ## What we learned
>
> Making it runnable before it was finished found five real faults in a morning — including a case
> where the callback was delivered exactly on time and nothing was ever assigned to anyone, which is
> invisible to a system watching only promises. One of those five was a label we had written wrong,
> and we corrected the label rather than the code.
>
> ## What's next
>
> Analysis during the call rather than after it, and a coverage view across a whole service for an
> operator facing an assessment.
>
> ## ⚠️ What is real and what is not
>
> **All data is synthetic.** We wrote the call scripts ourselves and voiced them with ElevenLabs. The
> telco "Meridian Mobile" is fictional. **No real customer recordings, transcripts, or employer
> records are used anywhere in this project.**
>
> **The deployed site runs the deterministic layers only** — scoring, timing, signals, the
> intervention point — so a case always yields the same result and no page view spends a token. **It
> does not call a model, and there is no upload route.** The LLM extraction runs in the evaluation
> harness, which is where the numbers above come from. Every case page reports its `extractor` and
> `llm calls` in a Run panel, so the page corroborates this rather than contradicting it.
>
> We are not integrated with a phone network. Audio is played back, not received live.

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
