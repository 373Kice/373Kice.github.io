/**
 * some JavaScript code for this blog theme
 */
/* jshint asi:true */

/////////////////////////header////////////////////////////
/**
 * clickMenu
 */
(function() {
  if (window.innerWidth <= 770) {
    var menuBtn = document.querySelector('#headerMenu')
    var nav = document.querySelector('#headerNav')
    menuBtn.onclick = function(e) {
      e.stopPropagation()
      if (menuBtn.classList.contains('active')) {
        menuBtn.classList.remove('active')
        nav.classList.remove('nav-show')
      } else {
        nav.classList.add('nav-show')
        menuBtn.classList.add('active')
      }
    }
    document.querySelector('body').addEventListener('click', function() {
      nav.classList.remove('nav-show')
      menuBtn.classList.remove('active')
    })
  }
}());

//////////////////////////search toggle////////////////////////////
(function() {
  var searchToggle = document.querySelector('#searchToggle')
  var searchContainer = document.querySelector('#searchContainer')
  var searchInput = document.querySelector('#search-input')
  var searchClose = document.querySelector('#searchClose')
  if (!searchToggle || !searchContainer) return

  function openSearch() {
    searchContainer.classList.add('search-open')
    setTimeout(function() { searchInput.focus() }, 100)
  }

  function closeSearch() {
    searchContainer.classList.remove('search-open')
    if (searchInput) searchInput.value = ''
    var results = document.querySelector('#search-results')
    if (results) {
      results.innerHTML = ''
      results.classList.remove('search-active')
    }
  }

  searchToggle.addEventListener('click', function(e) {
    e.stopPropagation()
    if (searchContainer.classList.contains('search-open')) {
      closeSearch()
    } else {
      openSearch()
    }
  })

  if (searchClose) {
    searchClose.addEventListener('click', closeSearch)
  }

  // 按 / 键打开搜索
  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
      var tag = document.activeElement ? document.activeElement.tagName : ''
      if (tag !== 'INPUT' && tag !== 'TEXTAREA') {
        e.preventDefault()
        openSearch()
      }
    }
    if (e.key === 'Escape') {
      closeSearch()
    }
  })
}());

//////////////////////////dark mode toggle////////////////////////////
(function() {
  var toggle = document.querySelector('#darkModeToggle')
  var icon = toggle ? toggle.querySelector('i') : null
  if (!toggle) return

  // 读取已保存的主题偏好
  var savedTheme = localStorage.getItem('theme')
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark')
    if (icon) { icon.className = 'fa-solid fa-sun' }
  }

  toggle.onclick = function() {
    var html = document.documentElement
    var isDark = html.getAttribute('data-theme') === 'dark'
    if (isDark) {
      html.removeAttribute('data-theme')
      localStorage.setItem('theme', 'light')
      if (icon) { icon.className = 'fa-regular fa-moon' }
    } else {
      html.setAttribute('data-theme', 'dark')
      localStorage.setItem('theme', 'dark')
      if (icon) { icon.className = 'fa-solid fa-sun' }
    }
  }
}());

//////////////////////////back to top////////////////////////////
(function() {
  var backToTop = document.querySelector('.back-to-top')
  var backToTopA = document.querySelector('.back-to-top a')
  // console.log(backToTop);
  window.addEventListener('scroll', function() {

    // 页面顶部滚进去的距离
    var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop)

    if (scrollTop > 200) {
      backToTop.classList.add('back-to-top-show')
    } else {
      backToTop.classList.remove('back-to-top-show')
    }
  })

  // backToTopA.addEventListener('click',function (e) {
  //     e.preventDefault()
  //     window.scrollTo(0,0)
  // })
}());

//////////////////////////hover on demo//////////////////////////////
(function() {
  var demoItems = document.querySelectorAll('.grid-item')
}());
