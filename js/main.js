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

//////////////////////////dark mode toggle////////////////////////////
(function() {
  // 绑定所有 .header-icon-btn 中的暗色模式按钮（桌面 + 移动）
  var toggles = document.querySelectorAll('#darkModeToggle, #darkModeToggleMob')
  if (toggles.length === 0) return

  var savedTheme = localStorage.getItem('theme')
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.setAttribute('data-theme', 'dark')
    toggles.forEach(function(btn) {
      var icon = btn.querySelector('i')
      if (icon) { icon.className = 'fa-solid fa-sun' }
    })
  }

  toggles.forEach(function(toggle) {
    toggle.onclick = function() {
      var html = document.documentElement
      var isDark = html.getAttribute('data-theme') === 'dark'
      if (isDark) {
        html.removeAttribute('data-theme')
        localStorage.setItem('theme', 'light')
        toggles.forEach(function(btn) {
          var icon = btn.querySelector('i')
          if (icon) { icon.className = 'fa-regular fa-moon' }
        })
      } else {
        html.setAttribute('data-theme', 'dark')
        localStorage.setItem('theme', 'dark')
        toggles.forEach(function(btn) {
          var icon = btn.querySelector('i')
          if (icon) { icon.className = 'fa-solid fa-sun' }
        })
      }
    }
  })
}());

//////////////////////////search toggle////////////////////////////
(function() {
  var searchToggles = document.querySelectorAll('#searchToggle, #searchToggleMob')
  var searchContainer = document.querySelector('#searchContainer')
  var searchInput = document.querySelector('#search-input')
  var searchClose = document.querySelector('#searchClose')
  if (searchToggles.length === 0 || !searchContainer) return

  function openSearch() {
    searchContainer.classList.add('search-open')
    setTimeout(function() { searchInput.focus() }, 100)
  }

  function closeSearch(resetInput) {
    searchContainer.classList.remove('search-open')
    if (resetInput !== false && searchInput) {
      searchInput.value = ''
    }
    var results = document.querySelector('#search-results')
    if (results) {
      results.innerHTML = ''
      results.classList.remove('search-active')
    }
  }

  searchToggles.forEach(function(toggle) {
    toggle.addEventListener('click', function(e) {
      e.stopPropagation()
      if (searchContainer.classList.contains('search-open')) {
        closeSearch()
      } else {
        openSearch()
      }
    })
  })

  if (searchClose) {
    searchClose.addEventListener('click', function(e) {
      e.stopPropagation()
      closeSearch()
    })
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

//////////////////////////back to top////////////////////////////
(function() {
  var backToTop = document.querySelector('.back-to-top')
  window.addEventListener('scroll', function() {
    var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop)
    if (scrollTop > 200) {
      backToTop.classList.add('back-to-top-show')
    } else {
      backToTop.classList.remove('back-to-top-show')
    }
  })
}());

//////////////////////////hover on demo//////////////////////////////
(function() {
  var demoItems = document.querySelectorAll('.grid-item')
}());
