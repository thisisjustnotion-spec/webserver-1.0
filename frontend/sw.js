self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  // 실시간 Socket.IO 통신 및 Base64 이미지는 캐싱 없이 그대로 통과
  e.respondWith(fetch(e.request));
});