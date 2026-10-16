# Sun Drenched

A responsive swimwear website prototype built from the supplied Sun Drenched homepage wireframe and photography.

Live site: https://nicrios.github.io/sundrenched/

## Local development

This is a buildless HTML, CSS, and JavaScript site.

```sh
python3 -m http.server 4177 --bind 127.0.0.1
```

Open http://127.0.0.1:4177/.

## Structure

- `index.html`: utility navigation, collection cards, ocean and community stories, promotional banner, footer, and accessible content dialogs.
- `shop.html`: 16-product shop grid with placeholder images, product names, and prices from the shop wireframe. It uses the same utility navigation, header, footer, and dialogs as the homepage.
- `assets/css/styles.css`: reference palette, typography, responsive layouts, and logo framing.
- `assets/js/main.js`: mobile navigation, local collection/story search, and dialog controls.
- `assets/images/`: supplied product, lifestyle, and underwater photography. `brand-reference.png` preserves the supplied artwork; CSS frames the original header and footer logos without recreating them.
- `.github/workflows/pages.yml`: publishes `index.html`, `shop.html`, and `assets/` to GitHub Pages.

The layout follows the wireframe on desktop and tablet, including the source-specific photo crops. Photos use the palette brown at 20% opacity, with 30% on the hero and 50% on the mobile jewelry card. DynaPuff is used as a close visual match for the reference headings; the original heading font was not supplied. Below 641px, navigation collapses to a menu, product cards use two columns, and editorial sections stack. The shop uses four product columns above that breakpoint. Shop navigation, homepage promotions, and the swimwear and wetsuit cards link to `shop.html`; the jewelry button remains inactive until that collection is ready. Collection previews remain available through search. Editorial buttons open previews, and email links launch the visitor's mail app. Utility social icons open Instagram, TikTok, and X; replace those platform URLs when brand profiles are available. This prototype has no product-detail pages, checkout, payments, accounts, inventory, or form backend. Product cards are display-only and use `assets/images/product-placeholder.svg`. The displayed products, prices, collection and promotional text are design copy.

## Publication and checks

Use a feature branch and pull request. Merging to `main` deploys the site through the existing Pages workflow.

For layout changes, check 390px, 768px, and 1440px widths, verify every image loads, and exercise the menu, dialogs, Escape behavior, internal links, and footer links. Use `node --check assets/js/main.js` and `git diff --check` for the affected source.
