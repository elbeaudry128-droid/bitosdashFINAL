// BitOS Cloud v4 — Cloudflare Worker CORS Proxy
// Proxies mining pool and HiveOS API requests to bypass CORS from GitHub Pages / Cloudflare Pages

const ALLOWED_ORIGINS = [
  'https://elbeaudry128-droid.github.io',
  'https://bitosdashfinal.pages.dev',
  'http://localhost:8000',
  'http://localhost:5500',
  'http://127.0.0.1:8000',
];

const PROXY_ROUTES = {
  '/proxy/supportxmr':   'https://supportxmr.com/api',
  '/proxy/moneroocean':  'https://api.moneroocean.stream',
  '/proxy/k1pool':       'https://api-kas.k1pool.com/api',
  '/proxy/coingecko':    'https://api.coingecko.com/api/v3',
  '/proxy/xmrchain':     'https://xmrchain.net/api',
  '/proxy/kaspa':        'https://api.kaspa.org',
  '/proxy/hiveos':       'https://api2.hiveos.farm/api/v2',
  '/proxy/rvn-2miners':  'https://rvn.2miners.com/api',
};

function corsHeaders(origin) {
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname === '/' || url.pathname === '') {
      return new Response(JSON.stringify({
        service: 'BitOS CORS Proxy',
        version: '4.0.0',
        routes: Object.keys(PROXY_ROUTES),
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
      });
    }

    let targetBase = null;
    let matchedPrefix = null;
    for (const [prefix, base] of Object.entries(PROXY_ROUTES)) {
      if (url.pathname.startsWith(prefix)) {
        targetBase = base;
        matchedPrefix = prefix;
        break;
      }
    }

    if (!targetBase) {
      return new Response(JSON.stringify({ error: 'Unknown route' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
      });
    }

    const subPath = url.pathname.slice(matchedPrefix.length);
    const targetUrl = targetBase + subPath + url.search;

    const proxyHeaders = new Headers();
    proxyHeaders.set('User-Agent', 'BitOS-Proxy/4.0');
    proxyHeaders.set('Accept', 'application/json');

    const authHeader = request.headers.get('Authorization');
    if (authHeader) {
      proxyHeaders.set('Authorization', authHeader);
    }

    const contentType = request.headers.get('Content-Type');
    if (contentType) {
      proxyHeaders.set('Content-Type', contentType);
    }

    try {
      const proxyReq = {
        method: request.method,
        headers: proxyHeaders,
      };

      if (request.method === 'POST' || request.method === 'PUT') {
        proxyReq.body = request.body;
      }

      const resp = await fetch(targetUrl, proxyReq);

      const responseHeaders = new Headers(corsHeaders(origin));
      responseHeaders.set('Content-Type', resp.headers.get('Content-Type') || 'application/json');
      responseHeaders.set('X-Proxy-Status', String(resp.status));

      if (request.method === 'GET' && resp.ok) {
        responseHeaders.set('Cache-Control', 'public, max-age=30');
      }

      return new Response(resp.body, {
        status: resp.status,
        headers: responseHeaders,
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Proxy error', message: err.message }), {
        status: 502,
        headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
      });
    }
  },
};
