/*
 * toasts.js — módulo de notificações do Escolta System
 * ───────────────────────────────────────────────────────
 * • Consome automaticamente #messages-data produzido pelo base.html
 * • Expõe window.Toast.push(type, title, desc?) para uso em JS
 * • Auto-dismiss em 4s (7s para erros)
 * • Empilha no canto superior direito
 */
(function () {
  const ICONS = {
    success: '<polyline points="20 6 9 17 4 12"/>',
    error:   '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    warning: '<path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    info:    '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
  };

  // Mapa de tags do Django messages framework para nossos tipos
  const DJANGO_LEVEL_MAP = {
    debug:   'info',
    info:    'info',
    success: 'success',
    warning: 'warning',
    error:   'error',
  };

  function ensureStack() {
    let stack = document.getElementById('toast-stack');
    if (!stack) {
      stack = document.createElement('div');
      stack.id = 'toast-stack';
      stack.className = 'toast-stack';
      document.body.appendChild(stack);
    }
    return stack;
  }

  function push(type, title, desc) {
    type = type || 'info';
    if (!ICONS[type]) type = 'info';
    const stack = ensureStack();
    const t = document.createElement('div');
    t.className = 'toast';
    t.dataset.type = type;
    t.innerHTML = `
      <div class="toast-icon">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2.5"
             stroke-linecap="round" stroke-linejoin="round">${ICONS[type]}</svg>
      </div>
      <div class="toast-body">
        <div class="toast-title"></div>
        ${desc ? '<div class="toast-desc"></div>' : ''}
      </div>
      <button class="toast-close" aria-label="Fechar">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    `;
    // Inserir texto com segurança (sem innerHTML para conteúdo dinâmico)
    t.querySelector('.toast-title').textContent = title || '';
    if (desc) t.querySelector('.toast-desc').textContent = desc;

    const close = () => {
      t.style.opacity = '0';
      t.style.transform = 'translateX(20px)';
      setTimeout(() => t.remove(), 220);
    };
    t.querySelector('.toast-close').addEventListener('click', close);
    stack.appendChild(t);

    const timeout = type === 'error' ? 7000 : 4000;
    setTimeout(close, timeout);
  }

  // Lê mensagens Django serializadas em <script id="messages-data">
  function consumeDjangoMessages() {
    const el = document.getElementById('messages-data');
    if (!el) return;
    let data;
    try { data = JSON.parse(el.textContent.trim() || '[]'); }
    catch (e) { return; }
    data.forEach(m => {
      const type = DJANGO_LEVEL_MAP[m.level] || 'info';
      push(type, m.text);
    });
  }

  document.addEventListener('DOMContentLoaded', consumeDjangoMessages);
  window.Toast = { push };
})();
