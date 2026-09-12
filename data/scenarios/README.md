# 场景脚本

**这是整条链路的输入，也是评测的 ground truth。**

因为脚本是我们自己写的，**标准答案在写的时候就确定了 —— 不需要事后标注**。

⚠️ **全部为合成数据。** 不使用任何真实客户录音、转录、工单或雇主内部资料。

---

## 怎么写一个新场景

复制任意一个 `demo-00X.json` 改。文件名 `demo-0NN.json`，序号往后排。

### 最关键的一条规则：证据锚定到句子序号

每条标注都带 `utterance_index`（在那一通电话的 `utterances` 数组里的下标，从 0 开始）。

**为什么这条重要**：评测时判断"系统抽出的承诺和标注的是不是同一条"，
靠的是 **index 精确匹配**，不是让另一个 LLM 去判断。

> 用模型评模型 = 循环论证，评委一问就塌。
> 评委里有一位统计学博士和一位评测专家，**他们一定会问"你怎么判断一次抽取是对的"**。

### 结构

```
case_id / customer_ref / language / note
ground_truth {
  should_escalate            该不该升级
  business_category          客户来电讨论什么（业务分类）
  root_cause                 为什么没解决、为什么升级（升级根因）  ← 与上一条是两套东西
  earliest_intervention_contact_seq   最早本可阻断的是第几通
  earliest_intervention_action        那时候应该做什么
  unresolved_need_ids / broken_promise_ids
  key_signals                本场景想测的风险信号
  why_this_scenario_exists   这个场景是用来测什么的（给队友看的）
}
contacts[] {
  seq / occurred_at / channel / summary
  transcript.utterances[]    { speaker, text, start_s, end_s }
  extraction { needs[] / promises[] / actions[] }   ← 标准答案，每条带 utterance_index
}
```

### 取值范围

**business_category**（客户来电讨论什么）
`计费争议` · `附加包未授权` · `网络质量` · `套餐变更` · `退费` · `服务态度`

**root_cause**（为什么升级）
`回电未兑现` · `权限不足` · `需求被误解` · `反复转接` · `政策空白` · `答复矛盾` · `无人负责` · `无`

**need.status** `resolved` · `unresolved` · `partial`
**promise.fulfilled** `true` · `false` · `null`（无法判断）

---

## ⚠️ 配比要求：必须有反例

如果每个场景都是"承诺未兑现 + 该升级"，**我们只能测召回，测不了精确率** ——
系统无脑说"有未兑现承诺"就 100% 正确。那样的评测没有意义。

目标配比：

| 类别 | 目标 | 现状 |
| --- | --- | --- |
| 该升级 | ~60% | 001 · 003 · 004 |
| **不该升级** | **~40%** | 002 ← **还差几个** |
| 承诺兑现了的 | 至少 3 个 | 002 · 004 |

### 两类硬样本（最值钱）

| 硬样本 | 证明什么 | 现状 |
| --- | --- | --- |
| **情绪激动，但问题其实已解决** | 系统不会被情绪带偏 | ✅ 002 |
| **情绪平静，但直接找监管 / 已投诉** | 系统不是在做情绪分析 | ✅ 003 |

**这两类直接回答"你们和 Observe.AI 那些情绪分析产品有什么不同"**，
是差异化那 7 分的证据。多写几个。

---

## 语境：澳大利亚，英文为主

**所有场景设定在澳洲电信市场，语言以英文为主。** 评委全是澳洲的
（UniMelb · BCG · Nous · Culture Amp），本地语境他们一秒就有代入感。

### 必须用对的澳洲要素

| 要素 | 说明 |
| --- | --- |
| **TIO**（Telecommunications Industry Ombudsman） | 澳洲电信投诉监察专员，**真实机构**。客户说"I've lodged a complaint with the Ombudsman"是最强的升级信号 |
| **Port out / porting** | 携号转网的本地说法 |
| **Early termination charge** | 提前解约费 |
| **Fault ticket** | 故障工单（vs 只在账户上留 note） |
| **网络运营商 vs 零售电信商** | 固网故障在两者之间来回推，是澳洲极真实的"无人负责"场景 |
| 货币 | **AUD** |
| 用词 | mobile（不是 cell）· fortnight · ring/rang · sorted · chase it up |

### ⚠️ 电信商用虚构名字

脚本里统一用 **"Meridian Mobile"**（虚构）。
**不要用 Telstra / Optus / Vodafone 等真实公司名** —— 编造关于真实企业的投诉记录
是不能做的事，跟比赛规则无关。

### 多语种怎么加（之后再做）

评审结论里的多语种卖点**仍然成立，但换一个更好的框法**：
澳洲本身就是多语种社会，**一个英语不流利的澳洲客户打给澳洲电信商**，
比"中国的通话"对这批评委更有说服力，也更贴近 Eleno 的市场。

**主流程稳定之后再加，不要一开始就上。**

---

## 还需要多少

明早 09:00 目标 **5 个**，周日下午扩到 **15–20 个**。

现在有 4 个（001–004）。**最缺的是"不该升级"的反例。**
