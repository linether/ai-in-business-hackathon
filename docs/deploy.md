# 部署：阿里云 ECS + DuckDNS + Caddy

**决定**：用自己的阿里云服务器（马来西亚），**不买域名**，用 DuckDNS 免费子域名 + Caddy 自动 HTTPS。

最终 URL 长这样：`https://complaintguard.duckdns.org`

---

## 为什么是 DuckDNS 而不是 nip.io

免费方案里只有 DuckDNS 可靠，原因很具体：

```
✅ duckdns.org   在公共后缀列表（PSL）里 → 每个子域名有独立的 Let's Encrypt 配额
❌ nip.io        不在 PSL → 全球用户共用一个配额
❌ sslip.io      不在 PSL → 配额已被耗尽，大量用户签不出证书
```

验证方式：`curl -s https://publicsuffix.org/list/public_suffix_list.dat | grep -x duckdns.org`

不在 PSL 意味着所有人的证书申请算在同一个域名头上，配额一被用完就集体失败——
**sslip.io 现在就是这个状态**（[issue #108](https://github.com/cunnie/sslip.io/issues/108)）。
在 PSL 里则每个子域名独立计算，我们不受别人影响。

其他免费方案的问题：

- **Let's Encrypt IP 证书**：2026-01 已 GA，但 Caddy 支持不完整
  （[issue #7399](https://github.com/caddyserver/caddy/issues/7399)），要走得换 Certbot + nginx，且证书只有 6 天
- **Cloudflare Tunnel**：命名隧道需要自有域名；快速隧道的 URL 是随机且临时的，不能用于提交
- **Freenom 免费域名（.tk/.ml）**：已停止新注册，不可靠

---

## 服务器现状（2026-09-12 21:30 实测，只读侦察）

| 项 | 结果 |
| --- | --- |
| 系统 | Ubuntu 22.04.5 LTS · x86_64（IP 见本地 `~/.ssh/config` 的 `aliyun`，不写进仓库） |
| **出站连通性** | ✅ **通过** —— Anthropic 401（连上了，未带 key）、ElevenLabs 404、pypi/github 200 |
| 80 / 443 / 8000 / 8080 | ✅ 全部空闲，无冲突 |
| Docker | ✅ 已安装且运行中 |
| 本机防火墙 | ufw 未启用 → **阿里云安全组是唯一一层** |
| 磁盘 | 40G / 剩 22G |
| **内存** | ⚠️ **1.6 GiB 总，1.1 GiB 可用** |

### ⚠️ 内存 1.6 GB 是硬约束，会影响技术选型

**不能在这台机器上跑任何本地模型** —— 本地 Whisper、本地 embedding、本地 LLM 全部装不下。

我们当前的架构本来就不需要（转录走 ElevenLabs Scribe API，判断走 LLM API），
FastAPI + Python 约占 150–300 MB，够用。**但这条应该作为架构评审的输入之一**：
任何"在服务器上跑个小模型"的方案在这台机器上不成立。

另外两点：

- 音频处理必须**流式 / 分块**，不能把整个文件读进内存
- 机器上跑着 **VS Code Server**（Remote 开发用），会占 300–500 MB。
  **周一评审前建议关掉**，把内存留给应用

### 还没做的一步

**阿里云安全组放行 80 / 443** —— 需要在阿里云控制台操作。ufw 未启用，所以安全组是唯一一层。

---

## 步骤

### 1. DuckDNS 注册子域名（3 分钟）

1. 打开 https://www.duckdns.org/ ，用 GitHub 或 Google 登录
2. 在 `domains` 框里输入一个名字，例如 `complaintguard` → 拿到 `complaintguard.duckdns.org`
   - ⚠️ 名字是全球先到先得，想好 2–3 个备选
   - 这是评委看到的 URL，取一个跟项目同名的
3. 把 `current ip` 填成 ECS 的**公网 IP**，点 update

ECS 是固定公网 IP，所以**设一次就够，不需要装定时更新脚本**。

验证：`dig +short complaintguard.duckdns.org` 应该返回你的 IP。

### 2. 阿里云安全组（5 分钟）

放行入方向 **80/TCP** 和 **443/TCP**。默认全封，这是最常见的卡点。

**80 端口不能省** —— Let's Encrypt 的 HTTP-01 验证要走它。

### 3. ⚠️ 先验证出站连通性（2 分钟，最先做）

在 ECS 上确认能访问我们要用的外部 API：

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://api.elevenlabs.io/v1/models
curl -sS -o /dev/null -w '%{http_code}\n' https://api.anthropic.com/v1/models
```

马来西亚区域（国际站）通常没问题，但**必须先验证，不要假设**。
**这一步不通，整个自建方案要重新考虑**，越早知道越好。

### 4. 装 Caddy

Caddy 自动申请和续期证书，不需要手动跑 certbot。

Caddyfile 的全部内容就这三行：

```
complaintguard.duckdns.org {
    reverse_proxy localhost:8000
}
```

首次启动时 Caddy 会自动通过 HTTP-01 拿到证书。

### 5. 先部署一个 hello-world

**在应用写好之前就做。** 目的不是上线应用，是打通链路、拿到 URL、把流程跑一遍。

**部署永远不能是周一早上的任务。**

### 6. 配自动部署（可选，但很值）

GitHub Action 在 push 到 `main` 时 ssh 进服务器 `git pull` + 重启。
SSH 私钥放 GitHub Secrets，不要进仓库。

---

## 验收标准

- 队里任何人**用手机流量**（不是队里 wifi）打开 URL，能看到页面，地址栏是 `https://` 带锁
- 往 `main` 推一个小改动，几分钟后 URL 上能看到变化
- `/health` 返回 200
- `git grep` 搜不到任何 API key

---

## 不管怎样都要做的

1. 密钥只放服务器环境变量 / GitHub Secrets，仓库里只留 `.env.example`
2. **加一个「试试预置场景」按钮** —— 评委一键看到完整流程，不必自己准备音频。
   这是降低演示失败率最有效的一招
3. 给 LLM 调用加上限或限流 —— 公开 URL 背后接 LLM API，被刷会烧光额度
4. 加 `/health` 端点
5. **周一上午预热一次并验证**

## 两条风险提醒

**优先级**：初赛 80 分**全部来自 3–5 分钟视频**，线上 URL 是加分项不是及格线
（FAQ 原文：live app 不强制，但没有会扣分）。**周日晚若必须二选一，先录视频。**

**单点**：周一早上若服务器出问题，只有 @linether 能修，没有平台状态页和自动重启。
缓解就是上面那条——视频录好了，服务器挂了也不致命。
