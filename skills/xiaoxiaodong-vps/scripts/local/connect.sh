#!/usr/bin/env bash
# 建立 `ssh <名称>` 免密登录。
#
#   connect.sh --alias bwg --host 1.2.3.4 [--port 22] [--user root] --key ~/Downloads/key.zip
#   connect.sh --alias bwg --host 1.2.3.4 --password-file /私密目录/pw      # 用完即删除该文件
#   connect.sh --alias bwg --host 1.2.3.4 --password-prompt                 # 在终端里自己输入密码
#
# 密钥统一放在 ~/.ssh/xxd-vps/<名称>/，在 ~/.ssh/config 最前面写入 Host 段（ssh 以第一次出现的值为准，
# 放在最前面才不会被已有的 `Host *` 覆盖）。脚本不会打印密码或私钥内容。
set -euo pipefail

ALIAS="" HOST="" PORT=22 USER_NAME=root KEY="" PWFILE="" PWPROMPT=0
while [ $# -gt 0 ]; do
  case "$1" in
    --alias) ALIAS="$2"; shift 2 ;;
    --host) HOST="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --user) USER_NAME="$2"; shift 2 ;;
    --key) KEY="$2"; shift 2 ;;
    --password-file) PWFILE="$2"; shift 2 ;;
    --password-prompt) PWPROMPT=1; shift ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

fail() { echo "[connect] 停止：$*" >&2; exit 2; }
say() { echo "[connect] $*"; }

[[ "$ALIAS" =~ ^[A-Za-z][A-Za-z0-9-]{0,30}$ ]] || fail "--alias 只能用字母、数字和连字符，并以字母开头"
[[ "$HOST" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || fail "--host 必须是服务器的 IPv4 地址"
[[ "$PORT" =~ ^[0-9]+$ ]] || fail "--port 必须是数字"
modes=0; [ -n "$KEY" ] && modes=$((modes+1)); [ -n "$PWFILE" ] && modes=$((modes+1)); [ "$PWPROMPT" = 1 ] && modes=$((modes+1))
[ "$modes" = 1 ] || fail "--key、--password-file、--password-prompt 必须且只能选一个"

CONFIG="$HOME/.ssh/config"
DIR="$HOME/.ssh/xxd-vps/$ALIAS"
umask 077
mkdir -p "$HOME/.ssh" "$DIR"
chmod 700 "$HOME/.ssh" "$HOME/.ssh/xxd-vps" "$DIR"
touch "$CONFIG"; chmod 600 "$CONFIG"

# 名称已被占用时不覆盖别的服务器
existing=$(ssh -G "$ALIAS" 2>/dev/null | awk '$1=="hostname"{print $2}')
if grep -Eq "^[[:space:]]*Host[[:space:]]+(.*[[:space:]])?${ALIAS}([[:space:]]|$)" "$CONFIG"; then
  [ "$existing" = "$HOST" ] || fail "ssh 名称 \"$ALIAS\" 已经指向另一台服务器（$existing），请换一个名称"
  ALREADY=1
else
  ALREADY=0
fi

SSH_BASE=(-o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -p "$PORT")
TMP=$(mktemp -d)
cleanup() { rm -rf "$TMP"; [ -n "$PWFILE" ] && rm -f "$PWFILE"; return 0; }
trap cleanup EXIT

is_private_key() { head -c 64 "$1" 2>/dev/null | grep -q -- '-----BEGIN .*PRIVATE KEY-----'; }

if [ -n "$KEY" ]; then
  KEY="${KEY/#\~/$HOME}"
  [ -f "$KEY" ] || fail "找不到密钥文件：$KEY（macOS 若拦截“下载”文件夹，请先把文件复制到桌面）"
  src="$KEY"
  if [[ "$KEY" == *.zip ]]; then
    unzip -q -o "$KEY" -d "$TMP/zip" || fail "解压失败：$KEY"
    found=()
    while IFS= read -r -d '' f; do is_private_key "$f" && found+=("$f"); done < <(find "$TMP/zip" -type f ! -name '*.pub' -print0)
    [ "${#found[@]}" = 1 ] || fail "压缩包里应当正好有一把私钥，实际找到 ${#found[@]} 把"
    src="${found[0]}"
  fi
  [[ "$src" == *.ppk ]] && fail "这是 PuTTY 格式（.ppk），请在服务商后台下载 OpenSSH 格式的私钥"
  is_private_key "$src" || fail "不是 OpenSSH 私钥文件：$src"
  IDFILE="$DIR/id_provider"
  install -m 600 "$src" "$IDFILE"
  ssh-keygen -y -P '' -f "$IDFILE" > "$IDFILE.pub" 2>/dev/null || fail "这把私钥带口令，请改用服务商的密码登录方式"
  chmod 644 "$IDFILE.pub"
else
  IDFILE="$DIR/id_ed25519"
  [ -f "$IDFILE" ] || ssh-keygen -q -t ed25519 -N '' -C "xxd-vps-$ALIAS" -f "$IDFILE"
  if [ "$PWPROMPT" = 1 ]; then
    [ -t 0 ] || fail "--password-prompt 需要在终端里由你本人输入密码"
    PWFILE="$TMP/pw"
    printf '服务器 root 密码（输入时不显示）：' >&2; IFS= read -rs pw; echo >&2
    printf '%s' "$pw" > "$PWFILE"; unset pw
  fi
  [ -s "$PWFILE" ] || fail "密码文件为空"
  chmod 600 "$PWFILE"
  ver=$(ssh -V 2>&1 | sed -nE 's/^OpenSSH_([0-9]+)\.([0-9]+).*/\1\2/p')
  [ -n "$ver" ] && [ "$ver" -ge 84 ] || fail "本机 OpenSSH 版本太旧（需要 8.4+），请改用 --password-prompt 之外的方式或升级系统"
  printf '#!/bin/sh\ncat "$XXD_PW_FILE"\n' > "$TMP/askpass"; chmod 700 "$TMP/askpass"
  say "用密码登录一次，写入本机公钥"
  XXD_PW_FILE="$PWFILE" SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY="${DISPLAY:-none}" \
    ssh "${SSH_BASE[@]}" -o PubkeyAuthentication=no -o PreferredAuthentications=password,keyboard-interactive \
        -o NumberOfPasswordPrompts=1 "$USER_NAME@$HOST" \
        'umask 077; mkdir -p ~/.ssh; IFS= read -r K; touch ~/.ssh/authorized_keys; grep -qxF "$K" ~/.ssh/authorized_keys || printf "%s\n" "$K" >> ~/.ssh/authorized_keys' \
        < "$IDFILE.pub" 2>"$TMP/err" \
    || fail "密码登录失败：$(tail -n 2 "$TMP/err" | tr '\n' ' ')（密码错误、服务商要求首次改密码，或服务器禁止了密码登录）"
fi

say "验证密钥登录"
ssh "${SSH_BASE[@]}" -i "$IDFILE" -o IdentitiesOnly=yes -o BatchMode=yes "$USER_NAME@$HOST" 'id -u' > "$TMP/uid" 2>"$TMP/err" \
  || fail "密钥登录失败：$(tail -n 2 "$TMP/err" | tr '\n' ' ')（如果用的是服务商密钥，可能需要先在服务商后台把它绑定到这台服务器）"

if [ "$ALREADY" = 0 ]; then
  cp "$CONFIG" "$CONFIG.bak-xxd-$(date +%Y%m%d%H%M%S)"
  rel="~${IDFILE#"$HOME"}"
  {
    printf '# 小小东 VPS：%s\nHost %s\n  HostName %s\n  User %s\n  Port %s\n  IdentityFile %s\n  IdentitiesOnly yes\n  ServerAliveInterval 30\n  ServerAliveCountMax 3\n\n' \
      "$ALIAS" "$ALIAS" "$HOST" "$USER_NAME" "$PORT" "$rel"
    cat "$CONFIG"
  } > "$TMP/config"
  install -m 600 "$TMP/config" "$CONFIG"
fi

uid=$(ssh -o BatchMode=yes "$ALIAS" 'id -u' 2>/dev/null) || fail "ssh $ALIAS 无法免密登录，请检查 ~/.ssh/config"
[ "$uid" = 0 ] || say "注意：登录用户不是 root，后续命令需要加 sudo"
fp=$( { ssh-keygen -F "[$HOST]:$PORT" -l; ssh-keygen -F "$HOST" -l; } 2>/dev/null | grep -v '^#' | awk '{print $2" "$NF}' | head -n1)
say "完成：以后用 ssh $ALIAS 登录（密钥：~${IDFILE#"$HOME"}）"
[ -n "$fp" ] && say "服务器主机指纹：$fp"
exit 0
