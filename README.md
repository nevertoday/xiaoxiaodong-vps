# 小小东 VPS

> 买一台自己的 VPS，让 AI 按小小东的方案配置好，再把订阅导入 Clash Verge Rev 就能用。

很多人用 Claude、ChatGPT 时走的是几百上千人共用的节点，甚至是来源不明的供应商节点。这类 IP 被大量账号和脚本反复使用，信誉和风险都说不清。Claude 对网络环境要求很严，最稳的办法是**自己买一台 VPS，只给自己用**。

这个项目是我自己服务器的配置方案，做成了一个 AI skill。你只要告诉 AI 服务器 IP、登录方式、想用的登录名称，它会自动完成：

- **代理节点**：3x-ui 管理，Reality 主力节点 + TLS 备用节点，只走 IPv4 出口；
- **订阅 + AI 分流**：Clash Verge Rev / OpenClash / Shadowrocket 订阅，Claude、ChatGPT、Gemini、Grok 等 AI 网站的规则已经配好；
- **CLIProxyAPI**：带管理中心的 API 服务，每 30 分钟自动更新到最新版，坏版本自动回滚；
- **正规 HTTPS 证书**：Let's Encrypt 签给服务器 IP 的证书，自动续期，打开不会提示"不是私密连接"；
- **安全**：以后用 `ssh 你起的名字` 免密登录，关闭密码登录，防火墙只开必要端口；
- **维护**：规则每日更新、配置每日备份、一条命令验收全部功能。

## 三步完成

### 第一步：买一台服务器

目前请直接买**搬瓦工**：它的线路帮我熬过了 ChatGPT 和 Claude 好几轮严格的风控，也是现在唯一有货的推荐。

**[点这里购买搬瓦工 BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

我也推荐 [DMIT](https://www.dmit.io/aff.php?aff=23544)，同样很稳定，但**现在暂时缺货**，不用等它补货。

> 两个都是我的邀请链接，通过它们购买我可能获得佣金。库存、价格以官网为准，任何套餐都不能保证一定通过 AI 服务的风控。

系统选 **Ubuntu 24.04 LTS**（或 Debian 12/13）。开通后在服务商后台记下：**服务器 IP、root 密码（或密钥文件）、SSH 端口**。

### 第二步：让 AI 配置服务器

准备一个能在电脑上执行命令的 AI 工具：[Claude Code](https://claude.com/claude-code) 或 [Codex](https://github.com/openai/codex)。Windows 用户请在 WSL 里使用。

**复制下面这段话，填上你的服务器信息，发给 AI：**

```text
请按「小小东 VPS」方案配置我新买的服务器。

方案地址：https://github.com/nevertoday/xiaoxiaodong-vps
请先把这个项目下载到本机，完整阅读 skills/xiaoxiaodong-vps/SKILL.md，
严格按里面的步骤和规则，用项目里的脚本完成部署和验收。

我的服务器：
- IP：
- 登录方式：初始密码（请让我在终端里自己输入）
- SSH 用户名和端口：默认
- 以后想用这个名字登录：bwg
```

只需要改三处：

- **IP**：填服务商后台显示的服务器 IP；
- **登录方式**：服务商给的是密钥文件，就改成 `密钥文件：文件在电脑上的路径`（zip 也可以）；
- **名字**：把 `bwg` 换成你喜欢的名字，以后输入 `ssh 这个名字` 就能登录服务器。

用户名和端口不是 root / 22 的，把"默认"改成实际值。机房城市、每月流量额度可以不填，AI 会按服务商机房设置时区。

然后等它跑完，通常十几分钟。中途 AI 会请你在终端里输入一次服务器密码。密码不要发在聊天里；配置完成后服务器会关闭密码登录，只能用你电脑上的密钥登录。

> AI 如果说下载不了项目，就手动[下载 ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) 并解压，在上面那段话里加一句"项目已经在：解压后的文件夹路径"。

<details>
<summary>经常配服务器？也可以把它装成 skill，以后一句话就能调用</summary>

复制到终端执行一次：

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

之后对 AI 说"用 xiaoxiaodong-vps 帮我配置新买的服务器"就行（Claude Code 里也可以输入 `/xiaoxiaodong-vps`，Codex 里输入 `$xiaoxiaodong-vps`），AI 会自己问你要服务器信息。

</details>

完成后你会得到一个只保存在你电脑上的文件 `~/xxd-vps/你的名字/登录信息.md`，里面有：

| 内容 | 用来做什么 |
| --- | --- |
| `ssh 你的名字` | 以后登录服务器 |
| Clash 订阅地址 | 电脑 Clash Verge Rev、路由器 OpenClash |
| Shadowrocket 订阅地址 | iPhone |
| 3x-ui 面板地址、账号、密码 | 管理节点 |
| CLIProxyAPI 管理中心地址和登录 Key | 添加你自己的上游账号 |
| CLIProxyAPI API 地址和 API Key | 给支持的应用调用 |

### 第三步：导入订阅

电脑安装 **[Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases)**，在"订阅 / Profiles"里粘贴 **Clash 订阅地址**，选中它，然后打开 **规则模式 + 系统代理**。AI 网站的分流已经配好，不需要自己加规则。

iPhone 用 Shadowrocket 导入 **Shadowrocket 订阅地址**；路由器 OpenClash 导入 **Clash 订阅地址**。

最后打开 <https://ip.net.coffee/claude/> 看出口评分，确认显示的是你 VPS 的 IP。**70 分以上**心里可以踏实一些；分数太低，可以让 AI 帮你排查（IP 历史、DNS 泄漏、IPv6 等），问题出在 IP 本身时换 IP 更有效。

更多客户端设置和使用习惯建议，见 [客户端与使用建议](./docs/客户端与使用建议.md)。

## 以后需要维护时

想检查服务器是否一切正常，复制这段话发给 AI（把 `bwg` 换成你的名字）：

```text
请按「小小东 VPS」方案检查我的服务器：ssh bwg

方案地址：https://github.com/nevertoday/xiaoxiaodong-vps
请下载项目，阅读 skills/xiaoxiaodong-vps/SKILL.md 的"以后的复核和维护"部分，
先做只读验收，把没通过的项目和原因告诉我，我同意后再修。
不要在聊天里显示密码、订阅地址或 Key。
```

它会检查服务、证书、订阅、节点、CLIProxyAPI、自动更新、备份、防火墙和 SSH，只报告问题，不乱改。

遇到问题先看 [常见问题](./skills/xiaoxiaodong-vps/references/troubleshooting.md)。想知道每个设计为什么这样做，看 [方案详解](./skills/xiaoxiaodong-vps/references/design.md)。

## 项目结构

```
skills/xiaoxiaodong-vps/
├── SKILL.md                 AI 执行的步骤和规则
├── references/
│   ├── design.md            方案详解：每个部分是什么、为什么
│   └── troubleshooting.md   常见问题与修复
└── scripts/
    ├── local/connect.sh     在你电脑上建立 ssh 名称免密登录
    ├── local/remote.sh      上传工具、分阶段执行、保存登录信息
    └── server/xxd-vps.py    在服务器上完成全部部署和验收
docs/客户端与使用建议.md
```

## 安全与隐私

- 项目里不包含任何真实服务器的 IP、密钥、密码、订阅地址或 Key。
- 每台服务器的密码、UUID、Reality 密钥、订阅路径、CLIProxyAPI Key 都在部署时**随机新生成**，只保存在服务器的 `/etc/xxd-vps/credentials.json`（仅 root 可读）和你电脑上的 `登录信息.md`。
- 部署过程中 AI 不会在聊天里显示这些信息。请不要把登录信息文件、完整订阅地址或 Key 发到群里、截图或上传到任何地方。
- 自建节点只给自己和信任的家人用，不要大范围分享。
- 发现安全问题请按 [SECURITY.md](./SECURITY.md) 私下联系。

## 方案边界

服务商线路、运营商网络、IP 历史信誉、客户端版本、上游 AI 账号权限都会影响最终效果。这个项目能把服务器配置标准化并逐项验收，但不能保证每个地区每个运营商都能连上同一个 IP，也不能保证 AI 账号本身不被风控。

## License

[MIT](./LICENSE)
