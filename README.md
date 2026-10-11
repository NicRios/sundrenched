# Sun Drenched

A responsive website prototype in progress. The starter includes editable page sections, a mobile menu, accessible disclosure controls, and automatic GitHub Pages deployment. It has no checkout, account system, or backend.

Live preview: https://nicrios.github.io/sundrenched/

## Develop locally

No install or build step is required.

```sh
python3 -m http.server 4177 --bind 127.0.0.1
```

Open http://127.0.0.1:4177/ in a browser.

## Project structure

- `index.html`: page content and semantic layout.
- `assets/css/styles.css`: design tokens, layout, and mobile styles.
- `assets/js/main.js`: mobile navigation behavior.
- `assets/images/`: add approved photography and design assets here.
- `assets/favicon.svg`: temporary project monogram.
- `.github/workflows/pages.yml`: publishes only `index.html` and `assets/`.

## Continue the design

Replace the labeled visual placeholders and draft copy with approved project material. The current theme and illustrations establish a starting direction, not a final identity. Keep URLs relative so local preview and GitHub Pages use the same files. Check narrow mobile and desktop widths after layout changes.

## Publish

Work on a feature branch and open a pull request. Merging to `main` runs the Pages workflow; it can also be started manually from Actions. Repository Pages settings use GitHub Actions. A successful deployment publishes at the live preview URL above.
