const CACHE = "parchis-shell-v2";
const APP_FILES = ["/", "/styles.css", "/app.js", "/game.js", "/manifest.json", "/icon.svg"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(APP_FILES)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const requestUrl = new URL(event.request.url);
  if (requestUrl.origin !== self.location.origin) return;
  event.respondWith((async () => {
    try {
      const response = await fetch(event.request);
      if (response.ok) {
        const cache = await caches.open(CACHE);
        await cache.put(event.request.mode === "navigate" ? "/" : event.request, response.clone());
      }
      return response;
    } catch (error) {
      const cached = await caches.match(event.request.mode === "navigate" ? "/" : event.request);
      if (cached) return cached;
      throw error;
    }
  })());
});
