# BitOS Cloud v4 — Quick Start

## GitHub Pages (recommended)

Open in your browser:
```
https://elbeaudry128-droid.github.io/bitosdashFINAL/
```

Install as PWA: Chrome menu ⋮ → **Add to Home Screen**

---

## Termux (Android local server)

### One-command install
```bash
curl -sSL https://raw.githubusercontent.com/elbeaudry128-droid/bitosdashFINAL/main/setup-termux.sh | bash
```

### Manual launch
```bash
cd ~/bitosdashFINAL
python bitos-termux.py
```

→ Opens Chrome on `http://localhost:8765`

---

## Endpoints

| Route | Description |
|---|---|
| `/` | Dashboard |
| `/status` | Server status (JSON) |
| `/api/proxy-test` | API connectivity test |

### CORS Proxies (Termux server)
| Route | Target |
|---|---|
| `/proxy/hiveos` | `api2.hiveos.farm` |
| `/proxy/coingecko` | `api.coingecko.com` |
| `/proxy/kaspa` | `api.kaspa.org` |
| `/proxy/moneroocean` | `api.moneroocean.stream` |
| `/proxy/k1pool` | `api-kas.k1pool.com` |
| `/proxy/xmrchain` | `xmrchain.net` |
| `/proxy/asic/<ip>/<path>` | Local ASIC HTTP |

---

## Troubleshooting

**Dashboard blank** → Open Chrome DevTools (F12), check for errors

**"Page not accessible"** → Use `http://` not `https://` for local server

**Port busy** → `fuser -k 8765/tcp` then relaunch

**APIs return 502** → Normal in sandboxed environments; works on local network
