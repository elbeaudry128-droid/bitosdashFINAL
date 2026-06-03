**# GitHub Copilot Chat**

- Extension: 0.50.1 (prod)
- VS Code: 1.122.1 (8761a5560cfd65fdd19ce7e2bd18dab5c0a4d84e)
- OS: linux 6.8.0-1052-azure x64
- Remote Name: codespaces
- Extension Kind: Workspace
- GitHub Account: elbeaudry128-droid

## Network

User Settings:

```json
  "http.systemCertificatesNode": true,
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to <https://api.github.com>:

- DNS ipv4 Lookup: 140.82.112.5 (1 ms)
- DNS ipv6 Lookup: Error (30 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (49 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (100 ms)
- Node.js fetch (configured): HTTP 200 (102 ms)

Connecting to <https://api.individual.githubcopilot.com/_ping>:

- DNS ipv4 Lookup: 140.82.113.21 (4 ms)
- DNS ipv6 Lookup: Error (8 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (48 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (99 ms)
- Node.js fetch (configured): HTTP 200 (113 ms)

Connecting to <https://proxy.individual.githubcopilot.com/_ping>:

- DNS ipv4 Lookup: 20.85.130.105 (7 ms)
- DNS ipv6 Lookup: Error (3 ms): getaddrinfo ENOTFOUND proxy.individual.githubcopilot.com
- Proxy URL: None (50 ms)
- Electron fetch: Unavailable
- Node.js https: HTTP 200 (109 ms)
- Node.js fetch (configured): HTTP 200 (107 ms)

Connecting to <https://mobile.events.data.microsoft.com>: HTTP 404 (120 ms)
Connecting to <https://dc.services.visualstudio.com>: HTTP 404 (110 ms)
Connecting to <https://copilot-telemetry.githubusercontent.com/_ping>: HTTP 200 (101 ms)
Connecting to <https://telemetry.individual.githubcopilot.com/_ping>: HTTP 200 (106 ms)
Connecting to <https://default.exp-tas.com>: HTTP 400 (155 ms)

Number of system certificates: 432

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).
