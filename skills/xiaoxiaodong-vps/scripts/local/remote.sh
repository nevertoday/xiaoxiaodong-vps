#!/usr/bin/env bash
# 把服务器端工具上传到 VPS 并执行一个阶段。
#
#   remote.sh <ssh名称> upload
#   remote.sh <ssh名称> init --ip 1.2.3.4 --alias bwg --timezone America/Los_Angeles [--quota-gb 1000 --reset-day 1]
#   remote.sh <ssh名称> base | cert | xui | sub | cliproxy | maint | verify [--full]
#   remote.sh <ssh名称> save        # 把登录信息保存到本机 ~/xxd-vps/<名称>/登录信息.md，不在终端显示
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
    umask 077
    out="$HOME/xxd-vps/$ALIAS"
    mkdir -p "$out"; chmod 700 "$HOME/xxd-vps" "$out"
    ssh -o BatchMode=yes "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py export" > "$out/登录信息.md.tmp"
    [ -s "$out/登录信息.md.tmp" ] || { rm -f "$out/登录信息.md.tmp"; echo "[remote] 导出失败" >&2; exit 2; }
    mv "$out/登录信息.md.tmp" "$out/登录信息.md"; chmod 600 "$out/登录信息.md"
    echo "[remote] 登录信息已保存：$out/登录信息.md（仅本机账户可读）"
    ;;
  *)
    args=""; for x in "$@"; do args="$args $(printf '%q' "$x")"; done
    ssh -o BatchMode=yes -o ServerAliveInterval=30 "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py $CMD$args"
    ;;
esac
