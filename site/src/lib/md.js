// 极简行内格式：**粗体**、`代码`、[文字](https://网址)。只用于站内自己写的数据（Wiki、FAQ），先转义再替换。
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export const inline = (s) =>
  esc(s)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, '<code class="xxd-code-inline">$1</code>')
    .replace(/\[([^\]]+)\]\((https:\/\/[^)\s]+)\)/g, '<a class="xxd-link" href="$2" target="_blank" rel="noopener">$1</a>');
