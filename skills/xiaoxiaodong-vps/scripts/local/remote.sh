#!/usr/bin/env bash
# 把服务器端工具上传到 VPS 并执行一个阶段。
#
#   remote.sh <ssh名称> upload
#   remote.sh <ssh名称> init --ip 1.2.3.4 --alias bwg --timezone America/Los_Angeles [--quota-gb 1000 --reset-day 1]
#   remote.sh <ssh名称> base | cert | xui | sub | cliproxy | maint | verify [--full]
#   remote.sh <ssh名称> save [--lang en]   # 把登录信息保存到桌面（中文「小小东VPS-<名称>-登录信息.md」，其他语言「XXD-VPS-<名称>-login-<语言>.md」），不在终端显示
set -euo pipefail
ALIAS="${1:?用法：remote.sh <ssh名称> <阶段> [参数]}"; shift
CMD="${1:?缺少阶段名}"; shift
HERE="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE=/root/xxd-vps-deploy
SUDO=""
[ "$(ssh -o BatchMode=yes "$ALIAS" 'id -u')" = 0 ] || SUDO="sudo"

case "$CMD" in
  upload)
    tar -C "$HERE" -czf - server | ssh -o BatchMode=yes "$ALIAS" "$SUDO rm -rf $REMOTE && $SUDO mkdir -p $REMOTE && $SUDO tar -xzf - -C $REMOTE"
    echo "[remote] 已上传到 $ALIAS:$REMOTE"
    ;;
  save)
    LANG_CODE="zh"
    [ "${1:-}" = "--lang" ] && LANG_CODE="${2:?--lang 需要语言代码}"
    umask 077
    # 放在桌面方便找到；没有桌面目录（如 Linux 服务器、WSL）时放在主目录
    dir="$HOME/Desktop"; [ -d "$dir" ] || dir="$HOME"
    if [ "$LANG_CODE" = zh ]; then out="$dir/小小东VPS-${ALIAS}-登录信息.md"; else out="$dir/XXD-VPS-${ALIAS}-login-${LANG_CODE}.md"; fi
    tmp=$(mktemp "$dir/.xxd-vps-$ALIAS.XXXXXX")
    if ! ssh -o BatchMode=yes "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py export --lang $(printf '%q' "$LANG_CODE")" > "$tmp" || [ ! -s "$tmp" ]; then
      rm -f "$tmp"; echo "[remote] 导出失败" >&2; exit 2
    fi
    chmod 600 "$tmp"; mv "$tmp" "$out"
    echo "[remote] 登录信息已保存：${out}（仅本机账户可读）"
    ;;
  *)
    args=""; for x in "$@"; do args="$args $(printf '%q' "$x")"; done
    ssh -o BatchMode=yes -o ServerAliveInterval=30 "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py $CMD$args"
    ;;
esac
