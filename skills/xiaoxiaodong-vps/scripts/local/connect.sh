#!/usr/bin/env bash
# 建立 `ssh <名称>` 免密登录。
#
#   connect.sh --alias bwg --host 1.2.3.4 [--port 22] [--user root] --key ~/Downloads/key.zip
#   connect.sh --alias bwg --host 1.2.3.4 --password-file /私密目录/pw      # 用完即删除该文件
#   connect.sh --alias bwg --host 1.2.3.4 --password-prompt                 # 在终端里自己输入密码
#   connect.sh --alias bwg --host 1.2.3.4 --password-dialog                 # 弹出系统密码框（桌面版 AI 应用没有终端时用）
#
# 密钥统一放在 ~/.ssh/xxd-vps/<名称>/，在 ~/.ssh/config 最前面写入 Host 段（ssh 以第一次出现的值为准，
# 放在最前面才不会被已有的 `Host *` 覆盖）。脚本不会打印密码或私钥内容。
set -euo pipefail

ALIAS="" HOST="" PORT=22 USER_NAME=root KEY="" PWFILE="" PWPROMPT=0 PWDIALOG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --alias) ALIAS="$2"; shift 2 ;;
    --host) HOST="$2"; shift 2 ;;
    --port) PORT="$2"; shift 2 ;;
    --user) USER_NAME="$2"; shift 2 ;;
    --key) KEY="$2"; shift 2 ;;
    --password-file) PWFILE="$2"; shift 2 ;;
    --password-prompt) PWPROMPT=1; shift ;;
    --password-dialog) PWDIALOG=1; shift ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

fail() { echo "[connect] 停止：$*" >&2; exit 2; }
say() { echo "[connect] $*"; }

[[ "$ALIAS" =~ ^[A-Za-z][A-Za-z0-9.-]{0,30}$ ]] || fail "--alias 只能用字母、数字、点和连字符，并以字母开头"
[[ "$HOST" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || fail "--host 必须是服务器的 IPv4 地址"
[[ "$PORT" =~ ^[0-9]+$ ]] || fail "--port 必须是数字"
modes=0; [ -n "$KEY" ] && modes=$((modes+1)); [ -n "$PWFILE" ] && modes=$((modes+1)); [ "$PWPROMPT" = 1 ] && modes=$((modes+1)); [ "$PWDIALOG" = 1 ] && modes=$((modes+1))
[ "$modes" = 1 ] || fail "--key、--password-file、--password-prompt、--password-dialog 必须且只能选一个"

CONFIG="$HOME/.ssh/config"
DIR="$HOME/.ssh/xxd-vps/$ALIAS"
umask 077
mkdir -p "$HOME/.ssh" "$DIR"
chmod 700 "$HOME/.ssh" "$HOME/.ssh/xxd-vps" "$DIR"
touch "$CONFIG"; chmod 600 "$CONFIG"

# 名称已被占用时不覆盖别的服务器
existing=$(ssh -G "$ALIAS" 2>/dev/null | awk '$1=="hostname"{print $2}')
if grep -Eq "^[[:space:]]*Host[[:space:]]+(.*[[:space:]])?${ALIAS//./\\.}([[:space:]]|$)" "$CONFIG"; then
  [ "$existing" = "$HOST" ] || fail "ssh 名称 \"$ALIAS\" 已经指向另一台服务器（${existing}），请换一个名称"
  ALREADY=1
else
  ALREADY=0
fi

SSH_BASE=(-o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 -p "$PORT")
TMP=$(mktemp -d)
cleanup() { rm -rf "$TMP"; [ -n "$PWFILE" ] && rm -f "$PWFILE"; return 0; }
trap cleanup EXIT

# 弹出系统自带的密码框，密码只写到标准输出（由调用方重定向进权限 600 的临时文件），不进命令行参数和对话
ask_password_dialog() {
  local msg="请输入服务器 $1 的 root 密码（商家开通邮件或后台里那个）。"
  if [ "$(uname -s)" = Darwin ]; then
    # 取消时 osascript 返回非零；末尾的换行去掉
    local out
    out=$(osascript -e 'on run argv' \
      -e 'text returned of (display dialog (item 1 of argv) default answer "" with hidden answer with title "小小东 VPS" buttons {"取消", "确定"} default button "确定" cancel button "取消" giving up after (item 2 of argv as integer))' \
      -e 'end run' "$msg" "${XXD_PW_TIMEOUT:-600}" 2>/dev/null) || return 1
    [ -n "$out" ] || return 1
    printf '%s' "$out"
  elif command -v powershell.exe >/dev/null 2>&1; then
    # Windows（Git Bash 或 WSL）：用 Windows 自带 PowerShell 弹一个带掩码的输入框
    WSLENV="${WSLENV:+$WSLENV:}XXD_MSG" XXD_MSG="$msg" powershell.exe -NoProfile -STA -Command '
      Add-Type -AssemblyName System.Windows.Forms
      [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
      $f = New-Object Windows.Forms.Form -Property @{ Text = "小小东 VPS"; Width = 420; Height = 170; StartPosition = "CenterScreen"; TopMost = $true; FormBorderStyle = "FixedDialog"; MaximizeBox = $false; MinimizeBox = $false }
      $l = New-Object Windows.Forms.Label -Property @{ Text = $env:XXD_MSG; Left = 12; Top = 12; Width = 380; Height = 34 }
      $t = New-Object Windows.Forms.TextBox -Property @{ Left = 12; Top = 50; Width = 380; UseSystemPasswordChar = $true }
      $ok = New-Object Windows.Forms.Button -Property @{ Text = "确定"; Left = 236; Top = 84; Width = 75; DialogResult = "OK" }
      $no = New-Object Windows.Forms.Button -Property @{ Text = "取消"; Left = 317; Top = 84; Width = 75; DialogResult = "Cancel" }
      $f.Controls.AddRange(@($l, $t, $ok, $no)); $f.AcceptButton = $ok; $f.CancelButton = $no
      if ($f.ShowDialog() -ne "OK" -or $t.Text -eq "") { exit 1 }
      [Console]::Out.Write($t.Text)' 2>/dev/null
  elif command -v zenity >/dev/null 2>&1; then
    local out; out=$(zenity --password --title="小小东 VPS" 2>/dev/null) || return 1
    [ -n "$out" ] || return 1
    printf '%s' "$out"
  else
    return 1
  fi
}

is_private_key() { head -c 64 "$1" 2>/dev/null | grep -q -- '-----BEGIN .*PRIVATE KEY-----'; }

if [ -n "$KEY" ]; then
  KEY="${KEY/#\~/$HOME}"
  [ -f "$KEY" ] || fail "找不到密钥文件：${KEY}（macOS 若拦截“下载”文件夹，请先把文件复制到桌面）"
  src="$KEY"
  if [[ "$KEY" == *.zip ]]; then
    if command -v unzip >/dev/null 2>&1; then
      unzip -q -o "$KEY" -d "$TMP/zip" || fail "解压失败：$KEY"
    elif command -v powershell.exe >/dev/null 2>&1 && command -v cygpath >/dev/null 2>&1; then
      # Windows 的 Git Bash 可能没有 unzip，改用系统自带的 PowerShell 解压
      mkdir -p "$TMP/zip"
      powershell.exe -NoProfile -Command "Expand-Archive -Force -LiteralPath '$(cygpath -w "$KEY")' -DestinationPath '$(cygpath -w "$TMP/zip")'" >/dev/null || fail "解压失败：$KEY"
    else
      fail "本机没有 unzip，请先把压缩包解压，再把里面的私钥文件路径给我"
    fi
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
  if [ "$PWDIALOG" = 1 ]; then
    PWFILE="$TMP/pw"
    ask_password_dialog "$HOST" > "$PWFILE" || fail "密码框被取消，或者这台电脑弹不出密码框（可以改用 --password-prompt 在终端里输入）"
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
        'umask 077; mkdir -p ~/.ssh; IFS= read -r K; touch ~/.ssh/authorized_keys; grep -qxF "$K" ~/.ssh/authorized_keys || printf "%s\n" "$K" >> ~/.ssh/authorized_keys
         if [ "$(id -u)" = 0 ] && /usr/sbin/sshd -T 2>/dev/null | grep -qi "^pubkeyauthentication no"; then
           cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak-xxd-pubkey
           sed -i -E "s/^[[:space:]]*PubkeyAuthentication[[:space:]]+no[[:space:]]*$/PubkeyAuthentication yes/I" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null
           /usr/sbin/sshd -t && { systemctl reload ssh 2>/dev/null || systemctl reload sshd 2>/dev/null || systemctl restart ssh; }
           echo "XXD_PUBKEY_ENABLED" >&2
         fi' \
        < "$IDFILE.pub" 2>"$TMP/err" \
    || fail "密码登录失败：$(tail -n 2 "$TMP/err" | tr '\n' ' ')（密码错误、服务商要求首次改密码，或服务器禁止了密码登录）"
  if grep -q XXD_PUBKEY_ENABLED "$TMP/err"; then
    say "服务器原本关闭了 SSH 密钥登录（服务商镜像默认），已打开（原配置备份为 sshd_config.bak-xxd-pubkey）"
  fi
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
# a non-22 port is stored as [host]:port, so the plain-host lookup finds nothing; never let that abort the script
fp=$( { ssh-keygen -F "[$HOST]:$PORT" -l; ssh-keygen -F "$HOST" -l; } 2>/dev/null | grep -v '^#' | awk '{print $2" "$NF}' | head -n1) || true
say "完成：以后用 ssh $ALIAS 登录（密钥：~${IDFILE#"$HOME"}）"
[ -n "$fp" ] && say "服务器主机指纹：$fp"
exit 0
