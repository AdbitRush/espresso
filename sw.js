/* Espresso PWA service worker.
   - Page/HTML: network-first (fresh when online, cached fallback offline)
   - Everything else (icons, fonts): stale-while-revalidate */
const V = "espresso-v5";
const PREFIX = "espresso-";
const SHELL = [
  "./", "./index.html", "./manifest.webmanifest",
  "./favicon.svg", "./favicon-32.png", "./qr.svg", "./images/bg.jpg",
  "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      // Only our OWN generations: espresso, JokeStream and Golden Games are all
      // served from adbitrush.github.io and Cache Storage is per-ORIGIN, so a
      // blanket "delete everything that isn't mine" wiped the other apps' offline
      // caches every time this one shipped an update.
      .then((keys) => Promise.all(keys.filter((k) => k !== V && k.startsWith(PREFIX)).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;
  const isFont = /fonts\.(googleapis|gstatic)\.com$/.test(url.host);
  if (!sameOrigin && !isFont) return;

  const isDoc = req.mode === "navigate" || req.destination === "document";
  if (isDoc) {
    // network-first so an updated app shows up immediately when online
    e.respondWith(
      fetch(req)
        .then((res) => { const c = res.clone(); caches.open(V).then((x) => x.put(req, c)); return res; })
        .catch(() => caches.match(req).then((r) => r || caches.match("./index.html")))
    );
    return;
  }

  // stale-while-revalidate for assets
  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => { if (res && res.status === 200) { const c = res.clone(); caches.open(V).then((x) => x.put(req, c)); } return res; })
        .catch(() => cached);
      return cached || network;
    })
  );
});
