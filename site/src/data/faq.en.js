// English FAQ: same groups and order as faq.js.
export const FAQ_EN = [
  { id: "cost", title: "Costs", items: [
    ["How much does it cost in total?", "Only the server is a required cost, paid quarterly or yearly — check the provider's site for prices. Clash Verge Rev on computers is free; Shadowrocket on iPhone is a one-off purchase of about US$3 on the US App Store. Certificates, rules and the AI API software are all free, and you don't need a domain."],
    ["What happens when I run out of traffic?", "Most providers throttle or pause the server until the next reset day. A few hundred GB to 1 TB a month is usually plenty for a household; the recommended BandwagonHost plan has 2 TB a month. Apps show usage against 1 TB a month by default, with the reset day worked out from when the server was provisioned; if your plan differs, tell AI the real quota and reset day."],
    ["What if the server expires without renewal?", "The provider suspends it, then deletes it after a while — and the IP is taken back, so you'd have to buy and set up again. Turn on auto-renew in the provider's dashboard or put the expiry date in your calendar."],
    ["Can I get a refund?", "It depends on the provider; many only refund within a short period after purchase. Check before buying."],
  ]},
  { id: "safe", title: "Security and privacy", items: [
    ["Can the provider see what I do?", "Most sites you visit use HTTPS, so the provider can't see page contents, but it can see traffic volume and which addresses you connect to. Choose a reputable provider and don't use it for anything illegal."],
    ["If AI configures it, could my passwords leak?", "The setup forbids the AI from showing passwords, subscription URLs or keys in chat; login info is only written to a file on your own computer. Once set up, the server only accepts your computer's key, and passwords can no longer be used to log in remotely."],
    ["I lost the login-info file. What now?", "As long as `ssh your-name` still logs you in, ask AI to export it again (the skill's `save` step). If the computer is gone too, log in through the provider's rescue console and ask AI to help you recover."],
    ["Someone else learned my subscription URL. What now?", "They can use your line. Ask AI to give you a new subscription URL (the subscription ID on the server and your local login-info file must change together); the old one stops working. Then re-import on your own devices."],
    ["Is it safe to share with family?", "Yes — import the same subscription URL on their devices. Don't share it beyond your family."],
  ]},
  { id: "speed", title: "Speed and stability", items: [
    ["Why is it slower in the evening?", "From 8 to 11 pm, routes from China abroad are most congested — like rush hour. The server's bandwidth is rarely the bottleneck. If it matters a lot, choose a plan with a better route."],
    ["It suddenly stopped connecting. What should I do?", "First try another network (mobile data, other Wi-Fi). Still nothing? Have AI health-check the server. If the server is fine but it still won't connect where you are, the IP is probably blocked in mainland China. BandwagonHost and DMIT can both change it (usually for a fee; when it's free is in the How-to \"IP blocked in China\"). Afterwards, reinstall the OS and set the server up again."],
    ["If the main node fails, does it switch to the backup?", "Yes. The subscription's \"auto switch\" group tests regularly and moves to the backup node when the main one is down. You can also pick one manually."],
    ["The speed test is low. Is the server bad?", "Not necessarily. The test site, the time of day and your home Wi-Fi all affect results. See the how-to \"Run and read a speed test\"."],
  ]},
  { id: "account", title: "AI accounts", items: [
    ["Will my AI account get banned with this setup?", "Nobody can guarantee anything. To lower the risk: stick to the same server, don't hop between nodes in different countries, set your computer's time zone to the server's location, and follow each AI service's terms of use."],
    ["A site says mine is a data-center IP and wants verification. Normal?", "Yes. Your own server is still a data-center IP, so a few sites ask for one extra verification step. Just complete it."],
    ["Does CLIProxyAPI give me free AI?", "No. It only turns your own AI accounts into an API; quota and costs are still your account's."],
  ]},
  { id: "device", title: "Devices and usage", items: [
    ["How many devices can use one subscription?", "There is no hard limit — your and your family's phones, computers and tablets can all be connected at once. More devices use traffic faster."],
    ["Which mode should Clash Verge use on a computer?", "Choose \"Rule\" mode and turn on \"Tun Mode\". Don't use \"Global\" — Chinese sites would take a detour abroad too."],
    ["Can Windows and Mac use the same setup?", "Yes — import the same Clash subscription and use the same settings. But check each computer carefully: Rule mode with Tun Mode on (service installed); on Windows, Strict Route on too; DNS Overwrite off on both; set the IPv6 switch after checking each computer's current network — the two may differ; finally fully restart the browser and test for leaks on each. See the how-to \"Turn on TUN mode\"."],
    ["I already have Gmail. Can I switch to a new address?", "Yes. In your Google Account open Personal info → Email → Google Account email (or go straight to myaccount.google.com/google-account-email). Eligible accounts can change to a new @gmail.com address — once a year, up to three times; the old address becomes an alias that still receives mail, and your data stays in the same account. It changes the address rather than adding a second mailbox; if you need a separate mailbox, create a new account. See the how-to “Change your Gmail address”."],
    ["I can't sign in to Google abroad / no SMS codes?", "Abroad or on a new IP, Google often asks for extra verification, and relying only on SMS to a home number easily gets you stuck. Before leaving, set up a passkey or an authenticator on the Google Account Security page and save your backup codes. See the how-to “Secure your Google account”."],
    ["I can't find Shadowrocket on the China App Store.", "It isn't listed there. Download it from another region's App Store (for example the US) with a non-China Apple ID — see the how-to \"Create a non-China Apple ID\"."],
  ]},
  { id: "tech", title: "Technical", items: [
    ["Can I do everything manually, without AI?", "Yes. Step 3 has a \"Type it yourself\" route with every command listed. The commands run in your own computer's terminal: on a Mac use the built-in Terminal; on Windows install Git for Windows and use its Git Bash."],
    ["Can I install other things on the server?", "Yes, but avoid the ports this setup uses (22, 80, 443, 2443, 2096, 8318, 53998) and allow the new service's port in the firewall. Ask AI first whether it might conflict."],
    ["Why don't 3x-ui and Xray auto-update?", "A newer Xray once stopped Shadowrocket from connecting, so the versions are pinned and only upgraded after checking compatibility with every app. CLIProxyAPI, certificates and rules do update automatically."],
  ]},
];
