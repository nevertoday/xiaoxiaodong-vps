// 构建后处理：部署在子路径（BASE_PATH=/xiaoxiaodong-vps/）时，给 dist 里所有以 / 开头的站内链接补上前缀。
// 已经带前缀的（组件里 link() 生成的）不重复加。根路径部署时什么都不做。
import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const base = (process.env.BASE_PATH || "/").replace(/\/$/, "");
if (!base) process.exit(0);
const walk = (dir) => readdirSync(dir).flatMap((f) => (statSync(join(dir, f)).isDirectory() ? walk(join(dir, f)) : [join(dir, f)]));
let n = 0;
for (const file of walk("dist").filter((f) => f.endsWith(".html"))) {
  const html = readFileSync(file, "utf8");
  const out = html
    .replace(/(href|src)="\/(?!\/)([^"]*)"/g, (m, attr, rest) => {
      if (("/" + rest).startsWith(base + "/")) return m;
      n++;
      return `${attr}="${base}/${rest}"`;
    })
    // astro.config.mjs 里 redirects 生成的跳转页（meta refresh）不带前缀，也补上
    .replace(/content="0;url=\/(?!\/)([^"]*)"/g, (m, rest) => {
      if (("/" + rest).startsWith(base + "/")) return m;
      n++;
      return `content="0;url=${base}/${rest}"`;
    });
  if (out !== html) writeFileSync(file, out);
}
console.log(`✓ 已给 ${n} 个站内链接补上前缀 ${base}`);
