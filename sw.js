// ============================================================
// 373Kice Service Worker — 离线缓存策略
// ============================================================
// 策略：
//   - 静态资源（CSS/JS/字体/图标）：Cache First
//   - 页面/文章（HTML）：Network First，回退到缓存
//   - API/外部资源：Network Only

const CACHE_NAME = '373kice-v1'
const PRECACHE_URLS = [
  '/',
  '/css/main.css',
  '/js/main.js',
  '/js/smooth-scroll.min.js',
  '/js/pageContent.js',
  '/manifest.json',
  '/favicon.ico'
]

// ----- 安装：预缓存核心资源 -----
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(PRECACHE_URLS)
    }).then(function() {
      return self.skipWaiting()
    })
  )
})

// ----- 激活：清理旧缓存 -----
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.filter(function(name) {
          return name !== CACHE_NAME
        }).map(function(name) {
          return caches.delete(name)
        })
      )
    }).then(function() {
      return self.clients.claim()
    })
  )
})

// ----- 请求拦截 -----
self.addEventListener('fetch', function(event) {
  var request = event.request
  var url = new URL(request.url)

  // 只处理同源请求
  if (url.origin !== location.origin) return

  var path = url.pathname

  // 静态资源：Cache First
  if (path.match(/\.(css|js|json|png|jpg|gif|svg|ico|woff2?|ttf|eot)$/)) {
    event.respondWith(cacheFirst(request))
    return
  }

  // 页面/文章：Network First
  if (path.match(/^\/\d{4}\//) || path === '/' || path.match(/^\/page\//)) {
    event.respondWith(networkFirst(request))
    return
  }

  // 其他：Network First
  event.respondWith(networkFirst(request))
})

// ----- 缓存优先策略 -----
function cacheFirst(request) {
  return caches.match(request).then(function(cached) {
    return cached || fetch(request).then(function(response) {
      return caches.open(CACHE_NAME).then(function(cache) {
        cache.put(request, response.clone())
        return response
      })
    })
  })
}

// ----- 网络优先策略（带缓存回退） -----
function networkFirst(request) {
  return fetch(request).then(function(response) {
    return caches.open(CACHE_NAME).then(function(cache) {
      cache.put(request, response.clone())
      return response
    })
  }).catch(function() {
    return caches.match(request).then(function(cached) {
      return cached || new Response('离线', { status: 503 })
    })
  })
}
