# 小小东 VPS

> 买一台搬瓦工 VPS，按小小东的方案配置好，再把订阅导入 Clash Verge Rev 使用。

这份项目分享的是我自己使用的服务器配置方案：让你拥有自己的代理节点，以及 CLIProxyAPI 接口和管理页面。配置包含 3x-ui、AI 网站分流、证书、安全设置和后续自动维护。

**你要做的事只有三步：购买服务器 → 让 Codex / Claude Code 按本项目配置 → 导入订阅使用。** 不需要先学会 Linux、端口或代理规则。这里提供的是部署文档，下载项目后仍需在你自己的 VPS 上执行配置。

[项目主页](https://github.com/nevertoday/xiaoxiaodong-vps) · [完整部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md) · [部署模板](./部署模板.md) · [安全说明](./SECURITY.md)

## 第一步：买一台搬瓦工服务器

我个人优先推荐搬瓦工。以前使用它的一些线路，帮我度过了 ChatGPT 和 Claude 使用中网络不稳定的时期，因此这份教程从搬瓦工开始。

**[点击这里购买搬瓦工 VPS](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

我也推荐 DMIT；遇到 DMIT 缺货时，直接先选搬瓦工，不必等补货。库存和价格以购买页面为准。上面是我的邀请链接，通过它购买，我可能获得佣金。

买好并开通后，在服务商后台找到 **服务器 IP、SSH 用户名、SSH 端口和初始密码**。如果提供的是密钥文件，保存到自己的电脑即可。选系统时，优先选择受支持的 Ubuntu LTS。

## 第二步：让 Codex / Claude Code 按本方案配置

在电脑上打开能够操作终端、执行 SSH 的 Codex 或 Claude Code，[下载并解压本项目](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip)，让它打开解压后的文件夹。

**复制下面这段话，替换服务器信息后发送即可：**

```text
请阅读当前项目的《3x-ui-CLIProxyAPI-服务器部署蓝图.md》，按小小东 VPS 方案配置我的新服务器，并完成文档中的验收。

服务器 IP：填写这里
SSH 用户名：root（以服务商提供的信息为准）
SSH 端口：填写服务商给的端口
登录方式：初始密码；请提示我通过安全方式输入
以后希望用这个命令登录：ssh bwg

请完成 3x-ui、代理节点、AI 网站分流、CLIProxyAPI、可信 HTTPS 证书、SSH 密钥登录、安全设置和自动维护。时区按机房地区确认。
只操作这台新服务器。完成后把面板登录信息、两种订阅地址、CLIProxyAPI 地址和 Key 保存到我的本机文件，并告诉我文件在哪里。
```

如果使用密钥，把“登录方式”改为“密钥文件：你的本机文件路径”。无需填写 UUID、端口方案、规则或证书参数，这些已经写在部署蓝图中。密码使用工具的安全输入方式提供，不要写进公开仓库、Issue 或截图。

完成后，你应当拿到这些结果：

| 拿到的内容 | 用来做什么 |
| --- | --- |
| `ssh bwg` 登录方式 | 以后维护服务器 |
| 3x-ui 面板地址、账号和密码 | 管理自己的代理节点 |
| OpenClash / Mihomo 订阅地址 | 导入电脑的 Clash Verge Rev 或路由器 |
| Shadowrocket 订阅地址 | 导入 iPhone 的 Shadowrocket |
| CLIProxyAPI 管理地址和登录 Key | 管理模型接口与上游授权 |
| CLIProxyAPI API 地址和 API Key | 供支持的应用调用接口 |

CLIProxyAPI 部署完成后，还需要你在管理页面添加自己的上游账号或供应商 API Key，才能调用模型。

## 第三步：导入订阅，开始使用

电脑安装 **[Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)**，在“配置”中导入上一步拿到的 **OpenClash / Mihomo 订阅地址**，选择该配置，然后开启 **规则模式 + 系统代理**。

AI 网站的分流规则已包含在方案里，通常不用自己再写规则。iPhone 用户将 **Shadowrocket 订阅地址** 导入 Shadowrocket；路由器用户将 **OpenClash / Mihomo 订阅地址** 导入 OpenClash。

最后打开平时使用的网站测试。也可以访问 <https://ip.net.coffee/claude/> 查看出口评分，先确认它检测到的是你的 VPS IP。评分是第三方参考，不能保证 Claude 或其他服务一定可用。

**到这里就完成了。** 遇到问题时，把客户端报错和本项目一起提供给配置服务器的工具排查；不要公开密码、完整订阅地址或 Key。

## 需要更多细节时再看

| 你的目的 | 建议阅读 |
| --- | --- |
| 第一次购买、配置和使用 | 按本 README 上面的三步操作 |
| 部署时需要遵循的完整配置要求 | [3x-ui + CLIProxyAPI 多服务器部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md) |
| 单独复制部署说明，或做后续复核 | [新服务器部署模板](./部署模板.md) |
| 报告公开文档中的安全问题 | [SECURITY.md](./SECURITY.md) |

## 下载与在线阅读

如果你只想保存到本机，直接下载整个项目 ZIP：

- [下载项目 ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip)
- [浏览 GitHub 项目](https://github.com/nevertoday/xiaoxiaodong-vps)

也可以单独打开或保存这些 Markdown 文件：

- [README 在线版](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/README.md)
- [部署蓝图原文](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/3x-ui-CLIProxyAPI-%E6%9C%8D%E5%8A%A1%E5%99%A8%E9%83%A8%E7%BD%B2%E8%93%9D%E5%9B%BE.md)
- [部署模板原文](https://raw.githubusercontent.com/nevertoday/xiaoxiaodong-vps/main/%E9%83%A8%E7%BD%B2%E6%A8%A1%E6%9D%BF.md)
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

这一项由部署工具处理，你可以不填写。配置时按服务商控制台的机房地区确认时区，公网 IP 只用于交叉核对，不能单独依赖 IP 地理库。

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
