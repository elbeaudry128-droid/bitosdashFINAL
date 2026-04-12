#!/usr/bin/env python3
# BitOS Cloud Dashboard v3 — Serveur HTTP Linux (single-file build)
# index.html + manifest.json + sw.js EMBEDDED — only app.js needed alongside
import argparse, getpass, hashlib, http.server, json, os, platform, secrets
import socket, ssl, subprocess, sys, threading, time
import urllib.parse, urllib.request, urllib.error
from http.cookies import SimpleCookie
from pathlib import Path


# ══ EMBEDDED STATIC ASSETS ══════════════════════════════════════════
EMBEDDED_INDEX_HTML = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=5,user-scalable=yes,viewport-fit=cover">
<meta name="theme-color" content="#080c14">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="mobile-web-app-capable" content="yes">
<title>BitOS Cloud v3 — Mining Dashboard</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%2300e5ff'/%3E%3Ctext x='50' y='68' font-size='60' font-weight='800' text-anchor='middle' fill='%23080c14' font-family='monospace'%3EB%3C/text%3E%3C/svg%3E">
<style>
:root{
  --bg:#080c14;--panel:#0d1421;--panel2:#111a2e;--border:#1e2d47;
  --text:#e8f0fe;--muted:#5a7090;--accent:#00e5ff;--accent2:#7c3aed;
  --green:#00d97e;--red:#ff2d55;--yellow:#ffb800;--orange:#ff7a00;
}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;
  min-height:100vh;overflow-x:hidden}
body{padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
a{color:var(--accent);text-decoration:none}
button{cursor:pointer;font-family:inherit}
input,select,textarea{font-family:inherit;background:var(--panel2);border:1px solid var(--border);
  color:var(--text);border-radius:8px;padding:10px 12px;outline:none}
input:focus,select:focus,textarea:focus{border-color:var(--accent)}

.app{max-width:1400px;margin:0 auto;padding:20px}
.header{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;
  padding-bottom:16px;border-bottom:1px solid var(--border)}
.logo{display:flex;align-items:center;gap:12px}
.logo-icon{width:44px;height:44px;background:linear-gradient(135deg,var(--accent),var(--accent2));
  border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:22px;
  font-weight:800;color:var(--bg);font-family:monospace}
.logo-text h1{font-size:18px;font-weight:800}
.logo-text .ver{font-size:11px;color:var(--muted);font-family:monospace}

.nav{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:20px}
.nav-btn{background:var(--panel);border:1px solid var(--border);color:var(--muted);
  padding:10px 16px;border-radius:10px;font-size:13px;font-weight:600;transition:all .15s}
.nav-btn.active{background:var(--accent);color:var(--bg);border-color:var(--accent)}
.nav-btn:hover:not(.active){border-color:var(--accent);color:var(--text)}

.page{display:none}
.page.active{display:block}

.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px}
.card-title{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;
  font-family:monospace;margin-bottom:10px}
.card-value{font-size:26px;font-weight:800;margin-bottom:4px}
.card-sub{font-size:12px;color:var(--muted)}

#toast-wrap{position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;
  gap:8px;max-width:340px}
.toast{background:var(--panel);border:1px solid var(--border);border-radius:10px;font-size:12px;
  box-shadow:0 8px 24px rgba(0,0,0,.4);transition:opacity .3s}

.modal{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;display:none;
  align-items:center;justify-content:center;padding:20px}
.modal.show{display:flex}
.modal-box{background:var(--panel);border:1px solid var(--border);border-radius:16px;
  padding:24px;width:100%;max-width:480px;max-height:90vh;overflow-y:auto}

.pwa-install{position:fixed;bottom:20px;right:20px;background:var(--accent);color:var(--bg);
  border:none;border-radius:50%;width:54px;height:54px;font-size:22px;display:none;
  align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,229,255,.4);z-index:500}

@media(max-width:640px){
  .app{padding:12px}
  .header{flex-direction:column;gap:12px;align-items:flex-start}
  .nav{overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch}
  .nav-btn{flex-shrink:0}
  .card-value{font-size:22px}
}
</style>
</head>
<body>

<div class="app">
  <header class="header">
    <div class="logo">
      <div class="logo-icon">B</div>
      <div class="logo-text">
        <h1>BitOS Cloud</h1>
        <div class="ver">v3.4.0 — Mining Dashboard</div>
      </div>
    </div>
    <div id="header-status"></div>
  </header>

  <nav class="nav">
    <button class="nav-btn active" onclick="showPage('dash')">Dashboard</button>
    <button class="nav-btn" onclick="showPage('xmr')">XMR</button>
    <button class="nav-btn" onclick="showPage('kas')">KAS</button>
    <button class="nav-btn" onclick="showPage('rigs')">Rigs</button>
    <button class="nav-btn" onclick="showPage('wallet')">Wallet</button>
    <button class="nav-btn" onclick="showPage('settings')">Settings</button>
  </nav>

  <div id="page-dash" class="page active">
    <div class="grid" id="dash-grid">
      <div class="card">
        <div class="card-title">Total Hashrate</div>
        <div class="card-value" id="kpi-hashrate">— H/s</div>
        <div class="card-sub">Tous workers actifs</div>
      </div>
      <div class="card">
        <div class="card-title">Revenu 24h</div>
        <div class="card-value" id="kpi-revenue">$ —</div>
        <div class="card-sub">XMR + KAS estimés</div>
      </div>
      <div class="card">
        <div class="card-title">Workers Online</div>
        <div class="card-value" id="kpi-workers">—</div>
        <div class="card-sub">HiveOS sync</div>
      </div>
      <div class="card">
        <div class="card-title">Solde Total</div>
        <div class="card-value" id="kpi-balance">$ —</div>
        <div class="card-sub">XMR + KAS pools</div>
      </div>
    </div>
  </div>

  <div id="page-xmr" class="page"></div>
  <div id="page-kas" class="page"></div>
  <div id="page-rigs" class="page"></div>
  <div id="page-wallet" class="page"></div>
  <div id="page-settings" class="page"></div>
</div>

<div id="toast-wrap"></div>
<button class="pwa-install" id="pwa-install-btn" onclick="installPWA()">+</button>

<script>
// showPage, el, setText, getApiBase defined in app.js

if('serviceWorker' in navigator){
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('sw.js').catch(function(e){console.warn('SW:',e);});
  });
}
</script>
<script defer src="app.js"></script>
<script>
window.addEventListener('load', function(){
  setTimeout(function(){
    if(typeof renderDash !== 'function'){
      console.warn('[BitOS] app.js non chargé ou incomplet');
    }
  }, 1500);
});
</script>
</body>
</html>
'''

EMBEDDED_MANIFEST_JSON = r'''{
  "name": "BitOS Cloud Dashboard",
  "short_name": "BitOS",
  "description": "Mining dashboard for XMR & KAS with HiveOS integration",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#080c14",
  "theme_color": "#080c14",
  "lang": "fr",
  "categories": ["finance", "utilities", "productivity"],
  "icons": [
    {
      "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 192 192'%3E%3Crect width='192' height='192' rx='38' fill='%2300e5ff'/%3E%3Ctext x='96' y='130' font-size='115' font-weight='800' text-anchor='middle' fill='%23080c14' font-family='monospace'%3EB%3C/text%3E%3C/svg%3E",
      "sizes": "192x192",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    },
    {
      "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Crect width='512' height='512' rx='100' fill='%2300e5ff'/%3E%3Ctext x='256' y='350' font-size='310' font-weight='800' text-anchor='middle' fill='%23080c14' font-family='monospace'%3EB%3C/text%3E%3C/svg%3E",
      "sizes": "512x512",
      "type": "image/svg+xml",
      "purpose": "any maskable"
    }
  ]
}
'''

EMBEDDED_SW_JS = r'''// BitOS Cloud v3 — Service Worker (offline + stale-while-revalidate)
const CACHE = 'bitos-v3.4.0';
const ASSETS = ['/', '/index.html', '/app.js', '/manifest.json'];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS).catch(()=>{})));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Ne jamais cacher les proxy API ni l'auth
  if (url.pathname.startsWith('/proxy/') ||
      url.pathname.startsWith('/api/') ||
      url.pathname === '/login' ||
      url.pathname === '/logout') {
    return; // passthrough
  }
  if (e.request.method !== 'GET') return;

  // Stale-while-revalidate
  e.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(e.request).then(cached => {
        const fetchPromise = fetch(e.request).then(resp => {
          if (resp && resp.status === 200 && resp.type === 'basic') {
            cache.put(e.request, resp.clone());
          }
          return resp;
        }).catch(() => cached);
        return cached || fetchPromise;
      })
    )
  );
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
'''

EMBEDDED_ASSETS = {
    'index.html':   ('text/html; charset=utf-8',       EMBEDDED_INDEX_HTML),
    'manifest.json':('application/json',               EMBEDDED_MANIFEST_JSON),
    'sw.js':        ('application/javascript; charset=utf-8', EMBEDDED_SW_JS),
}

DASHBOARD_FILE = 'index.html'
DEFAULT_PORT   = 8765
VERSION = '3.4.1-merged'

PROXY_RULES = {
    '/proxy/hiveos':    'https://api2.hiveos.farm/api/v2',
    '/proxy/coingecko': 'https://api.coingecko.com/api/v3',
    '/proxy/kaspa':     'https://api.kaspa.org',
    '/proxy/xmr-pool':  'https://supportxmr.com/api',
    '/proxy/kas-pool':  'https://api-kas.k1pool.com/api',
    '/proxy/xmrchain':  'https://xmrchain.net/api',
}

BANNER = r"""
  ╔══════════════════════════════════════════════════════════╗
  ║   BitOS Cloud v3 — Dashboard Server                      ║
  ╚══════════════════════════════════════════════════════════╝
"""

START_TIME = time.time()
AUTH_ENABLED = False
AUTH_PASS_HASH = ''
AUTH_TOKENS = set()
AUTH_FAIL_COUNT = {}
AUTH_FAIL_LOCK = 5
AUTH_LOCK_TIME = 300
AUTH_FAIL_TIMES = {}

def hash_password(pwd): return hashlib.sha256(pwd.encode('utf-8')).hexdigest()
def generate_token(): return secrets.token_urlsafe(32)

def is_locked(ip):
    if ip not in AUTH_FAIL_COUNT: return False
    if AUTH_FAIL_COUNT[ip] >= AUTH_FAIL_LOCK:
        first_fail = AUTH_FAIL_TIMES.get(ip, 0)
        if time.time() - first_fail < AUTH_LOCK_TIME: return True
        AUTH_FAIL_COUNT.pop(ip, None); AUTH_FAIL_TIMES.pop(ip, None)
    return False

def record_fail(ip):
    AUTH_FAIL_COUNT[ip] = AUTH_FAIL_COUNT.get(ip, 0) + 1
    if ip not in AUTH_FAIL_TIMES: AUTH_FAIL_TIMES[ip] = time.time()

def reset_fails(ip):
    AUTH_FAIL_COUNT.pop(ip, None); AUTH_FAIL_TIMES.pop(ip, None)

LOGIN_PAGE = '''<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BitOS — Connexion</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#080c14;color:#e8f0fe;font-family:system-ui,sans-serif;
  display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#0d1421;border:1px solid #1e2d47;border-radius:16px;
  padding:40px 32px;width:100%;max-width:380px;text-align:center}
.logo{width:56px;height:56px;background:linear-gradient(135deg,#00e5ff,#7c3aed);
  border-radius:14px;display:flex;align-items:center;justify-content:center;
  font-size:24px;font-weight:800;color:#fff;margin:0 auto 20px}
h1{font-size:20px;font-weight:800;margin-bottom:6px}
.sub{color:#5a7090;font-size:12px;margin-bottom:28px}
input{width:100%;background:#111a2e;border:1px solid #1e2d47;border-radius:10px;
  padding:14px 16px;color:#e8f0fe;font-size:16px;outline:none;margin-bottom:16px}
input:focus{border-color:#00e5ff}
button{width:100%;background:#00e5ff;color:#080c14;border:none;border-radius:10px;
  padding:14px;font-size:14px;font-weight:800;cursor:pointer}
.err{color:#ff2d55;font-size:12px;margin-top:12px;min-height:18px}
</style></head><body>
<div class="box"><div class="logo">B</div><h1>BitOS Cloud</h1>
<div class="sub">Authentification requise</div>
<form id="f" onsubmit="return go()">
<input type="password" id="p" placeholder="Mot de passe" autofocus>
<button type="submit">Se connecter</button></form>
<div class="err" id="err"><!--ERR--></div></div>
<script>
async function go(){var p=document.getElementById('p').value;if(!p)return false;
try{var r=await fetch('/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({password:p})});var d=await r.json();
if(d.ok){window.location.href=d.redirect||'/';}
else{document.getElementById('err').textContent=d.error||'Mot de passe incorrect';
document.getElementById('p').value='';document.getElementById('p').focus();}}
catch(e){document.getElementById('err').textContent='Erreur reseau';}return false;}
</script></body></html>'''

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    log_file = None

    def log_message(self, fmt, *args):
        msg = f"[{self.address_string()}] {fmt % args}"
        if self.log_file:
            with open(self.log_file, 'a') as f: f.write(msg + '\n')
        if '/proxy/' not in (fmt % args):
            print(f"  \033[90m{msg}\033[0m")

    def _check_auth(self):
        if not AUTH_ENABLED: return True
        ip = self.client_address[0]
        if ip in ('127.0.0.1', '::1', 'localhost'): return True
        if is_locked(ip): return False
        ch = self.headers.get('Cookie', '')
        if ch:
            c = SimpleCookie(ch)
            if 'bitosdash_token' in c and c['bitosdash_token'].value in AUTH_TOKENS:
                return True
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if 'token' in qs and qs['token'][0] in AUTH_TOKENS: return True
        return False

    def _send_401(self):
        path = self.path.split('?')[0]
        if path.startswith('/proxy/') or path.startswith('/api/'):
            data = json.dumps({'error':'auth_required','login':'/login'}).encode()
            self.send_response(401)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',len(data))
            self.end_headers(); self.wfile.write(data)
        else:
            self.send_response(302); self.send_header('Location','/login'); self.end_headers()

    def do_OPTIONS(self): self._send_cors(204); self.end_headers()
    def do_GET(self): self._route('GET')
    def do_POST(self): self._route('POST')
    def do_PUT(self): self._route('PUT')
    def do_PATCH(self): self._route('PATCH')
    def do_DELETE(self): self._route('DELETE')

    def _send_cors(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age','86400')

    def _route(self, method):
        path = self.path.split('?')[0]
        if path == '/login': self._serve_login(); return
        if path == '/api/auth' and method == 'POST': self._handle_auth(); return
        if path == '/logout': self._handle_logout(); return
        if path == '/favicon.ico': self.send_error(404); return
        if not self._check_auth(): self._send_401(); return
        self._handle(method)

    def _serve_login(self):
        if not AUTH_ENABLED:
            self.send_response(302); self.send_header('Location','/'); self.end_headers(); return
        ip = self.client_address[0]
        page = LOGIN_PAGE
        if is_locked(ip):
            remain = int(AUTH_LOCK_TIME - (time.time() - AUTH_FAIL_TIMES.get(ip, 0)))
            page = page.replace('<!--ERR-->', f'IP verrouillee — reessayez dans {max(1,remain//60)} min')
        data = page.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',len(data))
        self.send_header('Cache-Control','no-store')
        self.end_headers(); self.wfile.write(data)

    def _handle_auth(self):
        ip = self.client_address[0]
        if is_locked(ip):
            remain = int(AUTH_LOCK_TIME - (time.time() - AUTH_FAIL_TIMES.get(ip,0)))
            data = json.dumps({'ok':False,'error':f'IP verrouillee — reessayez dans {max(1,remain//60)} min'}).encode()
            self._send_cors(429)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',len(data)); self.end_headers(); self.wfile.write(data); return
        cl = int(self.headers.get('Content-Length',0))
        body = self.rfile.read(cl) if cl > 0 else b'{}'
        try: payload = json.loads(body)
        except Exception: payload = {}
        password = payload.get('password','')
        if hash_password(password) == AUTH_PASS_HASH:
            token = generate_token(); AUTH_TOKENS.add(token); reset_fails(ip)
            data = json.dumps({'ok':True,'redirect':'/'}).encode()
            self._send_cors(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',len(data))
            self.send_header('Set-Cookie',f'bitosdash_token={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400')
            self.end_headers(); self.wfile.write(data)
            print(f"  Connexion reussie depuis {ip}")
        else:
            record_fail(ip)
            remaining = AUTH_FAIL_LOCK - AUTH_FAIL_COUNT.get(ip,0)
            if is_locked(ip):
                msg = f'IP verrouillee — {AUTH_FAIL_LOCK} echecs — reessayez dans 5 min'
            else:
                msg = f'Mot de passe incorrect ({remaining} tentative(s) restante(s))'
            data = json.dumps({'ok':False,'error':msg}).encode()
            self._send_cors(401)
            self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',len(data)); self.end_headers(); self.wfile.write(data)

    def _handle_logout(self):
        ch = self.headers.get('Cookie','')
        if ch:
            c = SimpleCookie(ch)
            if 'bitosdash_token' in c: AUTH_TOKENS.discard(c['bitosdash_token'].value)
        self.send_response(302)
        self.send_header('Location','/login')
        self.send_header('Set-Cookie','bitosdash_token=; Path=/; Max-Age=0')
        self.end_headers()

    def _handle(self, method):
        path = self.path.split('?')[0]
        for prefix, target in PROXY_RULES.items():
            if path == prefix or path.startswith(prefix+'/') or path.startswith(prefix+'?'):
                self._proxy(method, prefix, target); return
        if path.startswith('/proxy/asic/'): self._proxy_asic(method, path); return
        if path in ('/status','/api/status'): self._serve_status(); return
        if path == '/api/proxy-test': self._serve_proxy_test(); return
        self._serve_static(path)

    def _proxy(self, method, prefix, target):
        suffix = self.path[len(prefix):]
        if suffix and not suffix.startswith('/') and not suffix.startswith('?'):
            suffix = '/' + suffix
        url = target + suffix
        body = None
        cl = int(self.headers.get('Content-Length',0))
        if cl > 0: body = self.rfile.read(cl)
        req_headers = {'Accept':'application/json','User-Agent':f'BitOS-Cloud-Dashboard/{VERSION}'}
        for k in ('Content-Type','Authorization'):
            v = self.headers.get(k)
            if v: req_headers[k] = v
        try:
            req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                ct = resp.headers.get('Content-Type','application/json')
                status = resp.status
        except urllib.error.HTTPError as e:
            data = e.read() or b'{}'; ct = 'application/json'; status = e.code
        except Exception as e:
            data = json.dumps({'error':str(e),'proxy':True,'url':url}).encode()
            ct = 'application/json'; status = 502
        self._send_cors(status)
        self.send_header('Content-Type',ct)
        self.send_header('Content-Length',len(data))
        self.send_header('X-Proxy-By','BitOS-Server')
        self.end_headers(); self.wfile.write(data)

    def _serve_static(self, path):
        if path in ('/',''): path = '/' + DASHBOARD_FILE
        name = path.lstrip('/')

        # Check embedded assets first
        if name in EMBEDDED_ASSETS:
            mime, content = EMBEDDED_ASSETS[name]
            data = content.encode('utf-8')
            self._send_cors(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', len(data))
            self.send_header('Cache-Control','no-cache' if name.endswith('.html') else 'max-age=300')
            self.end_headers(); self.wfile.write(data)
            return

        # Fall through to filesystem (for app.js and any other file)
        file_path = (Path('.') / name).resolve()
        base_path = Path('.').resolve()
        if not str(file_path).startswith(str(base_path)):
            self.send_error(403,'Acces refuse'); return
        if not file_path.exists() or not file_path.is_file():
            self.send_error(404,f'Non trouve: {path}'); return
        MIME = {'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8',
            '.css':'text/css; charset=utf-8','.json':'application/json','.png':'image/png',
            '.ico':'image/x-icon','.svg':'image/svg+xml','.woff2':'font/woff2','.woff':'font/woff',
            '.txt':'text/plain; charset=utf-8','.md':'text/markdown; charset=utf-8'}
        ext = file_path.suffix.lower()
        mime = MIME.get(ext,'application/octet-stream')
        data = file_path.read_bytes()
        self._send_cors(200)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',len(data))
        cache = 'no-cache' if ext == '.html' else 'max-age=300'
        self.send_header('Cache-Control',cache)
        self.end_headers(); self.wfile.write(data)

    def _serve_status(self):
        data = json.dumps({'status':'ok','version':VERSION,'file':DASHBOARD_FILE,
            'proxies':list(PROXY_RULES.keys()),'uptime':int(time.time()-START_TIME),
            'host':socket.gethostname(),'platform':platform.system(),'lan_ip':get_lan_ip(),
            'cors':'enabled','auth':AUTH_ENABLED,'sessions':len(AUTH_TOKENS)},indent=2).encode()
        self._send_cors(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',len(data))
        self.end_headers(); self.wfile.write(data)

    def _proxy_asic(self, method, path):
        parts = path[len('/proxy/asic/'):].split('/',1)
        asic_ip = parts[0]
        rest = '/' + parts[1] if len(parts) > 1 else '/'
        target_url = 'http://' + asic_ip + rest
        body = None
        cl = int(self.headers.get('Content-Length',0))
        if cl > 0: body = self.rfile.read(cl)
        req_headers = {'Accept':'application/json, text/html, */*',
            'User-Agent':f'BitOS-Cloud-Dashboard/{VERSION}',
            'Content-Type':self.headers.get('Content-Type','application/json')}
        auth = self.headers.get('Authorization')
        if auth: req_headers['Authorization'] = auth
        try:
            req = urllib.request.Request(target_url, data=body, headers=req_headers, method=method)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read(); ct = resp.headers.get('Content-Type','application/json'); status = resp.status
        except urllib.error.HTTPError as e:
            data = e.read() or b'{}'; ct = 'application/json'; status = e.code
        except Exception as e:
            data = json.dumps({'error':str(e),'asic_ip':asic_ip,'proxy':True}).encode()
            ct = 'application/json'; status = 502
        self._send_cors(status)
        self.send_header('Content-Type',ct)
        self.send_header('Content-Length',len(data))
        self.send_header('X-Proxy-ASIC',asic_ip)
        self.end_headers(); self.wfile.write(data)

    def _serve_proxy_test(self):
        results = {}
        for prefix, target in PROXY_RULES.items():
            try:
                req = urllib.request.Request(target+'/',
                    headers={'User-Agent':f'BitOS-Cloud-Dashboard/{VERSION}'}, method='GET')
                with urllib.request.urlopen(req, timeout=5) as resp:
                    results[prefix] = {'ok':True,'status':resp.status,'target':target}
            except urllib.error.HTTPError as e:
                results[prefix] = {'ok':True,'status':e.code,'target':target}
            except Exception as e:
                results[prefix] = {'ok':False,'error':str(e)[:80],'target':target}
        data = json.dumps({'proxy_tests':results,'timestamp':int(time.time()),
            'total':len(results),'ok':sum(1 for v in results.values() if v.get('ok'))},indent=2).encode()
        self._send_cors(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',len(data))
        self.end_headers(); self.wfile.write(data)

def print_qr(url):
    try:
        import qrcode
        qr = qrcode.QRCode(border=1); qr.add_data(url); qr.make(fit=True)
        print(); qr.print_ascii(invert=True)
    except ImportError:
        print(f"\n  Acces mobile : {url}")

def watchdog(interval=2):
    last_mtime = 0
    while True:
        try:
            mtime = Path(DASHBOARD_FILE).stat().st_mtime
            if last_mtime and mtime != last_mtime:
                print(f"\n  {DASHBOARD_FILE} modifie — rafraichissez le navigateur")
            last_mtime = mtime
        except FileNotFoundError: pass
        time.sleep(interval)

def create_ssl_context():
    cert = Path('/tmp/bitosdash_cert.pem'); key = Path('/tmp/bitosdash_key.pem')
    if not cert.exists():
        try:
            subprocess.run(['openssl','req','-x509','-newkey','rsa:2048',
                '-keyout',str(key),'-out',str(cert),'-days','365','-nodes',
                '-subj','/CN=localhost/O=BitOS/C=FR'], check=True, capture_output=True)
            print("  Certificat auto-signe genere")
        except Exception as e:
            print(f"  HTTPS impossible: {e}"); return None
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(cert), str(key))
    return ctx

def get_lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80)); return s.getsockname()[0]
    except Exception: return '127.0.0.1'

def main():
    global AUTH_ENABLED, AUTH_PASS_HASH
    parser = argparse.ArgumentParser(description='BitOS Cloud Dashboard v3')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--host', type=str, default='')
    parser.add_argument('--lan', action='store_true')
    parser.add_argument('--qr', action='store_true')
    parser.add_argument('--https', action='store_true')
    parser.add_argument('--open', action='store_true')
    parser.add_argument('--log', type=str, default='')
    parser.add_argument('--no-watch', action='store_true')
    parser.add_argument('--password', type=str, default='')
    parser.add_argument('--no-auth', action='store_true')
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    # index.html is embedded, no disk check required

    if args.lan and not args.no_auth:
        AUTH_ENABLED = True
        if args.password: pwd = args.password
        else:
            print("\n  Mode LAN — mot de passe requis\n")
            pwd = getpass.getpass("  Mot de passe BitOS : ")
            if not pwd: print("  Mot de passe vide — abandon."); sys.exit(1)
            pwd2 = getpass.getpass("  Confirmer :          ")
            if pwd != pwd2: print("  Les mots de passe ne correspondent pas."); sys.exit(1)
        AUTH_PASS_HASH = hash_password(pwd); pwd = '***'

    host = args.host or ('0.0.0.0' if args.lan else '127.0.0.1')
    port = args.port
    proto = 'https' if args.https else 'http'
    lan_ip = get_lan_ip()
    local_url = f"{proto}://localhost:{port}"
    lan_url = f"{proto}://{lan_ip}:{port}"

    if args.log: DashboardHandler.log_file = args.log

    print(BANNER)
    print(f"  Repertoire : {script_dir}")
    print(f"  Dashboard  : {DASHBOARD_FILE}")
    print(f"  Auth       : {'activee' if AUTH_ENABLED else 'desactivee'}")
    print(f"  Local      : {local_url}")
    if args.lan: print(f"  LAN        : {lan_url}")

    if args.qr: print_qr(lan_url if args.lan else local_url)

    if not args.no_watch:
        threading.Thread(target=watchdog, daemon=True).start()

    try:
        server = http.server.ThreadingHTTPServer((host, port), DashboardHandler)
        if args.https:
            ctx = create_ssl_context()
            if ctx:
                server.socket = ctx.wrap_socket(server.socket, server_side=True)
                print(f"\n  HTTPS active")
        print(f"\n  Serveur demarre — Ctrl+C pour arreter\n")
        if args.open:
            import webbrowser
            threading.Timer(0.8, lambda: webbrowser.open(local_url)).start()
        server.serve_forever()
    except PermissionError:
        print(f"\n  Port {port} refuse"); sys.exit(1)
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f"\n  Port {port} deja utilise")
        else: print(f"\n  Erreur reseau: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n  Serveur arrete\n")

if __name__ == '__main__':
    main()
