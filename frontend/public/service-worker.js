/* The post-build versioning step replaces this token so every uploaded build
 * installs a fresh worker even when this source file did not otherwise change. */
const BUILD_VERSION = '__DHARMASEARCH_BUILD_VERSION__';
const APP_CACHE = `dharmasearch-app-${BUILD_VERSION}`;
const AUDIO_CACHE = 'dharmasearch-audio-v1';
const MAX_AUDIO_BYTES = 50 * 1024 * 1024;

const CORE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/scripture-data.json',
  '/audio-manifest.json',
  '/icons/dharmasearch-192.png',
  '/icons/dharmasearch-512.png',
];

function sameOriginUrl(request) {
  return new URL(request.url).origin === self.location.origin;
}

async function discoverBuildAssets() {
  const response = await fetch('/asset-manifest.json', { cache: 'no-store' });
  if (!response.ok) throw new Error(`asset-manifest returned ${response.status}`);
  const manifest = await response.json();
  return Object.values(manifest.files || {})
    .filter(path => /\.(?:css|js)$/.test(path))
    .filter(path => !path.startsWith('/audio/'));
}

async function precacheApp() {
  const cache = await caches.open(APP_CACHE);
  const buildAssets = await discoverBuildAssets();
  await cache.addAll([...new Set([...CORE_URLS, ...buildAssets])]);
}

self.addEventListener('install', event => {
  event.waitUntil(precacheApp().then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(
      names
        .filter(name => name.startsWith('dharmasearch-app-') && name !== APP_CACHE)
        .map(name => caches.delete(name)),
    );
    await self.clients.claim();
  })());
});

function withCachedAt(response) {
  const headers = new Headers(response.headers);
  headers.set('x-dharmasearch-cached-at', String(Date.now()));
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

async function responseSize(response) {
  const declared = Number(response.headers.get('content-length'));
  if (Number.isFinite(declared) && declared >= 0) return declared;
  return (await response.clone().blob()).size;
}

async function trimAudioCache(cache) {
  const entries = await Promise.all((await cache.keys()).map(async request => {
    const response = await cache.match(request);
    return {
      request,
      size: response ? await responseSize(response) : 0,
      cachedAt: Number(response?.headers.get('x-dharmasearch-cached-at')) || 0,
    };
  }));
  entries.sort((left, right) => left.cachedAt - right.cachedAt);

  let total = entries.reduce((sum, entry) => sum + entry.size, 0);
  for (const entry of entries) {
    if (total <= MAX_AUDIO_BYTES) break;
    if (await cache.delete(entry.request)) total -= entry.size;
  }
}

function audioCacheKey(request) {
  return new Request(request.url, {
    method: 'GET',
    credentials: 'same-origin',
  });
}

async function responseForAudioRequest(response, request) {
  const range = request.headers.get('range');
  if (!range) return response;

  const match = /^bytes=(\d*)-(\d*)$/.exec(range);
  const payload = await response.arrayBuffer();
  const total = payload.byteLength;
  if (!match || !total) {
    return new Response(null, {
      status: 416,
      headers: { 'Content-Range': `bytes */${total}` },
    });
  }

  let start;
  let end;
  if (!match[1]) {
    const suffixLength = Number(match[2]);
    if (!Number.isInteger(suffixLength) || suffixLength <= 0) {
      return new Response(null, {
        status: 416,
        headers: { 'Content-Range': `bytes */${total}` },
      });
    }
    start = Math.max(total - suffixLength, 0);
    end = total - 1;
  } else {
    start = Number(match[1]);
    end = match[2] ? Math.min(Number(match[2]), total - 1) : total - 1;
  }

  if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || start > end || start >= total) {
    return new Response(null, {
      status: 416,
      headers: { 'Content-Range': `bytes */${total}` },
    });
  }

  const headers = new Headers(response.headers);
  headers.set('Accept-Ranges', 'bytes');
  headers.set('Content-Length', String(end - start + 1));
  headers.set('Content-Range', `bytes ${start}-${end}/${total}`);
  return new Response(payload.slice(start, end + 1), {
    status: 206,
    statusText: 'Partial Content',
    headers,
  });
}

async function audioOnDemand(request, event) {
  const cache = await caches.open(AUDIO_CACHE);
  const cacheKey = audioCacheKey(request);
  const cached = await cache.match(cacheKey);
  if (cached) {
    const touched = withCachedAt(cached.clone());
    event.waitUntil(cache.put(cacheKey, touched.clone()).then(() => trimAudioCache(cache)));
    return responseForAudioRequest(touched, request);
  }

  // Fetch without the Range header so one canonical response can satisfy every
  // browser range request and replay offline.
  const response = await fetch(request.url, {
    cache: 'no-store',
    credentials: 'same-origin',
  });
  if (response.ok && response.status === 200) {
    const stored = withCachedAt(response.clone());
    event.waitUntil(cache.put(cacheKey, stored).then(() => trimAudioCache(cache)));
    return responseForAudioRequest(response, request);
  }
  return response;
}

async function staleWhileRevalidate(request, event, fallbackUrl) {
  const cache = await caches.open(APP_CACHE);
  const cached = await cache.match(request);
  const network = fetch(request, { cache: 'no-store' }).then(response => {
    if (response.ok) event.waitUntil(cache.put(request, response.clone()));
    return response;
  });

  if (cached) {
    event.waitUntil(network.catch(() => undefined));
    return cached;
  }

  try {
    return await network;
  } catch (error) {
    if (fallbackUrl) {
      const fallback = await cache.match(fallbackUrl);
      if (fallback) return fallback;
    }
    throw error;
  }
}

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET' || !sameOriginUrl(request)) return;

  const url = new URL(request.url);
  if (url.pathname.startsWith('/audio/') && url.pathname.endsWith('.mp3')) {
    event.respondWith(audioOnDemand(request, event));
    return;
  }

  const appAsset = request.mode === 'navigate'
    || ['document', 'script', 'style'].includes(request.destination)
    || CORE_URLS.includes(url.pathname)
    || url.pathname === '/asset-manifest.json';

  if (appAsset) {
    event.respondWith(
      staleWhileRevalidate(request, event, request.mode === 'navigate' ? '/index.html' : null),
    );
  }
});

self.addEventListener('message', event => {
  if (event.data?.type === 'SKIP_WAITING') self.skipWaiting();
  if (event.data?.type === 'GET_VERSION') {
    event.source?.postMessage({ type: 'SW_VERSION', version: BUILD_VERSION });
  }
});
