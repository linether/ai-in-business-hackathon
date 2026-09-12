# Who owns what

Filled in at the **Sat 21:00 AEST** decision point, once the idea is locked. Until then it's empty on
purpose — you can't split work that hasn't been defined.

## Ownership

自己在 `BOARD.md` 上 `CLAIM` 认领，认领后我把它记到这里。

### 已认领

| 领域 | 负责人 | 认领时间 |
| --- | --- | --- |
| **主链路 + 抽取层**（③④⑤） | **@Genicayyy** | 09-12 21:18 AEST |
| **前端 + 证据面板**（⑨） | **@Ranchelwood** | 09-12 20:54 AEST |
| 规则 / 评分 / 阻断点（⑥⑦⑧） | @linether | 代码已在仓库里 |
| 部署与线上 URL | @linether | 服务器访问权限在他手上 |

### 全队共同承担（不设单一负责人）

经讨论决定这三块**大家一起做**，不指派给某一个人：

| 领域 | 分值 | 怎么一起做 |
| --- | --- | --- |
| **场景脚本 + 音频生成 + 标注** | 评测和 demo 的共同地基 | 每人认领几个场景来写。写脚本时就写好标准答案 = ground truth |
| **评测 notebook** | 数据与模型 **6 分** | 脚本齐了之后，谁先有空谁起头，其他人补指标 |
| **Demo 视频 + Pitch + 价值数字** | **初赛 80 分全部由视频评定** + 商业价值 25 分 | 脚本全队一起对，录制集中在一个时段完成 |

⚠️ **共同承担的风险是最后没人动手。** 所以每一块都要有人在 `BOARD.md` 上起个头
（"我先写 5 个场景" / "我起个 notebook 框架"），别默认别人会开始。

## Principles for splitting

- **Two people never own the same file at the same time.** Claim on `BOARD.md` before you start.
- The demo path is owned by one person end-to-end. Everything else supports it.
- Non-code work is real work. The video, the numbers and the README are worth more rubric points than
  most features.
- If you're blocked for more than 20 minutes, post `BLOCKED` on the board rather than grinding.

## Checkpoints

| When (AEST) | What |
| --- | --- |
| Sat 21:00 | Idea locked, roles assigned, hello-world deployed |
| Sat 22:00 | Stop for the night. Tired judgement on Sunday costs more than the hours gained |
| Sun 12:00 | **Feature freeze target.** Not started by now = doesn't ship |
| Sun 18:00 | Demo path frozen. Video recording starts |
| Sun 22:00 | Full submission dry run: repo public, README, live URL, video, Devpost draft |
| Mon 10:00 | **Submit.** The buffer is the point |
| Mon 12:00 | Deadline. Late is not considered |
