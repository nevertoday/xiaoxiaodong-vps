# 小小东 VPS

> 一套面向个人 VPS 的 3x-ui/Xray、AI 分流、CLIProxyAPI 和持续维护文档。

项目目标是把“自己购买 VPS、自己生成凭据、自己维护节点和接口”的流程写清楚，方便人工部署，也方便交给能够执行 SSH 命令的 AI。文档只提供通用方案，不包含任何真实服务器密钥或账号凭据。

[项目主页](https://github.com/nevertoday/xiaoxiaodong-vps) · [完整部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md) · [AI 提示词](./AI-部署提示词.md) · [安全说明](./SECURITY.md)

## 先看哪一份文件

| 你的目的 | 建议阅读 |
| --- | --- |
| 了解项目、选择客户端、复制下载地址 | 本 README |
| 从零部署一台 VPS | [3x-ui + CLIProxyAPI 多服务器部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md) |
| 直接把要求交给 Codex 或其他执行型 AI | [交给 AI 的部署提示词](./AI-部署提示词.md) |
| 报告公开文档中的安全问题 | [SECURITY.md](./SECURITY.md) |

## 下载与在线阅读

如果你只想保存到本机，直接下载整个项目 ZIP：

- [下载项目 ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip)
- [浏览 GitHub 项目](https://github.com/nevertoday/xiaoxiaodong-vps)

也可以单独打开或保存这些 Markdown 文件：

- [README 在线版](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/README.md)
- [部署蓝图原文](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/3x-ui-CLIProxyAPI-%E6%9C%8D%E5%8A%A1%E5%99%A8%E9%83%A8%E7%BD%B2%E8%93%9D%E5%9B%BE.md)
- [AI 提示词原文](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/AI-%E9%83%A8%E7%BD%B2%E6%8F%90%E7%A4%BA%E8%AF%8D.md)
- [安全说明原文](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/SECURITY.md)

## 这套方案包含什么

| 模块 | 作用 |
| --- | --- |
| 3x-ui / Xray | 管理节点、Reality 主入口和 TLS 备用入口 |
| OpenClash / Mihomo | 路由器和桌面端使用的 YAML 订阅与规则 |
| Shadowrocket | 移动端使用的通用订阅 |
| AI 分流 | Gemini、Grok、Muse、OpenAI、Claude、Google AI 等策略组 |
| CLIProxyAPI | API 入口、Management Center、健康检查和上游账号管理 |
| HTTPS 证书 | Let's Encrypt IP 证书、Nginx/Xray 共用、短周期自动续期和失败检查 |
| 自动维护 | 版本校验、定时升级、备份、回滚、日志轮换和端口检查 |
| 安全基础 | SSH 密钥、UFW、systemd 限权、IPv4 优先和代理侧 IPv6 关闭 |

每台服务器都应独立生成 UUID、Reality 密钥、订阅路径、面板密码、管理密钥和 API Key。不能把一台服务器的数据库、OAuth、订阅或用户凭据直接复制到另一台。

## 推荐使用路径

### 1. 购买并记录一台 VPS

准备好以下信息：

- 公网 IPv4；
- SSH 用户名和端口；
- 本机私钥路径，或服务商提供的初始密码；
- 服务商控制台标注的机房地区；
- 操作系统、CPU 架构、内存和流量限制。

如果服务商只有初始密码，先用密码写入公钥并确认密钥登录成功，再关闭密码认证。不要在密钥登录验证前关闭密码认证。

### 2. 填写变量并交给 AI

打开 [AI-部署提示词](./AI-部署提示词.md)，先填写这一段：

```text
SERVER_IP=服务器公网 IPv4
SSH_USER=root
SSH_PORT=22
SSH_KEY_PATH=/Users/你的用户名/.ssh/server-key
SSH_ALIAS=server-name
SERVER_REGION=服务商标注的机房地区
SERVER_TIMEZONE=America/Los_Angeles
```

然后把完整提示词和[部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md)交给能够执行本机 SSH 命令的 AI。私钥正文不要粘贴到聊天中；只提供本机文件路径，并要求 AI 输出脱敏结果。

### 3. 用实际客户端验收

部署完成后，先打开订阅地址，确认返回 HTTP 200；再导入客户端，选择规则模式，最后分别测试普通网站和 Gemini、Grok、Muse、OpenAI、Claude。

不要只看“面板能打开”。节点握手、订阅解析、AI 规则命中、CLIProxyAPI `/v1/models`、防火墙、自动升级和备份都要完成验收。

## 桌面端推荐：Clash Verge Rev

Windows、macOS 和 Linux 建议使用 **Clash Verge Rev**。项目里的规则、AI 分流组和节点参数已经在服务器端准备好，客户端通常只需要导入 Mihomo YAML 订阅。

官方入口：

- [Clash Verge Rev 项目主页](https://github.com/clash-verge-rev/clash-verge-rev)
- [官方 Releases 下载页](https://github.com/clash-verge-rev/clash-verge-rev/releases)

使用步骤：

1. 从 Releases 下载与你的系统和 CPU 架构对应的版本；
2. 打开 **Profiles / 配置**；
3. 粘贴服务器提供的 **OpenClash / Mihomo YAML 订阅地址**，保存并更新；
4. 选中刚导入的配置；
5. 运行模式选择 **Rule / 规则**；
6. 打开 **System Proxy / 系统代理**。

规则已经包含 Gemini、Grok、Muse、OpenAI、Claude 等 AI 分流，通常不需要手工添加规则。普通浏览器和大多数桌面应用先使用系统代理；只有某个程序不遵守系统代理时，再单独评估 TUN / 服务模式、DNS 和权限。

旧版 Clash for Windows 0.19.20 可能无法解析本项目使用的 Mihomo 字段，出现下面的错误时，应升级到支持 Mihomo 的客户端：

```text
yaml: unmarshal errors:
  line 24: cannot unmarshal !!seq into string
  line 27: cannot unmarshal !!seq into string
  line 30: cannot unmarshal !!seq into string
```

不要把 Shadowrocket 的 Base64 订阅地址当成 Clash Verge Rev 的 YAML 订阅地址。

## 服务器时区策略

时区必须作为部署变量明确指定。以服务商控制台的机房地区为准，公网 IP 只用于交叉核对，不能单独依赖 IP 地理库。

常见值：

| 机房地区 | `SERVER_TIMEZONE` |
| --- | --- |
| 美国西部、洛杉矶 | `America/Los_Angeles` |
| 统一使用 UTC | `Etc/UTC` |
| 中国大陆本地机房 | `Asia/Shanghai` |

部署时执行：

```bash
timedatectl set-timezone "$SERVER_TIMEZONE"
timedatectl show --property=Timezone --value
timedatectl show --property=NTPSynchronized --property=LocalRTC
```

时区只影响服务器本地时间、日志和未明确指定时区的定时任务，不会改变公网 IP、代理出口、路由或 Claude 风控结果。

## 为什么建议自己买 VPS

很多人直接使用共享节点或所谓“万人共用”的供应商节点。这样的 IP 可能被大量账号、自动化脚本和不同来源的用户反复使用，IP 信誉、ASN、出口行为和账号环境都更难判断。

自己购买 VPS、自己生成凭据、自己维护节点，可以控制：

- 出口 IP 是否与陌生用户共用；
- UUID、Reality 密钥和订阅路径如何生成；
- DNS、IPv6、规则和出站线路如何检查；
- 配置如何备份、升级和回滚。

自建不能保证通过 Claude、ChatGPT 或其他服务的风控，但能减少共享节点带来的不确定性。也不要把自建节点大范围分享给陌生人。

## 个人推荐的 VPS 服务商

### 搬瓦工 BandwagonHost

库存、地区和套餐会变化，最终以官网实时页面为准。个人使用中，部分搬瓦工线路和 IP 稳定性较好，但任何套餐和 IP 都不能保证一定通过 AI 服务的风控。

我的邀请链接：

<https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55>

### DMIT

购买前请确认当前套餐、库存、地区、流量、带宽、路由和退款规则。

我的邀请链接：

<https://www.dmit.io/aff.php?aff=23544>

两家链接都是邀请链接。如果通过链接购买，我可能获得推广佣金；这不代表对具体套餐、线路、IP 或 AI 可用性的保证。

## 配置完成后的检查

可以用下面的第三方页面检查当前代理出口的 Claude 相关评分：

<https://ip.net.coffee/claude/>

个人会把 **70 分以上** 当作相对安心的参考线，不把它当作 Claude 官方许可或稳定性保证。测试时确认页面检测到的是代理出口 IP，而不是本地宽带 IP。

分数偏低时，可以让 AI 检查：

- IP 黑名单、滥用历史、ASN 和机房类型；
- 反向 DNS、DNS 泄漏和 IPv6 暴露；
- Reality、SNI、short ID、UUID 和客户端规则；
- 是否残留旧订阅、旧用户或共享使用痕迹。

如果问题来自服务商 IP 的历史信誉，配置优化不一定能彻底解决，换 IP 或更换套餐可能更有效。

## 设备环境与使用行为

- 按隐私需要关闭不必要的系统定位权限；这不会改变代理出口 IP，也不能保证通过任何服务的风控；
- 如果长期固定使用某个 VPS 出口，可以让电脑时区与 VPS 所在地区一致，并避免频繁切换；
- 保持系统语言、浏览器、登录设备和网络习惯相对稳定；
- 不要把个人账号变成公共 API、共享节点或批量调用入口；
- 避免短时间内大量相似提问、并发刷请求、自动化轮询、批量导出或类似模型蒸馏厂的行为；
- 不要绕过速率限制、验证码、账号限制或服务商安全措施；
- 遵守所在地法律、服务商条款和 AI 服务使用政策，不提交违法、暴力伤害、恶意入侵或窃取隐私的请求。

## 安全边界

公开项目不包含任何真实服务器的：

- SSH 私钥；
- 面板密码；
- 订阅密钥；
- Reality 私钥；
- OAuth 文件；
- CLIProxyAPI 管理密钥或 API Key。

部署时必须为每台服务器重新生成凭据，并通过本机安全文件或密钥管理器注入。不要把真实密钥提交到 Git，也不要把完整订阅地址公开发到公共群组。发现文档安全问题，请按 [SECURITY.md](./SECURITY.md) 联系维护者。

## 方案边界

服务商线路、运营商网络、客户端版本、IP 历史信誉、上游账号权限和供应商 API 限额都会影响最终结果。这套项目可以标准化部署和验收，但不能保证所有地区都能访问同一个 IP，也不能保证上游 AI 账号本身可用。

最重要的原则是：每台服务器独立生成凭据，先验证 SSH 和服务，再交付给用户；所有自动更新都必须可校验、可健康检查、可回滚。
