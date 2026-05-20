// ============================================================
// 搜索功能 — Lunr.js 全文检索
// ============================================================

(function() {
  var searchInput = document.querySelector('#search-input')
  var searchResults = document.querySelector('#search-results')
  if (!searchInput) return

  var posts = []
  var idx = null

  // 加载搜索索引
  function loadIndex() {
    var xhr = new XMLHttpRequest()
    xhr.open('GET', '/search.json', true)
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          posts = JSON.parse(xhr.responseText)
          buildIndex()
        } catch(e) {
          console.log('搜索索引解析失败:', e)
        }
      }
    }
    xhr.onerror = function() {
      console.log('搜索索引加载失败')
    }
    xhr.send()
  }

  // 构建 Lunr 索引
  function buildIndex() {
    if (typeof lunr === 'undefined') {
      console.log('Lunr.js 未加载')
      return
    }
    idx = lunr(function() {
      this.ref('url')
      this.field('title', { boost: 10 })
      this.field('content', { boost: 5 })
      this.field('excerpt', { boost: 3 })
      this.field('categories', { boost: 2 })
      this.field('tags', { boost: 2 })

      posts.forEach(function(post) {
        this.add(post)
      }, this)
    })
  }

  // 执行搜索
  function doSearch(query) {
    if (!idx || !query || query.length < 1) {
      searchResults.innerHTML = ''
      searchResults.classList.remove('search-active')
      return
    }

    var results = idx.search(query)
    var html = ''

    if (results.length === 0) {
      html = '<div class="search-empty">未找到匹配结果</div>'
    } else {
      html = '<ul class="search-result-list">'
      var count = 0
      results.forEach(function(result) {
        if (count >= 10) return
        var post = posts.find(function(p) { return p.url === result.ref })
        if (!post) return
        count++
        html += '<li>'
        html += '<a href="' + post.url + '" class="search-result-item">'
        html += '<span class="search-result-title">' + highlight(post.title, query) + '</span>'
        html += '<span class="search-result-date">' + post.date + '</span>'
        html += '<span class="search-result-excerpt">' + highlight(post.excerpt, query) + '</span>'
        html += '</a>'
        html += '</li>'
      })
      html += '</ul>'
    }

    searchResults.innerHTML = html
    searchResults.classList.add('search-active')
  }

  // 高亮匹配关键词
  function highlight(text, query) {
    if (!text) return ''
    var words = query.trim().split(/\s+/)
    var result = text
    words.forEach(function(word) {
      if (word.length < 1) return
      var escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      var regex = new RegExp('(' + escaped + ')', 'gi')
      result = result.replace(regex, '<mark>$1</mark>')
    })
    return result
  }

  // 输入事件
  searchInput.addEventListener('input', function(e) {
    doSearch(e.target.value)
  })

  searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      searchContainer.classList.remove('search-open')
      searchResults.innerHTML = ''
      searchResults.classList.remove('search-active')
      searchInput.value = ''
      searchInput.blur()
    }
  })

  // 加载索引
  loadIndex()
}())
