const SHELL_CACHE = "nl-audioboek-shell-v6";
const AUDIO_CACHE = "nl-audioboek-audio-v3";
const SUBS_CACHE = "nl-audioboek-subs-v1";

const SHELL_ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/favicon-32.png",
  "./icons/icon-180.png",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./fonts/Onest-latin.woff2",
  "./fonts/Onest-latin-ext.woff2",
  "./fonts/JetBrainsMono-latin.woff2",
  "./fonts/JetBrainsMono-latin-ext.woff2",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => cache.addAll(SHELL_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== SHELL_CACHE && key !== AUDIO_CACHE && key !== SUBS_CACHE)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Audio files: cache-first, populate cache on first listen so the book
  // works offline once a chapter has been played at least once.
  if (url.pathname.includes("/Audio/")) {
    event.respondWith(
      caches.open(AUDIO_CACHE).then((cache) =>
        cache.match(event.request).then((cached) => {
          if (cached) return cached;
          return fetch(event.request).then((response) => {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          });
        })
      )
    );
    return;
  }

  // Subtitles: cache-first, populate on first view (not every task has one yet).
  if (url.pathname.includes("/subtitles/")) {
    event.respondWith(
      caches.open(SUBS_CACHE).then((cache) =>
        cache.match(event.request).then((cached) => {
          if (cached) return cached;
          return fetch(event.request).then((response) => {
            if (response.ok) cache.put(event.request, response.clone());
            return response;
          });
        })
      )
    );
    return;
  }

  // The page itself: network-first so new deploys show up on the next launch,
  // cached copy only when offline. (Cache-first here froze installed apps on
  // whatever version they first saw.)
  const isPage = event.request.mode === "navigate" || url.pathname.endsWith("/index.html");
  if (isPage && url.origin === self.location.origin) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(SHELL_CACHE).then((cache) => cache.put("./index.html", copy));
          }
          return response;
        })
        .catch(() => caches.match("./index.html").then((cached) => cached || caches.match("./")))
    );
    return;
  }

  // Other shell assets (icons, fonts, manifest): cache-first, falling back to network.
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
