# 小小东 VPS

很多人使用 Claude 时，直接购买所谓“共享节点”或万人共用的代理。这样的 IP 往往被大量账号、自动化脚本和不同来源的用户反复使用，甚至可能来自供应商统一分发的高风险节点。即使节点短期能打开 Claude，也不能说明它适合长期使用；一旦 IP 信誉、ASN、出口行为或账号环境被标记，可能出现验证、限流、登录异常，甚至触发更严格的风控。

Claude 对访问环境通常比较敏感。自己购买 VPS、自己部署节点、自己维护访问凭据，可以减少共享 IP 带来的不确定性，也方便在出现问题时检查线路、IP 信誉、DNS、IPv6、规则和客户端配置。

## 为什么建议自己买 VPS

自建并不能保证一定通过 Claude 或 ChatGPT 的风控，但至少可以控制这些关键因素：

- 出口 IP 不与陌生用户共用；
- 节点 UUID、Reality 密钥和订阅路径由自己生成；
- 不需要把账号、OAuth 或 API Key 交给共享节点供应商；
- 可以单独更换 IP、调整规则、关闭 IPv6、检查 DNS 和出站线路；
- 可以保留配置备份，并在升级或故障后回滚。

不要把自建节点大范围分享给陌生人。共享人数越多，IP 信誉和账号风控的不确定性越高。

## 个人推荐的 VPS 服务商

我个人主要推荐两家：

### 搬瓦工 BandwagonHost

目前如果 DMIT 没有合适库存，可以优先查看搬瓦工。库存、地区和套餐会变化，最终以官网实时页面为准。

个人使用体验中，搬瓦工的部分线路和 IP 稳定性较好，曾帮助我应对过 ChatGPT 和 Claude 较严格的访问环境与风控检查。但这属于个人经验，不代表任何套餐或 IP 都能保证通过风控，也不代表购买后一定可以使用 Claude。

我的邀请链接：

<https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55>

### DMIT

DMIT 的部分套餐线路和网络稳定性较好，也适合自己购买后部署。库存和可购买地区会变化，购买前应确认当前套餐、流量、带宽、路由和退款规则。

我的邀请链接：

<https://www.dmit.io/aff.php?aff=23544>

## 部署内容

本项目提供一套可复用的 VPS 部署蓝图，覆盖：

- 3x-ui / Xray；
- Reality 443 和 TLS 备用节点；
- OpenClash / Mihomo 与 Shadowrocket 订阅；
- Gemini、Grok、Muse、OpenAI、Claude 等 AI 分流；
- IPv4 优先出站和代理侧 IPv6 关闭；
- CLIProxyAPI 与 Management Center；
- CLIProxyAPI 自动升级、SHA-256 校验、健康检查和失败回滚；
- SSH 密钥登录、UFW、防火墙、systemd 安全配置；
- 配置备份、端口检查和故障排查。

详细方案见：[3x-ui + CLIProxyAPI 多服务器部署蓝图](./3x-ui-CLIProxyAPI-服务器部署蓝图.md)。

## 桌面端推荐：Clash Verge Rev

对于 Windows、macOS 和 Linux 桌面端，建议使用 **Clash Verge Rev** 导入已经配置好的 Mihomo 订阅。项目里的规则、AI 分流组和节点参数已经在服务器端准备好，用户不需要再手工编写规则。

官方入口：

- [Clash Verge Rev 项目主页](https://github.com/clash-verge-rev/clash-verge-rev)
- [官方 Releases 下载页](https://github.com/clash-verge-rev/clash-verge-rev/releases)

使用步骤：

1. 从官方 Releases 下载与你的系统和 CPU 架构对应的稳定版；
2. 打开 Clash Verge Rev，进入 **Profiles / 配置**；
3. 粘贴服务器提供的 **OpenClash / Mihomo YAML 订阅地址**，保存并更新；
4. 选中刚导入的配置；
5. 将运行模式设置为 **Rule / 规则**；
6. 打开 **System Proxy / 系统代理**。

当前方案建议先使用“规则模式 + 系统代理”，不要手工改写 AI 规则，也不要一开始就切换到 Global / 全局或 Direct / 直连。访问 Gemini、Grok、Muse、OpenAI、Claude 时，配置会按已经写好的规则自动选择对应策略组；访问国内站点时则按国内直连规则处理。

如果某个程序不遵守系统代理，再考虑开启 TUN / 服务模式，并重新检查 DNS 和权限。普通浏览器和大多数桌面应用先使用系统代理即可。

旧版 Clash for Windows 0.19.20 可能无法解析本项目使用的 Mihomo 字段，出现 \`yaml: cannot unmarshal !!seq into string\` 时，应升级到 Clash Verge Rev 或其他支持 Mihomo 的客户端。不要把 Shadowrocket 的 Base64 订阅地址当成 Clash Verge Rev 的 YAML 订阅地址。

## 部署后检查 Claude IP 评分

配置完成后，可以使用下面的第三方页面检查当前出口 IP 的 Claude 相关评分：

<https://ip.net.coffee/claude/>

个人建议把 **70 分以上** 作为一个相对安心的参考线。这个分数只是第三方检测结果，不是 Claude 官方许可，也不能保证账号一定不触发风控。测试时应确认检测到的是实际代理出口 IP，而不是本地宽带 IP，并尽量使用干净的浏览器环境进行复测。

如果分数偏低，可以让 Codex 协助检查：

- IP 是否被列入黑名单或存在滥用历史；
- ASN、机房类型和地理位置是否异常；
- 反向 DNS、DNS 泄漏和 IPv6 是否暴露；
- 节点协议、SNI、Reality 参数和客户端规则是否正确；
- 是否存在多人共用、旧订阅残留或异常访问记录。

如果问题来自服务商 IP 的历史信誉，配置优化不一定能彻底解决，换一个干净的 IP 或更换套餐可能更有效。

## 安全说明

本项目只发布通用架构和占位符，不包含任何真实服务器的：

- SSH 私钥；
- 面板密码；
- 订阅密钥；
- Reality 私钥；
- OAuth 文件；
- CLIProxyAPI 管理密钥或 API Key。

部署时必须为每台服务器重新生成凭据，并通过本机安全文件或密钥管理器注入。不要把真实密钥提交到 Git，也不要把完整订阅地址公开发到公共群组。

## 关联与免责声明

本文中的 DMIT 和 BandwagonHost 链接是我的邀请链接。如果通过链接购买，我可能获得相应的推广佣金；这不会改变文档中的技术方案，也不代表对服务商、套餐、线路或 Claude 可用性的保证。购买前请自行确认价格、库存、地区、流量、退款和服务条款。

这是一份部署和运维参考方案。服务商线路、运营商网络、客户端版本、IP 历史信誉、上游账号权限和供应商 API 限额都会影响最终结果。完成部署后，必须按蓝图中的验收清单进行实际连接测试。
