// README 顶部的教程入口卡：每种语言 × 浅色/深色 × 宽版（电脑）/窄版（手机）共 4 张动画 SVG。
// 改文案或样式后运行：node docs/readme/build-buttons.mjs
// 动画是 SVG 内的 CSS（GitHub 的 <img> 里能播放）；系统开了「减少动态效果」时直接显示完成状态。
// README 里用 <picture> 按 max-width: 600px 切窄版，<img width="100%"> 铺满正文宽度。
import { writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const FONT = `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans','Apple SD Gothic Neo','Malgun Gothic','Microsoft YaHei','Noto Sans CJK SC','Noto Sans Arabic','Noto Sans',Helvetica,Arial,sans-serif`;
const EN = "vps.xiaoxiaodong.ai/en";
// steps 的第 5 项（下标 VERIFY）是核验，上方挂「别跳过」标签
const VERIFY = 4;
export const LANGS = {
  zh: { eyebrow: "免费图文教程 · 零基础 · 每步有截图 · 第一次约 1 小时", title: "跟着教程学，搭好还要验好", steps: ["装 Codex", "买服务器", "AI 远程配置", "导入订阅", "逐项核验", "放心用"], tag: "别跳过", cta: "开始学习", ctaSub: "从第 1 步开始", host: "vps.xiaoxiaodong.ai" },
  en: { eyebrow: "Free illustrated guide · For beginners · Screenshots at every step · ~1 hour", title: "Learn step by step: set up, then verify", steps: ["Get Codex", "Buy server", "AI setup", "Import", "Verify", "Use it"], tag: "Don’t skip", cta: "Start learning", ctaSub: "Begin at step 1", host: EN },
  ko: { eyebrow: "무료 그림 가이드 · 초보자 OK · 단계마다 스크린샷 · 처음엔 약 1시간", title: "따라 배우기: 설정하고, 꼭 검증까지", steps: ["Codex 설치", "서버 구매", "AI가 설정", "구독 추가", "꼼꼼히 검증", "안심 사용"], tag: "필수", cta: "배우기 시작", ctaSub: "1단계부터", host: EN },
  ja: { eyebrow: "無料の図解ガイド · 初心者OK · 全ステップに画面付き · 初回は約1時間", title: "手順どおりに学ぶ：設定して、必ず検証", steps: ["Codex導入", "サーバー購入", "AIが設定", "取り込み", "検証", "利用開始"], tag: "必須", cta: "学習を始める", ctaSub: "ステップ1から", host: EN },
  ar: { eyebrow: "دليل مصوّر مجاني · للمبتدئين · صور لكل خطوة · نحو ساعة", title: "تعلّم خطوة بخطوة: أعِدّ ثم تحقّق", steps: ["ثبّت Codex", "اشترِ خادمًا", "الإعداد الآلي", "الاستيراد", "التحقّق", "الاستخدام"], tag: "لا تتخطَّها", cta: "ابدأ التعلّم", ctaSub: "من الخطوة 1", host: EN, rtl: true },
  es: { eyebrow: "Guía ilustrada gratis · Para principiantes · Capturas en cada paso · ~1 hora", title: "Aprende paso a paso: configura y verifica", steps: ["Codex", "Servidor", "IA configura", "Importar", "Verificar", "¡A usar!"], tag: "No lo saltes", cta: "Empieza a aprender", ctaSub: "Desde el paso 1", host: EN },
  fr: { eyebrow: "Guide illustré gratuit · Pour débutants · Captures à chaque étape · ~1 heure", title: "Apprenez pas à pas : installez, puis vérifiez", steps: ["Codex", "Serveur", "Config. IA", "Importer", "Vérifier", "Utiliser"], tag: "À ne pas sauter", cta: "Commencer", ctaSub: "Dès l’étape 1", host: EN },
  ru: { eyebrow: "Бесплатно · Для новичков · Скриншоты на каждом шаге · ~1 час", title: "Учитесь по шагам: настройте и проверьте", steps: ["Codex", "Сервер", "Настройка", "Импорт", "Проверка", "Готово"], tag: "Не пропускайте", cta: "Начать обучение", ctaSub: "С шага 1", host: EN },
  de: { eyebrow: "Kostenlose Bildanleitung · Für Einsteiger · Screenshots zu jedem Schritt · ~1 Stunde", title: "Schritt für Schritt: einrichten, dann prüfen", steps: ["Codex", "Server", "KI-Setup", "Import", "Prüfen", "Loslegen"], tag: "Nicht überspringen", cta: "Jetzt lernen", ctaSub: "Ab Schritt 1", host: EN },
  pt: { eyebrow: "Guia ilustrado grátis · Para iniciantes · Capturas em cada passo · ~1 hora", title: "Aprenda passo a passo: configure e verifique", steps: ["Codex", "Servidor", "IA configura", "Importar", "Verificar", "Pronto"], tag: "Não pule", cta: "Começar a aprender", ctaSub: "Do passo 1", host: EN },
};
const THEMES = {
  light: { bg: "#111111", fg: "#ffffff", ctaBg: "#ffffff", ctaFg: "#111111" }, // GitHub 浅色主题下：深色卡片
  dark: { bg: "#f3f0ea", fg: "#171612", ctaBg: "#171612", ctaFg: "#f3f0ea" },  // GitHub 深色主题下：浅色卡片
};
const DUR = 8, FILL = 0.62; // 进度线在每轮前 62% 走完，停到 92% 后重来

// 两种版式。所有坐标按从左到右写，阿拉伯语整体镜像。
const LAYOUTS = {
  wide: { W: 880, H: 212, P: 32, eyebrow: [58, 14], title: [98, 30], ty: 148, label: 14, labelDy: 30,
    cta: { x: 880 - 32 - 216, y: 32, w: 216, h: 212 - 64, main: [62, 24], sub: [88, 13], host: [212 - 64 - 24, 12], arrowY: 212 - 64 - 28, arrowRight: true },
    track: (W, P, cta) => [P + 34, cta.x - 54] },
  narrow: { W: 480, H: 316, P: 24, eyebrow: [46, 13], title: [82, 24], ty: 140, label: 12.5, labelDy: 26,
    cta: { x: 24, y: 208, w: 432, h: 84, main: [38, 22], sub: [62, 12.5], host: null, arrowY: 42, arrowRight: true },
    track: (W, P) => [P + 30, W - P - 30] },
};

// 粗略估算文字宽度（em），用来在超宽时缩小字号
function em(s) {
  let w = 0;
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (c >= 0x3000) w += 1;
    else if (c >= 0x0600 && c <= 0x06ff) w += 0.5;
    else if (ch === " ") w += 0.28;
    else if (/[A-ZА-ЯЁ0-9]/.test(ch)) w += 0.64;
    else if (/[.,·’'ilIjt:;!|]/.test(ch)) w += 0.3;
    else w += 0.53;
  }
  return w;
}
const fit = (s, base, avail, bold) => +Math.min(base, avail / (em(s) * (bold ? 1.1 : 1.04))).toFixed(1);

function svg(s, c, Lk) {
  const L = LAYOUTS[Lk], { W, H, P } = L, rtl = !!s.rtl, n = s.steps.length;
  const mx = (x) => (rtl ? W - x : x); // 镜像
  const C = L.cta;
  const ctaX = rtl ? W - C.x - C.w : C.x;
  const textRight = Lk === "wide" ? C.x - 40 : W - P, avail = textRight - P;
  const [ta, tb] = L.track(W, P, C);
  const xs = s.steps.map((_, i) => mx(ta + (tb - ta) * i / (n - 1)));
  const gap = (tb - ta) / (n - 1), len = tb - ta, ty = L.ty;
  const labelSize = Math.min(...s.steps.map((t) => fit(t, L.label, gap - 4, true))); // 同一张卡的标签统一字号
  const labelSizes = s.steps.map(() => labelSize);
  const pct = (i) => +(FILL * i / (n - 1) * 100).toFixed(1);
  const dir = rtl ? `direction="rtl"` : "";
  const txt = (x, y, size, w, t, extra = "") => `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${size}" font-weight="${w}" ${extra}>${t}</text>`;
  const ink = (o = "") => `fill="${c.fg}" ${o}`;
  let css = `
.track{stroke-dasharray:${len};animation:fill ${DUR}s linear infinite}
@keyframes fill{0%{stroke-dashoffset:${len};opacity:1}${FILL * 100}%{stroke-dashoffset:0}92%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.arrow{animation:nudge 1.2s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(${rtl ? -6 : 6}px)}}
.shine{animation:shine ${DUR}s ease-in-out infinite}
@keyframes shine{0%,${FILL * 100}%{transform:translateX(-90px)}${FILL * 100 + 14}%,100%{transform:translateX(${C.w + 90}px)}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite}
@keyframes ring{0%{transform:scale(1);opacity:.55}100%{transform:scale(${Lk === "wide" ? 1.09 : 1.04},${Lk === "wide" ? 1.12 : 1.18});opacity:0}}
.ok{animation:ok ${DUR}s ease infinite}
@keyframes ok{0%,${pct(n - 1)}%{opacity:0}${pct(n - 1) + 4}%,92%{opacity:1}100%{opacity:0}}
.vr{transform-box:fill-box;transform-origin:center;animation:vr ${DUR}s ease-out infinite}
@keyframes vr{0%,${pct(VERIFY)}%{transform:scale(1);opacity:0}${pct(VERIFY) + 1}%{opacity:.8}${pct(VERIFY) + 14}%,100%{transform:scale(2.6);opacity:0}}`;
  s.steps.forEach((_, i) => {
    const p = pct(i);
    css += `
.n${i}{animation:n${i} ${DUR}s steps(1,end) infinite}
@keyframes n${i}{0%{fill-opacity:0}${p}%{fill-opacity:1}92%{fill-opacity:1}100%{fill-opacity:0}}
.l${i}{animation:l${i} ${DUR}s ease infinite}
@keyframes l${i}{0%{opacity:.4}${Math.max(p - 0.1, 0)}%{opacity:.4}${p + 3}%{opacity:1}92%{opacity:1}100%{opacity:.4}}`;
  });
  css += `\n@media (prefers-reduced-motion:reduce){*{animation:none!important}.ring,.vr{opacity:0}}`;

  // 进度节点
  const nodes = xs.map((x, i) => {
    const last = i === n - 1, v = i === VERIFY;
    let g = `<rect class="n${i}" x="${x - 6}" y="${ty - 6}" width="12" height="12" ${ink(`stroke="${c.fg}" stroke-width="1.5"`)}/>`;
    if (v) g += `<rect class="vr" x="${x - 6}" y="${ty - 6}" width="12" height="12" fill="none" stroke="${c.fg}" stroke-width="1.5"/>`;
    if (last) g += `<path class="ok" d="M${x - 3.5} ${ty}l2.5 2.5 4.5-5" fill="none" stroke="${c.bg}" stroke-width="1.8" stroke-linejoin="miter"/>`;
    g += txt(x, ty + L.labelDy, labelSizes[i], last || v ? 700 : 500, s.steps[i], `class="l${i}" ${ink()} text-anchor="middle" ${dir}`);
    return g;
  }).join("\n");
  // 「别跳过」标签：挂在核验节点正上方
  const tagSize = Lk === "wide" ? 12 : 11, tagW = Math.min(em(s.tag) * tagSize * 1.06 + 14, gap * 1.6), tagH = tagSize + 9;
  const vx = xs[VERIFY], tagY = ty - 16 - tagH;
  const tag = `<rect x="${vx - tagW / 2}" y="${tagY}" width="${tagW}" height="${tagH}" ${ink()}/>` +
    `<path d="M${vx - 4} ${tagY + tagH}l4 5 4-5z" ${ink()}/>` +
    txt(vx, tagY + tagH / 2 + tagSize * 0.36, fit(s.tag, tagSize, tagW - 12, true), 700, s.tag, `fill="${c.bg}" text-anchor="middle" ${dir}`);

  // 按钮
  const pad = 22, cx = rtl ? ctaX + C.w - pad : ctaX + pad;
  const mainSize = fit(s.cta, C.main[1], C.w - pad * 2 - (Lk === "narrow" ? 44 : 0), true);
  let ctaText = txt(cx, C.y + C.main[0], mainSize, 700, s.cta, `fill="${c.ctaFg}" ${dir}`) +
    txt(cx, C.y + C.sub[0], C.sub[1], 400, s.ctaSub, `fill="${c.ctaFg}" fill-opacity=".72" ${dir}`);
  if (C.host) ctaText += txt(cx, C.y + C.host[0], fit(s.host, C.host[1], C.w - pad * 2 - 44, false), 400, s.host, `fill="${c.ctaFg}" fill-opacity=".5" text-anchor="${rtl ? "end" : "start"}" direction="ltr" unicode-bidi="embed"`);
  const ax = C.arrowRight ? (rtl ? ctaX + pad + 28 : ctaX + C.w - pad - 28) : cx, ay = C.y + C.arrowY;
  const arrow = rtl ? `M${ax} ${ay}h-28M${ax - 19} ${ay - 9}l-9 9 9 9` : `M${ax} ${ay}h28M${ax + 19} ${ay - 9}l9 9-9 9`;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${s.title}">
<title>${s.title}</title>
<style>${css}
</style>
<defs><clipPath id="cc"><rect x="${ctaX}" y="${C.y}" width="${C.w}" height="${C.h}"/></clipPath>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="${c.ctaFg}" stop-opacity="0"/><stop offset=".5" stop-color="${c.ctaFg}" stop-opacity=".1"/><stop offset="1" stop-color="${c.ctaFg}" stop-opacity="0"/></linearGradient></defs>
<rect width="${W}" height="${H}" fill="${c.bg}"/>
${txt(mx(P), L.eyebrow[0], fit(s.eyebrow, L.eyebrow[1], avail, false), 400, s.eyebrow, `${ink(`fill-opacity=".62"`)} ${dir}`)}
${txt(mx(P), L.title[0], fit(s.title, L.title[1], avail, true), 700, s.title, `${ink()} ${dir}`)}
<line x1="${mx(ta)}" y1="${ty}" x2="${mx(tb)}" y2="${ty}" stroke="${c.fg}" stroke-opacity=".22" stroke-width="1.5"/>
<line class="track" x1="${mx(ta)}" y1="${ty}" x2="${mx(tb)}" y2="${ty}" stroke="${c.fg}" stroke-width="1.5"/>
${tag}
${nodes}
<rect class="ring" x="${ctaX}" y="${C.y}" width="${C.w}" height="${C.h}" fill="none" stroke="${c.fg}" stroke-width="1.5"/>
<rect x="${ctaX}" y="${C.y}" width="${C.w}" height="${C.h}" fill="${c.ctaBg}"/>
<g clip-path="url(#cc)"><rect class="shine" x="${ctaX - 70}" y="${C.y}" width="70" height="${C.h}" fill="url(#sg)"/></g>
${ctaText}
<g class="arrow"><path d="${arrow}" fill="none" stroke="${c.ctaFg}" stroke-width="1.75" stroke-linejoin="miter"/></g>
</svg>
`;
}

export const pictureHtml = (lang, href) => {
  const b = `docs/readme/button-${lang}`, s = LANGS[lang];
  return `<a href="${href}"><picture>` +
    `<source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="${b}-narrow-dark.svg">` +
    `<source media="(max-width: 600px)" srcset="${b}-narrow-light.svg">` +
    `<source media="(prefers-color-scheme: dark)" srcset="${b}-dark.svg">` +
    `<img src="${b}-light.svg" width="100%" alt="${s.title} · ${s.cta} · ${s.host}"></picture></a>`;
};

const here = fileURLToPath(import.meta.url);
if (process.argv[1] === here) {
  const out = process.argv[2] || dirname(here);
  for (const [lang, s] of Object.entries(LANGS))
    for (const [th, c] of Object.entries(THEMES)) {
      writeFileSync(`${out}/button-${lang}-${th}.svg`, svg(s, c, "wide"));
      writeFileSync(`${out}/button-${lang}-narrow-${th}.svg`, svg(s, c, "narrow"));
    }
  console.log(`wrote ${Object.keys(LANGS).length * 4} cards to ${out}`);
}
