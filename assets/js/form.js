(() => {
  const forms = [...document.querySelectorAll('[data-contact-form]')];
  if (!forms.length) return;

  const language = document.documentElement.lang === 'en' ? 'en' : 'uk';
  const messages = {
    uk: {
      sending: 'Надсилаємо звернення…',
      delivered: 'Дякуємо. Звернення успішно доставлено.',
      mock: 'Тестовий режим: форму перевірено, але повідомлення не надсилалося в Telegram.',
      error: 'Не вдалося надіслати звернення. Спробуйте ще раз або зв’яжіться з нами напряму.'
    },
    en: {
      sending: 'Sending your enquiry…',
      delivered: 'Thank you. Your enquiry has been delivered.',
      mock: 'Test mode: the form was validated, but no message was sent to Telegram.',
      error: 'The enquiry could not be sent. Please try again or contact us directly.'
    }
  }[language];

  let csrfToken = '';
  const csrfEndpoint = new URL('csrf.php', forms[0].action).href;
  const refreshToken = async () => {
    try {
      const response = await fetch(csrfEndpoint, {
        credentials: 'same-origin',
        headers: { Accept: 'application/json' }
      });
      if (!response.ok) throw new Error('Token request failed');
      const data = await response.json();
      csrfToken = data.token || '';
    } catch (_) {
      csrfToken = '';
    }
  };

  const initialTokenRequest = refreshToken();

  forms.forEach((form) => {
    const status = form.querySelector('[data-form-status]');
    const submit = form.querySelector('button[type="submit"]');
    const setStatus = (message, type = '') => {
      status.textContent = message;
      status.className = `form-status ${type}`.trim();
    };

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      submit.disabled = true;
      setStatus(messages.sending);
      await initialTokenRequest;

      if (!csrfToken) {
        setStatus(messages.mock, 'success');
        form.reset();
        submit.disabled = false;
        return;
      }

      try {
        const data = new FormData(form);
        data.set('csrf_token', csrfToken);
        data.set('language', language);
        data.set('source', `${window.location.pathname}${window.location.hash}`);
        const response = await fetch(form.action, {
          method: 'POST',
          body: data,
          credentials: 'same-origin',
          headers: { Accept: 'application/json' }
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || !result.ok) throw new Error(result.message || 'Request failed');
        setStatus(result.delivered ? messages.delivered : messages.mock, 'success');
        form.reset();
        await refreshToken();
      } catch (_) {
        setStatus(messages.error, 'error');
      } finally {
        submit.disabled = false;
      }
    });
  });
})();
