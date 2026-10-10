#!/usr/bin/env python3
"""小小东 VPS 服务器部署工具。

在一台全新的 Debian / Ubuntu VPS 上以 root 运行。每个阶段都可重复执行：已完成的部分会跳过，
失败后修好原因再跑同一个阶段即可。凭据只写入 /etc/xxd-vps/credentials.json（0600），
除 `export` 外，任何阶段都不会把密码、Key、订阅路径打印到终端。

    python3 xxd-vps.py init --ip 1.2.3.4 --alias bwg --timezone America/Los_Angeles
    python3 xxd-vps.py all          # base → cert → xui → sub → cliproxy → maint → verify
    python3 xxd-vps.py verify
    python3 xxd-vps.py export       # 仅在把输出重定向到本机文件时使用
"""
import argparse, base64, datetime, hashlib, http.client, ipaddress, json, os, pathlib, re, secrets
import shutil, socket, sqlite3, ssl, string, subprocess, sys, tarfile, tempfile, time, urllib.error
import urllib.parse, urllib.request, uuid, zipfile

HERE = pathlib.Path(__file__).resolve().parent
FILES = HERE / 'files'
ETC = pathlib.Path('/etc/xxd-vps')
DEPLOY = ETC / 'deploy.json'
CREDS = ETC / 'credentials.json'
OPT = pathlib.Path('/opt/xxd-vps')
RULES = pathlib.Path('/var/lib/xxd-vps/rules')
BACKUPS = pathlib.Path('/var/backups/xxd-vps')
XUI = pathlib.Path('/usr/local/x-ui')
XUI_DB = pathlib.Path('/etc/x-ui/x-ui.db')
CERTBOT = OPT / 'certbot'
CPA_BIN = pathlib.Path('/opt/cli-proxy-api/cli-proxy-api')
CPA_CONF = pathlib.Path('/etc/cliproxyapi/config.yaml')
CPA_STATE = pathlib.Path('/var/lib/cliproxyapi')

# 已在生产环境验证的组合。Xray 26.9.x 起会拒绝不带 ML-KEM 的 ClientHello，Shadowrocket 连不上，
# 因此 3x-ui 自带的新内核要换成固定版本。升级前必须先在测试机上用 Shadowrocket 和 Mihomo 实测。
XUI_VERSION = 'v3.8.5'
XUI_SHA256 = {'amd64': '6a85c110a04a727613c933c54ae602b8d37dab8876c6e20a6d46623010dd9d3c',
              'arm64': '2dd601a32426fb19b0eafdffaead374a9cdb66be4dfb39407f9f50fa4e7234e7'}
XRAY_VERSION = 'v26.7.28'
XRAY_ASSET = {'amd64': ('Xray-linux-64.zip', '8195d909f1109b8f3d99eefe401a3c451d7bf4af71f24d3815420f77e5dd2a40'),
              'arm64': ('Xray-linux-arm64-v8a.zip', 'f5698bb218ada3b4022db26fafc39601c5f53b46b19eb76c9616325985807501')}

PORT = {'panel': 53998, 'sub': 2096, 'cliproxy': 8318, 'reality': 443, 'tls': 2443, 'http': 80,
        'xui_sub': 2095, 'sub_proxy': 2097, 'cliproxy_local': 8317, 'reality_target': 8443}
UA = 'xxd-vps/1'


# ---------------------------------------------------------------- helpers
def say(msg):
    print('[xxd-vps] ' + msg, flush=True)


def die(msg):
    print('[xxd-vps] 停止：' + msg, file=sys.stderr, flush=True)
    sys.exit(2)


def run(cmd, check=True, quiet=False, timeout=600, env=None, input=None):
    """Run a command; never echo its arguments (they may carry secrets)."""
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env, input=input)
    if check and p.returncode:
        tail = (p.stderr or p.stdout).strip().splitlines()[-5:]
        die(f'{pathlib.Path(cmd[0]).name} 退出码 {p.returncode}\n' + '\n'.join(tail))
    if not quiet and p.stdout.strip() and os.environ.get('XXD_VERBOSE'):
        print(p.stdout.strip())
    return p


def write(path, text, mode=0o644, owner=None):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.' + path.name + '.')
    with os.fdopen(fd, 'w') as f:
        f.write(text)
    os.chmod(tmp, mode)
    if owner:
        shutil.chown(tmp, *owner)
    os.replace(tmp, path)


def load(path):
    return json.loads(pathlib.Path(path).read_text())


def rand(n, alphabet=string.ascii_letters + string.digits):
    return ''.join(secrets.choice(alphabet) for _ in range(n))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def install_file(src, dest, mode=0o755):
    """Copy into the destination directory first, then rename: /tmp may be a different filesystem."""
    dest = pathlib.Path(dest)
    fd, tmp = tempfile.mkstemp(dir=dest.parent, prefix='.' + dest.name + '.')
    with os.fdopen(fd, 'wb') as out, open(src, 'rb') as inp:
        shutil.copyfileobj(inp, out)
    os.chmod(tmp, mode)
    os.replace(tmp, dest)


def download(url, dest):
    run(['curl', '--fail', '--silent', '--show-error', '--location', '--retry', '3', '--connect-timeout', '10',
         '--max-time', '300', '--user-agent', UA, '--output', str(dest), url])


def github_latest(repo):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/latest',
                                 headers={'User-Agent': UA, 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        rel = json.load(r)
    if rel.get('draft') or rel.get('prerelease') or not re.fullmatch(r'v\d+\.\d+\.\d+', rel.get('tag_name', '')):
        die(f'{repo} 最新版本信息异常')
    return rel


def asset_digest(rel, name):
    for a in rel.get('assets', []):
        if a['name'] == name and (a.get('digest') or '').startswith('sha256:'):
            return a['digest'][7:]
    return None


def arch():
    m = os.uname().machine
    return {'x86_64': 'amd64', 'aarch64': 'arm64'}.get(m) or die('不支持的 CPU 架构：' + m)


def systemctl(*args, check=True):
    return run(['systemctl', *args], check=check, quiet=True)


def active(unit):
    return subprocess.run(['systemctl', 'is-active', '--quiet', unit]).returncode == 0


def unit(name, text):
    write(f'/etc/systemd/system/{name}', text)


def deploy():
    if not DEPLOY.exists():
        die('还没有初始化，请先运行 init')
    return load(DEPLOY)


def creds():
    return load(CREDS)


def save_creds(c):
    write(CREDS, json.dumps(c, indent=2, ensure_ascii=False), 0o600)


def mark(phase, **info):
    d = deploy()
    d.setdefault('done', {})[phase] = dict(info, at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'))
    write(DEPLOY, json.dumps(d, indent=2, ensure_ascii=False), 0o600)


def https_get(host, port, path, headers=None, timeout=10):
    """GET over HTTPS with full certificate verification against the server IP."""
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
    conn.request('GET', path, headers=headers or {'User-Agent': UA})
    r = conn.getresponse()
    body = r.read()
    conn.close()
    return r.status, r.headers, body


def local_ipv4s():
    out = run(['ip', '-j', '-4', 'address', 'show'], quiet=True).stdout
    return {a['local'] for x in json.loads(out) for a in x.get('addr_info', [])}


def public_ipv4():
    for url in ('https://api.ipify.org', 'https://ifconfig.me/ip', 'https://ipv4.icanhazip.com'):
        try:
            p = subprocess.run(['curl', '-4', '-fsS', '--max-time', '8', url], capture_output=True, text=True)
            ip = p.stdout.strip()
            ipaddress.IPv4Address(ip)
            return ip
        except Exception:
            continue
    return None


# ---------------------------------------------------------------- init
def cmd_init(a):
    if os.geteuid() != 0:
        die('需要 root 权限运行')
    try:
        ipaddress.IPv4Address(a.ip)
    except ValueError:
        die('--ip 必须是服务器的公网 IPv4')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9-]{0,30}', a.alias):
        die('--alias 只能用字母、数字和连字符，并以字母开头')
    if not pathlib.Path('/usr/share/zoneinfo/' + a.timezone).exists():
        die('无效时区：' + a.timezone)
    osr = dict(l.split('=', 1) for l in pathlib.Path('/etc/os-release').read_text().splitlines() if '=' in l)
    os_id = osr.get('ID', '').strip('"')
    if os_id not in ('ubuntu', 'debian'):
        die(f'目前只支持 Ubuntu / Debian，这台是 {os_id}。请在服务商后台重装为 Ubuntu 24.04 LTS 或 Debian 12/13')
    if sys.version_info < (3, 10):
        die('系统 Python 低于 3.10，证书工具无法安装；请重装为 Ubuntu 22.04+ 或 Debian 12+')
    arch()
    # 只操作用户指定的这台服务器
    if a.ip not in local_ipv4s() and public_ipv4() != a.ip:
        die(f'这台机器的公网 IP 不是 {a.ip}，可能连错了服务器')
    if DEPLOY.exists():
        old = load(DEPLOY)
        if old['ip'] != a.ip:
            die('这台服务器已按另一个 IP 初始化过')
    elif XUI_DB.exists():
        die('检测到已有的 3x-ui 数据库（不是本工具创建的）。为避免覆盖别人的配置，已停止')
    mem = int(re.search(r'MemTotal:\s+(\d+)', pathlib.Path('/proc/meminfo').read_text()).group(1)) // 1024
    if mem < 900:
        say(f'提示：内存只有 {mem} MB，CLIProxyAPI 并发较多时余量很小，建议 2 GB')
    ssh_port = a.ssh_port or int(os.environ.get('SSH_CONNECTION', '0 0 0 22').split()[3])
    d = {'ip': a.ip, 'alias': a.alias, 'timezone': a.timezone, 'ssh_port': ssh_port,
         'quota_gb': a.quota_gb, 'reset_day': a.reset_day, 'os': f"{os_id} {osr.get('VERSION_ID', '').strip(chr(34))}",
         'arch': arch(), 'memory_mb': mem, 'done': load(DEPLOY).get('done', {}) if DEPLOY.exists() else {}}
    ETC.mkdir(mode=0o700, exist_ok=True)
    write(DEPLOY, json.dumps(d, indent=2, ensure_ascii=False), 0o600)
    if not CREDS.exists():
        name = a.alias
        save_creds({
            'panel_username': 'u' + rand(11).lower(), 'panel_password': rand(24),
            'panel_path': '/' + rand(18) + '/',
            'sub_path': '/' + rand(14) + '/', 'clash_path': '/' + rand(14) + '/', 'json_path': '/' + rand(14) + '/',
            'sub_id_clash': rand(16).lower(), 'sub_id_mobile': rand(16).lower(),
            'uuid_clash': str(uuid.uuid4()), 'uuid_mobile': str(uuid.uuid4()),
            'short_id': secrets.token_hex(8),
            'reality_name': f'{name}-Reality', 'tls_name': f'{name}-TLS',
            'email_clash': f'{name}-openclash', 'email_mobile': f'{name}-shadowrocket',
            'cliproxy_management_key': rand(32), 'cliproxy_api_key': 'sk-' + rand(40),
        })
        say('已为这台服务器生成全新的独立凭据（不会显示在终端）')
    else:
        say('沿用这台服务器已有的凭据')
    say(f"初始化完成：{d['os']} / {d['arch']} / {mem} MB / SSH 端口 {ssh_port}")


# ---------------------------------------------------------------- base
SSHD_DROPIN = """# 小小东 VPS：只允许密钥登录。文件名以 01 开头，保证先于云镜像自带的 50-cloud-init.conf 生效。
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
UseDNS no
"""

SYSCTL = """net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
net.ipv4.tcp_mtu_probing=1
net.ipv4.tcp_slow_start_after_idle=0
net.core.rmem_max=16777216
net.core.wmem_max=16777216
"""


def cmd_base(a):
    d = deploy()
    say('时区与时间同步')
    run(['timedatectl', 'set-timezone', d['timezone']])
    run(['timedatectl', 'set-ntp', 'true'], check=False)

    say('安装系统依赖（apt）')
    env = dict(os.environ, DEBIAN_FRONTEND='noninteractive')
    run(['apt-get', 'update', '-q'], env=env, timeout=900)
    run(['apt-get', 'install', '-y', '-q', 'curl', 'ca-certificates', 'nginx', 'python3-venv', 'python3-yaml',
         'ufw', 'openssl', 'tar', 'iproute2'], env=env, timeout=1800)

    say('网络调优（BBR + fq）')
    run(['modprobe', 'tcp_bbr'], check=False)
    write('/etc/sysctl.d/99-xxd-vps.conf', SYSCTL)
    run(['sysctl', '-p', '/etc/sysctl.d/99-xxd-vps.conf'], check=False)

    for user, home in (('cliproxy', str(CPA_STATE)), ('xxd-sub', '/var/lib/xxd-vps-sub')):
        if subprocess.run(['id', user], capture_output=True).returncode:
            run(['useradd', '--system', '--home-dir', home, '--shell', '/usr/sbin/nologin', user])

    say('防火墙（UFW）')
    run(['ufw', 'allow', f"{d['ssh_port']}/tcp"])
    for p in ('http', 'reality', 'tls', 'sub', 'cliproxy', 'panel'):
        run(['ufw', 'allow', f'{PORT[p]}/tcp'])
    run(['ufw', 'default', 'deny', 'incoming'])
    run(['ufw', 'default', 'allow', 'outgoing'])
    run(['ufw', '--force', 'enable'])

    say('SSH：关闭密码登录，只保留密钥')
    keys = pathlib.Path('/root/.ssh/authorized_keys')
    if not keys.exists() or not keys.read_text().strip():
        die('root 没有可用的 authorized_keys，关闭密码登录会把你锁在外面。请先完成本机的密钥登录')
    main = pathlib.Path('/etc/ssh/sshd_config')
    text = main.read_text()
    if not re.search(r'^\s*Include\s+/etc/ssh/sshd_config\.d/\*\.conf', text, re.M):
        write(main, 'Include /etc/ssh/sshd_config.d/*.conf\n' + text, 0o644)
    write('/etc/ssh/sshd_config.d/01-xxd-vps.conf', SSHD_DROPIN, 0o644)
    run(['sshd', '-t'])
    eff = run(['sshd', '-T'], quiet=True).stdout.lower()
    if 'passwordauthentication no' not in eff or 'kbdinteractiveauthentication no' not in eff:
        die('sshd 生效配置仍允许密码登录，请检查 /etc/ssh/sshd_config.d/ 下的其他文件')
    for svc in ('ssh', 'sshd'):
        if subprocess.run(['systemctl', 'reload', svc], capture_output=True).returncode == 0:
            break
    mark('base')
    say('base 完成')


# ---------------------------------------------------------------- cert + nginx
def cert_paths(ip):
    live = pathlib.Path('/etc/letsencrypt/live') / ip
    return live / 'fullchain.pem', live / 'privkey.pem'


def cert_ok(ip, seconds=86400):
    full, _ = cert_paths(ip)
    if not full.exists():
        return False
    ok_ip = subprocess.run(['openssl', 'x509', '-in', str(full), '-noout', '-checkip', ip], capture_output=True).returncode == 0
    ok_time = subprocess.run(['openssl', 'x509', '-in', str(full), '-noout', '-checkend', str(seconds)], capture_output=True).returncode == 0
    return ok_ip and ok_time


def nginx_reload():
    run(['nginx', '-t'])
    if active('nginx'):
        systemctl('reload', 'nginx')
    else:
        systemctl('enable', '--now', 'nginx')


def cmd_cert(a):
    d = deploy()
    ip = d['ip']
    say('Nginx：80 端口只用于证书校验')
    pathlib.Path('/var/www/acme').mkdir(parents=True, exist_ok=True)
    for p in ('/etc/nginx/sites-enabled/default',):
        pathlib.Path(p).unlink(missing_ok=True)
    write('/etc/nginx/sites-available/xxd-vps-acme', f"""server {{
    listen 80 default_server;
    server_name {ip};
    access_log off;
    location ^~ /.well-known/acme-challenge/ {{ root /var/www/acme; }}
    location / {{ return 404; }}
}}
""")
    link = pathlib.Path('/etc/nginx/sites-enabled/xxd-vps-acme')
    if not link.exists():
        link.symlink_to('/etc/nginx/sites-available/xxd-vps-acme')
    nginx_reload()

    say('Certbot 5.x（独立虚拟环境，不用系统旧版）')
    if not (CERTBOT / 'bin/certbot').exists():
        run([sys.executable, '-m', 'venv', str(CERTBOT)])
        run([str(CERTBOT / 'bin/pip'), 'install', '-q', '--upgrade', 'pip'], timeout=900)
        run([str(CERTBOT / 'bin/pip'), 'install', '-q', 'certbot>=5.4,<6'], timeout=900)
    ver = run([str(CERTBOT / 'bin/certbot'), '--version'], quiet=True).stdout.strip()

    if not cert_ok(ip):
        say(f'申请 Let\'s Encrypt IP 证书（{ver}，shortlived）')
        p = run([str(CERTBOT / 'bin/certbot'), 'certonly', '--non-interactive', '--agree-tos',
                 '--register-unsafely-without-email', '--webroot', '-w', '/var/www/acme',
                 '--ip-address', ip, '--cert-name', ip, '--preferred-profile', 'shortlived',
                 '--key-type', 'ecdsa', '--preferred-challenges', 'http'], check=False)
        if p.returncode or not cert_ok(ip, 3600):
            tail = '\n'.join((p.stderr or p.stdout).strip().splitlines()[-8:])
            die('IP 证书申请失败（不会改用自签名证书继续）。常见原因：服务商安全组没放行 TCP 80。\n' + tail)
    else:
        say('IP 证书已存在且有效')

    hook = pathlib.Path('/etc/letsencrypt/renewal-hooks/deploy/20-xxd-vps')
    write(hook, '#!/bin/sh\nset -eu\nnginx -t\nsystemctl reload nginx\nsystemctl try-restart x-ui.service\n', 0o755)
    unit('xxd-vps-cert-renew.service', f"""[Unit]
Description=Renew the trusted IP certificate
Wants=network-online.target
After=network-online.target nginx.service
[Service]
Type=oneshot
ExecStart={CERTBOT}/bin/certbot -q renew --no-random-sleep-on-renew
""")
    unit('xxd-vps-cert-renew.timer', """[Unit]
Description=Check IP certificate renewal every six hours
[Timer]
OnCalendar=*-*-* 00,06,12,18:00:00 UTC
RandomizedDelaySec=600
Persistent=true
[Install]
WantedBy=timers.target
""")
    systemctl('daemon-reload')
    systemctl('enable', '--now', 'xxd-vps-cert-renew.timer')

    full, key = cert_paths(ip)
    say('Nginx：订阅 2096、Reality 回落 127.0.0.1:8443、CLIProxyAPI 8318')
    write('/etc/nginx/conf.d/xxd-vps-websocket.conf',
          'map $http_upgrade $xxd_connection_upgrade { default upgrade; "" close; }\n')
    tls = f"""    ssl_certificate {full};
    ssl_certificate_key {key};
    ssl_protocols TLSv1.2 TLSv1.3;
    access_log off;"""
    write('/etc/nginx/sites-available/xxd-vps', f"""# Reality 回落目标：未通过 Reality 认证的连接看到的是本机真实的 IP 证书站点
server {{
    listen 127.0.0.1:{PORT['reality_target']} ssl;
    server_name {ip};
{tls}
    location / {{ return 404; }}
}}
# 订阅入口：只转发已知订阅路径，规则镜像直接由 Nginx 提供
server {{
    listen {PORT['sub']} ssl;
    server_name {ip};
{tls}
    location ^~ /rules/ {{ alias {RULES}/; autoindex off; default_type text/yaml; limit_except GET {{ deny all; }} }}
    location / {{ proxy_pass http://127.0.0.1:{PORT['sub_proxy']}; proxy_set_header Host {ip}; proxy_set_header X-Forwarded-Proto https; proxy_read_timeout 30s; }}
}}
# CLIProxyAPI：管理中心 + /v1 接口，长连接和流式输出不缓冲
server {{
    listen {PORT['cliproxy']} ssl;
    server_name {ip};
{tls}
    client_max_body_size 256m;
    location = / {{ return 302 /management.html; }}
    location / {{
        proxy_pass http://127.0.0.1:{PORT['cliproxy_local']};
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $xxd_connection_upgrade;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }}
}}
""")
    link = pathlib.Path('/etc/nginx/sites-enabled/xxd-vps')
    if not link.exists():
        link.symlink_to('/etc/nginx/sites-available/xxd-vps')
    RULES.mkdir(parents=True, exist_ok=True)
    nginx_reload()
    mark('cert', certbot=ver)
    say('cert 完成')


# ---------------------------------------------------------------- 3x-ui
class Panel:
    """3x-ui API over HTTPS with an API token (no browser session, no CSRF)."""

    def __init__(self, ip, path, token):
        self.base = f'https://{ip}:{PORT["panel"]}{path}panel/api/'
        self.token = token
        self.ctx = ssl.create_default_context()

    def call(self, method, path, data=None):
        body = json.dumps(data).encode() if data is not None else None
        req = urllib.request.Request(self.base + path, data=body, method=method, headers={
            'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json', 'User-Agent': UA})
        try:
            with urllib.request.urlopen(req, timeout=30, context=self.ctx) as r:
                res = json.load(r)
        except urllib.error.HTTPError as e:
            die(f'3x-ui API {path} 返回 HTTP {e.code}')
        return res

    def ok(self, method, path, data=None):
        res = self.call(method, path, data)
        if not res.get('success'):
            die(f"3x-ui API {path} 失败：{res.get('msg')}")
        return res.get('obj')


def install_xui():
    ar = arch()
    name = f'x-ui-linux-{ar}.tar.gz'
    with tempfile.TemporaryDirectory(prefix='xxd-xui-') as td:
        td = pathlib.Path(td)
        say(f'下载 3x-ui {XUI_VERSION}（SHA-256 校验）')
        download(f'https://github.com/MHSanaei/3x-ui/releases/download/{XUI_VERSION}/{name}', td / name)
        if sha256(td / name) != XUI_SHA256[ar]:
            die('3x-ui 安装包校验失败')
        with tarfile.open(td / name) as t:
            for m in t.getmembers():
                if m.name.startswith('/') or '..' in pathlib.PurePosixPath(m.name).parts or not (m.isfile() or m.isdir()):
                    die('3x-ui 安装包结构异常')
            try:
                t.extractall(td, filter='data')
            except TypeError:
                t.extractall(td)
        if XUI.exists():
            shutil.rmtree(XUI)
        shutil.move(str(td / 'x-ui'), str(XUI))
    for p in [XUI / 'x-ui', *XUI.glob('bin/xray-linux-*'), XUI / 'x-ui.sh']:
        if p.exists():
            p.chmod(0o755)


def pin_xray():
    ar = arch()
    binary = XUI / 'bin' / f'xray-linux-{ar}'
    first = (run([str(binary), 'version'], check=False, quiet=True).stdout.splitlines() or [''])[0]
    if XRAY_VERSION.lstrip('v') in first:
        return
    asset, digest = XRAY_ASSET[ar]
    with tempfile.TemporaryDirectory(prefix='xxd-xray-') as td:
        td = pathlib.Path(td)
        say(f'固定 Xray 内核为 {XRAY_VERSION}（兼容 Shadowrocket 与 Mihomo）')
        download(f'https://github.com/XTLS/Xray-core/releases/download/{XRAY_VERSION}/{asset}', td / asset)
        if sha256(td / asset) != digest:
            die('Xray 安装包校验失败')
        with zipfile.ZipFile(td / asset) as z:
            (td / 'xray').write_bytes(z.read('xray'))
        install_file(td / 'xray', binary)
    write(ETC / 'xray-pin.json', json.dumps({'version': XRAY_VERSION, 'sha256': sha256(binary),
          'reason': 'Xray 26.9.x rejects ClientHello without ML-KEM (Shadowrocket); 26.7.28 verified with Shadowrocket and Mihomo'}, indent=2))


def xui_unit():
    unit('x-ui.service', f"""[Unit]
Description=3x-ui panel and Xray
After=network-online.target nginx.service
Wants=network-online.target
[Service]
Type=simple
WorkingDirectory={XUI}
ExecStart={XUI}/x-ui
ExecReload=/bin/kill -USR1 $MAINPID
Restart=on-failure
RestartSec=5s
UMask=0077
LimitNOFILE=262144
[Install]
WantedBy=multi-user.target
""")
    systemctl('daemon-reload')


def render_clash(ip, c):
    t = (FILES / 'clash-template.yaml').read_text()
    return t.replace('{{SERVER_IP}}', ip).replace('{{REALITY_NAME}}', c['reality_name']).replace('{{TLS_NAME}}', c['tls_name'])


def xui_settings(d, c):
    ip = d['ip']
    full, key = cert_paths(ip)
    sub_base = f'https://{ip}:{PORT["sub"]}'
    template = json.loads((FILES / 'xray-template.json').read_text())
    settings = {
        'webPort': str(PORT['panel']), 'webListen': '', 'webDomain': '', 'webBasePath': c['panel_path'],
        'webCertFile': str(full), 'webKeyFile': str(key), 'sessionMaxAge': '360',
        'trustedProxyCIDRs': '127.0.0.1/32,::1/128', 'timeLocation': d['timezone'], 'remarkTemplate': '{{INBOUND}}',
        'subEnable': 'true', 'subListen': '127.0.0.1', 'subPort': str(PORT['xui_sub']), 'subDomain': ip,
        'subCertFile': '', 'subKeyFile': '', 'subPath': c['sub_path'], 'subURI': sub_base + c['sub_path'],
        'subJsonEnable': 'true', 'subJsonAlwaysArray': 'true', 'subJsonPath': c['json_path'], 'subJsonURI': sub_base + c['json_path'],
        'subClashEnable': 'true', 'subClashPath': c['clash_path'], 'subClashURI': sub_base + c['clash_path'],
        'subClashEnableRouting': 'true', 'subClashAutoDetect': 'true', 'subClashUserAgentRegex': '(?i)(clash|mihomo)',
        'subClashRules': render_clash(ip, c), 'subProfileMode': 'none',
        'subUpdates': '12', 'subTitle': f"{d['alias']}", 'subEncrypt': 'true',
        'xrayTemplateConfig': json.dumps(template, separators=(',', ':')), 'restartXrayOnClientDisable': 'true',
    }
    db = sqlite3.connect(str(XUI_DB))
    try:
        for k, v in settings.items():
            if db.execute('select 1 from settings where key=?', (k,)).fetchone():
                db.execute('update settings set value=? where key=?', (v, k))
            else:
                db.execute('insert into settings(key,value) values(?,?)', (k, v))
        db.commit()
    finally:
        db.close()
    XUI_DB.chmod(0o600)


def reality_keys():
    out = run([str(XUI / 'bin' / f'xray-linux-{arch()}'), 'x25519'], quiet=True).stdout
    priv = re.search(r'Private\s*key:\s*(\S+)', out, re.I)
    pub = re.search(r'(?:Public\s*key|Password(?:\s*\(PublicKey\))?):\s*(\S+)', out, re.I)
    if not priv or not pub:
        die('无法解析 xray x25519 输出')
    return priv.group(1), pub.group(1)


def wait_panel(ip, path, seconds=60):
    for _ in range(seconds):
        try:
            status, _, _ = https_get(ip, PORT['panel'], path)
            if status in (200, 301, 302, 307, 308):
                return
        except Exception:
            pass
        time.sleep(1)
    die('3x-ui 面板没有在 HTTPS 53998 上响应')


def xray_layout_problem(c):
    """Reality: OpenClash 身份带 vision、Shadowrocket 身份不带；TLS 入口都不带 flow；空 SNI 可用；出站只走 IPv4。"""
    try:
        conf = json.loads((XUI / 'bin/config.json').read_text())
    except (OSError, ValueError):
        return '读不到 config.json'
    ib = {i.get('port'): i for i in conf.get('inbounds', [])}
    want = {PORT['reality']: {c['email_clash']: 'xtls-rprx-vision', c['email_mobile']: ''},
            PORT['tls']: {c['email_clash']: '', c['email_mobile']: ''}}
    for port, flows in want.items():
        if port not in ib:
            return f'缺少 {port} 入口'
        got = {x.get('email'): x.get('flow', '') for x in ib[port]['settings'].get('clients', [])}
        if got != flows:
            return f'{port} 入口的身份或 flow 不对'
    rs = ib[PORT['reality']]['streamSettings']['realitySettings']
    if '' not in rs.get('serverNames', []):
        return 'Reality 未接受空 SNI'
    if rs.get('minClientVer') != '1.0.0':
        return 'Reality 没有放开客户端最低版本（Mihomo / Shadowrocket 会被拒）'
    if not any(o.get('tag') == 'direct-ipv4' for o in conf.get('outbounds', [])):
        return '缺少 IPv4 出站'
    return None


def cmd_xui(a):
    d, c = deploy(), creds()
    ip = d['ip']
    if not cert_ok(ip, 3600):
        die('证书不可用，请先完成 cert 阶段')
    fresh = not (XUI / 'x-ui').exists()
    if fresh:
        install_xui()
    pin_xray()
    xui_unit()
    if active('x-ui'):
        systemctl('stop', 'x-ui')
    full, key = cert_paths(ip)
    run([str(XUI / 'x-ui'), 'setting', '-username', c['panel_username'], '-password', c['panel_password'],
         '-port', str(PORT['panel']), '-webBasePath', c['panel_path'], '-webCert', str(full), '-webCertKey', str(key)],
        quiet=True, timeout=60)
    xui_settings(d, c)
    systemctl('enable', '--now', 'x-ui')
    wait_panel(ip, c['panel_path'])

    out = run([str(XUI / 'x-ui'), 'setting', '-getApiToken', '-tokenName', 'xxd-vps-deploy'],
              quiet=True, timeout=60).stdout
    m = re.search(r'apiToken:\s*(\S+)', out)
    if not m:
        die('无法获取 3x-ui API Token')
    api = Panel(ip, c['panel_path'], m.group(1))

    if 'reality_private' not in c:
        c['reality_private'], c['reality_public'] = reality_keys()
        save_creds(c)

    inbounds = api.ok('GET', 'inbounds/list') or []
    by_port = {int(i['port']): i for i in inbounds}
    sniff = {'enabled': True, 'destOverride': ['http', 'tls', 'quic'], 'routeOnly': True}
    if PORT['reality'] not in by_port:
        say('创建 Reality 主入口 443（自回落到本机 IP 证书站点，不借用第三方网站）')
        by_port[PORT['reality']] = api.ok('POST', 'inbounds/add', {
            'enable': True, 'remark': c['reality_name'], 'listen': '', 'port': PORT['reality'], 'protocol': 'vless',
            'expiryTime': 0, 'total': 0, 'trafficReset': 'never', 'shareAddrStrategy': 'custom', 'shareAddr': ip,
            'settings': {'clients': [], 'decryption': 'none', 'encryption': 'none', 'fallbacks': []},
            'streamSettings': {'network': 'tcp', 'security': 'reality', 'tcpSettings': {'header': {'type': 'none'}},
                               'realitySettings': {'show': False, 'xver': 0, 'target': f"127.0.0.1:{PORT['reality_target']}",
                                                   # 客户端按规范不会把 IP 当作 SNI 发送，必须同时接受空 SNI
                                                   'serverNames': [ip, ''], 'privateKey': c['reality_private'],
                                                   'shortIds': [c['short_id']],
                                                   'settings': {'publicKey': c['reality_public'], 'fingerprint': 'chrome',
                                                                'serverName': ip, 'spiderX': '/'},
                                                   # Xray 26.x 默认拒绝低于 v26.3.27 的客户端，Mihomo / Shadowrocket 会被拒
                                                   'minClientVer': '1.0.0'}},
            'sniffing': sniff})
    if PORT['tls'] not in by_port:
        say('创建 TLS 备用入口 2443（同一张 IP 证书）')
        by_port[PORT['tls']] = api.ok('POST', 'inbounds/add', {
            'enable': True, 'remark': c['tls_name'], 'listen': '', 'port': PORT['tls'], 'protocol': 'vless',
            'expiryTime': 0, 'total': 0, 'trafficReset': 'never', 'shareAddrStrategy': 'custom', 'shareAddr': ip,
            'disableFlow': True,
            'settings': {'clients': [], 'decryption': 'none', 'encryption': 'none', 'fallbacks': []},
            'streamSettings': {'network': 'tcp', 'security': 'tls', 'tcpSettings': {'header': {'type': 'none'}},
                               'tlsSettings': {'serverName': ip, 'minVersion': '1.2', 'alpn': ['h2', 'http/1.1'],
                                               'certificates': [{'certificateFile': str(full), 'keyFile': str(key)}],
                                               'settings': {'fingerprint': 'chrome'}}},
            'sniffing': sniff})
    ids = [int(by_port[PORT['reality']]['id']), int(by_port[PORT['tls']]['id'])]
    for email, cid, sub, flow, note in ((c['email_clash'], c['uuid_clash'], c['sub_id_clash'], 'xtls-rprx-vision', 'OpenClash / Mihomo / Clash Verge Rev'),
                                         (c['email_mobile'], c['uuid_mobile'], c['sub_id_mobile'], '', 'Shadowrocket')):
        found = api.call('GET', 'clients/get/' + urllib.parse.quote(email))
        if found.get('success'):
            missing = [i for i in ids if i not in ((found.get('obj') or {}).get('inboundIds') or [])]
            if missing:
                say(f'把订阅身份重新挂到入口上：{note}')
                api.ok('POST', 'clients/' + urllib.parse.quote(email) + '/attach', {'inboundIds': missing})
                # 重新挂载不会带上 flow，需要再写一次
                api.ok('POST', 'clients/update/' + urllib.parse.quote(email),
                       {'email': email, 'id': cid, 'subId': sub, 'flow': flow, 'totalGB': 0, 'expiryTime': 0,
                        'enable': True, 'limitIp': 0, 'comment': note})
            continue
        say(f'创建订阅身份：{note}')
        api.ok('POST', 'clients/add', {'client': {'email': email, 'id': cid, 'subId': sub, 'flow': flow, 'totalGB': 0,
                                                  'expiryTime': 0, 'enable': True, 'limitIp': 0, 'comment': note},
                                       'inboundIds': ids})
    api.ok('POST', 'server/restartXrayService')
    for _ in range(20):
        listening = run(['ss', '-Hlnt'], quiet=True).stdout
        if f":{PORT['reality']} " in listening and f":{PORT['tls']} " in listening:
            break
        time.sleep(1)
    else:
        die('Xray 没有监听 443 / 2443')
    problem = xray_layout_problem(c)
    if problem:
        die('生成的 Xray 配置不符合预期：' + problem)
    mark('xui', version=XUI_VERSION, xray=XRAY_VERSION)
    say('xui 完成')


# ---------------------------------------------------------------- subscription + rules
def served_clash(d, c):
    st, _, body = https_get(d['ip'], PORT['sub'], c['clash_path'] + c['sub_id_clash'], {'User-Agent': 'mihomo'})
    return body.decode('utf-8', 'replace') if st == 200 else ''


def rule_problems(clash_text):
    """客户端实际拿到的订阅里，每个 rule-provider 声明的 behavior 必须和本机镜像文件的格式一致，否则会丢规则。"""
    import yaml
    try:
        conf = yaml.safe_load(clash_text) or {}
    except yaml.YAMLError:
        return ['订阅不是合法 YAML']
    if not conf.get('rule-providers'):
        return ['订阅里没有 rule-providers']
    bad = []
    for name, p in conf.get('rule-providers', {}).items():
        f = RULES / p['url'].rsplit('/', 1)[1]
        if not f.exists():
            bad.append(name + ' 缺文件')
            continue
        if p.get('format') == 'mrs':
            continue
        kinds = set()
        for x in (yaml.safe_load(f.read_text()) or {}).get('payload') or []:
            try:
                ipaddress.ip_network(str(x), strict=False)
                kinds.add('ipcidr')
            except ValueError:
                kinds.add('classical' if ',' in str(x) else 'domain')
        if not kinds or kinds - {p['behavior']}:
            bad.append(f"{name}（声明 {p['behavior']}，实际 {'/'.join(sorted(kinds)) or '空'}）")
    return bad


def cmd_sub(a):
    d, c = deploy(), creds()
    ip = d['ip']
    say('规则镜像：从公开上游下载到本机，客户端只访问你自己的服务器')
    OPT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FILES / 'rule-sources.json', ETC / 'rule-sources.json')
    RULES.mkdir(parents=True, exist_ok=True)
    for f in (FILES / 'rules').iterdir():
        shutil.copy2(f, RULES / f.name)
        (RULES / f.name).chmod(0o644)
    shutil.copy2(FILES / 'xxd-vps-refresh-rules', '/usr/local/sbin/xxd-vps-refresh-rules')
    os.chmod('/usr/local/sbin/xxd-vps-refresh-rules', 0o755)
    p = run(['/usr/local/sbin/xxd-vps-refresh-rules'], check=False, timeout=900)
    if p.returncode:
        die('规则下载不完整：' + p.stdout.strip().splitlines()[-1])
    if any(l.startswith('WARN') for l in p.stdout.splitlines()):
        say('部分规则本次没下载到，沿用了上一份')

    say('订阅中间层：只放行已知订阅路径，并在客户端显示本月流量')
    iface = json.loads(run(['ip', '-j', 'route', 'show', 'default'], quiet=True).stdout)[0]['dev']
    cfg = {'interface': iface, 'total_bytes': int(d['quota_gb']) * 1024 ** 3 if d.get('quota_gb') else 0,
           'reset_day': d.get('reset_day'), 'upstream': f"http://127.0.0.1:{PORT['xui_sub']}", 'upstream_host': ip,
           'paths': [c['sub_path'], c['json_path'], c['clash_path']], 'profile_title': d['alias']}
    write(ETC / 'sub-proxy.json', json.dumps(cfg, indent=2), 0o640, owner=('root', 'xxd-sub'))
    ETC.chmod(0o711)
    (OPT / 'sub-proxy').mkdir(parents=True, exist_ok=True)
    shutil.copy2(FILES / 'sub-proxy.py', OPT / 'sub-proxy/server.py')
    unit('xxd-vps-sub.service', f"""[Unit]
Description=Subscription front with traffic usage display
After=network-online.target x-ui.service
Wants=network-online.target x-ui.service
[Service]
User=xxd-sub
Group=xxd-sub
ExecStart=/usr/bin/python3 {OPT}/sub-proxy/server.py
Restart=always
RestartSec=3
UMask=0077
StateDirectory=xxd-vps-sub
StateDirectoryMode=0700
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
[Install]
WantedBy=multi-user.target
""")
    systemctl('daemon-reload')
    systemctl('enable', 'xxd-vps-sub')
    systemctl('restart', 'xxd-vps-sub')
    time.sleep(2)
    check_subscriptions(d, c, fatal=True)
    bad = rule_problems(served_clash(d, c))
    if bad:
        die('订阅里的规则与本机镜像不一致：' + '；'.join(bad))
    mark('sub')
    say('sub 完成')


def check_subscriptions(d, c, fatal=False):
    ip, results = d['ip'], {}
    try:
        st, _, body = https_get(ip, PORT['sub'], c['clash_path'] + c['sub_id_clash'], {'User-Agent': 'mihomo'})
        text = body.decode('utf-8', 'replace')
        results['clash'] = st == 200 and c['reality_name'] in text and c['tls_name'] in text and 'AI-人工智能' in text
    except Exception:
        results['clash'] = False
    try:
        st, _, body = https_get(ip, PORT['sub'], c['sub_path'] + c['sub_id_mobile'], {'User-Agent': 'Shadowrocket'})
        links = base64.b64decode(body + b'=' * (-len(body) % 4)).decode('utf-8', 'replace')
        results['shadowrocket'] = st == 200 and links.count('vless://') >= 2
    except Exception:
        results['shadowrocket'] = False
    if fatal and not all(results.values()):
        die('订阅检查失败：' + json.dumps(results))
    return results


# ---------------------------------------------------------------- CLIProxyAPI
CPA_CONFIG = """# CLIProxyAPI — generated by xxd-vps. Nginx terminates HTTPS on {public_port}; the service listens locally.
config-version: 8
server:
  host: 127.0.0.1
  port: {local_port}
  trusted-proxies:
  - 127.0.0.1
  tls:
    enable: false
  discovery:
    enabled: false
management:
  allow-remote: true
  secret-key: {management_key}
  disable-control-panel: false
  # 管理中心页面由 cliproxy-auto-update 校验后更新，不让程序自己联网替换
  disable-auto-update-panel: true
  panel-github-repository: https://github.com/router-for-me/Cli-Proxy-API-Management-Center
access:
  api-keys:
  - {api_key}
oauth:
  auth-dir: {state}/auth
routing:
  strategy: round-robin
  retry:
    request-retry: 3
    max-retry-interval: 30
requests:
  proxy-url: ''
  streaming:
    keepalive-seconds: 15
    bootstrap-retries: 1
  nonstream-keepalive-interval: 15
plugins:
  enabled: true
  dir: {state}/plugins
observability:
  logs:
    debug: false
    logging-to-file: true
    logs-max-total-size-mb: 128
    error-logs-max-files: 10
    request-log: false
  usage:
    usage-statistics-enabled: true
  pprof:
    enable: false
"""


def cmd_cliproxy(a):
    d, c = deploy(), creds()
    owner = ('cliproxy', 'cliproxy')
    for p in (pathlib.Path('/etc/cliproxyapi'), CPA_STATE, CPA_STATE / 'auth', CPA_STATE / 'logs', CPA_STATE / 'plugins', CPA_STATE / 'static'):
        p.mkdir(parents=True, exist_ok=True)
        p.chmod(0o700)
        shutil.chown(p, *owner)
    if not CPA_BIN.exists():
        rel = github_latest('router-for-me/CLIProxyAPI')
        tag = rel['tag_name']
        name = f"CLIProxyAPI_{tag[1:]}_linux_{ {'amd64': 'amd64', 'arm64': 'aarch64'}[arch()] }.tar.gz"
        digest = asset_digest(rel, name)
        with tempfile.TemporaryDirectory(prefix='xxd-cpa-') as td:
            td = pathlib.Path(td)
            say(f'下载 CLIProxyAPI {tag}（SHA-256 校验）')
            download(f'https://github.com/router-for-me/CLIProxyAPI/releases/download/{tag}/{name}', td / name)
            if not digest:
                download(f'https://github.com/router-for-me/CLIProxyAPI/releases/download/{tag}/checksums.txt', td / 'sums')
                digest = next((l.split()[0] for l in (td / 'sums').read_text().splitlines() if l.split()[-1].lstrip('*') == name), None)
            if not digest or sha256(td / name) != digest:
                die('CLIProxyAPI 安装包校验失败')
            with tarfile.open(td / name) as t:
                m = [x for x in t.getmembers() if x.name.lstrip('./') == 'cli-proxy-api' and x.isfile()]
                if len(m) != 1:
                    die('CLIProxyAPI 安装包里找不到主程序')
                CPA_BIN.parent.mkdir(parents=True, exist_ok=True)
                with t.extractfile(m[0]) as src, open(td / 'bin', 'wb') as dst:
                    shutil.copyfileobj(src, dst)
            install_file(td / 'bin', CPA_BIN)
        CPA_BIN.parent.chmod(0o755)
    html = CPA_STATE / 'static/management.html'
    if not html.exists():
        rel = github_latest('router-for-me/Cli-Proxy-API-Management-Center')
        digest = asset_digest(rel, 'management.html')
        with tempfile.TemporaryDirectory(prefix='xxd-cpamc-') as td:
            tmp = pathlib.Path(td) / 'management.html'
            say(f"下载 Management Center {rel['tag_name']}")
            download(f"https://github.com/router-for-me/Cli-Proxy-API-Management-Center/releases/download/{rel['tag_name']}/management.html", tmp)
            if not digest or sha256(tmp) != digest:
                die('Management Center 校验失败')
            shutil.copy2(tmp, html)
        html.chmod(0o600)
        shutil.chown(html, *owner)
    if not CPA_CONF.exists():
        write(CPA_CONF, CPA_CONFIG.format(public_port=PORT['cliproxy'], local_port=PORT['cliproxy_local'], state=CPA_STATE,
                                          management_key=c['cliproxy_management_key'], api_key=c['cliproxy_api_key']),
              0o600, owner=owner)
    # 不设置 MemoryMax：并发高时人为的内存上限只会制造 OOM
    unit('cli-proxy-api.service', f"""[Unit]
Description=CLIProxyAPI
After=network-online.target
Wants=network-online.target
[Service]
User=cliproxy
Group=cliproxy
WorkingDirectory={CPA_STATE}
Environment=HOME={CPA_STATE}
Environment=MANAGEMENT_STATIC_PATH={CPA_STATE}/static
ExecStart={CPA_BIN} -config {CPA_CONF}
Restart=always
RestartSec=3
UMask=0077
LimitNOFILE=65536
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/etc/cliproxyapi {CPA_STATE}
[Install]
WantedBy=multi-user.target
""")
    systemctl('daemon-reload')
    systemctl('enable', 'cli-proxy-api')
    systemctl('restart', 'cli-proxy-api')
    for _ in range(30):
        if check_cliproxy(d, c):
            break
        time.sleep(1)
    else:
        die('CLIProxyAPI 公网 HTTPS /v1/models 检查失败')
    mark('cliproxy')
    say('cliproxy 完成（还没有上游账号，需要你在管理中心自己添加）')


def check_cliproxy(d, c):
    try:
        st, _, body = https_get(d['ip'], PORT['cliproxy'], '/v1/models',
                                {'Authorization': 'Bearer ' + c['cliproxy_api_key'], 'User-Agent': UA})
        return st == 200 and isinstance(json.loads(body).get('data'), list)
    except Exception:
        return False


# ---------------------------------------------------------------- maintenance
def cmd_maint(a):
    d = deploy()
    say('CLIProxyAPI 自动更新：每 30 分钟检查，校验 → 原子替换 → 健康检查 → 失败回滚')
    shutil.copy2(FILES / 'cliproxy-auto-update', '/usr/local/sbin/cliproxy-auto-update')
    os.chmod('/usr/local/sbin/cliproxy-auto-update', 0o755)
    write('/etc/cliproxy-auto-update/instances.json', json.dumps([{
        'service': 'cli-proxy-api.service', 'binary': str(CPA_BIN), 'config': str(CPA_CONF),
        'static_dir': str(CPA_STATE / 'static'), 'local_url': f"http://127.0.0.1:{PORT['cliproxy_local']}/v1/models",
        'public_url': f"https://{d['ip']}:{PORT['cliproxy']}/v1/models"}], indent=2), 0o600)
    unit('cliproxy-auto-update.service', """[Unit]
Description=CLIProxyAPI transactional auto-update
After=network-online.target
Wants=network-online.target
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/cliproxy-auto-update
TimeoutStartSec=15min
TimeoutStopSec=120s
UMask=0077
""")
    unit('cliproxy-auto-update.timer', """[Unit]
Description=CLIProxyAPI auto-update every 30 minutes
[Timer]
OnCalendar=*-*-* *:00,30:00 UTC
RandomizedDelaySec=120s
Persistent=true
Unit=cliproxy-auto-update.service
[Install]
WantedBy=timers.target
""")
    unit('xxd-vps-rules.service', """[Unit]
Description=Refresh local rule mirror
Wants=network-online.target
After=network-online.target
[Service]
Type=oneshot
UMask=0022
ExecStart=/usr/local/sbin/xxd-vps-refresh-rules
""")
    unit('xxd-vps-rules.timer', """[Unit]
Description=Daily rule mirror refresh
[Timer]
OnCalendar=daily
RandomizedDelaySec=1800
Persistent=true
[Install]
WantedBy=timers.target
""")
    # 把部署工具本身留在服务器上，供备份和复核使用
    OPT.mkdir(parents=True, exist_ok=True)
    if HERE != OPT / 'tool':
        if (OPT / 'tool').exists():
            shutil.rmtree(OPT / 'tool')
        shutil.copytree(HERE, OPT / 'tool')
    tool = pathlib.Path('/usr/local/sbin/xxd-vps')
    tool.unlink(missing_ok=True)
    tool.symlink_to(OPT / 'tool/xxd-vps.py')
    (OPT / 'tool/xxd-vps.py').chmod(0o755)
    unit('xxd-vps-backup.service', """[Unit]
Description=Daily configuration backup
[Service]
Type=oneshot
UMask=0077
ExecStart=/usr/local/sbin/xxd-vps backup
""")
    unit('xxd-vps-backup.timer', """[Unit]
Description=Daily configuration backup
[Timer]
OnCalendar=*-*-* 03:15:00
RandomizedDelaySec=15m
Persistent=true
[Install]
WantedBy=timers.target
""")
    systemctl('daemon-reload')
    for t in ('cliproxy-auto-update.timer', 'xxd-vps-rules.timer', 'xxd-vps-backup.timer'):
        systemctl('enable', '--now', t)
    p = run(['/usr/local/sbin/cliproxy-auto-update', '--check'], check=False, timeout=300)
    if p.returncode:
        die('自动更新器自检失败：' + (p.stdout + p.stderr).strip().splitlines()[-1])
    cmd_backup(a)
    mark('maint')
    say('maint 完成')


BACKUP_PATHS = ['etc/xxd-vps', 'etc/cliproxyapi', 'etc/cliproxy-auto-update', 'etc/nginx/sites-available',
                'etc/nginx/conf.d', 'etc/letsencrypt', 'etc/ssh/sshd_config.d', 'etc/sysctl.d/99-xxd-vps.conf',
                'etc/ufw', 'etc/systemd/system', 'var/lib/cliproxyapi/auth', 'var/lib/cliproxyapi/plugins',
                'var/lib/xxd-vps/rules-state.json', 'usr/local/x-ui/bin/config.json']


def cmd_backup(a):
    BACKUPS.mkdir(mode=0o700, parents=True, exist_ok=True)
    BACKUPS.chmod(0o700)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dest = BACKUPS / f'config-{stamp}.tar.gz'
    with tempfile.TemporaryDirectory(prefix='xxd-backup-') as td:
        snap = pathlib.Path(td) / 'x-ui.db'
        if XUI_DB.exists():
            with sqlite3.connect(f'file:{XUI_DB}?mode=ro', uri=True) as src, sqlite3.connect(str(snap)) as dst:
                src.backup(dst)
        old = os.umask(0o077)
        try:
            with tarfile.open(dest, 'w:gz') as t:
                if snap.exists():
                    t.add(snap, arcname='etc/x-ui/x-ui.db')
                for rel in BACKUP_PATHS:
                    if pathlib.Path('/' + rel).exists():
                        t.add('/' + rel, arcname=rel)
        finally:
            os.umask(old)
    dest.chmod(0o600)
    for p in sorted(BACKUPS.glob('config-*.tar.gz'))[:-7]:
        p.unlink()
    say(f'备份完成：{dest}（保留最近 7 份，仅 root 可读）')


# ---------------------------------------------------------------- verify
def cmd_verify(a):
    d, c = deploy(), creds()
    ip, rows = d['ip'], []

    def check(name, ok, hint=''):
        rows.append((name, bool(ok), hint))

    for u in ('x-ui', 'nginx', 'cli-proxy-api', 'xxd-vps-sub'):
        check(f'服务 {u}', active(u))
    for t in ('xxd-vps-cert-renew.timer', 'cliproxy-auto-update.timer', 'xxd-vps-rules.timer', 'xxd-vps-backup.timer'):
        check(f'定时器 {t}', active(t))
    check('IP 证书有效（含本机 IP，剩余超过 1 天）', cert_ok(ip))
    listening = run(['ss', '-Hlnt'], quiet=True).stdout
    for p in ('http', 'reality', 'tls', 'sub', 'cliproxy', 'panel'):
        check(f'端口 {PORT[p]} 在监听', f':{PORT[p]} ' in listening)
    for p in ('reality', 'tls', 'sub', 'cliproxy', 'panel'):
        try:
            with socket.create_connection((ip, PORT[p]), timeout=8) as s:
                with ssl.create_default_context().wrap_socket(s, server_hostname=ip):
                    ok = True
        except Exception:
            ok = False
        check(f'{PORT[p]} 的 TLS 证书受系统信任', ok)
    try:
        st, _, _ = https_get(ip, PORT['panel'], c['panel_path'])
        check('3x-ui 面板 HTTPS 可打开', st in (200, 301, 302, 307, 308))
    except Exception:
        check('3x-ui 面板 HTTPS 可打开', False)
    subs = check_subscriptions(d, c)
    check('OpenClash / Mihomo 订阅（含两个节点和 AI 分流组）', subs['clash'])
    check('Shadowrocket 订阅（两条 vless 链接）', subs['shadowrocket'])
    try:
        bad = rule_problems(served_clash(d, c))
    except Exception:
        bad = ['订阅读取失败']
    check('规则镜像完整且格式匹配', not bad, '；'.join(bad))
    check('CLIProxyAPI /v1/models 返回 200', check_cliproxy(d, c))
    try:
        st, _, _ = https_get(ip, PORT['cliproxy'], '/management.html')
        check('CLIProxyAPI 管理中心可打开', st == 200)
    except Exception:
        check('CLIProxyAPI 管理中心可打开', False)
    problem = xray_layout_problem(c)
    check('节点结构（两种身份、flow、空 SNI、IPv4 出站）', not problem, problem or '')
    xray = (run([str(XUI / 'bin' / f'xray-linux-{arch()}'), 'version'], check=False, quiet=True).stdout.splitlines() or [''])[0]
    check(f'Xray 内核固定在 {XRAY_VERSION}', XRAY_VERSION.lstrip('v') in xray)
    eff = run(['sshd', '-T'], quiet=True).stdout.lower()
    check('SSH 已关闭密码登录', 'passwordauthentication no' in eff and 'kbdinteractiveauthentication no' in eff)
    check('SSH root 只能用密钥', re.search(r'permitrootlogin (prohibit-password|without-password)', eff))
    check('UFW 防火墙已启用', 'Status: active' in run(['ufw', 'status'], quiet=True).stdout)
    tz = run(['timedatectl', 'show', '--property=Timezone', '--value'], quiet=True).stdout.strip()
    check(f"时区为 {d['timezone']}", tz == d['timezone'])
    check('至少有一份配置备份', any(BACKUPS.glob('config-*.tar.gz')))
    if a.full:
        p = run([str(CERTBOT / 'bin/certbot'), 'renew', '--dry-run', '--run-deploy-hooks', '--cert-name', ip], check=False, timeout=300)
        check('证书续期演练（certbot renew --dry-run）', p.returncode == 0)
    for name, ok, hint in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}{'  ' + hint if hint and not ok else ''}")
    failed = [r for r in rows if not r[1]]
    write(ETC / 'last-verify.json', json.dumps({'at': time.time(), 'failed': [r[0] for r in failed], 'total': len(rows)},
                                              ensure_ascii=False, indent=2), 0o600)
    print(f'\n验收：{len(rows) - len(failed)}/{len(rows)} 通过')
    return 1 if failed else 0


# ---------------------------------------------------------------- export
def cmd_export(a):
    if sys.stdout.isatty() and not a.force:
        die('export 会输出全部密码和 Key，请重定向到本机文件，例如：ssh 别名 "xxd-vps export" > 登录信息.md')
    labels = json.loads((FILES / 'export-labels.json').read_text())
    if a.lang not in labels:
        die('不支持的语言：' + a.lang + '（可选：' + ', '.join(labels) + '）')
    L = labels[a.lang]
    d, c = deploy(), creds()
    ip, sub = d['ip'], f"https://{d['ip']}:{PORT['sub']}"
    nodes = L['nodes'].replace('{reality}', c['reality_name']).replace('{tls}', c['tls_name'])
    body = f"""# {L['title'].replace('{alias}', d['alias'])}

> {L['warn']}

| {L['item']} | {L['value']} |
| --- | --- |
| {L['ssh']} | `ssh {d['alias']}` |
| {L['ip']} | `{ip}` |
| {L['tz']} | `{d['timezone']}` |

## {L['subs']}

| {L['use']} | {L['url']} |
| --- | --- |
| Clash Verge Rev / OpenClash / Mihomo | `{sub}{c['clash_path']}{c['sub_id_clash']}` |
| {L['mobile']} | `{sub}{c['sub_path']}{c['sub_id_mobile']}` |

{nodes}

## {L['panel']}

| {L['item']} | {L['value']} |
| --- | --- |
| {L['addr']} | `https://{ip}:{PORT['panel']}{c['panel_path']}` |
| {L['user']} | `{c['panel_username']}` |
| {L['pass']} | `{c['panel_password']}` |

## CLIProxyAPI

| {L['item']} | {L['value']} |
| --- | --- |
| {L['cpa_mgmt']} | `https://{ip}:{PORT['cliproxy']}/management.html` |
| {L['cpa_key']} | `{c['cliproxy_management_key']}` |
| {L['cpa_base']} | `https://{ip}:{PORT['cliproxy']}/v1` |
| {L['api_key']} | `{c['cliproxy_api_key']}` |

{L['empty']}
"""
    if a.lang == 'ar':
        body = '<div dir="rtl">\n\n' + body + '\n</div>\n'
    print(body)
    return 0


# ---------------------------------------------------------------- main
PHASES = ['base', 'cert', 'xui', 'sub', 'cliproxy', 'maint']


def main():
    ap = argparse.ArgumentParser(description='小小东 VPS 服务器部署工具')
    sp = ap.add_subparsers(dest='cmd', required=True)
    i = sp.add_parser('init')
    i.add_argument('--ip', required=True)
    i.add_argument('--alias', required=True)
    i.add_argument('--timezone', required=True)
    i.add_argument('--ssh-port', type=int)
    i.add_argument('--quota-gb', type=int, help='每月流量额度（GB），只用于客户端显示')
    i.add_argument('--reset-day', type=int, help='流量每月重置日（1–28）')
    for name in PHASES + ['all', 'backup']:
        sp.add_parser(name)
    v = sp.add_parser('verify')
    v.add_argument('--full', action='store_true', help='额外做一次证书续期演练')
    e = sp.add_parser('export')
    e.add_argument('--force', action='store_true')
    e.add_argument('--lang', default='zh', help='登录信息文件的语言：zh en ko ja ar es fr ru de pt')
    a = ap.parse_args()
    if os.geteuid() != 0:
        die('需要 root 权限运行')
    os.umask(0o022)
    if a.cmd == 'init':
        return cmd_init(a)
    if a.cmd == 'all':
        for ph in PHASES:
            globals()['cmd_' + ph](a)
        a.full = True
        return cmd_verify(a)
    return globals()['cmd_' + a.cmd](a) or 0


if __name__ == '__main__':
    sys.exit(main())
