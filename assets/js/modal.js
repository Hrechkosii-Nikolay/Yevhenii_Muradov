(() => {
  const modal = document.querySelector('[data-project-modal]');
  if (!modal) return;

  const dialog = modal.querySelector('[role="dialog"]');
  const firstField = modal.querySelector('input:not([type="checkbox"])');
  const openers = document.querySelectorAll('[data-modal-open]');
  const closeButtons = modal.querySelectorAll('[data-modal-close]');
  let previouslyFocused = null;
  let previousPaddingRight = '';

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'textarea:not([disabled])',
    'select:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  const openModal = (event) => {
    event.preventDefault();
    previouslyFocused = document.activeElement;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    previousPaddingRight = document.body.style.paddingRight;
    if (scrollbarWidth > 0) document.body.style.paddingRight = `${scrollbarWidth}px`;
    modal.hidden = false;
    document.body.classList.add('modal-open');
    requestAnimationFrame(() => (firstField || dialog).focus());
  };

  const closeModal = () => {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove('modal-open');
    document.body.style.paddingRight = previousPaddingRight;
    if (previouslyFocused instanceof HTMLElement) previouslyFocused.focus();
  };

  openers.forEach((opener) => opener.addEventListener('click', openModal));
  closeButtons.forEach((button) => button.addEventListener('click', closeModal));

  document.addEventListener('keydown', (event) => {
    if (modal.hidden) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeModal();
      return;
    }
    if (event.key !== 'Tab') return;

    const focusable = [...modal.querySelectorAll(focusableSelector)].filter((element) => element.offsetParent !== null);
    if (!focusable.length) {
      event.preventDefault();
      dialog.focus();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
})();
