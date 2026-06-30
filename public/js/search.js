(function(){
  var input = document.getElementById('search-input');
  var dropdown = document.getElementById('search-results');
  if (!input || !dropdown) return;

  var index = null;
  var selected = -1;

  // Load search index
  fetch('/search-index.json')
    .then(function(r){ return r.json(); })
    .then(function(data){ index = data; })
    .catch(function(){ console.log('Search index not available'); });

  function fuzzyMatch(text, query) {
    text = text.toLowerCase();
    query = query.toLowerCase();
    if (text.indexOf(query) !== -1) return 1; // exact substring
    // Simple fuzzy: all chars in order
    var qi = 0;
    for (var i = 0; i < text.length && qi < query.length; i++) {
      if (text[i] === query[qi]) qi++;
    }
    return qi === query.length ? 0.5 : 0;
  }

  function search(query) {
    if (!index || query.length < 2) { dropdown.classList.remove('active'); return; }
    var results = [];
    for (var i = 0; i < index.length; i++) {
      var page = index[i];
      var score = 0;
      score += fuzzyMatch(page.title, query) * 3;
      score += fuzzyMatch(page.summary, query);
      if (page.tags) {
        for (var j = 0; j < page.tags.length; j++) {
          score += fuzzyMatch(page.tags[j], query) * 2;
        }
      }
      if (score > 0) results.push({ page: page, score: score });
    }
    results.sort(function(a,b){ return b.score - a.score; });
    results = results.slice(0, 8);

    if (results.length === 0) {
      dropdown.innerHTML = '<div class="search-no-results">No results for "' + escapeHtml(query) + '"</div>';
    } else {
      var html = '';
      for (var k = 0; k < results.length; k++) {
        var r = results[k];
        var sectionLabel = { cuisine: '🍜 Food', posts: '📝 Tech', tea: '🍵 Tea', baijiu: '🥃 Baijiu' }[r.page.section] || r.page.section;
        html += '<a class="search-result" href="' + r.page.url + '">';
        html += '<div class="result-title">' + highlightMatch(r.page.title, query) + '</div>';
        html += '<span class="result-section">' + sectionLabel + '</span>';
        html += '<span class="result-meta">' + r.page.date + '</span>';
        html += '<div class="result-summary">' + highlightMatch(truncate(r.page.summary, 120), query) + '</div>';
        html += '</a>';
      }
      dropdown.innerHTML = html;
    }
    dropdown.classList.add('active');
    selected = -1;
  }

  function highlightMatch(text, query) {
    var re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return escapeHtml(text).replace(re, '<mark>$1</mark>');
  }

  function escapeHtml(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function truncate(s, n) {
    return s.length > n ? s.substring(0, n) + '...' : s;
  }

  var timer;
  input.addEventListener('input', function(){
    clearTimeout(timer);
    timer = setTimeout(function(){ search(input.value.trim()); }, 200);
  });

  input.addEventListener('keydown', function(e){
    var items = dropdown.querySelectorAll('.search-result');
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selected = Math.min(selected + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selected = Math.max(selected - 1, -1);
      updateSelection(items);
    } else if (e.key === 'Enter' && selected >= 0) {
      e.preventDefault();
      items[selected].click();
    } else if (e.key === 'Escape') {
      dropdown.classList.remove('active');
      input.blur();
    }
  });

  function updateSelection(items) {
    items.forEach(function(item, i){
      if (i === selected) { item.classList.add('active'); item.scrollIntoView({block:'nearest'}); }
      else { item.classList.remove('active'); }
    });
  }

  // Click outside closes
  document.addEventListener('click', function(e){
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove('active');
    }
  });

  // Click on input shows recent if empty
  input.addEventListener('focus', function(){
    if (input.value.trim().length >= 2) search(input.value.trim());
  });
})();
