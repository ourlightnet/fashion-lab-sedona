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

  /* Copy buttons (press boilerplate) ------------------------------------ */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector(btn.dataset.copy);
      if (!el || !navigator.clipboard) return;
      navigator.clipboard.writeText(el.textContent.trim()).then(function () {
        var label = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = label; }, 1800);
      });
    });
  });

  /* Newsletter placeholder ---------------------------------------------- */
  /* Videos: show a thumbnail, load the YouTube player only when clicked */
  document.querySelectorAll('a.video__play[data-video]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + a.dataset.video + '?autoplay=1';
      f.title = a.getAttribute('aria-label') || 'Video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      var box = document.createElement('div');
      box.className = 'video__frame';
      box.appendChild(f);
      a.replaceWith(box);
    });
  });

  /* get-started.html?support shows only the two paid options (linked from
     the playbook's support buttons): hide [data-support-hide] and swap in
     each [data-support] text. */
  if (/[?&]support\b/.test(window.location.search)) {
    document.querySelectorAll('[data-support-hide]').forEach(function (el) { el.hidden = true; });
    document.querySelectorAll('[data-support]').forEach(function (el) { el.textContent = el.dataset.support; });
  }

  /* Sign-up forms (Brevo) ------------------------------------------------
     Each form.signup posts to its Brevo form URL in the action attribute.
     Brevo replies with a page we don't need, so the post goes to a hidden
     iframe and we show our own thank-you. With no action set yet, the form
     falls back to opening an email to the team. */
  document.querySelectorAll('form.signup').forEach(function (form, i) {
    var done = form.querySelector('.signup__done');
    // A checkbox group with data-joins sends its ticked values as one
    // comma-separated field (Brevo stores it as text) and needs at least one.
    // Phone and texting consent (.sms-only) show only when something other
    // than Email is ticked. Hidden fields are disabled so they aren't sent.
    var joined = form.querySelector('[data-joins]');
    var smsOnly = form.querySelectorAll('.sms-only');
    function syncChoices() {
      if (!joined) return;
      var boxes = joined.querySelectorAll('input[type=checkbox]');
      var picked = Array.prototype.filter.call(boxes, function (b) { return b.checked; }).map(function (b) { return b.value; });
      joined.querySelector('input[name="' + joined.dataset.joins + '"]').value = picked.join(', ');
      boxes[0].setCustomValidity(picked.length ? '' : 'Please choose at least one.');
      var show = picked.some(function (v) { return v !== 'Email'; });
      smsOnly.forEach(function (el) {
        el.hidden = !show;
        el.querySelectorAll('input, select').forEach(function (inp) { inp.disabled = !show; });
      });
    }
    syncChoices();
    form.addEventListener('change', syncChoices);
    form.addEventListener('reset', function () { setTimeout(syncChoices); });
    form.addEventListener('submit', function (e) {
      var action = form.getAttribute('action');
      if (!action) {
        e.preventDefault();
        var lines = [];
        form.querySelectorAll('input[name]:not([type=hidden]):not(.signup__trap)').forEach(function (inp) {
          if (inp.value) lines.push((inp.closest('label') ? inp.closest('label').firstChild.textContent.trim() : inp.name) + ': ' + inp.value);
        });
        window.location.href = 'mailto:info@fashionlabsedona.com?subject=' + encodeURIComponent(form.dataset.fallbackSubject || 'Fashion Lab updates') + '&body=' + encodeURIComponent('Please add me to the list.\n\n' + lines.join('\n'));
        return;
      }
      // Brevo wants the phone as digits only, without the country code.
      var phone = form.querySelector('input[name=SMS]');
      var cc = form.querySelector('select[name=SMS__COUNTRY_CODE]');
      if (phone) {
        var digits = phone.value.replace(/\D/g, '');
        var code = cc ? cc.value.replace(/\D/g, '') : '';
        if (code && digits.indexOf(code) === 0 && digits.length > 10) digits = digits.slice(code.length);
        phone.value = digits;
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
        // A form with data-next moves on to that page once it's sent.
        if (form.dataset.next) setTimeout(function () { window.location.href = form.dataset.next; }, 1200);
      }, 400);
    });
  });

  /* Email links ------------------------------------------------------------
     A mailto: link does nothing for people without an email app set up
     (common with Gmail in the browser). So every email link opens a small
     panel instead: open the email app, open Gmail, or copy the address. */
  var mailDialog;
  function openMail(href) {
    var q = href.replace(/^mailto:/i, '').split('?');
    var to = decodeURIComponent(q[0]);
    var params = new URLSearchParams(q[1] || '');
    var subject = params.get('subject') || '';
    var body = params.get('body') || '';
    if (!mailDialog) {
      // Styles live here, next to the panel, so the panel never shows unstyled.
      var st = document.createElement('style');
      st.textContent =
        '.mail-dialog{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:110;align-items:center;justify-content:center;padding:16px}' +
        '.mail-dialog.is-open{display:flex}' +
        '.mail-dialog__box{position:relative;background:#fff;color:#111;border-radius:8px;padding:32px 28px 28px;max-width:460px;width:100%;box-shadow:0 10px 30px rgba(0,0,0,.12)}' +
        '.mail-dialog__close{position:absolute;top:10px;right:12px;background:none;border:0;font-size:1.8rem;line-height:1;cursor:pointer;color:#111}' +
        '.mail-dialog__to{font-size:1.15rem;font-weight:700;margin:6px 0 4px;word-break:break-all}' +
        '.mail-dialog__subject{font-size:.9rem;margin:0 0 18px}' +
        '.mail-dialog__actions{display:grid;gap:10px}' +
        '.mail-dialog__actions .btn{width:100%;justify-content:center;text-align:center}';
      document.head.appendChild(st);
      mailDialog = document.createElement('div');
      mailDialog.className = 'mail-dialog';
      mailDialog.setAttribute('role', 'dialog');
      mailDialog.setAttribute('aria-modal', 'true');
      mailDialog.setAttribute('aria-labelledby', 'mail-dialog-title');
      mailDialog.innerHTML =
        '<div class="mail-dialog__box">' +
        '<button class="mail-dialog__close" type="button" aria-label="Close">×</button>' +
        '<h3 id="mail-dialog-title">Email us</h3>' +
        '<p class="mail-dialog__to"><a class="mail-dialog__addr"></a></p>' +
        '<p class="mail-dialog__subject muted"></p>' +
        '<div class="mail-dialog__actions">' +
        '<a class="btn btn--sedona mail-dialog__gmail" target="_blank" rel="noopener">Open in Gmail</a>' +
        '<a class="btn mail-dialog__app">Open my email app</a>' +
        '<button class="btn btn--ghost mail-dialog__copy" type="button">Copy address</button>' +
        '</div></div>';
      document.body.appendChild(mailDialog);
      var close = function () { mailDialog.classList.remove('is-open'); };
      mailDialog.querySelector('.mail-dialog__close').addEventListener('click', close);
      mailDialog.addEventListener('click', function (e) { if (e.target === mailDialog) close(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
      mailDialog.querySelector('.mail-dialog__copy').addEventListener('click', function () {
        var btn = this, addr = mailDialog.dataset.to;
        var done = function () { btn.textContent = 'Copied!'; setTimeout(function () { btn.textContent = 'Copy address'; }, 2000); };
        if (navigator.clipboard) navigator.clipboard.writeText(addr).then(done, function () { window.prompt('Copy our email address:', addr); });
        else window.prompt('Copy our email address:', addr);
      });
    }
    mailDialog.dataset.to = to;
    var addr = mailDialog.querySelector('.mail-dialog__addr');
    addr.textContent = to; addr.href = href;
    mailDialog.querySelector('.mail-dialog__subject').textContent = subject ? 'Subject: ' + subject : '';
    mailDialog.querySelector('.mail-dialog__app').href = href;
    mailDialog.querySelector('.mail-dialog__gmail').href = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(to) +
      (subject ? '&su=' + encodeURIComponent(subject) : '') + (body ? '&body=' + encodeURIComponent(body) : '');
    mailDialog.classList.add('is-open');
    mailDialog.querySelector('.mail-dialog__gmail').focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="mailto:"]');
    if (!a || a.closest('.mail-dialog') || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault();
    openMail(a.getAttribute('href'));
  });
})();
