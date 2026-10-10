# 方案详解

这份文档解释小小东 VPS 方案里每个部分是什么、为什么这样做。部署本身由 `scripts/` 完成，这里写的是背后的理由，改动方案前先读一遍。

## 整体结构

```
你的电脑 / 手机 / 路由器
  ├─ Clash 订阅 ─────────── HTTPS 2096 ─ Nginx ─ 订阅中间层(2097) ─ 3x-ui 订阅(2095)
  ├─ Shadowrocket 订阅 ──── HTTPS 2096 ─ 同上
  ├─ 规则文件 ───────────── HTTPS 2096 /rules/ ─ Nginx 直接读本机规则镜像
  ├─ 主力节点 Reality ────── TCP 443  ─ Xray（认证失败的连接回落到 127.0.0.1:8443）
  └─ 备用节点 TLS ───────── TCP 2443 ─ Xray

管理
  ├─ ssh 名称 ───────────── TCP 22（只允许密钥）
  ├─ 3x-ui 面板 ─────────── HTTPS 53998 + 随机路径
  └─ CLIProxyAPI ────────── HTTPS 8318 ─ Nginx ─ 127.0.0.1:8317（管理中心 + /v1 接口）
```

只有 Nginx、Xray、3x-ui 面板直接对公网监听；CLIProxyAPI、订阅服务、Reality 回落站点都只听 `127.0.0.1`。

| 端口 | 用途 |
| ---: | --- |
| 22 | SSH（以服务商给的端口为准） |
| 80 | 只用于 Let's Encrypt 证书校验，其他路径一律 404 |
| 443 | Reality 主力节点 |
| 2443 | VLESS + TLS 备用节点 |
| 2096 | 订阅地址和规则文件 |
| 8318 | CLIProxyAPI 管理中心和 API |
| 53998 | 3x-ui 面板 |

## SSH：用名称登录，只认密钥

- 每台服务器一把独立密钥，放在 `~/.ssh/xxd-vps/名称/`。服务商给的是密码时，本机新生成 ED25519 密钥，用密码登录一次把公钥写进去。
- `~/.ssh/config` 写入 `Host 名称`，并且**放在文件最前面**：ssh 对每个参数取第一次出现的值，放在后面会被已有的 `Host *` 覆盖。带 `IdentitiesOnly yes`，避免 ssh 把电脑上所有密钥都试一遍触发服务器的失败次数限制。
- 确认密钥能登录之后才关闭密码登录，否则会把自己锁在外面。脚本在关闭前会检查 `authorized_keys` 不为空。
- 关闭密码登录的配置写在 `/etc/ssh/sshd_config.d/01-xxd-vps.conf`。**文件名以 01 开头是关键**：sshd 同样只认第一次出现的值，云镜像自带的 `50-cloud-init.conf` 常写着 `PasswordAuthentication yes`，排在它后面就不会生效。改完用 `sshd -T` 核对真正生效的值。
- `UseDNS no`：不对来访 IP 做反向解析，网络差时登录不会卡 5–30 秒，对安全没有影响。

## 证书：Let's Encrypt IP 证书，6 小时检查续期

订阅、面板、CLIProxyAPI、TLS 节点、Reality 回落站点共用同一张**签给服务器 IP 的** Let's Encrypt 证书，不需要域名，浏览器和客户端都信任，不会出现"您的连接不是私密连接"。

- Let's Encrypt 的 IP 证书只能用 `shortlived` 配置申请，有效期只有约 6 天，所以续期定时器每 6 小时检查一次。
- 系统软件源里的 Certbot 版本太旧，不支持 IP 证书，所以装在独立虚拟环境 `/opt/xxd-vps/certbot`（Certbot 5.x，需要 Python 3.10+）。
- 用 webroot 方式校验，80 端口只开放 `/.well-known/acme-challenge/`。服务商有安全组时，必须在后台也放行 TCP 80。
- 续期成功后的 deploy hook 依次执行 `nginx -t`、重载 Nginx、重启 3x-ui，让所有入口换上新证书。
- 申请失败就停止部署，**不使用自签名证书凑合**：自签名会让客户端报证书错误，用户就会被引导去关证书校验，安全性全没了。

## 3x-ui 与节点

### 固定版本

- 3x-ui 固定 **v3.8.5**，Xray 内核固定 **v26.7.28**，都用 SHA-256 校验安装包。
- 3x-ui 自带的新版 Xray（26.9.x 起）会拒绝不带 ML-KEM 的 TLS ClientHello，**Shadowrocket 因此连不上**。26.7.28 已在生产环境同时验证过 Shadowrocket 和 Mihomo。
- 3x-ui 和 Xray 都不自动升级。要升级，先在一台测试机上用真实的 Shadowrocket、Clash Verge Rev 实测，再改脚本里的版本号和校验值。

### 两个入口

1. **Reality 主力节点（TCP 443）**
   - 回落目标是本机 `127.0.0.1:8443` 上的 Nginx，它挂着这台服务器自己的 IP 证书。别人探测 443 时看到的是一个证书完全正常的 HTTPS 站点，而不是去冒用某个大网站的域名（"偷自己"）。
   - `serverNames` 同时写服务器 IP 和**空字符串**：客户端按 TLS 规范不会把 IP 地址当作 SNI 发送，服务器收到的 SNI 是空的，不写空字符串 Reality 认证必然失败。
   - `minClientVer: 1.0.0`：Xray 26.x 默认拒绝版本低于 v26.3.27 的客户端，Mihomo 和 Shadowrocket 都会被挡住。
   - 每台服务器独立生成 Reality 密钥对和 short ID。
2. **VLESS + TLS 备用节点（TCP 2443）**：用同一张 IP 证书。Reality 在某些网络下被干扰时可以切过去。

### 两套订阅身份

| 身份 | 用在 | 443 Reality | 2443 TLS |
| --- | --- | --- | --- |
| `名称-openclash` | Clash Verge Rev、OpenClash、Mihomo | `xtls-rprx-vision` | 不带 flow |
| `名称-shadowrocket` | Shadowrocket | 不带 flow | 不带 flow |

分开的原因：桌面端和路由器用 vision 流控；Shadowrocket 在生产环境里一直用不带 flow 的身份，单独一套最省心。两套身份有各自的 UUID 和订阅 ID，任何一个泄露都可以单独停掉，不影响另一个。

### IPv4 出站

Xray 出站用 `ForceIPv4` 并拦截 `::/0`：代理流量只从服务器的 IPv4 出去，避免网站看到 IPv6 出口、和 IPv4 出口对不上。服务器系统本身的 IPv6 不关闭。订阅里也设置了 `ipv6: false`。

## 订阅与 AI 分流规则

### 订阅地址

- 3x-ui 自带订阅服务，只监听 `127.0.0.1:2095`；对外由 Nginx 在 2096 提供 HTTPS。订阅路径、订阅 ID 都是随机生成的。
- 中间加了一层很小的订阅服务（`/opt/xxd-vps/sub-proxy`，127.0.0.1:2097）：
  - 只放行已知的订阅路径，其他请求一律 404；
  - 不记录请求地址，日志里不会出现订阅链接；
  - 按网卡实际流量在客户端显示"已用 / 总量"，可选每月重置日。
- 订阅地址直接用服务器 IP，不需要域名。国内能不能连上取决于这个 IP 的线路，换域名并不能解决线路问题。

### 规则

Clash 订阅自带完整规则（模板在 `scripts/server/files/clash-template.yaml`），客户端导入后选"规则"模式即可，不用自己写规则。顺序是：

1. 服务器自己的 IP、局域网地址直连；
2. **Gemini / Google AI 相关域名**（含登录、静态资源）→ `AI-人工智能`；
3. OpenAI、Claude、Gemini 规则集，以及 ChatGPT、Claude、Grok / xAI、Perplexity、Copilot、Cursor、Midjourney、Hugging Face、Muse 等域名 → `AI-人工智能`；
4. MetaCubeX 的 `category-ai-!cn` 兜底其他海外 AI 服务；
5. 国内域名和国内 IP 直连；YouTube、Netflix、Telegram、Apple、Microsoft、Google 各自分组；
6. 最后 `MATCH` 走代理。

AI 规则必须排在通用规则前面，否则 Gemini 的登录、静态资源域名可能被分到 Google 或直连组，出口不一致，容易出现"页面打得开但用不了"。

**规则文件放在你自己的服务器上**：服务器每天从 ACL4SSR、MetaCubeX、Loyalsoldier 的公开地址下载一次（`rule-sources.json`），保存到 `/var/lib/xxd-vps/rules/`，客户端只从 `https://你的IP:2096/rules/` 下载。好处是路由器在国内也不用直连 GitHub；某个上游下载失败时保留上一份，不会出现空规则。部署和验收时还会检查每个规则集声明的格式和文件实际内容一致（上游改过格式时会被发现）。

DNS 使用 fake-ip，国内域名走阿里 / 腾讯 DoH。AI 域名不在本地解析，直接按域名交给代理，由服务器解析。

## CLIProxyAPI

- 独立系统用户 `cliproxy` 运行，程序 `/opt/cli-proxy-api/`，配置 `/etc/cliproxyapi/config.yaml`（600），数据 `/var/lib/cliproxyapi/`。systemd 开启 `NoNewPrivileges`、`ProtectSystem=strict`、`ProtectHome` 等限制，只允许写自己的目录。
- 服务只听 `127.0.0.1:8317`，Nginx 在 8318 提供 HTTPS，关闭缓冲、超时 1 小时，流式输出和 WebSocket 都正常。
- 管理中心登录 Key 和 API Key 每台服务器独立随机生成；新部署的实例没有任何上游账号。
- **不设置内存上限**（不写 `MemoryMax`）。并发大时人为的上限只会让进程被 OOM 杀掉。1 GB 内存的机器余量小，建议 2 GB。

### 30 分钟自动更新

`cliproxy-auto-update.timer` 每 30 分钟（加最多 2 分钟随机延迟）运行 `/usr/local/sbin/cliproxy-auto-update`：

1. 从 GitHub 查询 CLIProxyAPI 最新稳定版（API 不可用时改用官方 releases 跳转）；
2. 下载对应架构的安装包，核对发布页公布的 SHA-256；
3. 备份当前程序和配置；
4. 原子替换程序文件，重启服务；
5. 带 API Key 检查本地 `/v1/models`，再检查公网 HTTPS；
6. 任何一步失败：自动换回旧程序和旧配置、重启并确认恢复，这个版本 24 小时内不再尝试；
7. 同时校验并更新 Management Center 页面（`management.html`）；
8. 文件锁保证不会两个更新同时运行；日志不包含任何 Key。

所以"秒速更新"的含义是：新版发布后通常半小时内自动装上，而且坏版本会自己回滚。

## 系统与维护

- 防火墙 UFW 默认拒绝入站，只开放上表端口；服务商有安全组的，后台也要放行同样端口。
- 网络调优：BBR + fq、MTU 探测、关闭空闲后慢启动、加大 socket 缓冲。
- 时区按机房所在地设置（`timedatectl`），并开启 NTP。时区只影响日志和本地时间，不影响出口 IP 和风控。
- 每天备份一次配置（3x-ui 数据库、证书、Nginx、CLIProxyAPI 配置与授权文件、systemd 单元等）到 `/var/backups/xxd-vps/`，目录 700、文件 600，保留 7 份。备份里含密钥，只留在服务器本机。
- 规则每天刷新一次；证书每 6 小时检查一次；CLIProxyAPI 每 30 分钟检查一次。

## 不包含的内容

- CLIProxyAPI 的上游账号、OAuth 文件、供应商 API Key：需要用户自己在管理中心添加。
- Hysteria2 等 UDP 协议、域名、CDN。
- 3x-ui / Xray 的自动升级。
