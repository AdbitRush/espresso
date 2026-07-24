/* Espresso PWA service worker — offline app shell + stale-while-revalidate. */
const V = "espresso-v1";
const SHELL = [
  "./", "./index.html", "./manifest.webmanifest",
  "./favicon.svg", "./favicon-32.png",
  "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== V).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const sameOrigin = req.url.startsWith(self.location.origin);
  const isFont = req.url.includes("fonts.googleapis.com") || req.url.includes("fonts.gstatic.com");
  if (!sameOrigin && !isFont) return; // let anything else hit the network normally

  e.respondWith(
    caches.match(req).then((cached) => {
      const network = fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(V).then((c) => c.put(req, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
