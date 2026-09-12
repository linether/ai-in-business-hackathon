# 主办方和赞助商提供了什么

来源：ElevenLabs 官方 Hacker Guide 全文 + 主办方 wiki。2026-09-12 拉取。

---

## ElevenLabs 给什么

### 额度：**Creator Plan 免费一个月（价值 $22），每人一份**

就这些。没有额外的黑客松专属额度，没有提升的速率限制。

**领取步骤**（每个人自己领）：

1. 加入 **ElevenLabs 的 Discord**：https://discord.com/invite/VnBvbbcdEC
   （注意：这跟比赛的 Discord 不是同一个）
2. 进入 `#🎟️│coupon-codes` 频道
3. 点 **Start Redemption**
4. 选择本次活动，**用你报名时填的邮箱**填表
5. 机器人私信发你兑换码

**技术支持**：ElevenLabs Discord 的 `#hackathon-support` 频道，
**活动期间有技术 moderator 在线**。有 API 问题直接去那里问，比自己猜快得多。

### 能用的产品

| 产品 | 能力 |
| --- | --- |
| **Generate Speech** | 文字转语音，32 种语言 |
| **Transcribe Speech** | 语音转文字（STT） |
| **Deploy Agents** | 语音/文字 agent 平台，32 语言、低延迟、可接知识库和工具 |
| **Dub audio file** | 音频翻译，保留情绪、时序、语调 |
| **Create Voices** | 创建和定制音色 |
| **Compose Music** | 文字生成音乐 |
| **Create Sound Effects** | 文字生成音效 |

Agents 平台原文：*"Deploy natural, human-sounding agents in 32 languages with low latency in voice or
chat. Connected to your knowledge base and tools, our agents handle complex workflows."*
有模板 agent 可以直接起步，也可以从零搭。

### ⚠️ 必须知道的一件事：**ElevenLabs 不提供情绪识别**

产品清单里**没有任何「从语音中识别情绪/语气」的 API**。它们做的是：
语音**生成**、语音**转录**、agent 编排、配音时**保留**情绪。

「听出对方语气」这件事，**得我们自己做**——韵律特征提取、或者接别的音频模型。

这不是坏消息：
- 坏的一面：工作量比想象中大，要自己搭
- **好的一面：正因为不是现成 API，它才不算「套壳」，技术难度那 8 分才拿得到**

但必须现在就知道，别以为调个接口就有。

### 额度是有限的，别在开发循环里烧光

Creator 是入门档，**额度和并发都有上限**。两条纪律：

- 开发时**缓存 TTS 输出**，别每次改代码都重新生成同一句话
- 测试用短句
- 具体的额度数字和并发限制去 dashboard 看，或者到 `#hackathon-support` 问

### 额外好处：官方 showcase + 周边

填一份 20 秒的匿名反馈表 https://forms.gle/gHs8mGFGSPt6Hrco9
并把项目提交到 https://showcase.elevenlabs.io/
被选中可以拿限量周边。**跟比赛评分无关，但顺手。**

### ElevenLabs 自己偏爱什么项目

Hacker Guide 里列了 2025 年最佳项目。看这个列表比看文档更能判断他们的口味：

| 项目 | 是什么 |
| --- | --- |
| Reconnect Generations | 用 AI 引导访谈，保存家人的声音和故事 |
| Aphasio | 失语症患者的言语练习 |
| Kisan | 面向印度小农户的语音优先多语种助手 |
| **Orva** | **牙科诊所的语音牙周图表记录 agent** |
| **AI Tutoring Whiteboard** | **AI 语音辅导做数学作业** |
| **Pronunciation Coach** | **练口语，即时 AI 反馈** |
| Leetcourt | 交互式法庭模拟，用于法律训练 |

**规律很清楚：他们偏爱「手或眼被占用、或者文字是障碍」的场景下，把语音当成界面。**
不是「给聊天机器人加个声音」。

无障碍、多语种触达、教育与练习、特定行业的语音工作流——这四类占了绝大多数。
**11 个里有 3 个是教育/练习类。**

---

## 主办方给什么

| 资源 | 详情 |
| --- | --- |
| **导师** | 全程有经验丰富的 mentor。周日上午去找一个聊——他们知道评委吃什么 |
| **场地** | The Spot **3 楼**，周六周日都有联合办公空间，主办方在现场 |
| **Discord** | https://discord.gg/KBq3tdZaF —— 官方通知和答疑渠道 |
| **工具限制** | **没有任何限制。** 原文：*"No, any technology can be used."* |
| **数据** | 主办方**不提供**数据集。要用什么数据自己想办法 |

---

## 我们还缺什么（自己解决）

- **情绪/韵律识别**：ElevenLabs 不给，自己搭
- **测试数据**：主办方不给，只能公开数据集 / 合成 / 自己手上的
- **电话线路**：没有人给 PSTN 号码。用浏览器麦克风或上传音频，
  并在视频里**明说**我们没有接真实电话网络
