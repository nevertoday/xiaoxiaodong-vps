// README 顶部的「打开图文教程」按钮：每种语言一套浅色 + 深色动画 SVG。
// 改文案或样式后运行：node docs/readme/build-buttons.mjs
// 动画是 SVG 内的 CSS（GitHub 的 <img> 里能播放）；系统开了「减少动态效果」时直接显示完成状态。
import { writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const FONT = `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans','Apple SD Gothic Neo','Malgun Gothic','Microsoft YaHei','Noto Sans CJK SC','Noto Sans Arabic','Noto Sans',Helvetica,Arial,sans-serif`;
const EN = "vps.xiaoxiaodong.ai/en";
export const LANGS = {
  zh: { eyebrow: "零基础 · 每步有截图 · 第一次约 1 小时", title: "跟着图文教程，一步步用上", steps: ["装 Codex", "买服务器", "AI 远程配置", "导入订阅", "用上了"], cta: "开始第 1 步", host: "vps.xiaoxiaodong.ai" },
  en: { eyebrow: "For beginners · Screenshots at every step · ~1 hour", title: "Follow along, step by step", steps: ["Get Codex", "Buy a server", "AI sets it up", "Import", "Done"], cta: "Start step 1", host: EN },
  ko: { eyebrow: "초보자 OK · 단계마다 스크린샷 · 처음엔 약 1시간", title: "가이드를 따라 한 단계씩", steps: ["Codex 설치", "서버 구매", "AI가 설정", "구독 가져오기", "완료"], cta: "1단계 시작", host: EN },
  ja: { eyebrow: "初心者OK · 全ステップに画面付き · 初回は約1時間", title: "ガイドに沿って一歩ずつ", steps: ["Codex導入", "サーバー購入", "AIが設定", "設定の取り込み", "完了"], cta: "ステップ1へ", host: EN },
  ar: { eyebrow: "للمبتدئين · صور لكل خطوة · نحو ساعة في المرة الأولى", title: "اتبع الدليل خطوة بخطوة", steps: ["ثبّت Codex", "اشترِ خادمًا", "الإعداد الآلي", "استورد الاشتراك", "جاهز"], cta: "ابدأ الخطوة 1", host: EN, rtl: true },
  es: { eyebrow: "Para principiantes · Capturas en cada paso · ~1 hora", title: "Sigue la guía paso a paso", steps: ["Codex", "Servidor", "La IA configura", "Importar", "Listo"], cta: "Empezar", host: EN },
  fr: { eyebrow: "Pour débutants · Captures à chaque étape · ~1 heure", title: "Suivez le guide pas à pas", steps: ["Codex", "Serveur", "L’IA configure", "Importer", "C’est prêt"], cta: "Commencer", host: EN },
  ru: { eyebrow: "Для новичков · Скриншоты на каждом шаге · ~1 час", title: "Следуйте шагам руководства", steps: ["Codex", "Сервер", "Настройка ИИ", "Импорт", "Готово"], cta: "К шагу 1", host: EN },
  de: { eyebrow: "Für Einsteiger · Screenshots zu jedem Schritt · ~1 Stunde", title: "Schritt für Schritt zum Ziel", steps: ["Codex", "Server", "KI richtet ein", "Import", "Fertig"], cta: "Zu Schritt 1", host: EN },
  pt: { eyebrow: "Para iniciantes · Capturas em cada passo · ~1 hora", title: "Siga o guia passo a passo", steps: ["Codex", "Servidor", "A IA configura", "Importar", "Pronto"], cta: "Começar", host: EN },
};
const THEMES = {
  light: { bg: "#111111", fg: "#ffffff", ctaBg: "#ffffff", ctaFg: "#111111" }, // GitHub 浅色主题下：深色卡片
  dark: { bg: "#f3f0ea", fg: "#171612", ctaBg: "#171612", ctaFg: "#f3f0ea" },  // GitHub 深色主题下：浅色卡片
};
const W = 640, H = 176, P = 28, CTA_W = 148, DUR = 7, FILL = 0.62; // 进度线在每轮前 62% 走完，停到 92% 后重来

// 粗略估算文字宽度（em），用来在超宽时缩小字号
function em(s) {
  let w = 0;
  for (const ch of s) {
    const c = ch.codePointAt(0);
    if (c >= 0x2e80 || (c >= 0x1100 && c <= 0x11ff)) w += c >= 0xff00 && c <= 0xff60 ? 1 : (c >= 0x3000 ? 1 : 0.6);
    else if (c >= 0x0600 && c <= 0x06ff) w += 0.5;
    else if (ch === " ") w += 0.28;
    else if (/[A-ZА-ЯЁ0-9]/.test(ch)) w += 0.64;
    else if (/[.,·’'ilIjt:;!|]/.test(ch)) w += 0.3;
    else w += 0.56;
  }
  return w;
}
const fit = (s, base, avail, bold) => +Math.min(base, avail / (em(s) * (bold ? 1.06 : 1))).toFixed(1);

function svg(s, c) {
  const rtl = !!s.rtl, n = s.steps.length;
  const ctaX = rtl ? P : W - P - CTA_W, ctaY = P, ctaH = H - 2 * P;
  const left = rtl ? ctaX + CTA_W + P : P, right = rtl ? W - P : ctaX - P; // 左侧文字区
  const avail = right - left;
  const a = rtl ? right - 26 : left + 26, b = rtl ? left + 52 : right - 24; // 进度线起点 → 终点
  const xs = s.steps.map((_, i) => a + (b - a) * i / (n - 1));
  const gap = Math.abs(b - a) / (n - 1);
  const labelSize = Math.min(...s.steps.map((t) => fit(t, 12.5, gap - 6, true)));
  const len = Math.abs(b - a), ty = 124, tx = rtl ? right : left, anchor = "start"; // rtl 文字的 start 就是右边
  const pct = (i) => +(FILL * i / (n - 1) * 100).toFixed(1);
  const dir = rtl ? `direction="rtl"` : "";
  let css = `
.track{stroke-dasharray:${len};animation:fill ${DUR}s linear infinite}
@keyframes fill{0%{stroke-dashoffset:${len};opacity:1}${FILL * 100}%{stroke-dashoffset:0}92%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.arrow{animation:nudge 1.4s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(${rtl ? -5 : 5}px)}}
.shine{animation:shine ${DUR}s ease-in-out infinite}
@keyframes shine{0%,${FILL * 100}%{transform:translateX(-80px)}${FILL * 100 + 14}%,100%{transform:translateX(${CTA_W + 80}px)}}
.ok{animation:ok ${DUR}s ease infinite}
@keyframes ok{0%,${pct(n - 1)}%{opacity:0}${pct(n - 1) + 4}%,92%{opacity:1}100%{opacity:0}}`;
  s.steps.forEach((_, i) => {
    const p = pct(i);
    css += `
.n${i}{animation:n${i} ${DUR}s steps(1,end) infinite}
@keyframes n${i}{0%{fill-opacity:0}${p}%{fill-opacity:1}92%{fill-opacity:1}100%{fill-opacity:0}}
.l${i}{animation:l${i} ${DUR}s ease infinite}
@keyframes l${i}{0%{opacity:.4}${Math.max(p - 0.1, 0)}%{opacity:.4}${p + 3}%{opacity:1}92%{opacity:1}100%{opacity:.4}}`;
  });
  css += `\n@media (prefers-reduced-motion:reduce){*{animation:none!important}}`;
  const t = (x, y, size, w, txt, extra = "") => `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${size}" font-weight="${w}" ${extra}>${txt}</text>`;
  const nodes = xs.map((x, i) => {
    const last = i === n - 1;
    return `<rect class="n${i}" x="${x - 6}" y="${ty - 6}" width="12" height="12" fill="${c.fg}" stroke="${c.fg}" stroke-width="1.5"/>` +
      (last ? `<path class="ok" d="M${x - 3.5} ${ty}l2.5 2.5 4.5-5" fill="none" stroke="${c.bg}" stroke-width="1.8" stroke-linejoin="miter"/>` : "") +
      t(x, ty + 26, labelSize, last ? 700 : 500, s.steps[i], `class="l${i}" fill="${c.fg}" text-anchor="middle" ${dir}`);
  }).join("\n");
  const cx = rtl ? ctaX + CTA_W - 20 : ctaX + 20, ay = ctaY + ctaH - 26;
  const arrow = rtl
    ? `M${cx} ${ay}h-22M${cx - 15} ${ay - 7}l-7 7 7 7`
    : `M${cx} ${ay}h22M${cx + 15} ${ay - 7}l7 7-7 7`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${s.title}">
<title>${s.title}</title>
<style>${css}
</style>
<defs><clipPath id="cc"><rect x="${ctaX}" y="${ctaY}" width="${CTA_W}" height="${ctaH}"/></clipPath>
<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="${c.ctaFg}" stop-opacity="0"/><stop offset=".5" stop-color="${c.ctaFg}" stop-opacity=".1"/><stop offset="1" stop-color="${c.ctaFg}" stop-opacity="0"/></linearGradient></defs>
<rect width="${W}" height="${H}" fill="${c.bg}"/>
${t(tx, 50, fit(s.eyebrow, 13, avail, false), 400, s.eyebrow, `fill="${c.fg}" fill-opacity=".62" text-anchor="${anchor}" ${dir}`)}
${t(tx, 84, fit(s.title, 24, avail, true), 700, s.title, `fill="${c.fg}" text-anchor="${anchor}" ${dir}`)}
<line x1="${a}" y1="${ty}" x2="${b}" y2="${ty}" stroke="${c.fg}" stroke-opacity=".22" stroke-width="1.5"/>
<line class="track" x1="${a}" y1="${ty}" x2="${b}" y2="${ty}" stroke="${c.fg}" stroke-width="1.5"/>
${nodes}
<rect x="${ctaX}" y="${ctaY}" width="${CTA_W}" height="${ctaH}" fill="${c.ctaBg}"/>
<g clip-path="url(#cc)"><rect class="shine" x="${ctaX - 60}" y="${ctaY}" width="60" height="${ctaH}" fill="url(#sg)"/></g>
${t(cx, ctaY + 52, fit(s.cta, 17, CTA_W - 40, true), 700, s.cta, `fill="${c.ctaFg}" text-anchor="${anchor}" ${dir}`)}
${t(cx, ctaY + 72, fit(s.host, 11, CTA_W - 32, false), 400, s.host, `fill="${c.ctaFg}" fill-opacity=".6" text-anchor="${rtl ? "end" : "start"}" direction="ltr" unicode-bidi="embed"`)}
<g class="arrow"><path d="${arrow}" fill="none" stroke="${c.ctaFg}" stroke-width="1.5" stroke-linejoin="miter"/></g>
</svg>
`;
}

const here = fileURLToPath(import.meta.url);
const out = process.argv[2] || dirname(here);
if (process.argv[1] === here) for (const [lang, s] of Object.entries(LANGS))
  for (const [th, c] of Object.entries(THEMES)) writeFileSync(`${out}/button-${lang}-${th}.svg`, svg(s, c));
if (process.argv[1] === here) console.log(`wrote ${Object.keys(LANGS).length * 2} buttons to ${out}`);
