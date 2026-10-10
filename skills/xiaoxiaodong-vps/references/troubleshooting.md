# 常见问题与修复

先看脚本 `停止：` 后面的原因，再在这里找对应条目。修好后**重跑同一个阶段**。

## 登录阶段（connect.sh）

**密码登录失败**
- 密码输错：请用户到服务商后台核对或重置 root 密码。
- 服务商要求首次登录改密码（提示 `You are required to change your password`）：请用户先用服务商后台的 VNC 控制台或自己的终端登录一次改掉密码，再用新密码重试。
- 服务器禁止了 root 密码登录：改用服务商提供的普通用户（`--user 用户名`），该用户需要能 `sudo`。

**服务商给的密钥登录不上**
- 有些服务商的密钥要先在后台"绑定"到这台服务器才生效；也有的只接受密码。请用户在后台确认，或改用密码方式。
- 压缩包里有多把私钥、是 PuTTY 的 `.ppk`、或私钥带口令：请用户下载 OpenSSH 格式、不带口令的私钥，或改用密码方式。

**macOS 读不到"下载"文件夹里的密钥**：系统隐私保护拦截了终端，请用户把文件拖到桌面，再给新路径。

**ssh 名称已被占用**：`~/.ssh/config` 里同名条目指向了别的服务器。换一个名称，不要改动原条目。

## init

- **公网 IP 不是用户给的 IP**：连错了服务器，或者 IP 抄错了。停下来和用户核对，不要加参数强行继续。
- **检测到已有 3x-ui 数据库**：这台机器装过别的面板。如果用户确认这是刚买的机器、上面没有要保留的东西，请他在服务商后台把系统重装为 Ubuntu 24.04 LTS，再从 connect 开始。
- **系统不支持**：只支持 Ubuntu 22.04+ / Debian 12+。请用户在后台重装系统。

## cert：IP 证书申请失败

1. 服务商有安全组 / 防火墙面板时，确认已放行 **TCP 80**（以及 443、2443、2096、8318、53998）。
2. 在用户电脑上测 `curl -sS -m 10 -o /dev/null -w '%{http_code}\n' http://IP/.well-known/acme-challenge/test`：返回 404 说明 80 端口通了。
3. Let's Encrypt 对同一 IP 有频率限制，短时间内失败多次时要等一段时间再试。
4. 不要改用自签名证书，也不要关掉客户端的证书校验。

## xui

- **3x-ui 面板没有在 HTTPS 53998 上响应**：`journalctl -u x-ui -n 50` 看原因。常见是证书路径不对（先确认 cert 阶段通过）或 53998 被其他程序占用（`ss -lntp | grep 53998`）。
- **生成的 Xray 配置不符合预期**：说明某个入口或身份缺失、flow 不对。重跑 `xui`，脚本会补齐缺的入口并重新挂好身份。

## sub

- **规则下载不完整**：服务器暂时访问不了 GitHub。过几分钟重跑 `sub`；已经下载成功的文件会保留。
- **订阅里的规则与本机镜像不一致**：某个上游改了文件格式。把 `files/clash-template.yaml` 里对应规则集的 `behavior` 改成实际格式（`domain` / `ipcidr` / `classical`），重跑 `xui` 和 `sub`。

## 客户端

**导入订阅后连不上**
1. Clash 类客户端用 **Clash 订阅**，Shadowrocket 用 **Shadowrocket 订阅**，不要混用。
2. 在同一订阅里换另一个节点（Reality ↔ TLS）试试。
3. 确认客户端版本较新（Clash Verge Rev 用最新版；旧的 Clash for Windows 不支持 Reality）。
4. 在服务器上跑 `xxd-vps verify`，看节点结构那一项是否 PASS。

**Clash for Windows 报 `yaml: unmarshal errors ... cannot unmarshal !!seq into string`**：客户端太旧，不支持 Mihomo 的配置字段。改用 Clash Verge Rev。

**国内连不上（超时），国外网络正常**
- 先在用户电脑上测：`curl -sS -o /dev/null -w '%{http_code}\n' --max-time 10 https://IP:2096/`。超时说明用户的网络到这个 IP 不通，与配置无关。
- 分别用 Wi-Fi、手机流量、不同运营商测试。只有某个运营商不通，多半是线路问题。
- 这种情况换配置、换域名都解决不了，只能联系服务商换 IP 或换线路更好的套餐。

**速度比别人慢很多**
- 先确认单位：Fast.com 显示 Mbps，下载工具常显示 MB/s（1 MB/s ≈ 8 Mbps）。
- 用同一台设备、同一网络、只切换节点来比较。
- 检查本地链路：Wi-Fi 是否 5 GHz、网线 / 路由器 LAN 口是否掉到百兆（`ethtool` 或路由器后台看协商速率）、路由器 CPU 是否跑满。
- 服务器侧：`ssh 名称 'sysctl -n net.ipv4.tcp_congestion_control'` 应显示 `bbr`。

**浏览器打开订阅地址提示"不是私密连接"**：证书不对或过期。`ssh 名称 'xxd-vps verify'` 看证书项；如果续期失败，查 `journalctl -u xxd-vps-cert-renew`，通常是 80 端口被安全组拦了。

**OpenClash 里 AI 网站很慢或解析超时**：本方案的订阅不会把 AI 域名交给本地 DNS 解析。如果你在 OpenClash 里自己加了指向 1.1.1.1 / 8.8.8.8 的 `nameserver-policy`，删掉即可（OpenClash 会强制关闭 `respect-rules`，这些 DNS 请求会直连海外而超时）。

## CLIProxyAPI

- **管理中心打得开但调用模型失败 / 模型列表为空**：还没添加上游账号或供应商 Key，这是正常的。
- **内存紧张**：`systemctl show cli-proxy-api -p MemoryCurrent`，`journalctl -k --since '24 hours ago' | grep -i oom`。1 GB 内存的机器建议升级到 2 GB；不要给服务加 `MemoryMax`。
- **自动更新情况**：`journalctl -u cliproxy-auto-update -n 30`；状态文件 `/var/lib/cliproxy-auto-update/last-run.json`。看到 `ROLLBACK verified` 表示新版本没通过健康检查，已经自动换回旧版。

## 什么时候不要动手

- 用户没要求的其他服务器、路由器、`~/.ssh/config` 里的其他条目。
- 3x-ui / Xray 的版本：除非已经在测试机上用真实客户端验证过新版本。
