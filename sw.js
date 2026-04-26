// BitOS Cloud v4 — Service Worker (cache-bust + stale-while-revalidate)
const CACHE = 'bitos-v4.2.0';
const ASSETS = ['/', '/index.html', '/app.js', '/style.css', '/manifest.json'];

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
  if (url.pathname.startsWith('/proxy/') ||
      url.pathname.startsWith('/api/') ||
      url.pathname === '/login' ||
      url.pathname === '/logout') {
    return;
  }
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.open(CACHE).then(cache =>
      fetch(e.request).then(resp => {
        if (resp && resp.status === 200 && resp.type === 'basic') {
          cache.put(e.request, resp.clone());
        }
        return resp;
      }).catch(() => cache.match(e.request))
    )
  );
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
