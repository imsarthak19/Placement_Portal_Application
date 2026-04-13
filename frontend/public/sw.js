// Simple service worker for PWA support
self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
    // Required to trigger install prompt
});
