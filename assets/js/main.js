(() => {
  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav-links');
  const dropdownButton = document.querySelector('.dropdown > button');
  const dropdown = document.querySelector('.dropdown');

  const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 20);
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav?.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
  });

  dropdownButton?.addEventListener('click', () => {
    const open = dropdownButton.getAttribute('aria-expanded') !== 'true';
    dropdownButton.setAttribute('aria-expanded', String(open));
    dropdown?.classList.toggle('is-open', open);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    nav?.classList.remove('is-open');
    dropdown?.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
    dropdownButton?.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-open');
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  }

  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });
})();
