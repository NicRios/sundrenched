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
function openDialog(id, opener) {
  const dialog = document.getElementById(id);
  if (dialog) {
    dialogOpeners.set(dialog, opener);
    dialog.showModal();
  }
}
document.querySelectorAll('[data-open]').forEach(button => {
  button.addEventListener('click', () => openDialog(button.dataset.open, button));
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

const searchInput = document.querySelector('#site-search');
const searchResults = document.querySelector('#search-results');
const searchStatus = document.querySelector('#search-status');
const searchDialog = document.querySelector('#search-dialog');
const searchButton = document.querySelector('[data-open="search-dialog"]');
const searchEntries = [
  { title: 'Shop all', description: 'Browse the Sun Drenched swimwear and surf-suit collection.', keywords: 'shop products swimwear swimsuits bikini surf suits heat wave', href: 'shop.html' },
  { title: 'Swimwear', description: 'Discover the Heat Wave collection and playful sun-inspired prints.', keywords: 'swim swimsuits one piece bikini heat wave new collection', dialog: 'swimwear-dialog' },
  { title: 'Wetsuits', description: 'Bold florals and long-sleeved surf suits for ocean days.', keywords: 'surf waves long sleeve floral swim collection', dialog: 'wetsuits-dialog' },
  { title: 'Jewelry', description: 'Shells, natural shapes, and a little piece of the coast.', keywords: 'necklace shells cowrie siren accessories collection', dialog: 'jewelry-dialog' },
  { title: 'Our ocean, our home', description: 'Small ways to care for the places we love.', keywords: 'about story ocean care environment beach wildlife coral', dialog: 'ocean-dialog' },
  { title: 'The Sun Drenched Journal', description: 'Beach-day inspiration and stories from our community.', keywords: 'blog stories community friends shoreline inspiration', dialog: 'journal-dialog' },
  { title: 'Care guide', description: 'Everyday tips for looking after swimwear and jewelry.', keywords: 'wash clean dry rinse product care', dialog: 'care-dialog' },
  { title: 'Frequently asked questions', description: 'Collection questions, care information, and getting in touch.', keywords: 'faq help contact availability email', dialog: 'faq-dialog' }
];
function renderSearch() {
  const query = searchInput.value.trim().toLocaleLowerCase();
  const terms = query.split(/\s+/).filter(Boolean);
  const matches = searchEntries.filter(entry => {
    const text = `${entry.title} ${entry.description} ${entry.keywords}`.toLocaleLowerCase();
    return terms.every(term => text.includes(term));
  });
  searchResults.replaceChildren();
  searchStatus.textContent = query
    ? (matches.length ? `${matches.length} ${matches.length === 1 ? 'match' : 'matches'} for “${searchInput.value.trim()}”` : 'No matches yet. Try swimwear, ocean, or care.')
    : 'Explore our collections and stories.';
  matches.forEach(entry => {
    const button = document.createElement(entry.href ? 'a' : 'button');
    if (entry.href) button.href = entry.href;
    else button.type = 'button';
    button.className = 'search-result';
    const title = document.createElement('strong');
    const description = document.createElement('span');
    title.textContent = entry.title;
    description.textContent = entry.description;
    button.append(title, description);
    button.addEventListener('click', () => {
      searchDialog.close();
      if (entry.dialog) openDialog(entry.dialog, searchButton);
    });
    searchResults.append(button);
  });
}
searchInput.addEventListener('input', renderSearch);
document.querySelector('.search-form').addEventListener('submit', event => {
  event.preventDefault();
  renderSearch();
});
renderSearch();
