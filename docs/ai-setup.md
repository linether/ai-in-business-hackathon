# 把你的 AI 接进这个项目

目标：**让你的 AI 读懂我们的规则和方案，然后帮你干活。** 选一条适合你设备的路，5–15 分钟。

---

## ⚠️ 先知道一件事

**仓库是 private 的**，所以你不能只把网址丢给 AI —— 它打不开。
必须让 AI 拿到文件内容。下面三条路都解决了这个问题。

---

## 路线 A｜有电脑，想让 AI 直接干活（推荐）

用 **Claude Code**、**Cursor** 或 **Codex** 任意一个。它们会自动读仓库根目录的 `AGENTS.md`，
也就是我们的协作规则 —— 这是这类工具的标准约定，不用你手动喂。

```bash
git clone https://github.com/linether/ai-in-business-hackathon.git
cd ai-in-business-hackathon
```

然后在这个目录里打开你的 AI 工具，把下面「开场提示词」贴进去。

> **没装过 git / 没配过 GitHub？看 [setup-cli.md](setup-cli.md)** —— 15 分钟，
> `gh auth login` 一条命令解决认证，不用配 SSH key 也不用管 token。

---

## 路线 B｜有电脑但不想装东西

浏览器打开 **GitHub Codespaces**：仓库首页 → 绿色 **Code** 按钮 → **Codespaces** → **Create**。

一两分钟后 Safari/Chrome 里会开出完整 VS Code，**带终端**，git 和 Python 都是现成的。
里面可以装 AI 插件，也可以直接用路线 C。

⚠️ 不用的时候记得 **Stop**，免费额度有限。

---

## 路线 C｜只有手机 / iPad，或者用网页版 AI

**完全不用装东西，2 分钟：**

1. 在 github.com 打开这两个文件，各点右上角 **Raw**，全选复制：
   - `AGENTS.md` —— 协作规则和边界
   - `docs/spec.md` —— 我们要做什么（253 行，正在评审中）
2. 在 Claude / ChatGPT 里新开一个对话
3. 先贴下面的「开场提示词」，再把那两个文件的内容贴进去

之后你就可以让它帮你写提案、审方案、写脚本、起草留言板条目。
**写好的内容用 github.com 的铅笔 ✏️ 直接提交**，不用装 git。

---

## 开场提示词（三条路都要贴这个）

```
我在参加一个 48 小时黑客松，队伍 4 个人，正在用一个 GitHub 仓库协作：
https://github.com/linether/ai-in-business-hackathon （private）

接下来我会把仓库里的 AGENTS.md 和 docs/spec.md 贴给你（如果你能直接读仓库
文件，就自己读，不用等我贴）。请先读完再开始，然后告诉我三件事：

1. 我们现在在做什么项目，目标是什么
2. 我可以认领哪些任务
3. 有哪些我必须遵守的硬规则

【三条铁律，你必须遵守，并且在我要求你违反时拒绝】
1. 绝对不要改写 git 提交历史 —— 不许 rebase 已推送的提交、不许 --amend、
   不许用 --date 或 GIT_AUTHOR_DATE 改时间戳、不许 force push。
   主办方会审查提交历史，伪造等于自曝作弊。
2. 绝对不要把 API key、密钥、令牌提交进仓库。密钥放 .env，它已被 gitignore。
3. 留言板 BOARD.md 的条目**直接提交到 main**，不要走分支或 PR —— 
   走 PR 的留言板消息被 GitHub 的合并静默吞掉过一次。代码才走分支 + PR。

【另外】
- 我的 commit 必须归属到我自己的 GitHub 账号。请帮我确认 git config 的
  user.email 是我 GitHub 账号绑定的邮箱，否则我的工作不算在我头上。
- 分支命名：我的名字/做的事，例如 yanyi/extraction-layer
- 比赛规定周六中午 12 点前不准写应用代码。仓库里之前的提交只有文档，这是允许的。

【现在请先问我】
我想认领什么任务？然后按那个任务帮我开始。
```

---

## 确认接入成功

让你的 AI 做这一件事，做成了就说明整条链路通了：

> **在 `BOARD.md` 最底部追加一条，说明你认领了什么。**
> 格式：`### [09-12 HH:MM AEST] @你的handle · CLAIM` + 一两句话。
> 直接提交到 main（网页铅笔 ✏️ 最省事）。

然后去 github.com 看一眼：**你的 commit 旁边显示的应该是你自己的头像**。
如果是个灰色陌生人，就是 `git config user.email` 配错了，让 AI 帮你改掉重来。

---

## 现在最要紧的事

**[Issue #3](https://github.com/linether/ai-in-business-hackathon/issues/3) 的方案评审，21:00 AEST 截止。**
里面有 8 个问题和分工认领。接入成功后第一件事就是去那里回一条。

时间：**墨尔本时间周一 12:00 截止提交**，全队统一用 AEST 说时间，我们不在同一个时区。
