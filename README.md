# laloplayamusical.github.io

Free bilingual (Spanish + English) coloring printables for **Lalo y la Playa Musical**, the YouTube kids channel [@laloplayamusical](https://www.youtube.com/@laloplayamusical).

Live: https://laloplayamusical.github.io

## What's here
- `index.html` – home grid of all coloring pages + "download all 10" pack
- `coloring/<slug>/` – one page per printable: preview, PDF download, matching YouTube Short (youtube-nocookie embed), tips for parents/teachers, related pages, schema.org LearningResource
- `pdf/`, `img/` – PDFs, pin images (also used as Pinterest pin media), thumbnails, avatar
- `sitemap.xml`, `robots.txt`, `feed.xml` (RSS; not connected to Pinterest — pins go out via Zernio to avoid duplicates)
- No analytics, cookies, forms or ads (kid-safe; audience is parents)

## Build
Sources live in `~/Workspace/OpenMontage/projects/lalo-pinterest` (PDFs + pins from its `build.py`).

```sh
uv run --with pillow build_site.py   # regenerates everything except style.css/Fredoka.ttf
git add -A && git commit -m "..." && git push   # GitHub Pages deploys main/ in ~1 min
```

## Adding a printable
1. Add the art + entry to `lalo-pinterest/build.py`, run it.
2. Add a row to `PAGES` in `build_site.py` (slug, EN, ES, about text, Short id or "", Short title).
3. Rebuild, push, then schedule its pin in Zernio (see `lalo-pinterest/README.md`).

## Pinterest site verification
Paste the `p:domain_verify` content value into `PINTEREST_VERIFY` in `build_site.py`, rebuild, push.
