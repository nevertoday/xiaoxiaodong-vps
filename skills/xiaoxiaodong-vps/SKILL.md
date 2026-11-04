---
name: xiaoxiaodong-vps
description: 按小小东 VPS 方案，把一台全新的 Debian / Ubuntu VPS 配置成自用代理节点 + CLIProxyAPI 服务器：ssh 名称免密登录、3x-ui（Reality 443 + TLS 2443）、OpenClash / Clash Verge Rev / Shadowrocket 订阅与 AI 分流、Let's Encrypt IP 证书自动续期、CLIProxyAPI 与 30 分钟自动更新、SSH/防火墙加固、备份与验收。用户只需提供服务器 IP、SSH 登录方式和想用的 ssh 名称。Use when the user runs /xiaoxiaodong-vps or $xiaoxiaodong-vps, or asks to 配置服务器、部署 VPS、搭节点、装 3x-ui、装 CLIProxyAPI、复刻小小东的服务器方案、新买的搬瓦工/DMIT 配一下、以后 ssh xxx 能登录, or to re-check / repair a server set up this way.
---

# 小小东 VPS

把用户刚买的一台 VPS，配置成和小小东自己用的服务器一样的结构。全部动作由本目录的脚本完成，你负责：问清楚信息、按顺序运行脚本、读懂报错并修复、最后把结果交给用户。

方案每一部分为什么这样设计，见 [references/design.md](references/design.md)；出错时先查 [references/troubleshooting.md](references/troubleshooting.md)。

## 语言

用户用什么语言和你说话，你就全程用那种语言交流（问问题、报进度、交付说明都是）。本文件里的中文模板，按用户的语言转述即可。

保存登录信息时用 `--lang` 生成对应语言的文件：中文 `zh`（默认）、English `en`、한국어 `ko`、日本語 `ja`、العربية `ar`、Español `es`、Français `fr`、Русский `ru`、Deutsch `de`、Português `pt`；其他语言用 `en`。脚本自己的终端输出是中文，你转述给用户就行。

## 必须遵守

1. **只操作用户这次给的这台服务器。** 不登录、不读取、不修改任何其他服务器；`~/.ssh/config` 里已有的条目一律不动。
2. **不在对话里显示任何秘密。** 密码、私钥、面板密码、订阅地址、CLIProxyAPI Key 都不要打印、复述或写进命令参数。脚本已经避免输出它们；登录信息只通过 `remote.sh save` 写进本机文件，你只告诉用户文件路径。
3. **每台服务器独立生成凭据。** 不复制别的服务器的数据库、UUID、Reality 密钥、订阅路径或 Key。
4. **证书必须是 Let's Encrypt 签发、浏览器信任的 IP 证书。** 申请失败就停下来解决（通常是服务商安全组没放行 TCP 80），绝不改用自签名证书继续。
5. **不改脚本里固定的版本**（3x-ui v3.8.5、Xray v26.7.28）。新版 Xray 会让 Shadowrocket 连不上，换版本必须先在测试机上用真实客户端验证。
6. 脚本报错时，按提示修复原因后**重跑同一个阶段**。每个阶段都可以重复执行，不要手工绕过检查，也不要删掉服务器重装来"解决"普通问题。

## 第一步：问用户要信息

用户常常是复制 README 里的那段话来的，消息里已经写了 IP、登录方式、名称。**已经给了的不要再问**，只补问缺的必填项；"默认"表示 root / 22；可选项没写就用默认值。例外：用户提到搬瓦工、或名字用的是 bwg，却没给第 7 项时，补问时（没有要补问的就在部署前）顺带问一次 VEID 和 API Key，说明不给的话客户端只能按默认 1000G 显示，而搬瓦工的套餐有 1T 也有 2T。缺信息时用一条消息问齐，不要一项一项追问：

```text
请告诉我这几项（服务商后台都能看到）：
1. 服务器 IP：
2. 登录方式：初始密码，或者密钥文件在电脑上的路径（zip 也可以）
3. SSH 用户名和端口：不知道就写"默认"（root / 22）
4. 以后想用什么名字登录：比如 bwg，以后输入 ssh bwg 就能进服务器

可选：
5. 机房在哪个城市（用来设时区，不填我按服务商机房判断）
6. 每月流量额度和重置日（只用于在客户端显示用量；不填默认 1000G，重置日按开通日自动推算）；商家的流量是双向还是单向计费；如果服务器之前已经用过，后台显示的本月已用量
7. 搬瓦工的机器：KiwiVM 的 VEID 和 API Key（KiwiVM 左侧菜单「API」页：页面写着 Your VEID，API Key 点页面上方按钮显示，private_ 开头）。给了的话客户端显示的用量和后台完全一致；不给也能用
```

**密码的处理：**

- 最好让用户自己输入，密码不进入对话。按你所在的环境选一种：
  - **桌面版应用**（Codex、Claude 桌面版等，用户面前没有终端）：直接运行 `connect.sh … --password-dialog`。电脑上会弹出系统密码框（Mac 是系统对话框，Windows 是 PowerShell 窗口），先告诉用户「马上会弹出一个密码框，请输入服务器的 root 密码」。用户取消或 10 分钟没输入，脚本会停下，再跑一次即可。
  - **Claude Code 终端版**：让用户输入 `! bash <本skill目录>/scripts/local/connect.sh --alias 名称 --host IP --password-prompt`。
  - **其他终端里的工具**：让用户在自己的终端运行同一条 `--password-prompt` 命令；或者直接用 `--password-dialog`。
  - 不要让用户去打开终端、装 WSL 或登录服务器来输入密码，这些都不需要。
- 如果用户已经把密码发在对话里：先把它写进一个只有本人可读的临时文件，再用 `--password-file`；脚本用完会自动删除该文件。不要把密码直接写在 `connect.sh` 的命令行参数里。

  ```bash
  umask 077; d=$(mktemp -d); printf '%s' '用户给的密码' > "$d/pw"; echo "$d/pw"
  ```

- 部署完成后服务器会关闭密码登录，这个密码就不能再用来 SSH 了。提醒用户：服务商后台的 VNC/救援控制台仍可能用它，建议在后台改掉。

**时区：** 按机房所在地设置，不要只看 IP 地理库。常见：洛杉矶/圣何塞/美西 `America/Los_Angeles`，纽约/美东 `America/New_York`，香港 `Asia/Hong_Kong`，东京 `Asia/Tokyo`，新加坡 `Asia/Singapore`，法兰克福 `Europe/Berlin`，伦敦 `Europe/London`。搬瓦工和 DMIT 的美国机房多数在洛杉矶。实在判断不了用 `Etc/UTC`，并告诉用户。

**ssh 名称：** 只能用字母、数字、连字符，字母开头。如果 `ssh -G 名称` 显示它已经指向别的服务器，请用户换一个。

## 第二步：建立 `ssh 名称` 免密登录

本目录记为 `$SKILL`（本 SKILL.md 所在目录；如果是从下载的项目里读到本文件，就是 `项目目录/skills/xiaoxiaodong-vps`）。本机需要 `bash` 和 `ssh`（OpenSSH 8.4+）。所有命令都在**用户自己的电脑**上运行，不要让用户登录服务器去装任何东西。

**Windows：** 这些由你自己检查、自己补，不要让用户判断或手动安装：

1. 运行 `bash --version`。能用（Git Bash 或 WSL 都行）就直接用它跑脚本。
2. 不能用：运行 `winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements` 装 Git for Windows（自带 bash 和新版 ssh；Windows 可能弹一次「是否允许」，请用户点「是」），装好后用 `"C:\Program Files\Git\bin\bash.exe"` 运行下面的命令。没有 winget 时，请用户从 https://git-scm.com/download/win 下载安装，一路默认。
3. 不要建议用户装 WSL。用户已经在 WSL 里的话照常用。
4. 在 Git Bash 里，`ssh -V` 应当显示 OpenSSH 8.4 以上（Git 自带的版本）；如果显示的是 Windows 自带的旧版，说明 PATH 顺序不对，用 Git 目录里的 `usr/bin/ssh.exe`。

```bash
# 密钥文件（OpenSSH 私钥或服务商给的 zip）
bash "$SKILL/scripts/local/connect.sh" --alias 名称 --host IP --port 端口 --user 用户名 --key 密钥路径

# 初始密码：弹出系统密码框，让用户自己输入（桌面版应用用这个）
bash "$SKILL/scripts/local/connect.sh" --alias 名称 --host IP --port 端口 --user 用户名 --password-dialog

# 初始密码：用户已经发在对话里时，先写进临时文件（用完自动删除）
bash "$SKILL/scripts/local/connect.sh" --alias 名称 --host IP --port 端口 --user 用户名 --password-file 文件路径
```

脚本会：把密钥放进 `~/.ssh/xxd-vps/名称/`（用密码时新生成一把 ED25519 密钥并写入服务器）、在 `~/.ssh/config` 最前面加一个 Host 段（先备份原文件）、验证 `ssh 名称` 能免密登录。

macOS 如果提示读不到"下载"文件夹里的文件，请用户把文件拖到桌面再给你路径。

## 第三步：部署

```bash
R="$SKILL/scripts/local/remote.sh"
bash "$R" 名称 upload
bash "$R" 名称 init --ip IP --alias 名称 --timezone 时区 [--quota-gb 1000 --reset-day 1]
bash "$R" 名称 base       # 时区、依赖、BBR、防火墙、关闭 SSH 密码登录
bash "$R" 名称 cert       # Let's Encrypt IP 证书 + 6 小时续期 + Nginx
bash "$R" 名称 xui        # 3x-ui、固定 Xray、Reality 443、TLS 2443、两套订阅身份
bash "$R" 名称 sub        # 规则镜像、订阅中间层、订阅检查
bash "$R" 名称 cliproxy   # CLIProxyAPI + Management Center
bash "$R" 名称 maint      # CLIProxyAPI 自动更新、规则每日刷新、每日备份
bash "$R" 名称 verify --full
```

- 用量显示更准（可选，任何商家都适用，不影响节点）：`bash "$R" 名称 traffic --used-gb 后台已用GB --count both|out|in|max`。`--used-gb` 按商家后台此刻的本月已用量校准一次，之后本机接着累加；`--count` 是商家的计费方式（双向 / 只算出站 / 只算入站 / 取大的一边，不知道就用默认 both）。不带参数只查看当前显示。周期按服务器所在时区的零点切换。
- 搬瓦工（KiwiVM）可选：用户给了 VEID 和 API Key（KiwiVM 后台 API 页面），`sub` 之后跑 `bash "$R" 名称 kiwivm --veid 数字 --key-file 文件`，订阅里的已用量、总额度、重置日就改用官方读数（每 10 分钟刷新，取不到时退回本机统计）。API Key 和密码一样先写进只有本人可读的临时文件，脚本用完删除；`--remove` 取消。
- 逐个阶段跑，每跑完一个用一句话告诉用户进度（例如"证书已签发，开始装 3x-ui"）。
- `init` 会核对这台机器的公网 IP 是否就是用户给的 IP，并拒绝覆盖不是本工具创建的 3x-ui；遇到这两种情况先问用户，不要强行继续。
- 只支持 Ubuntu 22.04+ / Debian 12+。其他系统请用户在服务商后台重装为 Ubuntu 24.04 LTS。
- 某阶段失败：读 `停止：` 后面的原因，对照 troubleshooting 修复，再重跑这个阶段。

## 第四步：交付

1. `verify --full` 必须全部 PASS。有 FAIL 就先修，修不了就如实告诉用户哪一项没通过、影响是什么；如果是教程或脚本的问题，建议用户到 GitHub 提 Issue（见 troubleshooting 最后一节）。
2. 保存登录信息到本机（不会显示在终端）：

   ```bash
   bash "$R" 名称 save --lang zh   # → 桌面「我的服务器-名称-订阅和账号.md」；其他语言是「my-server-名称-subscriptions-and-accounts-语言.md」。权限 600，没有桌面目录时放在主目录
   ```

3. 从用户这台电脑测一下能不能连到服务器（返回 404 表示连通、证书正常）：

   ```bash
   curl -sS -o /dev/null -w '%{http_code}\n' --max-time 10 https://IP:2096/
   ```

   超时说明用户当前网络到这个 IP 不通，见 troubleshooting 的"国内连不上"。

4. 用简短的话告诉用户：
   - 以后用 `ssh 名称` 登录；
   - 登录信息文件的路径（让用户自己打开，你不要读出来）；
   - 电脑装 Clash Verge Rev，导入文件里的 **Clash 订阅**，选"规则"模式并打开"虚拟网卡模式"（TUN，第一次按提示安装服务；只开系统代理时，浏览器的 WebRTC 会暴露真实 IP）；iPhone 用 Shadowrocket 导入 **Shadowrocket 订阅**；路由器 OpenClash 用 Clash 订阅；
   - CLIProxyAPI 现在是空的，要在管理中心添加自己的上游账号或供应商 Key；
   - 导入后打开 <https://ip.net.coffee/claude/>，显示服务器的 IP 就说明通了；重点看有没有泄露（DNS 出口不在中国、WebRTC 的 UDP 出口是服务器 IP），其次看「Claude AI 信任评分」，低于 70 分可以发邮件给服务商（比如搬瓦工）退掉这台、重新买一台，部署后再测，到 70 分以上就行，邮件模板在 <https://vps.xiaoxiaodong.ai/howto/refund-rebuy/>（不要说成「换 IP」，也不要说机房 IP 不会是满分）；要出差的话，出发前在手机和电脑上都测一遍。
   - 每个客户端怎么装、怎么检查泄露、AI 接口怎么用，都有图文教程：<https://vps.xiaoxiaodong.ai>（备用 <https://nevertoday.github.io/xiaoxiaodong-vps/>）。

## 以后的复核和维护

用户说"帮我检查一下 ssh 名称 这台服务器"时：先 `bash "$R" 名称 upload`，再 `bash "$R" 名称 verify --full`，只读复核，有问题再按对应阶段修。

- CLIProxyAPI 和管理中心每 30 分钟自动检查新版：SHA-256 校验 → 等到没有在途请求的空闲时刻（最多推迟 24 小时）→ 原子替换并重启（约 1 秒）→ 健康检查 → 失败自动回滚，同一坏版本 24 小时内不重试。日志：`journalctl -u cliproxy-auto-update`。
- 3x-ui 和 Xray **不自动升级**。
- 用户说检测网站提示 **WebRTC 泄露**、显示国内 IP：这是客户端只开了系统代理造成的，服务器和订阅都不用改。按仓库里的 `docs/Clash-Verge-WebRTC泄露修复手册.md`（<https://github.com/nevertoday/xiaoxiaodong-vps/blob/main/docs/Clash-Verge-WebRTC泄露修复手册.md>）一步步带用户修。只用虚拟网卡模式，不要禁用或限制 WebRTC。
- 服务器上的工具副本在 `/opt/xxd-vps/tool/`，命令 `xxd-vps verify` / `xxd-vps backup` 可直接在服务器上运行。
