/* =====================================================================
   SHIFA-RUQIYAH CENTRE - PWA SERVICE WORKER ENGINE
   Version: 1.0.0
   Strategy: Network-First for HTML/APIs, Stale-While-Revalidate for Assets
   ===================================================================== */

const CACHE_NAME = 'src-pwa-v1.0.3';

const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/customer.html',
  '/customer-panel/index.html',
  '/logo/src-logo.webp',
  '/logo/src-logo-256.png',
  '/logo/src-logo-512.png',
  '/logo/icon-192.png',
  '/logo/icon-512.png',
  '/logo/apple-touch-icon.png',
  '/manifest.json',
  '/manifest-admin.json'
];

// Install Event - Precache Core Shell
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[PWA SW] Pre-caching core portal shell assets');
      return cache.addAll(PRECACHE_ASSETS).catch(err => {
        console.warn('[PWA SW] Precaching warning (non-fatal):', err);
      });
    })
  );
});

// Activate Event - Clean up stale caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[PWA SW] Purging outdated cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Dynamic routing and offline support
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Ignore non-GET and cross-origin requests that are not CDN assets
  if (req.method !== 'GET') return;
  if (!url.protocol.startsWith('http')) return;

  // HTML Navigation - Network First, fallback to cache
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then(res => {
          if (res.status === 200) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
          }
          return res;
        })
        .catch(() => {
          return caches.match(req).then(cached => {
            if (cached) return cached;
            if (url.pathname.includes('customer')) {
              return caches.match('/customer.html');
            }
            return caches.match('/') || caches.match('/index.html');
          });
        })
    );
    return;
  }

  // Static assets (images, styles, scripts, fonts) - Stale While Revalidate
  event.respondWith(
    caches.match(req).then(cached => {
      const fetchPromise = fetch(req).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
        }
        return res;
      }).catch(() => null);

      return cached || fetchPromise;
    })
  );
});
