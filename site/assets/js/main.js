/* Fashion Lab Sedona — shared behaviour: mobile nav, lightbox, reveal,
   contract viewer, budget calculator. Vanilla JS, no dependencies. */
(function () {
  'use strict';

  /* Mobile nav ----------------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') nav.classList.remove('is-open');
    });
  }

  /* Reveal on scroll ----------------------------------------------------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* Lightbox ------------------------------------------------------------- */
  var galleries = document.querySelectorAll('[data-gallery]');
  if (galleries.length) {
    var lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML = '<button class="lb-close" aria-label="Close">×</button>' +
      '<button class="lb-prev" aria-label="Previous">‹</button>' +
      '<img alt="">' +
      '<button class="lb-next" aria-label="Next">›</button>' +
      '<div class="lb-cap"></div>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('.lb-cap');
    var items = [], index = 0;

    function show(i) {
      index = (i + items.length) % items.length;
      lbImg.src = items[index].href;
      lbImg.alt = items[index].querySelector('img') ? items[index].querySelector('img').alt : '';
      lbCap.textContent = items[index].dataset.caption || '';
    }
    function open(list, i) { items = list; lb.classList.add('is-open'); document.body.style.overflow = 'hidden'; show(i); }
    function close() { lb.classList.remove('is-open'); document.body.style.overflow = ''; }

    galleries.forEach(function (g) {
      var links = Array.prototype.slice.call(g.querySelectorAll('a[href]'));
      links.forEach(function (a, i) {
        a.addEventListener('click', function (e) { e.preventDefault(); open(links, i); });
      });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  /* Contract viewer ------------------------------------------------------ */
  var dlg = document.getElementById('docview');
  if (dlg) {
    var scroll = dlg.querySelector('.docview__scroll');
    var title = dlg.querySelector('.docview__title');
    document.querySelectorAll('[data-doc]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var tpl = document.getElementById('doc-' + btn.dataset.doc);
        if (!tpl) return;
        scroll.innerHTML = '';
        scroll.appendChild(tpl.content.cloneNode(true));
        title.textContent = btn.dataset.title || btn.querySelector('h3').textContent;
        if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
        scroll.scrollTop = 0;
      });
    });
    dlg.querySelector('.docview__close').addEventListener('click', function () { dlg.close(); });
    dlg.querySelector('.docview__print').addEventListener('click', function () { window.print(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }

  /* Budget calculator ---------------------------------------------------- */
  var budget = document.querySelector('table.budget');
  if (budget) {
    var fmt = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
    function recalc() {
      var totals = { income: 0, expense: 0 };
      budget.querySelectorAll('tbody').forEach(function (tb) {
        var kind = tb.dataset.kind; // income | expense
        var sub = 0;
        tb.querySelectorAll('input[data-your]').forEach(function (inp) {
          var v = parseFloat(inp.value); if (!isNaN(v)) sub += v;
        });
        var cell = tb.querySelector('.subtotal .your');
        if (cell) cell.textContent = fmt(sub);
        if (kind) totals[kind] += sub;
      });
      var inc = document.getElementById('sum-income'), exp = document.getElementById('sum-expense'), net = document.getElementById('sum-net');
      if (inc) inc.textContent = fmt(totals.income);
      if (exp) exp.textContent = fmt(totals.expense);
      var ec = document.getElementById('sum-expense-cell'), nc = document.getElementById('sum-net-cell');
      if (ec) ec.textContent = fmt(totals.expense);
      if (net) { var d = totals.income - totals.expense; if (nc) nc.textContent = (d < 0 ? '−' : '') + fmt(Math.abs(d)); net.textContent = (d < 0 ? '−' : '') + fmt(Math.abs(d)); net.className = d < 0 ? 'neg' : 'pos'; }
    }
    budget.addEventListener('input', recalc);
    var fill = document.getElementById('budget-fill');
    if (fill) fill.addEventListener('click', function () {
      budget.querySelectorAll('input[data-your]').forEach(function (inp) { inp.value = inp.dataset.sedona || ''; });
      recalc();
    });
    var clear = document.getElementById('budget-clear');
    if (clear) clear.addEventListener('click', function () {
      budget.querySelectorAll('input[data-your]').forEach(function (inp) { inp.value = ''; });
      recalc();
    });
    recalc();
  }

  /* Newsletter placeholder ---------------------------------------------- */
  /* Sign-up forms (Brevo) ------------------------------------------------
     Each form.signup posts to its Brevo form URL in the action attribute.
     Brevo replies with a page we don't need, so the post goes to a hidden
     iframe and we show our own thank-you. With no action set yet, the form
     falls back to opening an email to the team. */
  document.querySelectorAll('form.signup').forEach(function (form, i) {
    var done = form.querySelector('.signup__done');
    form.addEventListener('submit', function (e) {
      var action = form.getAttribute('action');
      if (!action) {
        e.preventDefault();
        var lines = [];
        form.querySelectorAll('input[name]:not([type=hidden]):not(.signup__trap)').forEach(function (inp) {
          if (inp.value) lines.push((inp.closest('label') ? inp.closest('label').firstChild.textContent.trim() : inp.name) + ': ' + inp.value);
        });
        window.location.href = 'mailto:fashionlabsedona@gmail.com?subject=' + encodeURIComponent(form.dataset.fallbackSubject || 'Fashion Lab updates') + '&body=' + encodeURIComponent('Please add me to the list.\n\n' + lines.join('\n'));
        return;
      }
      var name = 'signup-frame-' + i;
      if (!document.querySelector('iframe[name="' + name + '"]')) {
        var f = document.createElement('iframe');
        f.name = name; f.hidden = true; f.title = 'Sign-up';
        document.body.appendChild(f);
      }
      form.target = name;
      setTimeout(function () {
        form.reset();
        if (done) done.hidden = false;
      }, 400);
    });
  });
})();
