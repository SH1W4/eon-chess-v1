
// Service Worker para Aeon Chess
const CACHE_NAME = 'aeon-chess-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll([
        '/',
        '/static/js/bundle.js',
        '/static/css/main.css',
        '/favicon.ico'
      ]);
    })
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  
  if (request.url.includes('/api/')) {
    // API calls: Network first
    event.respondWith(
      fetch(request).then((response) => {
        const clonedResponse = response.clone();
        caches.open(DYNAMIC_CACHE).then((cache) => {
          cache.put(request, clonedResponse);
        });
        return response;
      }).catch(() => {
        return caches.match(request);
      })
    );
  } else {
    // Static assets: Cache first
    event.respondWith(
      caches.match(request).then((response) => {
        return response || fetch(request);
      })
    );
  }
});
