// 最终检查清单：每一项做到了就点亮，安心度 = 点亮的项数 × 10。顺序就是页面顺序和安心度刻度条的顺序。
// short：「还差」里显示的短名；hint：一句补充（可省）；href：教程里讲这件事的页面（站内路径，可省）。
export const CHECK_GROUPS = [
  { id: "line", title: "服务器和线路", en: { title: "Server and connection" }, items: [
    { id: "cn-optimized", text: "买的是针对中国线路优化的服务器", short: "线路优化", hint: "比如洛杉矶 CN2 GIA 机房。", href: "/guide/2-buy-server/",
      en: { text: "My server is on a route optimized for China", short: "Optimized route", hint: "For example a Los Angeles CN2 GIA data center." } },
    { id: "same-server", text: "用的是和我同款的推荐服务器", short: "同款服务器", hint: "搬瓦工或 DMIT。", href: "/guide/2-buy-server/",
      en: { text: "My server is the one I recommend — the same one I use", short: "Same server", hint: "BandwagonHost or DMIT." } },
    { id: "dns", text: "没有 DNS 泄露", short: "DNS 泄露", href: "/howto/dns-leak/",
      en: { text: "No DNS leak", short: "DNS leak" } },
    { id: "udp", text: "没有 UDP 泄露", short: "UDP 泄露", hint: "检测网站上叫「WebRTC UDP 泄露检测」。", href: "/howto/webrtc-leak/",
      en: { text: "No UDP leak", short: "UDP leak", hint: "On the test site it is called \"WebRTC UDP leak test\"." } },
  ]},
  { id: "computer", title: "电脑设置", en: { title: "Your computer" }, items: [
    { id: "timezone", text: "电脑时区改成了服务器所在地", short: "时区", hint: "服务器在洛杉矶，就改成洛杉矶。",
      en: { text: "My computer's time zone matches the server's location", short: "Time zone", hint: "Server in Los Angeles? Set Los Angeles." } },
    { id: "language", text: "浏览器的第一语言是英语", short: "浏览器语言",
      en: { text: "My browser's first language is English", short: "Browser language" } },
    { id: "desktop-only", text: "不用手机版，只用电脑版", short: "只用电脑版", href: "/faq/#asked-12",
      en: { text: "No mobile apps — desktop only", short: "Desktop only" } },
  ]},
  { id: "account", title: "账号和付款", en: { title: "Accounts and payment" }, items: [
    { id: "new-network", text: "账号是在这个新网络下注册的", short: "新网络注册", href: "/howto/gmail/",
      en: { text: "My accounts were created on this new network", short: "Signed up here" } },
    { id: "own-money", text: "钱是自己买的礼品卡或自己充值的，没经过他人之手", short: "钱没经他人之手", href: "/howto/payment/",
      en: { text: "I paid with gift cards I bought or money I topped up myself — nobody else handled it", short: "My own money" } },
    { id: "not-shared", text: "这个网络只自己独享，没有对外分享", short: "独享网络",
      en: { text: "I keep this network to myself and don't share it", short: "Not shared" } },
  ]},
];
