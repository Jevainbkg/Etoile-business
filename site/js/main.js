// JS minimal : menu mobile, année, apparition douce, validation du formulaire
(function () {
  var toggle = document.querySelector('.nav__toggle');
  var list = document.getElementById('nav-list');
  if (toggle && list) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      list.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && list.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        list.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Apparition des sections : le contenu reste visible sans JS
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // Formulaire : validation côté client (la validation serveur reste obligatoire)
  var form = document.querySelector('[data-form]');
  if (!form) return;
  var status = form.querySelector('.form__status');
  var msg = JSON.parse(form.getAttribute('data-messages'));
  function setError(input, text) {
    var err = document.getElementById(input.id + '-error');
    input.setAttribute('aria-invalid', text ? 'true' : 'false');
    if (err) err.textContent = text || '';
  }
  function check(input) {
    var v = input.value.trim();
    if (input.required && !v) { setError(input, msg.required); return false; }
    if (input.type === 'tel' && v && !/^\+?[0-9 ().-]{8,20}$/.test(v)) { setError(input, msg.phone); return false; }
    if (input.name === 'message' && v && v.length < 10) { setError(input, msg.short); return false; }
    setError(input, ''); return true;
  }
  var fields = form.querySelectorAll('input:not([type="hidden"]):not([name="botcheck"]), textarea');
  fields.forEach(function (f) { f.addEventListener('blur', function () { check(f); }); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var ok = true, first = null;
    fields.forEach(function (f) { if (!check(f)) { ok = false; first = first || f; } });
    if (!ok) { first.focus(); return; }
    if (form.botcheck.value) return; // honeypot rempli : robot, on ignore
    var action = form.getAttribute('action');
    var key = form.access_key ? form.access_key.value : '';
    if (!action || action.charAt(0) === '#' || key.charAt(0) === '[') { status.className = 'form__status form__status--error'; status.textContent = msg.error; return; }
    var btn = form.querySelector('[type="submit"]');
    btn.disabled = true;
    fetch(action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || j.success === false) throw new Error(); }); })
      .then(function () { form.reset(); status.className = 'form__status'; status.textContent = msg.success; })
      .catch(function () { status.className = 'form__status form__status--error'; status.textContent = msg.error; })
      .then(function () { btn.disabled = false; });
  });
})();
