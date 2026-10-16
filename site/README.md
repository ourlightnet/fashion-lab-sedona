# Fashion Lab Sedona — website

Static site, no build step. Open `index.html` in a browser or host the `site/` folder anywhere (Vercel, Netlify, GitHub Pages, any web host).

## Pages

- `index.html` — Fashion Lab Sedona showcase (2026 recap, photos, Create-a-Thon, about, pop-ups, team, sponsors, join).
- `your-town.html` — "Do the Fashion Lab in your own town or city!" teaser: what's in the playbook, plus a sign-up form. The full playbook is held in `../drafts/`.
- `popups.html` — past pop-ups and workshops.
- `2025.html`, `2024.html` — prior years' photos (Prior Years menu).
- `videos.html` — the YouTube videos.
- `designers.html` — the 2026 Create-a-Thon designers (photos in `assets/img/designers/`). `designers-2026/` forwards the old Squarespace address there.
- `sedonans.html` — the 2026 Sensational Sedonans from the E-Program (photos in `assets/img/sedonans/`, cropped from the E-Program PDF).
- `updates/` — sign-up page for Fashion Lab updates (fashionlabsedona.com/updates). `newsletter/` redirects there.

## Folders

- `assets/css/style.css` — all styles. Colors and fonts are CSS variables at the top.
- `assets/js/main.js` — mobile menu, photo lightbox, sign-up forms (Brevo).
- `assets/img/show/` — 2026 Fashion Show photos (KFM Designs, proofing watermark).
- `assets/img/lab/` — 2026 Create-a-Thon photos (KFM Designs, proofing watermark).
- `assets/img/folder/` — Create-a-Thon phone photos from the shared folder.
- `assets/img/team/`, `assets/img/site/` — headshots and graphics from the old Squarespace site.

## Editing

- Sign-up forms are `<form class="signup">` in `index.html` and `updates/index.html` (monthly updates, same Brevo form) and `your-town.html` (playbook list). Put each Brevo form's URL in the form's `action` attribute. The Brevo form URLs are already set. Fields must match each Brevo form exactly: the updates form sends `EMAIL`; the playbook form sends `FIRSTNAME`, `EMAIL`, `CITY`, `ORGANIZATION` and an optional phone (`SMS` digits plus `SMS__COUNTRY_CODE`). If you add a field in Brevo, add the same `name` here. While `action` is empty, the form opens an email to fashionlabsedona@gmail.com instead.
- Sponsors section on the home page is generated from `data/sponsors-2026.csv` (exported from the "Donors Fashion Lab Sedona 2026" Google Sheet). Put logo files in `site/assets/img/sponsors/` named by sponsor (e.g. `fabric-incubator.png`), then run `python3 tools/build_sponsors.py`; it lists the file names it expects. Sponsors without a logo show a name tile.
- Prior-year photos live in `assets/img/past/<year>/<lab|show|popups>/`.

## Local preview

```bash
python -m http.server 8765 --directory site
```

Then open http://localhost:8765
