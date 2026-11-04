# XXD VPS

[中文](./README.md) · **English** · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

Travelling to a country where the internet is hard to use? Keep using the websites and AI tools you rely on.

Step-by-step tutorial website: <https://vps.xiaoxiaodong.ai/en/> (Chinese version: <https://vps.xiaoxiaodong.ai>; mirror: <https://nevertoday.github.io/xiaoxiaodong-vps/en/>)

How it works: install Codex on your own computer, buy an overseas server, let Codex set it up remotely with this project, then import a subscription on your phone and computer. **You don't install anything on the server, and you don't log in to it.** The connection is yours alone, not shared with strangers.

## What you get

- **Your own connection** for your computer, phone and router. A main node and a backup node: if one fails, it switches to the other automatically.
- **Works right after import.** Routing rules for common websites and AI tools are already set. Websites in mainland China connect directly; everything else goes through your server.
- **CLIProxyAPI**: your own API endpoint and admin panel, updated to the latest version automatically.
  - ⚠️ **Don't connect a Claude account to CLIProxyAPI**: Anthropic's policy doesn't allow it. OpenAI has said ChatGPT accounts can be used this way — I personally love using it to make images.
- **Secure**: the server only accepts the key on your computer, and uses a proper HTTPS certificate, so browsers never warn "not secure".
- **Almost no upkeep**: certificates, rules and CLIProxyAPI update themselves, and the configuration is backed up every day.

## Four steps

### 1. Install Codex on your computer

Codex is OpenAI's AI app; you sign in with a paid ChatGPT plan. It goes on **your own computer**, not on the server.

- **Beginners**: install the desktop app. On Windows, search for **Codex** in the Microsoft Store and install it; on a Mac, download it from the [Codex website](https://openai.com/codex/). Open it and sign in with your ChatGPT account.
- **Experienced users**: use the [Codex](https://github.com/openai/codex) command line. Already installed? Run `codex` in your terminal and just talk to it.

No ChatGPT plan? Step 3 on the [tutorial website](https://vps.xiaoxiaodong.ai/en/guide/3-deploy/) has a "Type it yourself" route.

### 2. Buy a server

Right now, go with **BandwagonHost** — it's what I use myself.

I recommend this kind of server because of **lessons I paid for with real money and learned the hard way**: its routes are optimized for connections from mainland China, and it's so stable it turned me into a die-hard fan.

**[Buy BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=88&billingcycle=quarterly&configoption%5B17%5D=55)**

The plan in this link includes **2 TB of traffic per month** and 2 GB of RAM, in a Los Angeles CN2 GIA data center — more than enough for you and your family.

The ~~[1 TB plan](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)~~ I recommended before is out of stock and can't be ordered right now.

[DMIT](https://www.dmit.io/aff.php?aff=23544) is another one I really like using, but it's out of stock at the moment. No need to wait for it.

**Why only these two?** BandwagonHost and DMIT are the two I kept after a lot of testing, and the only ones I can recommend with confidence right now. The plan in the link above is also the only entry-level plan either of them has in stock at the moment. Many other providers look fine at first but are full of pitfalls: they work on ordinary days, then can't hold up when things get tense — connections drop or won't connect at all, and with AI services that can even put your account at risk. I've been burned by this so many times that I'm honestly worn out by it, so my advice is to buy here and skip the detours I went through.

> These are all my referral links. I may earn a commission if you buy through them, and I will use that income for charitable work. Prices and stock are as shown on the official sites.

Choose **Ubuntu 24.04** as the system. Once the server is ready, write down three things from the control panel: **server IP, root password (or key file) and SSH port**. On BandwagonHost, also note the **VEID and API key** (on the API page in KiwiVM's left menu — [how to find them](https://vps.xiaoxiaodong.ai/en/howto/traffic-and-ip/)) so the traffic your apps show matches the dashboard.

After buying, you don't log in to the server or install anything on it — the next step is Codex's job.

### 3. Let Codex set it up

Open Codex from step 1 (any other AI tool that can run commands on your computer works too). Copy the text below, fill it in and send it:

```text
Please set up my new server using the "XXD VPS" plan.

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
First download this project to my computer and read
skills/xiaoxiaodong-vps/SKILL.md in full. Follow its steps and rules
exactly, and use the project's scripts for setup and verification.
Please talk to me in English.

My server:
- IP:
- Login: initial password (let me type it myself; don't ask me to send it in the chat)
- SSH user and port: default
- Name I want to log in with: bwg
- BandwagonHost VEID and API Key (for official traffic usage; delete this line if it isn't BandwagonHost):
```

What to fill in:

- **IP**: the server IP from the control panel.
- **Login**: if your provider gave you a key file, change it to `key file: path to the file` (a zip is fine).
- **Name**: replace `bwg` with any name you like. Afterwards, typing `ssh that-name` logs you into the server.
- **BandwagonHost**: fill in the VEID and API key on the last line. Your apps then read the traffic quota, usage and reset day straight from BandwagonHost, so 1 TB and 2 TB plans both show correctly. **Not on BandwagonHost? Delete that line**; usage is then shown against 1000 GB a month.

If the user and port are not root / 22, replace "default" with the real values.

Then wait for the AI to finish, usually 10–20 minutes. At one point a password box pops up on your computer; type the server password into it once. **Never paste the password into the chat.** When setup is done, password login is turned off and only this computer can log in.

If the AI can't download the project, [download the ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) yourself, unzip it, and add a line to the text above: "The project is already at: folder path".

When it's done, a new file `my-server-your-name-subscriptions-and-accounts-en.md` appears on your desktop with:

- the **Clash subscription URL** for computer and router, and the **Shadowrocket subscription URL** for iPhone;
- the 3x-ui panel address, username and password;
- the CLIProxyAPI admin address, admin login key, API address and API key.

<details>
<summary>Set up servers often? Install it as a skill and call it in one sentence</summary>

Run once in a terminal:

```bash
git clone https://github.com/nevertoday/xiaoxiaodong-vps.git
mkdir -p ~/.claude/skills ~/.codex/skills
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.claude/skills/
cp -R xiaoxiaodong-vps/skills/xiaoxiaodong-vps ~/.codex/skills/
```

After that, just tell the AI "use xiaoxiaodong-vps to set up my new server" and it will ask you for the server details.

</details>

### 4. Import the subscription

- **Computer (Clash Verge Rev recommended)**: install [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), import the Clash subscription URL, choose **Rule** mode and turn on **TUN mode** (Virtual Network Interface; install the service when prompted). With System Proxy alone, the browser's WebRTC can reveal your real IP — see the [WebRTC leak fix guide](./docs/Clash-Verge-WebRTC泄露修复手册.md) (in Chinese, written so an AI assistant can follow it step by step).
- **iPhone**: import the Shadowrocket subscription URL in Shadowrocket.
- **Router (OpenClash)**: the same Clash subscription URL works, so every device at home uses the line. Add it under Config Subscribe (don't upload the YAML file, or the usage bar won't show and rules won't auto-update), turn off online subscription conversion, and use the Meta core.
- **Already using v2rayN (Windows / Mac / Linux)**: it works, but only as a fallback. Import the subscription URL from the "Shadowrocket (iPhone)" row (not the Clash row), pick the "bypass mainland China" routing, and turn on TUN against WebRTC leaks. That subscription has only the nodes — none of the AI routing or WeChat-direct rules — so Clash Verge Rev remains the recommended desktop app. See the [v2rayN guide](https://vps.xiaoxiaodong.ai/en/howto/v2rayn/).

Then open <https://ip.net.coffee/claude/>. If it shows your server's IP, you're connected. While you're there, check two things:

1. **Leaks first**: the DNS exit is not in China, and WebRTC's UDP exit is your server's IP (check on a computer).
2. **Then the Claude AI trust score**: if it's below 70, you can email your provider (for example BandwagonHost) to cancel this server, buy a new one, deploy it and test again. Once it's 70 or above, you're set. You can copy [these email templates](https://vps.xiaoxiaodong.ai/en/howto/refund-rebuy/).

## Before you travel

- **Set everything up and test it before you leave.** Once you're on a restricted network, downloading the project or even opening AI tools may get much harder.
- Install the clients and import the subscriptions on both phone and computer, and check that both nodes connect.
- The same server can feel faster or slower depending on where you are and which carrier you use. That's normal. If it won't connect somewhere, try another network first (hotel Wi-Fi, mobile data, another carrier). If none work, the IP is probably blocked there; your provider can give you a new one.
- Keep the connection to yourself and your family. Don't share it.

## Checking your server later

Send this to the AI (replace `bwg` with your name):

```text
Please check my server using the "XXD VPS" plan: ssh bwg

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
Download the project and read the "以后的复核和维护" (later checks and
maintenance) part of skills/xiaoxiaodong-vps/SKILL.md.
Only check first, tell me what failed and why, and fix things only after I agree.
Don't show passwords, subscription URLs or keys in the chat.
Please talk to me in English.
```

Detailed docs ([troubleshooting](./skills/xiaoxiaodong-vps/references/troubleshooting.md), [design notes](./skills/xiaoxiaodong-vps/references/design.md)) are currently in Chinese; your AI can read them for you.

## Feedback and suggestions

Have a suggestion, or found something unclear or not working as written? [Open an issue on GitHub](https://github.com/nevertoday/xiaoxiaodong-vps/issues), [message me on X](https://x.com/xiaoxiaodong) (@xiaoxiaodong), or add me (Xiaoxiaodong, 小小东) on WeChat. I'll add it to the guide.

<img src="https://vip.xiaoxiaodong.ai/site-assets/wechat-qr.png" width="160" alt="Xiaoxiaodong's WeChat QR code">

## Privacy

- This project contains no information about any real server.
- Every server's passwords, keys, subscription URLs and API keys are freshly generated during setup and stored only on the server and your own computer. The AI doesn't show them in the chat.
- Don't post your login file, subscription URLs or keys anywhere, and don't screenshot them.
- To report a security issue, see [SECURITY.md](./SECURITY.md).

## License

[MIT](./LICENSE)
