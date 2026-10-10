(() => {
  const controls = document.querySelector('[data-portfolio-filters]');
  if (!controls) return;

  const buttons = [...controls.querySelectorAll('[data-filter]')];
  const projects = [...document.querySelectorAll('[data-category]')];

  controls.addEventListener('click', (event) => {
    const button = event.target.closest('[data-filter]');
    if (!button) return;
    const filter = button.dataset.filter;

    buttons.forEach((item) => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });

    projects.forEach((project) => {
      project.hidden = filter !== 'all' && project.dataset.category !== filter;
    });
  });
})();
