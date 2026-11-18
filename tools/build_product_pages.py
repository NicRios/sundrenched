#!/usr/bin/env python3
"""Build the Sun Drenched product pages and link the shop grids to them.

Run from the repo root:   python3 tools/build_product_pages.py

What it does
  1. Writes one page per product (<slug>.html) using shop.html's utility bar, header,
     footer and dialogs, so the navigation stays identical to the rest of the site.
  2. Wraps every product card in shop.html, jewelry.html and wetsuits.html in a link to
     that product's page (safe to re-run; cards that are already linked are left alone).

All product facts, prices, reviews and policy text below are design copy for the prototype.
Prices must match the shop grid; the script stops if they ever drift apart.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_VERSION = "sellers-links"   # cache-busting tag on styles.css?v=...

# ---------------------------------------------------------------------------
# Product data, in Shop-page order
# ---------------------------------------------------------------------------
# cat: bikini | bodysuit | onepiece | wetsuit | jewelry     print: used to pick a related piece
PRODUCTS = [
    # --- bikini sets
    dict(slug="always-sunny-bikini-set", name="Always Sunny Bikini Set", cat="bikini", price=96, print="always-sunny",
         intro="Pink and chocolate starburst tiles come together in the Always Sunny Bikini Set, a playful print made for long beach days. The triangle top ties at the neck and back, and the matching side-tie bottoms let you dial in the fit.",
         reviews=(3, 1, 0)),
    dict(slug="heatwave-bikini-set", name="Heatwave Bikini Set", cat="bikini", price=96, print="heatwave",
         intro="Warm chocolate brown scattered with cream suns, the Heatwave Bikini Set is our signature print in its simplest form. A classic triangle top pairs with a cheeky-cut bottom with tie sides.",
         reviews=(5, 1, 0)),
    dict(slug="lei-me-down-bikini-set", name="Lei Me Down Bikini Set", cat="bikini", price=96, print="lei-me-down",
         intro="Inspired by fresh plumeria leis, the Lei Me Down Bikini Set layers pink, yellow and cream blooms in vertical stripes with deep burgundy trim. The triangle top and side-tie bottoms adjust to fit.",
         reviews=(2, 1, 0)),
    dict(slug="shellbound-bikini-set", name="Shellbound Bikini Set", cat="bikini", price=96, print="shellbound",
         intro="Coral and cream tiles filled with shells and starfish give the Shellbound Bikini Set its treasure-hunt charm. Halter ties up top and side ties below keep the fit easy to adjust.",
         reviews=(6, 2, 0)),
    # --- bodysuits
    dict(slug="heatwave-bodysuit", name="Heatwave Bodysuit", cat="bodysuit", price=250, print="heatwave",
         intro="The Heatwave Bodysuit takes our chocolate-and-cream sun print into a sleeveless, boy-leg shape with a scooped neckline, a one piece that feels as good on the sand as it does in the surf.",
         reviews=(4, 0, 0)),
    dict(slug="shellbound-bodysuit", name="Shellbound Bodysuit", cat="bodysuit", price=200, print="shellbound",
         intro="Sun-warmed coral shell tiles cover the Shellbound Bodysuit, a sleeveless boy-leg one piece with a scooped neckline and a comfortable, supportive fit.",
         reviews=(3, 2, 0)),
    dict(slug="apex-muse-bodysuit", name="Apex Muse Bodysuit", cat="bodysuit", price=200, print="apex-muse",
         intro="Tiny blue sharks swim across a sandy background on the Apex Muse Bodysuit, a sleeveless boy-leg one piece with a playful, surf-ready attitude.",
         reviews=(5, 1, 1)),
    dict(slug="always-sunny-bodysuit", name="Always Sunny Bodysuit", cat="bodysuit", price=250, print="always-sunny",
         intro="The Always Sunny Bodysuit wraps our pink and chocolate starburst tiles around a sleeveless, scoop-neck, boy-leg shape that moves with you from the first wave to the last.",
         reviews=(7, 1, 0)),
    # --- one pieces
    dict(slug="shellbound-one-piece", name="Shellbound One Piece", cat="onepiece", price=125, print="shellbound",
         intro="The Shellbound One Piece pairs coral shell-and-starfish tiles with a scooped neckline, thin straps and a high-cut leg that is easy to wear all day.",
         reviews=(4, 1, 0)),
    dict(slug="lei-me-down-one-piece", name="Lei Me Down One Piece", cat="onepiece", price=125, print="lei-me-down",
         intro="Plumeria-lei stripes in pink, yellow and cream run down the Lei Me Down One Piece, finished with a straight neckline, thin straps and tied sides for an adjustable high-cut leg.",
         reviews=(3, 0, 0)),
    dict(slug="always-sunny-front-zip-one-piece", name="Always Sunny Front Zip One Piece", cat="onepiece", price=250, print="always-sunny",
         intro="A sleeveless front-zip one piece in our pink and chocolate starburst print. Zip it all the way up for a sporty look or lower it a little for extra sun.",
         reviews=(5, 2, 0)),
    dict(slug="apex-muse-front-zip-one-piece", name="Apex Muse Front Zip One Piece", cat="onepiece", price=250, print="apex-muse",
         intro="Short sleeves, a front zip and a boy-leg cut make the Apex Muse Front Zip One Piece a surf-session favorite, covered in tiny blue sharks.",
         reviews=(6, 1, 0)),
    # --- wetsuits
    dict(slug="apex-muse-wetsuit", name="Apex Muse Wetsuit", cat="wetsuit", price=300, print="apex-muse",
         intro="Long sleeves, a high neck and a school of tiny blue sharks on sand: the Apex Muse Wetsuit is built for time in the water without giving up the print.",
         reviews=(3, 1, 0)),
    dict(slug="sea-adorned-wetsuit", name="Sea Adorned Wetsuit", cat="wetsuit", price=300, print=None,
         intro="Scalloped shells in blue and coral cover the Sea Adorned Wetsuit, a long-sleeve surf suit with a scooped neckline and a high-cut leg.",
         reviews=(2, 1, 0)),
    dict(slug="heatwave-wetsuit", name="Heatwave Wetsuit", cat="wetsuit", price=300, print="heatwave",
         intro="Chocolate brown and cream suns on a long-sleeve, high-neck surf suit. The Heatwave Wetsuit keeps our signature print and adds sun protection for long days out past the shore.",
         reviews=(4, 2, 0)),
    dict(slug="lei-me-down-wetsuit", name="Lei Me Down Wetsuit", cat="wetsuit", price=300, print="lei-me-down",
         intro="Plumeria-lei stripes in pink, yellow and lilac run down the Lei Me Down Wetsuit, a long-sleeve, crew-neck surf suit with a flattering high-cut leg.",
         reviews=(3, 1, 0)),
    # --- jewelry
    dict(slug="saltwater-soul-necklace", name="Saltwater Soul Necklace", cat="jewelry", price=85, print=None, metal="",
         intro="A bold cowrie shell hangs from a woven black cord, framed by a row of smaller natural shells. The Saltwater Soul Necklace is a statement piece that sits right at the collarbone.",
         fit="One size. The woven cord ties at the back, so you can set the length that sits best on you.",
         reviews=(4, 1, 0)),
    dict(slug="salt-and-sea-drop-necklace", name="Salt & Sea Drop Necklace", cat="jewelry", price=60, print=None, metal="gold-tone",
         intro="Two small cone shells drop from a fine gold-tone slider chain on the Salt & Sea Drop Necklace. Slide the beads to wear it short and delicate or long and loose.",
         fit="One size. The slider beads adjust the length, so it works from a close collarbone fit to a longer drop.",
         reviews=(3, 0, 0)),
    dict(slug="ocean-bloom-necklace", name="Ocean Bloom Necklace", cat="jewelry", price=75, print=None, metal="gold-tone",
         intro="A mix of spotted, striped and blush-pink shells strung with gold-tone beads, the Ocean Bloom Necklace looks like a morning of beachcombing, all in one piece.",
         fit="One size, worn close to the collarbone. A secure clasp makes it easy to put on and take off.",
         reviews=(5, 1, 0)),
    dict(slug="mermaids-kiss-pendant", name="Mermaid’s Kiss Pendant", cat="jewelry", price=50, print=None, metal="silver-tone",
         intro="A single cowrie shell wrapped in a twisted silver-tone band hangs from a fine chain on the Mermaid’s Kiss Pendant. Simple, polished and ready to layer.",
         fit="One size on a fine chain with a secure clasp, with the pendant sitting just below the collarbone.",
         reviews=(4, 0, 0)),
]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

# When a print has no sibling in another category, the "you may also like" row borrows one of these.
FALLBACK_CROSS = {
    "sea-adorned-wetsuit": "shellbound-one-piece",
    "saltwater-soul-necklace": "shellbound-bikini-set",
    "salt-and-sea-drop-necklace": "lei-me-down-bikini-set",
    "ocean-bloom-necklace": "shellbound-bodysuit",
    "mermaids-kiss-pendant": "always-sunny-front-zip-one-piece",
}
CROSS_PREFERENCE = ["onepiece", "bodysuit", "bikini", "wetsuit"]

# ---------------------------------------------------------------------------
# Category copy
# ---------------------------------------------------------------------------
SWIM_CARE = ("Rinse in cool fresh water after each wear, gently press out excess water and let it dry flat in the shade. "
             "Avoid wringing, rough surfaces and leaving damp pieces bundled in your beach bag. Always follow the care label.")
CATS = {
    "bikini": dict(
        label="bikini sets",
        features="Lined for coverage, with a soft finish that is comfortable against the skin. Mix and match with other Sun Drenched pieces to build your own set.",
        material="A soft, stretchy, quick-drying recycled swim fabric with a smooth finish and full lining.",
        care=SWIM_CARE,
        fit="Sold as a set in sizes XS to XL. Adjustable ties at the neck, back and hips let you fine-tune the fit. If you are between sizes, size up for a more relaxed fit.",
        designed="Sun-soaked beach days, long swims and lazy afternoons by the water.",
    ),
    "bodysuit": dict(
        label="bodysuits",
        features="A sleeveless, boy-leg cut with medium coverage and a stretchy, supportive fit, lined for comfort and made to move.",
        material="A soft, stretchy, quick-drying recycled swim fabric with a smooth finish and full lining.",
        care=SWIM_CARE,
        fit="True to size in XS to XL, with medium coverage and a snug, supportive fit. If you are between sizes, size up for more room through the hips.",
        designed="Beach days that turn into dinners, in a cut that works in the water and on land.",
    ),
    "onepiece": dict(
        label="one pieces",
        features="Lined for coverage and made from a stretchy fabric that holds its shape swim after swim.",
        material="A soft, stretchy, quick-drying recycled swim fabric with a smooth finish and full lining.",
        care=SWIM_CARE,
        fit="True to size in XS to XL, with medium coverage and a stretchy, supportive fit. If you are between sizes, size up for a more relaxed fit.",
        designed="Swimming, surfing and everything in between, comfortable enough to wear all day.",
    ),
    "wetsuit": dict(
        label="wetsuits",
        features="Cut close to the body so it stays put in the water, with long sleeves for extra coverage and a smooth, comfortable finish.",
        material="A stretchy, quick-drying recycled fabric with UPF 50+ sun protection and a smooth finish.",
        care=SWIM_CARE,
        fit="Cut close to the body, like a second skin, so it stays in place in the water. True to size in XS to XL; size up if you like a looser fit.",
        designed="Surf sessions, snorkeling, paddling and long days in the sun when you want extra coverage.",
    ),
    "jewelry": dict(
        label="jewelry",
        features="A small piece of the coast to wear every day, whether you pair it with a swimsuit or a sundress.",
        material="Made with natural shells, so every piece varies a little in color, size and pattern.",
        care="Keep jewelry dry between wears and store it gently. For questions about a specific piece, email info@sundrenched.com.",
        fit="",  # per product
        designed="Layering with your favorite swimwear and carrying a little piece of the coast with you.",
    ),
}
SHIPPING = ("Orders ship from Ewa Beach, Hawaii, within 2 to 3 business days. Unworn items with tags attached can be returned within 30 days; "
            "for hygiene reasons, swimwear must be unworn with the hygiene liner intact. Questions? Email info@sundrenched.com.")
SHIPPING_JEWELRY = ("Orders ship from Ewa Beach, Hawaii, within 2 to 3 business days. Unworn jewelry can be returned within 30 days. "
                    "Questions? Email info@sundrenched.com.")
PLASTIC = ("Sun Drenched is inspired by a life close to the ocean, so we are working to keep plastic out of it. Orders ship in recycled, "
           "plastic-free packaging, and we are building toward plastic-neutral production. Read more about how we care for the ocean on our About page.")

ICONS = {
    "description": '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12Z"/><circle cx="12" cy="12" r="2.6"/>',
    "material": '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14"/><path d="M5 19c3-4 6-7 9-9"/>',
    "fit": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m8 12 2 2m1.5-5.5 2 2m1.5-5.5 1.5 1.5"/>',
    "designed": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10Z"/>',
    "shipping": '<path d="M2 6h11v10H2zM13 10h4l3 3v3h-7"/><circle cx="6.5" cy="17.5" r="1.6"/><circle cx="16.5" cy="17.5" r="1.6"/>',
    "plastic": '<path d="M12 3s6 6.4 6 10.5a6 6 0 0 1-12 0C6 9.4 12 3 12 3Z"/>',
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(text):
    return html.escape(text, quote=True)

def money(value):
    return f"${value:,.2f} USD"

def related_for(product):
    """Same-category pieces first (cycling from the next product), then one piece from another category."""
    same = [p for p in PRODUCTS if p["cat"] == product["cat"]]
    i = same.index(product)
    others = [same[(i + k) % len(same)] for k in range(1, len(same))]
    cross = None
    if product["print"]:
        sibs = [p for p in PRODUCTS if p["print"] == product["print"] and p["cat"] != product["cat"]]
        sibs.sort(key=lambda p: CROSS_PREFERENCE.index(p["cat"]) if p["cat"] in CROSS_PREFERENCE else 99)
        cross = sibs[0] if sibs else None
    if cross is None:
        cross = BY_SLUG[FALLBACK_CROSS[product["slug"]]]
    return (others + [cross])[:4]

def review_stats(product):
    five, four, three = product["reviews"]
    total = five + four + three
    average = (5 * five + 4 * four + 3 * three) / total
    recommend = round((five + four) / total * 100)
    return dict(five=five, four=four, three=three, total=total, average=round(average + 1e-9, 1), recommend=recommend)

def card_html(product, lazy=True, indent="      "):
    """A product card that links to the product page (same markup the shop grids use)."""
    lazy_attr = ' loading="lazy"' if lazy else ""
    i = indent
    return (
        f'{i}<article class="product-card">\n'
        f'{i}  <a class="product-card__link" href="{product["slug"]}.html">\n'
        f'{i}    <img class="product-card__image" src="assets/images/products/{product["slug"]}.webp" width="600" height="900" alt=""{lazy_attr}>\n'
        f'{i}    <div class="product-card__details">\n'
        f'{i}      <h2 class="product-card__name">{esc(product["name"])}</h2>\n'
        f'{i}      <p class="product-card__price">{money(product["price"])}</p>\n'
        f'{i}    </div>\n'
        f'{i}  </a>\n'
        f'{i}</article>\n'
    )

def details_block(key, title, body_html, open_=False):
    return (
        f'          <details class="product-details__item"{" open" if open_ else ""}>\n'
        f'            <summary><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[key]}</svg><span>{title}</span></summary>\n'
        f'            <div class="product-details__body">{body_html}</div>\n'
        f'          </details>\n'
    )

def stars(rating):
    return f'<span class="stars" style="--rating:{rating}" role="img" aria-label="Rated {rating} out of 5 stars">★★★★★</span>'

def build_main(product):
    cat = CATS[product["cat"]]
    stats = review_stats(product)
    monthly = product["price"] / 12
    jewelry = product["cat"] == "jewelry"
    name = esc(product["name"])

    if jewelry:
        material = f'{cat["material"]} Metal details are {product["metal"]}.' if product["metal"] else cat["material"]
        fit = product["fit"]
        fit_title = "Length & Fit"
    else:
        material = cat["material"]
        fit = cat["fit"]
        fit_title = "Fit &amp; Sizing"

    description = f'<p>{esc(product["intro"])}</p><p>{esc(cat["features"])}</p>'
    if not jewelry:
        description += "<p>Shown in size S.</p>"

    details = "".join([
        details_block("description", "Description", description, open_=True),
        details_block("material", "Material &amp; Care", f'<p>{esc(material)}</p><p>{esc(cat["care"])}</p>'),
        details_block("fit", fit_title, f'<p>{esc(fit)}</p>'),
        details_block("designed", "Designed for", f'<p>{esc(cat["designed"])}</p>'),
        details_block("shipping", "Shipping &amp; Return", f'<p>{esc(SHIPPING_JEWELRY if jewelry else SHIPPING)}</p>'),
        details_block("plastic", "Plastic Neutral", '<p>' + esc(PLASTIC).replace("About page", '<a href="about.html">About page</a>') + '</p>'),
    ])

    total = stats["total"]
    rows = ""
    for stars_n, count in ((5, stats["five"]), (4, stats["four"]), (3, stats["three"]), (2, 0), (1, 0)):
        pct = round(count / total * 100)
        rows += (
            f'            <li class="rating-row"><span class="rating-row__label">{stars_n}<span aria-hidden="true"> ★</span><span class="visually-hidden"> star reviews</span></span>'
            f'<span class="rating-row__bar" aria-hidden="true"><span style="width:{pct}%"></span></span>'
            f'<span class="rating-row__count">{count}</span></li>\n'
        )

    related = "".join(card_html(p, lazy=True, indent="        ") for p in related_for(product))
    review_word = "Review" if total == 1 else "Reviews"

    return f'''<main id="main" class="page-shell product-page">
    <div class="product-layout">
      <div class="product-media">
        <img class="product-media__image" src="assets/images/products/{product["slug"]}.webp" width="1200" height="1800" alt="{name}">
      </div>

      <div class="product-info">
        <h1 class="product-title">{name}</h1>
        <p class="product-rating">{stars(stats["average"])} <a href="#reviews">{total} {review_word}</a></p>
        <p class="product-price">{money(product["price"])}</p>
        <p class="product-installments"><span class="product-installments__badge">0% APR</span> or from ${monthly:,.2f}/mo</p>
        <button class="button add-to-cart" type="button">Add To Cart</button>
        <p class="cart-note" role="status" aria-live="polite"></p>
        <div class="product-details">
{details}        </div>
      </div>

      <section class="product-reviews" id="reviews" aria-labelledby="reviews-title">
        <h2 class="visually-hidden" id="reviews-title">Customer reviews</h2>
        <p class="rating-summary"><span class="rating-summary__score">{stats["average"]}</span>{stars(stats["average"])}<span class="rating-summary__count">Based on {total} reviews</span></p>
        <ul class="rating-bars">
{rows}        </ul>
        <p class="recommend"><strong>{stats["recommend"]}%</strong> would recommend this product</p>
      </section>
    </div>

    <section class="related" aria-labelledby="related-title">
      <h2 class="related__title" id="related-title">You may also like</h2>
      <div class="product-grid">
{related}      </div>
    </section>
  </main>'''

def meta_description(product):
    first = product["intro"].split(". ")[0].rstrip(".") + "."
    return first

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def check_prices_against_shop():
    shop = (ROOT / "shop.html").read_text(encoding="utf-8")
    pairs = re.findall(r'product-card__name">([^<]*)</h2>\s*<p class="product-card__price">([^<]*)</p>', shop)
    shop_prices = {html.unescape(n): p for n, p in pairs}
    problems = []
    for p in PRODUCTS:
        want = money(p["price"])
        have = shop_prices.get(p["name"])
        if have != want:
            problems.append(f'{p["name"]}: shop page says {have}, data says {want}')
    if problems:
        sys.exit("Price mismatch, fix the data in this script or the shop page:\n  " + "\n  ".join(problems))

def build_pages():
    shop = (ROOT / "shop.html").read_text(encoding="utf-8")
    start = shop.index('<main id="main"')
    end = shop.index("</main>") + len("</main>")
    head, tail = shop[:start], shop[end:]
    for p in PRODUCTS:
        page_head = head
        page_head = re.sub(r"<title>.*?</title>", f"<title>{esc(p['name'])} — Sun Drenched</title>", page_head, count=1)
        page_head = re.sub(r'<meta name="description" content="[^"]*">',
                           f'<meta name="description" content="{esc(meta_description(p))}">', page_head, count=1)
        page_head = re.sub(r"styles\.css\?v=[^\"']*", f"styles.css?v={CSS_VERSION}", page_head)
        page = page_head + build_main(p) + tail
        (ROOT / f'{p["slug"]}.html').write_text(page, encoding="utf-8")
    print(f"Wrote {len(PRODUCTS)} product pages")

CARD_IMG = re.compile(r'(<img class="product-card__image" src="assets/images/products/(?P<slug>[a-z0-9-]+)\.webp"[^>]*>)')

def link_cards(filename):
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(?P<open>      <article class="product-card"(?: id="[^"]*")?>\n)'
        r'(?P<body>        <img class="product-card__image".*?\n        <div class="product-card__details">.*?\n        </div>\n)'
        r'(?P<close>      </article>\n)', re.S)
    changed = 0
    def wrap(m):
        nonlocal changed
        if "product-card__link" in m.group("body"):
            return m.group(0)
        img = CARD_IMG.search(m.group("body"))
        slug = img.group("slug")
        body = re.sub(r'alt="[^"]*"', 'alt=""', m.group("body"), count=1)
        body = "".join("  " + line + "\n" for line in body.rstrip("\n").split("\n"))
        changed += 1
        return f'{m.group("open")}        <a class="product-card__link" href="{slug}.html">\n{body}        </a>\n{m.group("close")}'
    path.write_text(pattern.sub(wrap, text), encoding="utf-8")
    print(f"{filename}: linked {changed} cards")

def set_css_version():
    for page in ROOT.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        new = re.sub(r"styles\.css\?v=[^\"']*", f"styles.css?v={CSS_VERSION}", text)
        if new != text:
            page.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    check_prices_against_shop()
    for shop_page in ("shop.html", "jewelry.html", "wetsuits.html"):
        link_cards(shop_page)
    build_pages()      # after linking, so the pages copy the final shop header and footer
    set_css_version()
