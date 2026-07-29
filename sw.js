/* 肌少症篩檢工具 Service Worker
 *
 * 目的：網路不順或完全沒訊號時，工具仍然打得開。
 *
 * 版本策略刻意選「網頁走 network-first」：
 * 只要連得上網就一定拿到最新版，連不上才回退到快取。
 * 臨床工具最怕的是平板卡在舊版本卻沒人發現，寧可慢一點也不要用到過期的判定邏輯。
 *
 * 改版時記得同步更新 VERSION，以及 index.html 裡的 APP_VERSION。
 */

const VERSION = "0.2.3";
const CACHE = `sarc-v${VERSION}`;
const NET_TIMEOUT = 3000;   // 網路多久沒回應就改用快取（毫秒）

const PRECACHE = [
  "./",
  "./index.html",
  "./education.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-512-maskable.png"
];

self.addEventListener("install", ev => {
  ev.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE))
    /* 這裡不呼叫 skipWaiting()：不要在使用者填到一半時抽換版本。
       等頁面提示、使用者按下「立即更新」才換。 */
  );
});

self.addEventListener("activate", ev => {
  ev.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* 頁面按下「立即更新」時會送這個訊息過來 */
self.addEventListener("message", ev => {
  if (ev.data && ev.data.type === "SKIP_WAITING") self.skipWaiting();
});

async function networkFirst(req){
  const cache = await caches.open(CACHE);
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), NET_TIMEOUT);
    const res = await fetch(req, { signal: ctrl.signal });
    clearTimeout(timer);
    if (res && res.ok) cache.put(req, res.clone());
    return res;
  } catch (e) {
    // 斷網或逾時：用快取。連該網址都沒快取就退回首頁，至少工具打得開。
    return (await cache.match(req)) || (await cache.match("./index.html")) || Response.error();
  }
}

async function cacheFirst(req){
  const cache = await caches.open(CACHE);
  const hit = await cache.match(req);
  if (hit) return hit;
  try {
    const res = await fetch(req);
    if (res && res.ok) cache.put(req, res.clone());
    return res;
  } catch (e) {
    return Response.error();
  }
}

self.addEventListener("fetch", ev => {
  const req = ev.request;
  if (req.method !== "GET") return;                  // 送去 Google 表單的 POST 不要攔
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // 跨網域交回給瀏覽器

  if (req.mode === "navigate" || req.destination === "document")
    ev.respondWith(networkFirst(req));
  else
    ev.respondWith(cacheFirst(req));
});
