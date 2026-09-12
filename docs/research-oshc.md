# 调研：OSHC / MTOP 方向

2026-09-12 18:20 AEST，@linether 用公开资料调研。**所有数字都附了来源，台上要引用的先自己核一遍。**

---

## ⚠️ 最重要的发现：我们提的「证据校验」功能，已经有在售产品做了

**StoryLoop**（https://storyloop.space/）—— 做的事几乎和我们讨论的一模一样：

- AI 把教育者的**粗略笔记、语音备忘、要点**变成 learning story 初稿
- 映射到课程框架的 learning outcomes，**"with evidence grounding"**
- **"Privacy + Evidence Guardian"——自动标记诊断性用语、身份信息、以及*没有证据支撑的声称***
- **"Observation Coach"——提示缺失的儿童声音或情境**
- 明确说明"**只在观察内容支撑时才关联课程框架**"、"**不会编造儿童引语或无依据的细节**"
- 导出到 Storypark、Educa、Kinderloop、Brightwheel
- 定价：免费 3 篇/月 · 教育者 $19/月 · $29 · 机构 $99 / $199

**换句话说，我在提案里说的那个"灵魂功能"——拒绝过度声称、标出证据缺口——
是别人已经上线并且收 $19/月的功能。**

这直接打击原创性（10 分）和差异化（7 分）。

### 但有一个缺口

**StoryLoop 支持的是 Te Whāriki（新西兰）和 EYLF V2.0（澳洲早期教育，0–5 岁）。
列表里没有 MTOP。** MTOP 是**学龄儿童照护**（OSHC）的框架，人群和框架都不同。

行业对比文章的原话：*"not every platform treats MTOP V2.0 as a first-class framework."*

但注意 —— **One Child**（https://onechild.com.au/）已经同时做到了两件事：
**"AI writing assistance included on every plan"** 且 **"MTOP V2.0 included by default rather than
as an upgrade"**，$10–79/月。

**所以"AI 写 MTOP 观察记录 + 证据校验"这个位置，已经被占了。**

---

## 竞品全景

| 产品 | 定位 | AI | MTOP | 价格 |
| --- | --- | --- | --- | --- |
| **StoryLoop** | 专做 learning story 起草 | ✅ 含证据校验 | ❌ 只列 Te Whāriki / EYLF | 免费 / $19 / $29 / $99 / $199 每月 |
| **One Child** | 文档专项 | ✅ 全plan含 | ✅ **默认一等公民** | $10–79/月（按核定名额） |
| **Storypark** | 全能管理平台 | — | 支持 | $0.99–1.29/孩/月，6,700 家机构、58 万家庭 |
| **Kinderloop** | 家园沟通 | — | 支持 | $1.25/孩/月 |
| **Educa** | 文档 | — | 支持 | $1.29–1.59/孩/月 |
| Xplor / OWNA / QikKids / Kinder M8 | 全能管理 | — | 支持 | — |

**这是一个成熟、拥挤、已被商业化服务的市场。**

---

## 市场规模（可以放进 pitch）

- 澳洲有 **5,077 家**可获补贴的 OSHC 服务点，其中 **4,000+ 设在学校场地内**
- **566,600 名**小学生在用（全澳小学生总数 2,260,382），覆盖 **35 万+ 个家庭**
- 平均每周出席 **12.4 小时**

来源：[Outside School Hours Council of Australia 向生产力委员会的提交](https://assets.pc.gov.au/__data/assets/pdf_file/0019/360091/sub082-childhood.pdf) ·
[澳洲教育部 OSHC 页面](https://www.education.gov.au/early-childhood/about/service-types/oshc)

---

## 工资费率（用来算钱）

- OSHC 受 **Children's Services Award 2010 (MA000120)** 覆盖
- **Level 3.1 临时工（casual），2025 年 7 月 1 日起最低 $32.73/小时**（casual 含 25% 加载）
- ⚠️ **2025 年 12 月 10 日 FWC 出了新裁定，新费率和新分类结构 2026 年 3 月 1 日生效。**
  **台上要引用的话，必须核对当前费率。**

来源：[Fair Work Commission](https://www.fwc.gov.au/documents/awardsandorders/html/pr740806.htm) ·
[Children's Services Award 指南](https://www.tanda.com.au/blog/childrens-services-award-rates)

---

## 文档负担确实有实证（但有个重要限定）

| 数据 | 来源 |
| --- | --- |
| 幼教教师**只有 30%** 的带薪工时是"不受打扰、不被打断"地与孩子在一起 | [Harrison et al. 2024, *Australasian Journal of Early Childhood*](https://journals.sagepub.com/doi/10.1177/18369391231219820) |
| **91.5%** 的受访教育者在典型的一周里有无薪加班（Cumming et al. 2021，n=73） | [The Australian Educational Researcher](https://link.springer.com/article/10.1007/s13384-025-00847-z) |
| **超过三分之二**的教育者为满足监管要求额外加班；**一半**在评级认证期间做无薪工作 | 同上 |
| **73%** 认同高工作量损害了服务质量 | 同上 |

**⚠️ 限定条件：上面这些研究主要针对早期教育（0–5 岁）从业者，不是专门针对 OSHC。**
这是相邻证据，不是直接证据。台上要说的话，得诚实标注——
**在这个评审团面前（两位负责任 AI 专家 + 一位统计学博士），混淆这两者会被抓住。**

---

## MTOP V2.0 的五个 Learning Outcomes（建系统要用）

1. Children and young people feel safe, secure and supported
2. Children and young people develop their autonomy, interdependence, resilience and agency
3. Children and young people develop knowledgeable, confident self-identities and a sense of
   positive self-worth
4. Children and young people learn to interact in relation to others with care, empathy and respect
5. Children and young people develop a sense of belonging to groups and communities and an
   understanding of the reciprocal rights and responsibilities necessary as active and informed
   citizens

官方文件（免费公开，可以直接做检索语料）：
[ACECQA — My Time, Our Place](https://www.acecqa.gov.au/sites/default/files/2018-05/my_time_our_place_framework_for_school_age_care_in_australia_0.pdf) ·
[V2.0 变更说明](https://www.acecqa.gov.au/sites/default/files/2023-01/Whats%20changed_My_Time_Our_Place_V2.0.pdf) ·
[ACECQA MTOP Practices–Outcomes 信息表](https://www.acecqa.gov.au/information-sheet-mtop-practices-outcomes-0)

**这是个好消息：框架全文公开可下载，检索语料不用自己造。**

---

# 结论与建议

## 坏消息要认

「AI 帮教育者写 MTOP 观察记录、并校验证据」**不是空白市场**。
StoryLoop 做了证据校验，One Child 做了 AI + 一等公民的 MTOP。
我们做出来会是一个 $19/月产品的 48 小时薄版本。

原创性会落在评分表的 5–6 档（"熟悉的点子，小改动"），差异化更难讲。

**但现在知道，比在台上被评委问"你知道 StoryLoop 吗"要好一万倍。**
差异化那 7 分的评分标准是：*"能清楚说出现有替代方案，并给出具体可信的理由说明自己不同。"*
**知道竞品且能定位，本身就是得分项。**

## 建议的转向：从「写这一篇」升到「这家机构扛不扛得住评级」

现有产品全部服务**同一个动作**：教育者写一篇 learning story，给家长看。

**没有产品回答机构主管的问题：**

> *"评级检查下周来。全服务这个季度的文档里，哪些孩子完全没有 Outcome 4 的证据？
> 哪些教育者的记录是空的？评估员会在哪里找到缺口？"*

这个转向改变了四件事：

| | 原方向 | 转向后 |
| --- | --- | --- |
| **用户** | 教育者，写记录 | **机构主管 / nominated supervisor，面对 ACECQA 评级** |
| **动作** | 生成一篇 | **在整个文档语料上做覆盖度分析** |
| **产出** | 一篇漂亮记录 | **缺口报告：哪个 outcome、哪个孩子、哪个教育者、哪一周没有证据** |
| **技术** | 单文档生成 | **语料级检索 + 覆盖度统计 + 缺口检测** |

为什么这个更强：

- **竞品不做这件事。** 它们是写作助手，不是合规体检
- **技术上更有意思**——对 Rashmika（专长：检索、评测、agentic 架构）来说，
  语料级覆盖分析远比单文档生成值得聊
- **买家不同**：机构主管有预算，而且 ACECQA 评级是**公开的**，直接影响招生
- **评测有真实 ground truth**：给定一批文档，哪些 outcome 被证据支撑了？可精确测量
- **数字更硬**：评级结果是商业后果，不只是省工时
- 仍然可以保留语音输入（教育者手上带着孩子），ElevenLabs 赛道不丢

## 还需要验证的

- ACECQA 评级到底怎么影响招生和拨款？**评级是公开可查的**，但商业影响有多大需要确认
- 「Working Towards」评级的实际后果
- 有没有机构真的在为这件事发愁——**这是 Lillian 或者认识行业内人的人能回答的**
