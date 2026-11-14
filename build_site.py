"""Build the Lalo free-printables site (static HTML for GitHub Pages).

Run:  uv run --with pillow build_site.py
Source PDFs + pin images come from OpenMontage/projects/lalo-pinterest (run its build.py first).
Kid-safe by design: no analytics, no cookies, no forms. YouTube embeds use youtube-nocookie.com.
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
SRC = Path.home() / "Workspace/OpenMontage/projects/lalo-pinterest"
BASE = "https://laloplayamusical.github.io"
YT = "https://www.youtube.com/@laloplayamusical"
BRAND = "Lalo y la Playa Musical"
# Paste the content value of Pinterest's <meta name="p:domain_verify"> tag here, then rebuild.
PINTEREST_VERIFY = ""

# slug, EN title, ES title, about text, YouTube Short id (or ""), short title
PAGES = [
    ("beach-ball", "Beach Ball Fun", "¡A jugar con la pelota!",
     "Lalo the baby manatee plays catch with a friend on the beach. A sweet way to talk about sharing and taking turns.",
     "PmBy1onZiYs", "¡Me toca a mí! (Taking turns song)"),
    ("sunscreen", "Sunscreen Time", "¡Protector solar!",
     "Sun-safety coloring page: Lalo gets ready for a beach day with sunscreen. Great before summer trips and pool days.",
     "", ""),
    ("sandcastle-crabs", "Sandcastle Crabs", "Cangrejitos en el castillo",
     "Three little crabs hide in the sandcastle. Pair it with Lalo's peekaboo song for toddlers.",
     "BSfpUXT2zAY", "¿Dónde están los cangrejitos? (Peekaboo song)"),
    ("brush-teeth", "Brush Your Teeth", "¡A cepillarse los dientes!",
     "Tooth-brushing coloring page for toddlers. Use it to build a happy morning and bedtime routine.",
     "", ""),
    ("recycle", "Recycle with Pita", "¡A reciclar con Pita!",
     "Pita and Lalo keep the beach clean. A simple first lesson about recycling and caring for nature.",
     "CUKiE0V7shw", "¡A limpiar la playa! (Clean the beach song)"),
    ("boo-boo", "Boo-Boo Care", "Ay, mi aletita",
     "Lalo hurts his flipper and Abuela Tortuga helps. A gentle page about boo-boos, comfort and feeling better.",
     "1WzIF5veljk", "Ay, ay, mi aletita (Boo-boo song)"),
    ("wash-hands", "Wash Your Hands", "¡A lavarse las manos!",
     "Hand-washing coloring page with soap and bubbles. Perfect for preschool hygiene lessons.",
     "rRnYZTIVOD8", "¡Lavamos las manitas! (Hand-washing song)"),
    ("thank-you", "Say Thank You", "¡Gracias, Abuela!",
     "Lalo says thank you to Abuela Tortuga. Practice the magic words: por favor y gracias.",
     "", ""),
    ("feelings", "Feelings Faces", "¿Cómo te sientes?",
     "Happy, sad, mad or scared? Color the feelings faces and name each emotion in Spanish and English.",
     "", ""),
    ("bedtime", "Bedtime Lullaby", "Canción de cuna",
     "A calm bedtime coloring page with Lalo under the moon. A quiet activity before sleep.",
     "", ""),
]

KEYWORDS = ("free coloring pages, bilingual printables, Spanish for toddlers, preschool Spanish, "
            "páginas para colorear, canciones infantiles, Lalo y la Playa Musical")


def esc(s):
    return html.escape(s, quote=True)


def head(title, desc, url, image, extra=""):
    verify = f'<meta name="p:domain_verify" content="{esc(PINTEREST_VERIFY)}">' if PINTEREST_VERIFY else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(KEYWORDS)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
{verify}
<link rel="icon" href="/img/favicon.png">
<link rel="alternate" type="application/rss+xml" title="{BRAND} printables" href="/feed.xml">
<link rel="stylesheet" href="/style.css">
{extra}
</head>
<body>
<header class="top"><a class="logo" href="/"><img src="/img/lalo-avatar.png" alt="Lalo the baby manatee" width="44" height="44">{BRAND}</a>
<a class="yt" href="{YT}" rel="noopener">▶ YouTube</a></header>
"""


FOOT = f"""<footer>
<p><b>{BRAND}</b> · Spanish songs for kids with English echoes · <a href="{YT}" rel="noopener">YouTube @laloplayamusical</a></p>
<p class="small">Free for home and classroom use. Please share the link instead of re-uploading the files.
This site has no ads, no tracking and no sign-ups.</p>
</footer>
</body>
</html>
"""


def video_block(vid, vtitle):
    if not vid:
        return f"""<section class="video none"><h2>Sing along with Lalo</h2>
<p>New bilingual songs every week on YouTube.</p>
<a class="btn red" href="{YT}" rel="noopener">▶ Watch on YouTube</a></section>"""
    return f"""<section class="video"><h2>Watch the song: {esc(vtitle)}</h2>
<div class="short"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{esc(vtitle)}" loading="lazy"
allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<a class="btn red" href="https://youtube.com/shorts/{vid}" rel="noopener">▶ Open on YouTube</a></section>"""


def card(i, slug, en, es):
    return f"""<a class="card" href="/coloring/{slug}/"><img src="/img/thumb-{i:02d}-{slug}.jpg" alt="{esc(en)} coloring page - {esc(es)}" loading="lazy" width="400" height="600">
<span class="en">{esc(en)}</span><span class="es">{esc(es)}</span></a>"""


def build():
    for d in ("pdf", "img", "coloring"):
        shutil.rmtree(ROOT / d, ignore_errors=True)
        (ROOT / d).mkdir()

    # assets
    for f in (SRC / "pdf").glob("*.pdf"):
        shutil.copy(f, ROOT / "pdf" / f.name)
    pfp = Image.open(SRC / "profile_photo_lalo.png").convert("RGB")
    pfp.resize((88, 88), Image.LANCZOS).save(ROOT / "img/lalo-avatar.png", optimize=True)
    pfp.resize((64, 64), Image.LANCZOS).save(ROOT / "img/favicon.png", optimize=True)

    feed_items, urls = [], [f"{BASE}/"]
    for i, (slug, en, es, about, vid, vtitle) in enumerate(PAGES, 1):
        pin = Image.open(SRC / "pins" / f"pin-{i:02d}-{slug}.png").convert("RGB")
        pin.save(ROOT / "img" / f"pin-{i:02d}-{slug}.jpg", quality=88, optimize=True)
        pin.resize((400, 600), Image.LANCZOS).save(ROOT / "img" / f"thumb-{i:02d}-{slug}.jpg", quality=85, optimize=True)

        url = f"{BASE}/coloring/{slug}/"
        img = f"{BASE}/img/pin-{i:02d}-{slug}.jpg"
        pdf = f"/pdf/lalo-coloring-{i:02d}-{slug}.pdf"
        title = f"{en} Free Coloring Page (Spanish + English) | {BRAND}"
        desc = f"Free printable {en.lower()} coloring page for toddlers and preschoolers, ages 2-5. {es}. {about}"
        ld = {
            "@context": "https://schema.org", "@type": "LearningResource",
            "name": f"{en} coloring page - {es}", "description": about, "url": url, "image": img,
            "isAccessibleForFree": True, "inLanguage": ["es", "en"], "learningResourceType": "Coloring page",
            "typicalAgeRange": "2-5", "educationalLevel": "Preschool",
            "publisher": {"@type": "Organization", "name": BRAND, "sameAs": [YT]},
        }
        others = [p for p in PAGES if p[0] != slug]
        rel = [others[(i + k) % len(others)] for k in range(3)]
        rel_html = "".join(card(PAGES.index(p) + 1, p[0], p[1], p[2]) for p in rel)

        page = head(title, desc, url, img, f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
        page += f"""<main class="detail">
<nav class="crumbs"><a href="/">Free coloring pages</a> › {esc(en)}</nav>
<h1>{esc(en)} <span>{esc(es)}</span></h1>
<div class="grid2">
<img class="preview" src="/img/pin-{i:02d}-{slug}.jpg" alt="{esc(en)} coloring page with Lalo the baby manatee - {esc(es)}" width="1000" height="1500">
<div>
<p class="lead">{esc(about)}</p>
<a class="btn" href="{pdf}" download>⬇ Download free PDF</a>
<p class="small">US Letter size, prints in black and white. Ages 2-5.</p>
<h2>Tips for parents and teachers</h2>
<ul>
<li>Say the title in Spanish together: <i>{esc(es)}</i></li>
<li>Name the colors in both languages: <i>azul / blue, rojo / red, amarillo / yellow</i>.</li>
<li>Play the song while coloring, then ask your child to sing the chorus.</li>
</ul>
<a class="btn ghost" href="/pdf/lalo-coloring-pack-all-10.pdf" download>⬇ Get all 10 pages (one PDF)</a>
</div>
</div>
{video_block(vid, vtitle)}
<h2>More free coloring pages</h2>
<div class="cards">{rel_html}</div>
</main>
"""
        page += FOOT
        (ROOT / "coloring" / slug).mkdir(parents=True)
        (ROOT / "coloring" / slug / "index.html").write_text(page)
        urls.append(url)
        feed_items.append((en, es, url, img, desc))

    # home
    cards = "".join(card(i, s, en, es) for i, (s, en, es, *_r) in enumerate(PAGES, 1))
    home_desc = ("Free bilingual coloring pages for toddlers and preschoolers. Print Spanish + English pages "
                 "with Lalo the baby manatee and sing along with his songs on YouTube.")
    home = head(f"Free Bilingual Coloring Pages for Kids (Spanish + English) | {BRAND}", home_desc, f"{BASE}/",
                f"{BASE}/img/pin-01-beach-ball.jpg")
    home += f"""<main>
<section class="hero">
<h1>Free bilingual coloring pages <span>Páginas para colorear gratis</span></h1>
<p>Print-and-color pages with Lalo the baby manatee and his beach friends. Each page goes with a short
Spanish song (with English echoes) for kids ages 2-5. Free for home, daycare and Spanish class.</p>
<a class="btn" href="/pdf/lalo-coloring-pack-all-10.pdf" download>⬇ Download all 10 (one PDF)</a>
<a class="btn red" href="{YT}" rel="noopener">▶ Watch Lalo on YouTube</a>
</section>
<div class="cards">{cards}</div>
</main>
"""
    home += FOOT
    (ROOT / "index.html").write_text(home)

    # 404
    (ROOT / "404.html").write_text(head(f"Page not found | {BRAND}", home_desc, f"{BASE}/", f"{BASE}/img/pin-01-beach-ball.jpg")
                                   + '<main class="hero"><h1>Oops! Page not found</h1><a class="btn" href="/">See all coloring pages</a></main>' + FOOT)

    # sitemap, robots, RSS
    today = date.today().isoformat()
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    items = "".join(f"""<item><title>{esc(en)} Free Coloring Page - {esc(es)}</title><link>{u}</link><guid>{u}</guid>
<description>{esc(d)}</description><enclosure url="{im}" type="image/jpeg" length="0"/></item>
""" for en, es, u, im, d in feed_items)
    (ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>{BRAND} - Free Printables</title><link>{BASE}/</link>
<description>{esc(home_desc)}</description>
{items}</channel></rss>
""")
    (ROOT / ".nojekyll").write_text("")
    print(f"built {len(PAGES)} pages + home -> {ROOT}")


if __name__ == "__main__":
    build()
