# BitOS Cloud v4 — Deployment Guide

## Option A — GitHub Pages (recommended)

A GitHub Actions workflow auto-deploys on every push to `main`.

### First-time setup (once)

1. Go to **https://github.com/elbeaudry128-droid/bitosdashFINAL/settings/pages**
2. Under **Source**, select: **"GitHub Actions"**
3. Done.

### Your public URL

```
https://elbeaudry128-droid.github.io/bitosdashFINAL/
```

### Install as PWA on TCL60

- Open the URL in **Chrome**
- Menu ⋮ → **Add to Home Screen**
- BitOS installs as a native-like app

### Manual deploy trigger

- https://github.com/elbeaudry128-droid/bitosdashFINAL/actions
- Select "Deploy to GitHub Pages" → "Run workflow"

---

## Option B — Termux (Android, local server)

Run BitOS directly on your phone with full CORS proxy support.

### Quick install (one command)

```bash
curl -sSL https://raw.githubusercontent.com/elbeaudry128-droid/bitosdashFINAL/main/setup-termux.sh | bash
```

### Manual launch

```bash
cd ~/bitosdashFINAL
python bitos-termux.py
```

Opens Chrome automatically on `http://localhost:8765`.

Options:
```
--port N      Custom port (default: 8765)
--no-open     Don't open Chrome automatically
```

---

## Option C — Cloudflare Worker (CORS proxy for GitHub Pages)

Deploy `cf-worker/worker.js` to Cloudflare Workers for full API proxy support on GitHub Pages.

```bash
cd cf-worker
npx wrangler deploy
```

---

## File structure

```
bitosdashFINAL/
├── index.html              ← main HTML
├── app.js                  ← frontend logic (v4)
├── style.css               ← extracted CSS
├── sw.js                   ← service worker (v4.1.0)
├── manifest.json           ← PWA manifest
├── _headers                ← Cloudflare/Pages headers
├── bitos-termux.py         ← local server (Termux/Android)
├── setup-termux.sh         ← Termux auto-installer
├── cf-worker/worker.js     ← Cloudflare Worker proxy
├── wrangler.toml           ← Wrangler config
├── .github/workflows/
│   ├── pages.yml           ← GitHub Pages deploy
│   └── ci.yml              ← CI tests (155 checks)
└── DEPLOY.md / OPEN.md     ← docs
```

GitHub Pages deploys: `index.html`, `app.js`, `style.css`, `manifest.json`, `sw.js`, `_headers`.

---

## Comparison

| Option | Setup | URL | Mobile | Live APIs | Best for |
|---|---|---|---|---|---|
| **GitHub Pages** | 2 clicks | public, fixed | PWA | via CF Worker | **Daily use** |
| **Termux** | 1 command | localhost | direct | full proxy | **On-phone mining** |
| **CF Worker** | wrangler deploy | — | — | full proxy | **API proxy for Pages** |
