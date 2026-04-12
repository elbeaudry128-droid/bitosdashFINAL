# BitOS Cloud v3 — Déploiement & Liens

## Déploiement simplifié (2 fichiers)

Un seul script Python contient le serveur + `index.html` + `manifest.json` + `sw.js` embarqués. Il suffit de :

```
bitosdash.py    ← serveur + assets embarqués (30 KB)
app.js          ← logique frontend (418 KB)
```

**Pas de `index.html`, pas de `manifest.json`, pas de `sw.js` à côté** — tout est dans `bitosdash.py`.

---

## Lancement

### Option 1 — Local uniquement (sans auth, plus rapide)

```bash
python3 bitosdash.py
```

→ http://localhost:8765

### Option 2 — LAN pour mobile (TCL60, iPad, etc.) avec mot de passe

```bash
python3 bitosdash.py --lan --qr
```

Le serveur demande un mot de passe au démarrage et affiche un **QR code** à scanner avec ton téléphone.

### Option 3 — LAN sans authentification (rapide, déconseillé sur WiFi public)

```bash
python3 bitosdash.py --lan --no-auth
```

### Option 4 — HTTPS auto-signé (pour PWA complète avec micro/notifications)

```bash
python3 bitosdash.py --https --lan --qr
```

### Option 5 — Ouverture automatique du navigateur

```bash
python3 bitosdash.py --open
```

---

## Accès depuis TCL60 (Chrome Android)

1. **Sur ton PC** : lance le serveur en mode LAN
   ```bash
   python3 bitosdash.py --lan --no-auth
   ```
2. **Note l'IP LAN** affichée dans le terminal (ex: `http://192.168.1.42:8765`)
3. **Sur le TCL60**, ouvre Chrome et tape cette URL
4. Une fois la page ouverte → **menu ⋮ → "Ajouter à l'écran d'accueil"** → BitOS devient une PWA plein écran

### Trouver ton IP LAN sur le PC

```bash
hostname -I | awk '{print $1}'
ip route get 1.1.1.1 | awk '{print $7; exit}'
```

---

## Endpoints du serveur

### Routes publiques (si auth)
| Route | Description |
|---|---|
| `/login` | Page de connexion |
| `/api/auth` | POST pour s'authentifier |
| `/logout` | Déconnexion |

### Routes protégées
| Route | Description |
|---|---|
| `/` | Dashboard (index.html embarqué) |
| `/app.js` | Logique frontend |
| `/manifest.json` | PWA manifest (embarqué) |
| `/sw.js` | Service Worker (embarqué) |
| `/status` | JSON état serveur |
| `/api/proxy-test` | Test de connectivité des APIs |

### Proxies CORS
| Route locale | Cible upstream |
|---|---|
| `/proxy/hiveos` | `https://api2.hiveos.farm/api/v2` |
| `/proxy/coingecko` | `https://api.coingecko.com/api/v3` |
| `/proxy/kaspa` | `https://api.kaspa.org` |
| `/proxy/xmr-pool` | `https://supportxmr.com/api` |
| `/proxy/kas-pool` | `https://api-kas.k1pool.com/api` |
| `/proxy/xmrchain` | `https://xmrchain.net/api` |
| `/proxy/asic/<ip>/<path>` | ASIC HTTP local (Antminer S21) |

---

## Diagnostic rapide

```bash
# Serveur démarré ?
curl http://localhost:8765/status

# APIs externes accessibles ?
curl http://localhost:8765/api/proxy-test

# Process sur le port 8765 ?
lsof -ti:8765

# Tuer le serveur
kill $(lsof -ti:8765)
```

---

## Fichiers du projet

| Fichier | Rôle | Taille |
|---|---|---|
| **`bitosdash.py`** ⭐ | Serveur + HTML/manifest/SW embarqués | ~30 KB |
| **`app.js`** ⭐ | Logique frontend (mining, wallets, charts) | ~418 KB |
| `server.py` | Version séparée (optionnelle) | ~20 KB |
| `index.html` | Version standalone (optionnelle) | ~7 KB |
| `manifest.json` | PWA manifest standalone | ~1 KB |
| `sw.js` | Service Worker standalone | ~1 KB |

> ⭐ = fichiers nécessaires pour le déploiement simplifié

---

## Options complètes de `bitosdash.py`

```
--port N        Port custom (défaut: 8765)
--host HOST     Interface (défaut: 127.0.0.1 ou 0.0.0.0 si --lan)
--lan           Accès depuis le réseau local
--qr            Afficher un QR code pour mobile
--https         HTTPS avec certificat auto-signé
--open          Ouvrir le navigateur automatiquement
--log FILE      Fichier de log
--no-watch      Désactiver le watchdog
--password PWD  Mot de passe explicite (mode LAN)
--no-auth       Désactiver l'auth en mode LAN
```
