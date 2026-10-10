# XXD VPS

[中文](./README.md) · **English** · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [العربية](./README.ar.md) · [Español](./README.es.md) · [Français](./README.fr.md) · [Русский](./README.ru.md) · [Deutsch](./README.de.md) · [Português](./README.pt.md)

Travelling to a country where the internet is hard to use? Keep using the websites and AI tools you rely on.

How it works: buy your own overseas server, let an AI set it up with this project, then import a subscription on your phone and computer. The connection is yours alone, not shared with strangers.

## What you get

- **Your own connection** for your computer, phone and router. A main node and a backup node: if one fails, it switches to the other automatically.
- **Works right after import.** Routing rules for common websites and AI tools are already set. Websites in mainland China connect directly; everything else goes through your server.
- **CLIProxyAPI**: your own API endpoint and admin panel, updated to the latest version automatically.
- **Secure**: the server only accepts the key on your computer, and uses a proper HTTPS certificate, so browsers never warn "not secure".
- **Almost no upkeep**: certificates, rules and CLIProxyAPI update themselves, and the configuration is backed up every day.

## Three steps

### 1. Buy a server

Right now, go with **BandwagonHost**. The network is stable and it's what I use myself:

**[Buy BandwagonHost](https://bandwagonhost.com/aff.php?aff=83651&a=add&pid=87&billingcycle=quarterly&configoption%5B17%5D=55)**

[DMIT](https://www.dmit.io/aff.php?aff=23544) is also good, but it's out of stock at the moment. No need to wait for it.

> Both are my referral links. I may earn a commission if you buy through them, and I will use that income for charitable work. Prices and stock are as shown on the official sites.

Choose **Ubuntu 24.04** as the system. Once the server is ready, write down three things from the control panel: **server IP, root password (or key file) and SSH port**.

### 2. Let an AI set it up

Open an AI tool that can run commands on your computer, such as [Codex](https://github.com/openai/codex) or [Claude Code](https://claude.com/claude-code) (on Windows, use it inside WSL). Copy the text below, fill it in and send it:

```text
Please set up my new server using the "XXD VPS" plan.

Plan: https://github.com/nevertoday/xiaoxiaodong-vps
First download this project to my computer and read
skills/xiaoxiaodong-vps/SKILL.md in full. Follow its steps and rules
exactly, and use the project's scripts for setup and verification.
Please talk to me in English.

My server:
- IP:
- Login: initial password (let me type it into the terminal myself)
- SSH user and port: default
- Name I want to log in with: bwg
```

You only need to change three things:

- **IP**: the server IP from the control panel.
- **Login**: if your provider gave you a key file, change it to `key file: path to the file` (a zip is fine).
- **Name**: replace `bwg` with any name you like. Afterwards, typing `ssh that-name` logs you into the server.

If the user and port are not root / 22, replace "default" with the real values.

Then wait for the AI to finish, usually 10–20 minutes. At one point it will ask you to type the server password into the terminal. **Never paste the password into the chat.** When setup is done, password login is turned off and only this computer can log in.

If the AI can't download the project, [download the ZIP](https://github.com/nevertoday/xiaoxiaodong-vps/archive/refs/heads/main.zip) yourself, unzip it, and add a line to the text above: "The project is already at: folder path".

When it's done, a new file `XXD-VPS-your-name-login-en.md` appears on your desktop with:

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

### 3. Import the subscription

- **Computer**: install [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev/releases), import the Clash subscription URL, choose **Rule** mode and turn on **System Proxy**.
- **iPhone**: import the Shadowrocket subscription URL in Shadowrocket.
- **Router**: import the Clash subscription URL in OpenClash.

Then open <https://ipinfo.io>. If it shows your server's IP, you're connected.

## Before you travel

- **Set everything up and test it before you leave.** Once you're on a restricted network, downloading the project or even opening AI tools may get much harder.
- Install the clients and import the subscriptions on both phone and computer, and check that both nodes connect.
- If some local network can't reach your server, try another one first (hotel Wi-Fi, mobile data, another carrier). If none work, the server's IP is probably blocked there. No configuration change will fix that; ask your provider for a new IP.
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

## Privacy

- This project contains no information about any real server.
- Every server's passwords, keys, subscription URLs and API keys are freshly generated during setup and stored only on the server and your own computer. The AI doesn't show them in the chat.
- Don't post your login file, subscription URLs or keys anywhere, and don't screenshot them.
- To report a security issue, see [SECURITY.md](./SECURITY.md).

Whether you can connect, and how fast, also depends on the local network and the server's routing. This project makes sure the server is configured correctly. It can't guarantee that one IP is reachable from every country and every carrier.

## License

[MIT](./LICENSE)
