import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

// 小小东 VPS 教程站：静态构建，界面全部用 xxd-ui-kit（public/xxd/ 里的一份，见 scripts/sync-xxd.mjs）。
// 主站 https://vps.xiaoxiaodong.ai 部署在根路径；GitHub Pages 备用地址用 SITE_URL / BASE_PATH 构建到子路径
// （组件里的链接走 data/nav.js 的 link()，正文里手写的 /xxx 链接由 scripts/base-links.mjs 在构建后补前缀）。
const site = process.env.SITE_URL || "https://vps.xiaoxiaodong.ai";
const base = process.env.BASE_PATH || "/";
export default defineConfig({
  site,
  base,
  trailingSlash: "always",
  integrations: [mdx()],
  build: { format: "directory" },
  // 11-04 第 1、2 步对调（先在电脑上装 AI，再买服务器），旧网址跳到新网址
  redirects: {
    "/guide/1-buy-server": "/guide/2-buy-server/",
    "/guide/2-ai-assistant": "/guide/1-ai-assistant/",
    "/en/guide/1-buy-server": "/en/guide/2-buy-server/",
    "/en/guide/2-ai-assistant": "/en/guide/1-ai-assistant/",
    // 不再推荐 WSL：原来的安装页跳到「在电脑上装 AI」
    "/howto/windows-wsl": "/guide/1-ai-assistant/",
    "/en/howto/windows-wsl": "/en/guide/1-ai-assistant/",
    // 配置只推荐 Codex：Claude Code 安装页跳到 Codex
    "/howto/install-claude-code": "/howto/install-codex/",
    "/en/howto/install-claude-code": "/en/howto/install-codex/",
  },
});
