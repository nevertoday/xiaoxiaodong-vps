// 站点结构的唯一来源：左侧导航、首页路线图、上一步 / 下一步、How-to 目录、搜索都从这里读。
// ready: false 的页面还没写，导航里显示「编写中」，不给链接。

const BASE = (import.meta.env.BASE_URL || "/").replace(/\/$/, "");
/** 当前页面的语言：/en/ 下是英文，其余是中文 */
export const langOf = (pathname) => (pathname.slice(BASE.length).startsWith("/en/") || pathname.slice(BASE.length) === "/en" ? "en" : "zh");
/** 站内链接：部署在子路径（GitHub Pages 备用地址）时自动加前缀；英文页加 /en */
export const link = (path, lang = "zh") => `${BASE}${lang === "en" ? "/en" : ""}${path}`;
/** 同一页的另一种语言 */
export const counterpart = (pathname) => {
  const p = pathname.slice(BASE.length) || "/";
  return BASE + (p.startsWith("/en/") || p === "/en" ? p.replace(/^\/en/, "") || "/" : "/en" + p);
};
/** 取某个对象在当前语言下的字段：en 时优先 x.en[key] */
export const t = (x, key, lang) => (lang === "en" && x.en && x.en[key] !== undefined ? x.en[key] : x[key]);

export const STEPS = [
  { n: 0, slug: "0-prepare", title: "准备", minutes: "读 10 分钟", ready: true, sum: "需要什么、花多少钱、要多久", en: { title: "Get ready", minutes: "10-minute read", sum: "What you need, what it costs, how long it takes" } },
  { n: 1, slug: "1-ai-assistant", title: "在电脑上装 Codex", minutes: "10 分钟", ready: true, sum: "在你自己的电脑上装 Codex，登录后测一句；没有 ChatGPT 账号也能走手动路线", en: { title: "Set up an AI assistant", minutes: "15 minutes", sum: "Test whether your AI can run commands; if not, install Claude Code or Codex — or take the manual route" } },
  { n: 2, slug: "2-buy-server", title: "买服务器", minutes: "20–30 分钟", ready: true, sum: "选商家和套餐，系统选 Ubuntu，记下 IP 和密码；服务器上什么都不用装", en: { title: "Buy a server", minutes: "20–30 minutes", sum: "Pick a provider and plan, choose Ubuntu, note the IP and password" } },
  { n: 3, slug: "3-deploy", title: "配置服务器", minutes: "约 10 分钟", ready: true, sum: "把信息发给电脑上的 AI，它远程配好；或者自己照着敲命令", en: { title: "Configure the server", minutes: "About 10 minutes", sum: "Let AI do it, or type the commands yourself" } },
  { n: 4, slug: "4-clients", title: "装客户端", minutes: "10 分钟", ready: true, sum: "电脑 Clash Verge、iPhone Shadowrocket、安卓、路由器", en: { title: "Install the apps", minutes: "10 minutes", sum: "Clash Verge on computers, Shadowrocket on iPhone, Android, routers" } },
  { n: 5, slug: "5-verify", title: "检查通没通", minutes: "5 分钟", ready: true, sum: "看出口 IP，查 DNS 和 WebRTC 泄露", en: { title: "Check it works", minutes: "5 minutes", sum: "Check your exit IP, DNS leaks and WebRTC leaks" } },
  { n: 6, slug: "6-ai-api", title: "用自己的 AI 接口", minutes: "15 分钟", ready: true, sum: "CLIProxyAPI 是什么、怎么加账号、怎么接到工具里", en: { title: "Use your own AI API", minutes: "15 minutes", sum: "What CLIProxyAPI is, adding accounts, connecting tools" } },
  { n: 7, slug: "7-daily", title: "日常使用和维护", minutes: "随用随看", ready: true, sum: "体检服务器、出差前检查、流量和续费", en: { title: "Everyday use and upkeep", minutes: "Whenever needed", sum: "Health checks, before you travel, traffic and renewals" } },
];
export const stepHref = (s, lang = "zh") => link(`/guide/${s.slug}/`, lang);

export const HOWTO = [
  { group: "账号和付款", en: { group: "Accounts and payment" }, items: [
    { slug: "gmail", title: "注册 Google 邮箱（Gmail）", en: { title: "Create a Google account (Gmail)" } },
    { slug: "gmail-change-address", title: "更换 Gmail 地址", en: { title: "Change your Gmail address" } },
    { slug: "google-account-security", title: "Google 账号安全设置", en: { title: "Secure your Google account" } },
    { slug: "apple-id", title: "注册境外 Apple ID", en: { title: "Create a non-China Apple ID" } },
    { slug: "apple-gift-card", title: "用礼品卡给美区 Apple ID 充值", en: { title: "Top up a US Apple ID with a gift card" } },
    { slug: "apple-paypal", title: "注册 PayPal 并绑定美区 Apple ID", en: { title: "Open PayPal and link it to a US Apple ID" } },
    { slug: "github", title: "注册 GitHub", en: { title: "Create a GitHub account" } },
    { slug: "payment", title: "在国外网站付款", en: { title: "Paying on overseas websites" } },
    { slug: "google-payment-card", title: "给 Google 账号绑定付款卡", en: { title: "Add a payment card to your Google account" } },
    { slug: "claude-app-store", title: "在 iPhone 上订阅 Claude（App Store）", en: { title: "Subscribe to Claude on iPhone (App Store)" } },
    { slug: "claude-google-play", title: "在安卓上订阅 Claude（Google Play）", en: { title: "Subscribe to Claude on Android (Google Play)" } },
  ]},
  { group: "服务器", en: { group: "Server" }, items: [
    { slug: "buy-bandwagonhost", title: "在搬瓦工买服务器", en: { title: "Buy a server from BandwagonHost" } },
    { slug: "buy-dmit", title: "在 DMIT 买服务器", en: { title: "Buy a server from DMIT" } },
    { slug: "reinstall-os", title: "后台重装系统为 Ubuntu", en: { title: "Reinstall the OS as Ubuntu" } },
    { slug: "root-password-vnc", title: "后台改 root 密码、用救援控制台", en: { title: "Change the root password and use the rescue console" } },
    { slug: "traffic-and-ip", title: "查看流量", en: { title: "Check traffic" } },
    { slug: "ip-blocked", title: "IP 被墙了怎么办", en: { title: "IP blocked in China" } },
    { slug: "refund-rebuy", title: "退掉服务器、重新买一台", en: { title: "Refund a server and buy a new one" } },
  ]},
  { group: "AI 工具", en: { group: "AI tools" }, items: [
    { slug: "install-codex", title: "安装 Codex 命令行版", en: { title: "Install the Codex CLI" } },
    { slug: "install-skill", title: "安装 xiaoxiaodong-vps skill", en: { title: "Install the xiaoxiaodong-vps skill" } },
    { slug: "ai-health-check", title: "让 AI 给服务器体检", en: { title: "Have AI health-check your server" } },
  ]},
  { group: "客户端", en: { group: "Apps" }, items: [
    { slug: "clash-verge-windows", title: "Clash Verge Rev（Windows）", en: { title: "Clash Verge Rev (Windows)" } },
    { slug: "clash-verge-mac", title: "Clash Verge Rev（Mac）", en: { title: "Clash Verge Rev (Mac)" } },
    { slug: "clash-verge-tun", title: "打开虚拟网卡模式（TUN）", en: { title: "Turn on TUN mode" } },
    { slug: "shadowrocket", title: "Shadowrocket（iPhone、iPad）", en: { title: "Shadowrocket (iPhone, iPad)" } },
    { slug: "android", title: "安卓客户端", en: { title: "Android apps" } },
    { slug: "v2rayn", title: "v2rayN（备选，电脑）", en: { title: "v2rayN (alternative, desktop)" } },
    { slug: "openclash", title: "OpenClash 路由器（进阶）", en: { title: "OpenClash on a router (advanced)" } },
  ]},
  { group: "检测", en: { group: "Checks" }, items: [
    { slug: "check-ip", title: "看出口 IP", en: { title: "Check your exit IP" } },
    { slug: "dns-leak", title: "查 DNS 泄露", en: { title: "Check for DNS leaks" } },
    { slug: "webrtc-leak", title: "查 WebRTC 泄露", en: { title: "Check for WebRTC leaks" } },
    { slug: "speed-test", title: "测速和看懂结果", en: { title: "Run and read a speed test" } },
  ]},
  { group: "AI 接口", en: { group: "AI API" }, items: [
    { slug: "cpa-login", title: "登录 CLIProxyAPI 管理中心", en: { title: "Log in to the CLIProxyAPI management center" } },
    { slug: "cpa-add-account", title: "给 CLIProxyAPI 添加账号", en: { title: "Add accounts to CLIProxyAPI" } },
    { slug: "cpa-clients", title: "把 AI 接口接到工具里", en: { title: "Connect your AI API to tools" } },
  ]},
  { group: "出行", en: { group: "Travel" }, items: [
    { slug: "travel-checklist", title: "出差前检查清单", en: { title: "Before-you-travel checklist" } },
  ]},
];
export const howtoHref = (slug, lang = "zh") => link(`/howto/${slug}/`, lang);
export const HOWTO_FLAT = HOWTO.flatMap((g) => g.items.map((i) => ({ ...i, group: g.group, groupEn: g.en.group })));

export const wikiHref = (slug, lang = "zh") => link(`/wiki/${slug}/`, lang);

// 正文里虚线标出的术语：悬停看一句话解释（Term 组件）。wiki: 对应的 Wiki 条目
export const GLOSSARY = {
  VPS: { tip: "在机房里租的一台虚拟电脑，24 小时开着，有自己的公网 IP。", wiki: "vps", en: "A virtual computer you rent in a data center. It runs 24/7 and has its own public IP." },
  "公网 IP": { tip: "互联网上的门牌号。别人要找到你的服务器，靠的就是它。", wiki: "ip", en: "Your address on the internet. Anyone who wants to reach your server uses it." },
  机房: { tip: "服务器放在哪座城市。离你越近、线路越好，延迟越低。", wiki: "vps", en: "The city your server lives in. Closer and better-connected means lower latency." },
  线路: { tip: "你家到机房走的那条「高速公路」。同一个机房，不同线路晚上的速度能差好几倍。", wiki: "vps", en: "The \"highway\" between you and the data center. The same data center can be several times slower at night on a worse route." },
  Ubuntu: { tip: "一种免费的 Linux 系统。这套方案只支持 Ubuntu 22.04 以上和 Debian 12 以上。", wiki: "vps", en: "A free Linux system. This setup supports Ubuntu 22.04+ and Debian 12+ only." },
  root: { tip: "Linux 的管理员账号，权限最大。买服务器后，商家会给你它的密码。", wiki: "ssh", en: "The Linux administrator account. Your provider gives you its password when you buy a server." },
  SSH: { tip: "远程登录服务器的方式。你（或 AI）用它在服务器上执行命令。", wiki: "ssh", en: "The way to log in to a server remotely and run commands — by you or by an AI assistant." },
  密钥: { tip: "一对文件：私钥留在你电脑上，公钥放在服务器上，对得上才能登录，比密码安全得多。", wiki: "ssh", en: "A pair of files: the private key stays on your computer, the public key goes on the server. Far safer than a password." },
  端口: { tip: "一台服务器上的不同「房间号」。SSH 默认是 22。", wiki: "port", en: "Numbered \"rooms\" on one server. SSH uses 22 by default." },
  NAT: { tip: "多台机器共用一个公网 IP，每台只分到几个端口。这套方案不能用 NAT 机器。", wiki: "ip", en: "Several machines share one public IP and each gets only a few ports. This setup cannot run on NAT machines." },
  KVM: { tip: "一种虚拟化方式，给你一台完整的独立系统。买的时候选 KVM。", wiki: "vps", en: "A virtualization type that gives you a complete, independent system. Choose KVM when buying." },
  订阅: { tip: "一个网址，客户端打开它就能拿到节点和分流规则，以后会自动更新。", wiki: "subscription", en: "A URL your app opens to fetch the nodes and routing rules. It updates itself later." },
  节点: { tip: "你的电脑连到服务器的那条加密通道。", wiki: "proxy", en: "The encrypted tunnel from your device to your server." },
  终端: { tip: "一个只能打字的窗口，用来输入命令。Mac 叫「终端」，Windows 有 PowerShell。", wiki: "ssh", en: "A text-only window for typing commands. On Mac it is Terminal; on Windows, PowerShell or WSL." },
  WSL: { tip: "Windows 里自带的一套 Linux 环境。这套教程用不到它；已经在用的照常用就行。", wiki: "vps", en: "A Linux environment built into Windows. This setup's scripts run inside it." },
  证书: { tip: "证明「这个网站确实是它自称的那个」的电子文件。有了它，浏览器才显示安全的小锁。", wiki: "https", en: "An electronic document proving a site is who it claims to be. It is what gives browsers the padlock." },
  分流: { tip: "按规则决定每个网站怎么走：国内的直接访问，国外和 AI 工具走你的服务器。", wiki: "routing", en: "Rules that decide how each site is reached: Chinese sites go direct; foreign sites and AI tools go through your server." },
  虚拟网卡: { tip: "TUN 模式：让电脑上所有软件的流量都先经过 Clash，包括浏览器的 WebRTC。", wiki: "tun", en: "TUN mode: every app's traffic passes through Clash first — including the browser's WebRTC." },
  "DNS 泄露": { tip: "你访问的网站名被交给本地网络去查，别人由此知道你在哪、在看什么。", wiki: "dns-leak", en: "The names of sites you visit get looked up by your local network, revealing where you are and what you browse." },
  WebRTC: { tip: "浏览器自带的视频通话功能，会向外报告你的 IP。", wiki: "webrtc", en: "The browser's built-in video-call feature. It reports your IP to websites." },
  "API Key": { tip: "调用接口时出示的「门禁卡」，谁拿到谁就能用，要保密。", wiki: "api", en: "The \"key card\" you show when calling an API. Whoever holds it can use it — keep it secret." },
  CLIProxyAPI: { tip: "装在你服务器上的一个程序：把你的 AI 账号变成一个接口，给各种 AI 工具用。", wiki: "cliproxyapi", en: "A program on your server that turns your own AI accounts into an API for all kinds of AI tools." },
};
