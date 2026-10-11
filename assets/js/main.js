const menuToggle = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() {
  menuToggle.setAttribute('aria-expanded', 'false');
  mobileNav.hidden = true;
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(open));
  mobileNav.hidden = !open;
});
mobileNav.querySelectorAll('a, button').forEach(link => link.addEventListener('click', closeMenu));
window.matchMedia('(min-width:641px)').addEventListener('change', event => {
  if (event.matches) closeMenu();
});
const dialogOpeners = new WeakMap();
document.querySelectorAll('[data-open]').forEach(button => {
  button.addEventListener('click', () => {
    const dialog = document.getElementById(button.dataset.open);
    if (dialog) {
      dialogOpeners.set(dialog, button);
      dialog.showModal();
    }
  });
});
document.querySelectorAll('dialog').forEach(dialog => {
  dialog.addEventListener('close', () => {
    if (dialogOpeners.get(dialog)?.closest('#mobile-nav') && mobileNav.hidden) menuToggle.focus();
  });
  dialog.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => dialog.close()));
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuToggle.focus();
  }
});
