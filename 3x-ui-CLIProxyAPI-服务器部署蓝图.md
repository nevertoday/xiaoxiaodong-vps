# 3x-ui + CLIProxyAPI 多服务器部署蓝图

> 目的：把一台全新 VPS 配置成可用于代理节点、AI 分流、CLIProxyAPI 接口和持续维护的独立服务器。  
> 本文是通用方案，不包含任何现有服务器的私钥、面板密码、订阅密钥、Reality 私钥、OAuth 文件或 CLIProxyAPI API Key。

相关入口：

- [项目 README](./README.md)：先了解方案、客户端和下载地址；
- [新服务器部署模板](./部署模板.md)：填写连接信息并复制可直接使用的代码块；
- [GitHub 项目 ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip)：保存整套文档。

## 阅读路径

1. 先填写“执行前必须收集的变量”；
2. 按“时区配置策略”“SSH 长期登录逻辑”“系统基础和安全加固”完成基础设置；
3. 再部署 3x-ui/Xray、订阅和 AI 分流；
4. 部署 CLIProxyAPI、自动升级和备份；
5. 最后按“交付验收清单”逐项留下结果。

使用部署工具时，建议同时提供本文件和[新服务器部署模板](./部署模板.md)，并要求先做只读预检，再按阶段执行。

## 结论：低配 AI 能不能照此部署

可以，但“拿到文档”本身不等于可以直接完成部署。执行 AI 还必须同时拥有：

- 服务器 IP、SSH 用户名、可用的 SSH 私钥或初始密码；
- 能执行远程命令的终端权限；
- 当前操作系统、CPU 架构和服务商网络信息；
- 允许安装软件、修改防火墙、写入 systemd 和 Nginx 的 root 权限；
- 可以访问 GitHub 或配置好的发行版镜像；
- 一套独立生成的凭据，而不是复制旧服务器的凭据。

低配 AI 可以按本文完成安装和验收，但必须逐项执行检查，不能只运行一个未经审计的一键脚本。每台服务器都应该生成自己的 UUID、Reality 密钥、订阅路径、面板密码、管理密钥和 API Key。

## 公网 HTTPS 证书策略

所有对外的 HTTPS 入口都必须使用受浏览器和客户端信任的 IP 证书。当前方案使用 Let's Encrypt 的 IP 证书，不把自签名证书作为正常交付结果。

证书实施要求：

- 使用 Python 3.10+ 和 Certbot 5.4+；当前验证版本为 5.8.0；
- 使用 `webroot` HTTP-01 校验，webroot 为 `/var/www/acme`，公网 TCP 80 必须可访问；
- 使用 Let's Encrypt `shortlived` profile 和 `--ip-address <SERVER_IP>` 申请 IP 证书；
- 证书统一放在 `/etc/letsencrypt/live/<SERVER_IP>/`，由 Nginx 和 Xray TLS 入口引用；
- 同一张证书用于订阅入口 2096、3x-ui 面板 53998、CLIProxyAPI 8318，以及 Xray TLS 2443；
- IP 证书有效期很短，必须设置每 6 小时检查一次的 systemd timer，并在 deploy hook 中执行 `nginx -t && systemctl reload nginx && systemctl try-restart x-ui.service`；
- 部署后必须用系统信任库验证签发者和 IP SAN，并执行 `certbot renew --dry-run --run-deploy-hooks`；
- 如果 IP 证书申请失败，部署应暂停并报告原因，不得悄悄改用自签名证书继续交付；
- 不能只检查端口能否握手，必须同时检查浏览器/`curl` 的证书信任、有效期和 `subjectAltName` 中的服务器 IP。

推荐申请形态如下，实际执行时将 IP 替换为本机值：

```bash
certbot certonly \
  --webroot -w /var/www/acme \
  --ip-address <SERVER_IP> \
  --preferred-profile shortlived \
  --key-type ecdsa \
  --preferred-challenges http
```

不要使用 `-k` 或 `--insecure` 来掩盖证书问题。节点配置中的 `skip-cert-verify` 只用于明确需要兼容自签名 TLS 节点的客户端，不能替代订阅、面板和 API 入口的正规证书。

## 总体架构

```
客户端
  ├─ OpenClash / Mihomo 订阅 ──> HTTPS 2096 ──> Nginx ──> 订阅生成器
  ├─ Shadowrocket 订阅 ───────> HTTPS 2096 ──> Nginx ──> 订阅生成器
  ├─ Reality 节点 ────────────> TCP 443 ──> Xray
  └─ TLS 备用节点 ────────────> TCP 2443 ─> Xray

管理员
  ├─ SSH 密钥登录 ────────────> TCP 22
  ├─ 3x-ui 面板 ──────────────> HTTPS 53998 ─> Nginx / 3x-ui
  └─ CLIProxyAPI 管理中心 ─────> HTTPS 8318 ─> CLIProxyAPI

CLIProxyAPI 客户端 ───────────> HTTPS 8318/v1 ─> CLIProxyAPI ─> 已配置的上游账号
```

所有服务器都要独立部署、独立生成凭据、独立备份，不能把旧服务器的数据库、OAuth、API Key 或用户订阅直接复制到新服务器。

## 执行前必须收集的变量

将下面的占位符替换成当前服务器信息。私钥正文不要放进聊天内容或 Markdown 文档。

```text
SERVER_IP=服务器公网 IPv4
SSH_USER=root
SSH_PORT=22
SSH_PASSWORD=初始密码（使用密钥时留空）
SSH_KEY_PATH=/本机/私钥路径（使用密码时留空）
SSH_ALIAS=自定义别名

SERVER_TIMEZONE=可选；不确定时由部署工具按服务商机房确认

PANEL_PORT=53998
SUBSCRIPTION_PORT=2096
CLIPROXY_PORT=8318
REALITY_PORT=443
TLS_PORT=2443
```

如果服务器只支持密码登录，应先使用初始密码登录、写入公钥并验证密钥登录，再关闭密码认证。不能在密钥登录验证前关闭密码认证。

## 时区配置策略

服务器时区必须作为部署变量明确指定，不要仅凭公网 IP 的地理库自动猜测。IP 归属、机房位置和实际出口线路可能不一致，最终应以服务商控制台标注的机房地区为准，并在部署前确认：

| 机房或使用地区 | 推荐时区变量 |
|---|---|
| 美国西部、洛杉矶 | `America/Los_Angeles` |
| 明确要求统一 UTC 的服务器 | `Etc/UTC` |
| 中国大陆本地管理环境 | `Asia/Shanghai` |

部署时执行：

```bash
timedatectl set-timezone "$SERVER_TIMEZONE"
timedatectl show --property=Timezone --value
timedatectl show --property=NTPSynchronized --property=LocalRTC
```

修改时区只改变服务器本地时间显示、日志时间和未明确指定时区的定时任务，不会改变公网 IP、代理出口、路由或 Claude 风控结果。自动升级定时器如果使用 `UTC` 日历表达式，修改服务器时区也不会改变它的实际 UTC 触发时间。

现有服务器如需调整，应通过 SSH 别名逐台执行并核对结果，不能把某一台服务器的时区设置复制成所有服务器的默认值。

## 一、SSH 长期登录逻辑

本机生成或保存一把只用于该服务器的 ED25519 私钥：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
chmod 600 ~/.ssh/<server-key>
```

在 `~/.ssh/config` 中建立别名：

```sshconfig
Host <SSH_ALIAS>
  HostName <SERVER_IP>
  User root
  Port 22
  IdentityFile ~/.ssh/<server-key>
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

验收：

```bash
ssh -o BatchMode=yes <SSH_ALIAS> 'hostname; id -u'
```

返回用户 ID 为 `0` 且不要求密码，才算密钥登录完成。记录公钥指纹和服务器主机指纹；不要记录私钥正文。

## 二、系统基础和安全加固

部署脚本应先确认系统版本、架构、磁盘、内存、时区和公网地址，再安装依赖。建议启用：

- UFW 或同等防火墙；
- SSH 密钥登录；
- systemd 服务自动重启；
- NTP 时间同步；
- 定期安全更新；
- 每日配置备份，保留至少 7 份；
- 日志轮换，避免 CLIProxyAPI 或 Nginx 日志填满磁盘。

典型开放端口：

| 端口 | 用途 |
|---:|---|
| 22/tcp | SSH |
| 80/tcp | 证书签发或 HTTP 跳转 |
| 443/tcp | Xray Reality 节点 |
| 2443/tcp | Xray TLS 备用节点 |
| 2096/tcp | OpenClash / Shadowrocket 订阅 |
| 8318/tcp | CLIProxyAPI 管理中心和 API |
| 53998/tcp | 3x-ui 面板 |

如果服务商支持安全组，云端安全组和 VPS 内部防火墙都要同时检查。面板和管理接口最好限制为管理员 IP；如果必须对公网开放，必须使用长随机路径、强密码和独立管理密钥。

3x-ui 和 CLIProxyAPI 的 systemd 服务可使用以下安全属性：

```ini
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
UMask=0077
LimitNOFILE=65536
```

## 三、3x-ui / Xray 节点方案

### 面板

- 3x-ui 使用独立的随机面板路径和随机管理员密码；
- 面板通过 HTTPS 访问；
- 面板密码不能与 SSH、CLIProxyAPI 或订阅密钥复用；
- 数据库使用新实例，不复制旧服务器用户表；
- 3x-ui 和 Xray 都设置为开机自动启动。

### 节点

每台服务器至少准备两种入口：

1. **Reality 主节点**
   - TCP 443；
   - Xray VLESS + Reality；
   - 每个用途使用独立 UUID；
   - 生成该服务器独有的 Reality 私钥、公钥和 short ID；
   - 使用可靠的 SNI、fingerprint 和 flow 参数；
   - 不复用其他服务器的 Reality 密钥。

2. **TLS 备用节点**
   - TCP 2443；
   - Xray VLESS + TLS；
   - 使用该服务器自己的 IP 证书或证书方案；
   - 作为 Reality 不可用时的备用入口。

建议至少分开生成：

- OpenClash / Mihomo 专用身份；
- Shadowrocket 专用身份；
- 管理员测试身份；
- 必要时再为不同用户生成独立 UUID。

这样可以单独撤销某个订阅或用户，不必影响整台服务器。

### IPv4 / IPv6

代理出站配置应明确：

```yaml
ipv6: false
```

并将出站优先固定到 IPv4。这里的含义是代理流量不使用 IPv6；不必为了这个需求粗暴关闭系统全部 IPv6，除非服务商线路或故障排查明确需要。

### 订阅

订阅服务通过 HTTPS 2096 提供：

- OpenClash / Mihomo YAML 订阅；
- Shadowrocket Base64 或通用订阅；
- 可选 JSON 订阅；
- 每个订阅使用独立的随机路径；
- 订阅响应不能暴露面板密码、CLIProxyAPI Key 或其他服务器的节点。

订阅 URL 使用纯 IP 也可以，不需要额外域名。中国网络访问是否成功，取决于 IP、端口、线路和运营商策略，域名本身不能替代线路质量。

## 四、代理规则和 AI 分流逻辑

规则应按域名和 IP 集合分层，至少包含：

- 中国大陆域名和 IP 直连；
- Gemini；
- Grok / xAI；
- OpenAI；
- Claude / Anthropic；
- Muse 及其相关接口；
- Google AI 相关域名；
- GitHub、模型下载和规则源；
- 广告、跟踪和恶意域名；
- 最终代理或直连兜底。

推荐策略组：

- AI 总组；
- Gemini；
- Grok；
- OpenAI；
- Claude；
- Muse；
- Google；
- 国际通用；
- 国内直连；
- 故障切换 / 自动选择。

规则顺序必须先处理特殊 AI 域名，再处理通用国际规则，最后才使用兜底规则。否则 Gemini、Grok 或 Muse 可能被错误地分到直连或普通代理组。

如果路由器位于中国网络，规则源不能只依赖启动时访问 GitHub。应在服务器上保存经过校验的本地规则镜像，并设置每日刷新；远程规则不可用时继续使用上一次成功版本。规则源更新失败不能让 OpenClash 整份配置失效。

### 客户端兼容性

现代 OpenClash / Mihomo 能使用完整的 Meta 配置。Clash for Windows 0.19.20 等旧客户端可能无法解析：

- `nameserver-policy` 的新字段结构；
- MRS / Meta 规则格式；
- Reality 节点；
- 新版代理组字段。

出现 `yaml: cannot unmarshal !!seq into string` 时，优先升级到支持 Mihomo 的客户端，或使用 Shadowrocket；不要把现代 Mihomo 配置直接当成旧版 CFW 配置。

### 桌面端建议：Clash Verge Rev

建议 Windows、macOS 和 Linux 用户使用 Clash Verge Rev。它适合直接加载本项目生成的 Mihomo YAML 订阅，规则和 AI 分流已经配置好，用户只需要选择运行方式。

官方入口：

- 项目主页：<https://github.com/clash-verge-rev/clash-verge-rev>
- 官方 Releases：<https://github.com/clash-verge-rev/clash-verge-rev/releases>

推荐设置：

1. 在 Profiles / 配置中添加 OpenClash / Mihomo YAML 订阅；
2. 选中刚更新的配置；
3. 运行模式选择 **Rule / 规则**；
4. 打开 **System Proxy / 系统代理**；
5. 先不要打开 Global / 全局、Direct / 直连或 TUN，除非具体应用不遵守系统代理。

因为规则已经包含 Gemini、Grok、Muse、OpenAI、Claude 等 AI 分流，客户端不需要再手工添加规则。若某个应用不走系统代理，再单独评估 TUN / 服务模式、DNS 和权限设置。

## 五、客户端环境和使用行为建议

节点配置完成后，建议用户保持设备环境稳定：

- 按隐私需要关闭不必要的系统定位权限；这不会改变代理出口 IP，也不是规避服务风控的手段；
- 如果长期固定使用某个 VPS 出口，可以将电脑时区设为 VPS 所在地区，并避免频繁来回切换；
- 时区、语言和浏览器设置应与真实的长期使用环境保持一致，不要把它们当成伪造地理位置的工具；
- 避免短时间内在多个国家、多个节点和多个账号之间频繁切换。

用户应遵守所在地法律、服务商条款和 AI 服务政策，不要提交违法、暴力伤害、恶意入侵、窃取隐私或其他违背人类基本安全与尊严的问题。不要把个人账号当作公共 API，也不要进行批量并发提问、自动化刷请求、批量导出、模型蒸馏或绕过速率限制等行为。确有批量处理需求时，应使用官方允许的 API、合理限速并确认授权范围。

## 六、CLIProxyAPI 部署逻辑

建议使用独立系统用户运行：

```text
用户：cliproxy
程序：/opt/cli-proxy-api/cli-proxy-api
配置：/etc/cliproxyapi/config.yaml
数据：/var/lib/cliproxyapi
API：8318
```

需要部署：

- CLIProxyAPI 主程序；
- CLIProxyAPI Management Center 静态文件；
- Nginx HTTPS 反代；
- Let's Encrypt IP 证书、短周期自动续期和 deploy hook；
- 独立管理密钥；
- 独立 API Key；
- `/v1/models` 健康检查；
- systemd 自动重启；
- 访问日志和错误日志轮换。

新服务器默认使用空白实例。只有用户明确提供并授权时，才添加上游账号、OAuth 文件或供应商 API Key。不同人员或不同服务器之间不能共享这些凭据。

验收项目：

```bash
systemctl is-active cli-proxy-api
curl -k https://<SERVER_IP>:8318/v1/models   -H 'Authorization: Bearer <API_KEY>'
```

返回 HTTP 200 且 JSON 中有 `data` 数组，才算 API 基础功能正常。模型列表为空不一定是服务故障，通常表示还没有添加上游账号或供应商 Key。

## 七、CLIProxyAPI 自动升级逻辑

自动更新只负责：

- CLIProxyAPI；
- CLIProxyAPI Management Center。

默认不自动升级：

- 3x-ui；
- Xray；
- Nginx；
- OpenClash 规则逻辑。

推荐使用 systemd timer，每 30 分钟检查一次最新版，并加入最多约 120 秒的随机延迟，避免多台服务器同时请求发行站。

更新流程：

1. 查询官方稳定版；
2. 如果 GitHub API 不可用，回退到官方 releases redirect；
3. 下载发行包和校验文件；
4. 校验 SHA-256；
5. 保留旧二进制和配置备份；
6. 原子替换新二进制；
7. 重启 CLIProxyAPI；
8. 检查本地 `/v1/models`；
9. 检查公网 HTTPS API；
10. 健康检查失败时自动恢复旧版本；
11. 记录版本、耗时和结果，但不记录密钥。

示例 timer：

```ini
[Timer]
OnCalendar=*-*-* *:00,30:00 UTC
RandomizedDelaySec=120s
Persistent=true
Unit=cliproxy-auto-update-all.service
```

为了避免坏版本反复重启，应对同一失败版本设置 24 小时退避。更新脚本必须有文件锁，避免两个升级任务同时运行。

“秒速更新”应理解为自动、定期、无人值守更新，而不是发现新版本后零延迟升级。当前方案通常在半小时内发现新版本，下载和健康检查通过后完成切换。

## 八、备份和回滚

每日备份至少包含：

- 3x-ui 配置和数据库；
- Xray 配置；
- CLIProxyAPI 配置；
- Nginx 配置；
- `/etc/letsencrypt` 证书、续期配置和 renewal hook；
- 订阅生成器配置；
- 本地规则镜像；
- systemd unit 文件；
- 版本和 SHA-256 清单。

备份目录必须是 `0700`，文件必须是 `0600`。备份中不能包含未加密的私钥、OAuth 或 API Key，除非备份本身已加密并有明确保管位置。

回滚时先恢复配置和旧程序，再重启服务，最后重新执行本地和公网健康检查。不能直接删除整台服务器重新安装来解决普通配置问题。

## 九、交付验收清单

部署完成后，执行以下检查：

```bash
ssh -o BatchMode=yes <SSH_ALIAS> 'hostname; id -u'
systemctl is-active x-ui
systemctl is-active xray
systemctl is-active nginx
systemctl is-active cli-proxy-api
systemctl is-active cliproxy-auto-update-all.timer
ss -lntp
free -m
```

另外核对：

- 3x-ui 面板 HTTPS 返回 200；
- 2096、53998、8318 和 2443 使用受信任的 Let's Encrypt IP 证书；
- `openssl s_client` 能看到正确的 Let's Encrypt issuer 和服务器 IP SAN；
- `certbot renew --dry-run --run-deploy-hooks` 成功；
- OpenClash 订阅 HTTPS 返回 200 且 YAML 可解析；
- Shadowrocket 订阅 HTTPS 返回 200；
- Reality 443 入口可握手；
- TLS 2443 入口可握手；
- CLIProxyAPI 管理中心可以打开；
- API Key 可以访问 `/v1/models`；
- IPv6 出站未被使用；
- Gemini、Grok、Muse、OpenAI、Claude 命中预期策略组；
- 防火墙只开放必要端口；
- 新服务器没有旧服务器的敏感信息；
- 自动升级 timer 已启用；
- 至少有一次成功的备份；
- 至少有一次成功的健康检查和回滚演练记录。

## 十、常见问题判断

### 订阅能打开，但节点连不上

依次检查：

1. 客户端是否支持 Reality；
2. 443 或 2443 是否被服务商安全组拦截；
3. UFW 是否放行；
4. SNI、Reality 公钥、short ID、UUID 是否完整；
5. 手机网络是否能访问该 IP；
6. 同一订阅中的另一节点是否正常。

### 中国移动数据访问订阅超时

这通常是 IP 线路、运营商策略、端口可达性或服务器侧防火墙问题。先分别测试：

- `https://<SERVER_IP>:2096/<PATH>`
- 443 Reality 节点；
- 2443 TLS 节点；
- Wi-Fi 和 4G/5G；
- 不同运营商。

不要仅凭“换一个域名”判断问题已解决。

### 速度明显低于朋友

不要只比较套餐名称。还应比较：

- 同一客户端和同一协议；
- 同一宽带、同一 Wi-Fi 频段；
- 本地设备到路由器的链路；
- OpenClash 是否启用 TUN、DNS 劫持和正确的 MTU；
- 路由器 CPU、网卡是否降速；
- 服务器 CPU、出口线路和上游限速；
- Fast.com 显示的是 Mbps 还是下载工具显示的 MB/s。

### CLIProxyAPI 内存不够

先查看：

```bash
free -m
systemctl show cli-proxy-api --property=MemoryCurrent,MemoryPeak,MemoryMax
journalctl -k --since '24 hours ago' | grep -i oom
```

2 GB 服务器适合常见的文本流式并发。1 GB 服务器在大量长连接、大上下文或多媒体请求下余量较小，应优先升级到 2 GB。不要先人为设置很小的 `MemoryMax`，否则会制造人为 OOM。

## 十一、自动化部署执行模板

将下面内容连同本文交给部署工具，并把真实私钥通过本机文件路径提供：

```text
目标：在全新 VPS 上独立部署 3x-ui/Xray、OpenClash 和 Shadowrocket 订阅、
CLIProxyAPI、Management Center、IPv4 出站、AI 分流、备份和自动升级。

服务器 IP：<SERVER_IP>
SSH 用户：<SSH_USER>
SSH 端口：<SSH_PORT>
本机私钥路径：<SSH_KEY_PATH>
SSH 别名：<SSH_ALIAS>

要求：
1. 不修改任何旧服务器。
2. 不复制旧服务器数据库、OAuth、API Key、订阅密钥或 Reality 私钥。
3. 为本机生成独立 UUID、Reality 密钥、订阅路径、面板凭据和 CLIProxyAPI Key。
4. 配置 Reality 443 和 TLS 2443。
5. 配置 OpenClash/Mihomo 与 Shadowrocket 两套独立节点身份。
6. 配置 Gemini、Grok、Muse、OpenAI、Claude 等 AI 分流。
7. 配置 ipv6: false 和 IPv4 优先出站。
8. 开放并验证 22、80、443、2443、2096、8318、53998。
9. 部署 CLIProxyAPI 和 Management Center。
10. 设置每 30 分钟检查最新版、SHA-256 校验、原子替换、健康检查和失败回滚。
11. 自动升级只处理 CLIProxyAPI 和 Management Center，不升级 3x-ui/Xray。
12. 完成服务、端口、订阅、API、规则和备份验收。
13. 不在聊天、日志或终端输出私钥和完整密钥。
14. 根据服务商机房地区确认 `SERVER_TIMEZONE`，执行 `timedatectl set-timezone`，并验证 NTP 同步；不要仅凭 IP 地理库猜测时区。
15. 最后只输出脱敏后的登录地址、订阅地址、版本和验收结果。
```

## 十二、方案边界

这套蓝图可以把部署工作标准化，但不能保证所有地区、所有运营商都能访问同一个 IP，也不能保证上游 AI 账号本身可用。线路质量、服务商封锁、客户端兼容性、上游账号权限和供应商 API 限额仍然需要实际测试。

最重要的原则是：每台服务器独立生成凭据，先验证 SSH 和服务，再开放给用户；所有自动更新都必须可校验、可健康检查、可回滚。
