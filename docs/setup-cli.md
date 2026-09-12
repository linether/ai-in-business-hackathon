# 本地开发环境配置（15 分钟）

四步：装工具 → 登录 → clone → 配身份。**不需要 SSH key，不需要管 token。**

---

## 1. 装 git 和 GitHub CLI

**macOS**（没有 brew 就先去 https://brew.sh 装）

```bash
brew install git gh
```

**Windows**（PowerShell）

```powershell
winget install --id Git.Git -e ; winget install --id GitHub.cli -e
```

装完**关掉终端重开**，否则找不到命令。

---

## 2. 登录 GitHub

```bash
gh auth login
```

依次选：

| 问题 | 选 |
| --- | --- |
| What account do you want to log into? | **GitHub.com** |
| What is your preferred protocol? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** ← 别选错，这步顺便配好 git 的认证 |
| How would you like to authenticate? | **Login with a web browser** |

然后终端会显示一个 **8 位一次性验证码**，复制它，回车会自动打开浏览器，粘贴进去确认即可。

验证：

```bash
gh auth status
```

看到 `✓ Logged in to github.com account 你的用户名` 就成了。

---

## 3. Clone 仓库

```bash
gh repo clone linether/ai-in-business-hackathon
```

仓库是 private 的，但上一步已经认证过，所以能直接拉下来。

---

## 4. 配好提交身份 ⚠️ 最容易出错的一步

**主办方会审查 git 提交历史。** 如果 `user.email` 和你的 GitHub 账号对不上，
你的 commit 在网页上会显示成一个灰色陌生人 —— **等于你的工作不算在你头上**，
四个人的队看起来像一个人做的。

先用这条命令生成**你自己的** GitHub noreply 邮箱（不会暴露你的真实邮箱）：

```bash
gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"'
```

把输出的那一串填进下面（把 `你的名字` 和 `上一步的输出` 换掉）：

```bash
git config --global user.name "你的名字" && git config --global user.email "上一步的输出"
```

---

## 5. 验证整条链路

在仓库目录里：

```bash
cd ai-in-business-hackathon && git config user.email && gh auth status
```

然后做一次真实提交测试 —— 在 `BOARD.md` 最底部加一条：

```
### [09-12 HH:MM AEST] @你的handle · CLAIM
我认领 xxx。本地环境已配好。
```

提交并推送：

```bash
git add BOARD.md && git commit -m "Claim role" && git push origin main
```

> 留言板条目**直接推 main**，不要走分支 —— 走 PR 的留言板消息被合并吞掉过一次。
> **代码才走分支 + PR。**

最后去 https://github.com/linether/ai-in-business-hackathon/commits/main
看一眼：**你的 commit 旁边应该是你自己的头像**。是灰色陌生人就回第 4 步重配。

---

## 6. 装 AI 编码工具

任选其一，都会自动读仓库根目录的 `AGENTS.md`（我们的协作规则），不用手动喂：

**Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

装好后在仓库目录里运行 `claude`。

**Cursor** —— https://cursor.com 下载，用 "Open Folder" 打开仓库目录。

进去之后把 `docs/ai-setup.md` 里的开场提示词贴给它。

---

## 日常流程

```bash
git pull origin main
```

写代码前先开分支：

```bash
git checkout -b 你的名字/你在做的事
```

写完推上去并开 PR：

```bash
git push -u origin HEAD && gh pr create --fill
```

---

## 卡住了

| 现象 | 原因 |
| --- | --- |
| `gh: command not found` | 终端没重开 |
| clone 报 404 / 权限错误 | 没接受仓库邀请，或 `gh auth status` 登的是另一个账号 |
| commit 显示灰色陌生人 | 第 4 步没做对 |
| push 被拒绝（rejected） | 先 `git pull origin main` 再推 |

还不行就在 [BOARD.md](../BOARD.md) 发一条 `BLOCKED`，写清楚卡在哪步、报错原文。
**别自己硬扛超过 20 分钟。**
