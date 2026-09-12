# ComplaintGuard 竞品补充说明

@linether 的调研补充，配合 [genicayyy-complaintguard.md](genicayyy-complaintguard.md) 一起看。
**提案本身已经点名了竞品，这里只补一件她那版没有的事：那些竞品具体做到了什么。**

## 风险：点名的竞品已经做了我们声称的两件事

提案里的差异化写的是「我们不是通用情绪分析」。**这个说法不够窄。**

| 产品 | 已有能力 | 对我们的威胁 |
| --- | --- | --- |
| **Observe.AI** | 会后分析含情绪、意图、合规遵从、**escalation risk**、CSAT 预测，覆盖全量通话 | **它已经在打"升级风险评分"** |
| **CallMiner Eureka** | **root cause analysis**（找出对话背后的根本问题）+ 情绪检测 | **它已经在打"根因分析"** |
| 行业通用 | 可挖掘"对话驱动因素、静默时段、**重复来电的根因**" | 重复来电分析不是新东西 |
| 专利 | 美国有 contact center AI **"prediction of promises"** 专利 | 承诺识别有先例 |

来源：[Observe.AI 指南](https://www.getmacha.com/blog/observe-ai-complete-guide) ·
[CallMiner vs Observe.ai](https://callminer.com/compare/callminer-vs-observe-ai) ·
[会话智能市场对比](https://www.miarec.com/conversation-intelligence-market-guide) ·
[US Patent 11410181](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11410181)

**所以台上不能说「我们预测投诉升级」，也不能说「我们做根因分析」——两句都会被戳穿。**

## 把主张再收窄一格

现有产品输出的是**分数**（`escalation risk = 0.87`）或**聚合趋势**（"本季度重复来电前三大根因"）。

我们输出的是**单个案例的因果时间线，并标出干预点**：

> 这一单升级，是因为 9 月 3 日第一通电话客服承诺 24 小时内回电、实际没发生；
> 客户 9 月 5 日、9 月 7 日两次重拨；**最早的阻断点是 9 月 4 日那个 24 小时截止时刻。**

**一条带干预点的时间线，和一个风险分数，是不同的产物。**
差异化那 7 分能不能拿到 6–7，取决于这句话说得多精确。

建议把提案里那句「Our difference is not generic sentiment analysis」改成大意如下的说法：

> Observe.AI 给的是一个升级风险分数，CallMiner 给的是聚合根因趋势。
> 两者都不告诉运营者**这一单**为什么会走到升级，也不指出**最早能阻断的那一刻**。
> 我们输出的是一条可回溯到对话证据的因果时间线，终点是一个可执行的动作。

## 另外两条建议

**跨通话关联是真正的护城河。** 单通电话分析是大路货。**demo 的高潮应该是
那个没兑现的承诺在第 1 通 → 第 2 通 → 第 3 通之间传导** —— 这才叫「链」，
也正是分数型产品给不了的单案例叙事。提案的 build order 第 5 步就是这个，
**别让它被挤到最后**。

**「未履行的承诺」当主角。** `承诺了 X，X 没发生` 是整个方案里最具体、最可验证、
最能直接转成行动的一条。demo 的高潮应该是这一刻，不是风险分数跳出来。
