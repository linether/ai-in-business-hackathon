# 队友加入仓库：发给 AI 的提示词

把下面这两步转发给还没进仓库的队友。

---

## 第一步：接受邀请（10 秒，必须先做）

打开这个链接，登录 GitHub 后点 **Accept invitation**：

https://github.com/linether/ai-in-business-hackathon/invitations

没有 GitHub 账号的先注册：https://github.com/signup

---

## 第二步：把下面整段发给 AI（Claude / ChatGPT 都行）

```
我要参加一个 48 小时黑客松，需要把队伍的 GitHub 仓库配置到我的电脑上，
请一步一步带我做完，每一步等我回复结果再继续下一步。

【背景】
- 仓库：https://github.com/linether/ai-in-business-hackathon （private）
- 我已经接受了协作者邀请（如果还没有，先提醒我去接受）
- 这是 4 人团队，比赛周一中午 12 点截止，时间很紧

【最重要的一条约束】
主办方会审查 Git 提交历史来判断是不是一个人做的、有没有提前写代码。
所以我的每一个 commit 都必须正确归属到我自己的 GitHub 账号上。
请特别帮我确认：本地 git 配置的 user.email 必须是我 GitHub 账号上
绑定的邮箱（或 GitHub 提供的 noreply 邮箱），否则 commit 不会算在我头上，
GitHub 上会显示成一个没有头像的陌生名字。

【请依次帮我完成】
1. 先问我用的是 Windows 还是 Mac，以及我平时用不用命令行，
   然后按我的情况给命令，不要一次性甩一大堆。
2. 检查我有没有装 git，没有就带我装。
3. 配置 git 的 user.name 和 user.email，并解释为什么 email 必须匹配。
4. 配置 GitHub 身份认证（推荐用 GitHub CLI `gh auth login`，
   或者 SSH key，别让我把密码写进命令里）。
5. 把仓库 clone 到我电脑上一个合理的位置。
6. 做一次验证性提交，确认我真的有写权限：
   - 新建分支，分支名格式是 我的名字/做的事，例如 `yanyi/setup`
   - 在仓库根目录的 README.md 里，找到 Team 那个表格，
     把我那一行的 GitHub 用户名填上（我会告诉你我的用户名）
   - commit 并 push 这个分支
   - 然后开一个 Pull Request 合并到 main
7. 最后带我去 GitHub 网页上确认：我的 commit 旁边显示的是我的头像和用户名，
   不是一个灰色的陌生账号。如果不对，帮我改掉重来。

【团队约定，请在配置时一并告诉我】
- main 分支要始终能跑 demo，不要直接往 main 推代码，走分支 + PR
- 分支命名：我的名字/做的事
- 密钥写在 .env 里，.env 已经被 gitignore 了，绝对不要提交任何 API key
- 仓库里的 docs/ 目录有赛题、评分细则和作战计划，clone 完先读一遍

【还有一件事】
比赛规定周六中午 12 点之前不准写任何应用代码。
仓库里周六之前的提交只有规划文档，这是允许的。
请不要帮我做任何会改写或伪造提交时间、提交历史的操作。
```

---

## 常见卡点

- **点了链接说 404** —— 没登录，或者登录的是另一个 GitHub 账号。先退出重登。
- **push 时报 403 / permission denied** —— 邀请还没接受，或者本地存的是别人的 GitHub 凭据。
- **commit 在网页上显示成灰色陌生人** —— `git config user.email` 和 GitHub 账号邮箱不一致，
  改完之后重新 commit 一次即可。
