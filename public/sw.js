
// Service Worker para Aeon Chess
const CACHE_NAME = 'aeon-chess-v1.0.0';
const STATIC_CACHE = 'aeon-chess-static-v1.0.0';
const DYNAMIC_CACHE = 'aeon-chess-dynamic-v1.0.0';

// Arquivos estáticos para cache
const STATIC_FILES = [
  '/',
  '/index.html',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico',
  '/images/placeholder.svg',
];

// Estratégias de cache
const cacheStrategies = {
  // Cache First para arquivos estáticos
  cacheFirst: async (request) => {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    try {
      const networkResponse = await fetch(request);
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    } catch (error) {
      return new Response('Network error', { status: 503 });
    }
  },

  // Network First para APIs
  networkFirst: async (request) => {
    try {
      const networkResponse = await fetch(request);
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
      return networkResponse;
    } catch (error) {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        return cachedResponse;
      }
      return new Response('Network error', { status: 503 });
    }
  },

  // Stale While Revalidate para recursos críticos
  staleWhileRevalidate: async (request) => {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then((networkResponse) => {
      cache.put(request, networkResponse.clone());
      return networkResponse;
    });

    return cachedResponse || fetchPromise;
  },
};

// Interceptar requisições
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Pular requisições não-GET
  if (request.method !== 'GET') {
    return;
  }

  // Pular requisições para APIs externas
  if (url.origin !== location.origin) {
    return;
  }

  // Estratégia baseada no tipo de recurso
  if (request.destination === 'image') {
    event.respondWith(cacheStrategies.staleWhileRevalidate(request));
  } else if (url.pathname.startsWith('/api/')) {
    event.respondWith(cacheStrategies.networkFirst(request));
  } else if (STATIC_FILES.includes(url.pathname)) {
    event.respondWith(cacheStrategies.cacheFirst(request));
  } else {
    event.respondWith(cacheStrategies.staleWhileRevalidate(request));
  }
});

// Instalação do Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(STATIC_FILES);
    })
  );
  self.skipWaiting();
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Limpeza periódica de cache
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAN_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              return caches.delete(cacheName);
            }
          })
        );
      })
    );
  }
});

// Background sync para funcionalidades offline
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Sincronizar dados offline
    const offlineData = await getOfflineData();
    if (offlineData.length > 0) {
      await syncOfflineData(offlineData);
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

async function getOfflineData() {
  // Implementar lógica para obter dados offline
  return [];
}

async function syncOfflineData(data) {
  // Implementar lógica para sincronizar dados
  console.log('Syncing offline data:', data);
}
