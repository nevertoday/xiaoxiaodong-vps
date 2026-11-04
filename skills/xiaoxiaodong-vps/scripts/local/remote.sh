#!/usr/bin/env bash
# 把服务器端工具上传到 VPS 并执行一个阶段。
#
#   remote.sh <ssh名称> upload
#   remote.sh <ssh名称> init --ip 1.2.3.4 --alias bwg --timezone America/Los_Angeles [--quota-gb 1000 --reset-day 1]
#   remote.sh <ssh名称> base | cert | xui | sub | cliproxy | maint | verify [--full]
#   remote.sh <ssh名称> kiwivm --veid 数字 --key-file 文件   # 搬瓦工：订阅用量改用官方读数（--remove 取消）
#   remote.sh <ssh名称> save [--lang en]   # 把登录信息保存到桌面（中文「我的服务器-<名称>-订阅和账号.md」，其他语言「my-server-<名称>-subscriptions-and-accounts-<语言>.md」），不在终端显示
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
    # 放在桌面方便找到。Windows（Git Bash / WSL）问系统要真正的桌面位置（可能被 OneDrive 挪走了）；都找不到时放在主目录
    dir="$HOME/Desktop"
    if command -v powershell.exe >/dev/null 2>&1; then
      win=$(powershell.exe -NoProfile -Command "[Environment]::GetFolderPath('Desktop')" 2>/dev/null | tr -d '\r')
      if [ -n "$win" ]; then
        if command -v cygpath >/dev/null 2>&1; then d=$(cygpath -u "$win"); elif command -v wslpath >/dev/null 2>&1; then d=$(wslpath -u "$win"); else d=""; fi
        [ -n "$d" ] && [ -d "$d" ] && dir="$d"
      fi
    fi
    [ -d "$dir" ] || dir="$HOME"
    if [ "$LANG_CODE" = zh ]; then out="$dir/我的服务器-${ALIAS}-订阅和账号.md"; else out="$dir/my-server-${ALIAS}-subscriptions-and-accounts-${LANG_CODE}.md"; fi
    tmp=$(mktemp "$dir/.xxd-vps-$ALIAS.XXXXXX")
    if ! ssh -o BatchMode=yes "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py export --lang $(printf '%q' "$LANG_CODE")" > "$tmp" || [ ! -s "$tmp" ]; then
      rm -f "$tmp"; echo "[remote] 导出失败" >&2; exit 2
    fi
    chmod 600 "$tmp"; mv "$tmp" "$out"
    echo "[remote] 登录信息已保存：${out}（仅本机账户可读）"
    ;;
  kiwivm)
    # 搬瓦工：订阅用量改用 KiwiVM 官方读数。API Key 放在只有本人可读的文件里，经 ssh 标准输入传过去，用完删除
    if [ "${1:-}" = "--remove" ]; then
      ssh -o BatchMode=yes "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py kiwivm --remove"
      exit
    fi
    [ "${1:-}" = "--veid" ] && [ "${3:-}" = "--key-file" ] && [ -f "${4:-}" ] \
      || { echo "用法：remote.sh <ssh名称> kiwivm --veid 数字 --key-file 文件 | --remove" >&2; exit 2; }
    veid="$2" keyfile="$4"
    trap 'rm -f "$keyfile"' EXIT
    key=$(tr -d '[:space:]' < "$keyfile")
    printf '{"veid": "%s", "api_key": "%s"}' "$veid" "$key" \
      | ssh -o BatchMode=yes "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py kiwivm"
    ;;
  *)
    args=""; for x in "$@"; do args="$args $(printf '%q' "$x")"; done
    ssh -o BatchMode=yes -o ServerAliveInterval=30 "$ALIAS" "$SUDO python3 $REMOTE/server/xxd-vps.py $CMD$args"
    ;;
esac
