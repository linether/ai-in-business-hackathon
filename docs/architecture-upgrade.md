# 架构升级提案：加一个蕴含校验环

**状态：提案，待评审。** 影响 [`spec.md`](spec.md) 第 4 节（架构）和第 6 节（评测）。
**尤其需要 @Genicayyy 过目** —— 这个改动落在她认领的抽取层里。

@linether 的调研 · 2026-09-12

---

## TL;DR

调研了 2026 年的 agent 架构实践之后，结论是：**我们只应该加一样东西，不是五样。**

加的是：**抽取之后的一轮蕴含校验（entailment check）**，以及随之而来的**三个分开的失败率指标**。

其余所有"升级"（自主 agent 循环、多 agent 协作、路由、向量库）我建议**明确不做**，
理由写在最后一节。

---

## 为什么不做成"真正的 agent"

2026 年的主流共识很一致：

> **能提前列出步骤的，就用 workflow。** 只有当"只有模型才能拆解任务"时，
> 才升级到 orchestrator-workers。
>
> 「Start with the simplest pattern that addresses the core problem, then layer
> additional patterns **only when a specific failure mode demands it**.
> Over-engineering agent architectures introduces coordination complexity that can
> outweigh the benefits.」

workflow 和 agent 的分界就一句话：**路径是代码定死的，还是模型自己决定的。**

我们的流程（转录 → 抽取 → 匹配 → 计时 → 评分 → 阻断点）**能完整地提前列出来**。
把它改成让模型自己决定下一步，是降级不是升级：变量更多、成本更高、更难评测，
而且换不来任何我们需要的能力。

**而且评分表也不要求。** 技术难度那 8 分列的是
「fine-tuning、RAG pipelines、agentic/multi-step reasoning、custom evaluation、
model chaining、embedding/vector search」—— 是"或"不是"且"。
我们已经命中 **model chaining** 和 **custom evaluation**。

来源：[Agentic Design Patterns 2026](https://www.sitepoint.com/the-definitive-guide-to-agentic-design-patterns-in-2026/) ·
[Agent Orchestration Patterns](https://thinking.inc/en/blue-ocean/agentic/agent-orchestration-patterns/)

---

## 那为什么这一个要加

因为**有一个具体的失败模式要求它**，而且这个失败模式在我们的场景里特别严重：

> **系统可能声称一位客服做出过某条他从未做出的承诺。**
> 而这条声称会直接进入"这一单为什么升级"的归因，**冤枉一个真人。**

这不是抽象的技术风险。在一个可能被用来评估客服绩效的系统里，
**凭空捏造一条"你承诺了却没做到"是最不可接受的错误。**

（我们在 spec 里已经写了"绝不用分数自动惩罚客服"——这是 @Genicayyy 在原提案里定的规矩。
蕴含校验是让那条规矩在技术上成立的机制。）

---

## 具体加什么

### 架构改动（spec §4）

```
③  结构化抽取       诉求 / 承诺 / 截止时间 / 动作          ← LLM
③b 蕴含校验  ★新增   逐条回查：引用的原文真的支撑这条声称吗？  ← LLM
                    通过 → 保留
                    不通过 → 丢弃并计数
④  跨通话状态跟踪
⑤  解决度匹配                                          ← LLM
⑥⑦⑧ 规则 / 评分 / 阻断点                                ← 确定性代码
```

这是 **evaluator–optimizer** 模式：抽取的模型是"doer"，校验的是"judge"，
有明确的停止条件。属于 agentic 范畴，**但它不是为了贴标签加的**——
它就是"证据可回溯"这个卖点的实现方式。

技术上对应业界叫 **claim-level entailment**：把输出拆成**原子声称**，
逐条对照原文做蕴含判断；**post-hoc verification** 是跑第二遍给每个
「声称–引证」对打分，低于阈值就拒绝。

来源：[RAG Groundedness Evaluation Guide](https://www.openlayer.com/blog/measuring-rag-groundedness-complete-evaluation-guide) ·
[Grounded generation](https://zeroentropy.dev/concepts/grounded-generation/)

### 评测改动（spec §6）—— 这块是打给技术评委的

调研里最有价值的一条：**幻觉不是一个指标，是四种不同的失败模式**
（factual / grounding / citation / reasoning），**每种需要不同的检测器**。
企业系统现在区分它们，而不是笼统报一个"准确率"。

所以我们报**三个分开的数**：

| 失败模式 | 我们的定义 | 怎么测 |
| --- | --- | --- |
| **Grounding** | 声称了一条转录里根本不存在的承诺 | 蕴含校验的拒绝率 |
| **Citation** | 引用的原文与转录不逐字一致 | 字符串比对，不用模型 |
| **Reasoning** | 承诺确实存在，但我们错判了它是否兑现 | 对照场景脚本的标准答案 |

**大多数队伍会报一个"准确率 85%"。我们报三个分开的失败率。**

来源：[LLM Hallucination 2026 Deep Dive](https://futureagi.com/blog/llm-hallucination-deep-dive-2026/)

### 埋点（几乎免费）

调研里另一条实践建议：

> **每个模式的健康度都是可测量的**——循环迭代次数、门控通过率、调用预算。
> **从第一天就埋点。**

每次运行记录：LLM 调用次数、token 数、耗时、**校验拒绝了几条**。
在界面上放一个小的"系统运行状况"区块。**成本极低，但它证明我们在认真对待可观测性。**

---

## 成本

- **每次抽取多一轮 LLM 调用** —— 走 Anthropic，**不占 ElevenLabs 额度**
- 代码量：一个校验函数 + 三个计数器 + 评测里的统计
- 估计半天以内，且**与前端、规则层并行不冲突**

---

## 明确不做的（以及为什么）

| 不做 | 原因 |
| --- | --- |
| ❌ 自主 agent 循环（模型自己决定下一步） | 步骤能预先列出，用它是降级 |
| ❌ 多 agent 协作 / orchestrator-workers | 没有需要模型来拆解的任务 |
| ❌ 按投诉类型路由到不同抽取 prompt | 36 小时内收益不抵复杂度 |
| ❌ 向量数据库 | 检索对象是一个固定的小分类法，用不着 |
| ⬜ 把案例时间线显式建成图结构 | **可选**。类型化边列表就够，别为了名词上 Neo4j |

---

## 台上怎么讲

> 我们在管线之外**只加了一样东西**：一个蕴含校验环。
> 加它是因为有一个具体的失败模式要求它 ——
> **系统可能声称一条客服从未做出的承诺，而这个错误会直接冤枉一个人。**
> 我们把它的发生率测出来了，是 X%。

**"只加了一个，因为只有一个失败模式值得加" —— 这比堆五个 agent 模式更能显出判断力。**

顺带三个本来就要做、但值得用对名词讲的机制：

- 跨通话状态跟踪 → **memory**
- 八级分类法检索 → **knowledge retrieval**
- 案例时间线（联系→诉求→承诺→动作，带时序边） → 一张**有向图**

---

## 需要确认的

1. **@Genicayyy**：校验环落在你认领的抽取层里，这个改动你认可吗？
   有没有更实际的做法（比如在抽取 prompt 里直接要求逐条给出处，再用代码校验引文是否逐字存在）？
2. 三个失败率的定义合理吗？还有没有该单独测的失败模式？
3. 时间上吃不吃得下 —— 如果主链路本身就紧张，这个可以**降级成只做 Citation 校验**
   （纯字符串比对，不用额外 LLM 调用，成本几乎为零，但仍然能报一个真实数字）
