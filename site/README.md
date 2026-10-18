# Fashion Lab Sedona — website

Static site, no build step. Open `index.html` in a browser or host the `site/` folder anywhere (Vercel, Netlify, GitHub Pages, any web host).

## Pages

- `index.html` — Fashion Lab Sedona showcase (2026 recap, photos, Create-a-Thon, about, pop-ups, team, sponsors, join).
- `your-town.html` — "Do the Fashion Lab in your own town or city!" teaser: what's in the playbook, plus a sign-up form. The full playbook is held in `../drafts/`.
- `designer-waitlist.html`, `model-waitlist.html` — 2027 waitlist sign-up pages (first name, last name, email, phone), with photos below. The home page, Get Involved, designers page and footers link here.
- `get-involved.html` — five ways to help (donate materials, volunteer, design for 2027, give, run a Fashion Lab in your town), the 2027 designer and model waitlists (`#designer-waitlist`, `#model-waitlist`), nominations and the updates form. The menu's "Get Involved" item points here.
- `popups.html` — past pop-ups and workshops.
- `2025.html`, `2024.html` — prior years' photos (Prior Years menu).
- `videos.html` — the YouTube videos.
- `photos-2026.html` — 2026 photos hub (big group shot, one card per event). Event pages: `createathon-2026.html` (Day 1 and Day 2), `show-2026.html` (Karl Mullings), `show-2026-leah.html` (Leah Joy Love, links to her Pixieset gallery until her photos are added), `afterparty-2026.html`, and `galleries-2026.html` (links to both photographers' full galleries). Every 2026 page ends with links to the 2025 and 2024 photos. Photos are culled to one shot per person and live in `assets/img/2026/<event>/`.
- `designers.html` — the 2026 Create-a-Thon designers (photos in `assets/img/designers/`). `designers-2026/` forwards the old Squarespace address there.
- `updates/` — sign-up page for Fashion Lab updates (fashionlabsedona.com/updates). `newsletter/` redirects there.
- `playbook-map.html` — team map of where playbook requests come from (not in the menu, not indexed). Rebuild it from a Brevo export with `python3 tools/build_request_map.py`; see the top of that script.
- `press.html` — press page: news coverage, fast facts, boilerplate, logos and photos, press contact. Add new clippings to the `press-list` at the top; PDF copies of articles go in `assets/press/`.

## Folders

- `assets/css/style.css` — all styles. Colors and fonts are CSS variables at the top.
- `assets/js/main.js` — mobile menu, photo lightbox, sign-up forms (Brevo).
- `assets/img/show/` — 2026 Fashion Show photos (KFM Designs, proofing watermark).
- `assets/img/lab/` — 2026 Create-a-Thon photos (KFM Designs, proofing watermark).
- `assets/img/folder/` — Create-a-Thon phone photos from the shared folder.
- `assets/img/team/`, `assets/img/site/` — headshots and graphics from the old Squarespace site.

## Editing

- Sign-up forms are `<form class="signup">` in `index.html` and `updates/index.html` (the Fashion Lab Sedona Mailing List, same Brevo form), `designer-waitlist.html` and `model-waitlist.html` (2027 waitlists, sending `FIRSTNAME`, `LASTNAME`, `EMAIL`, `SMS` and `SMS__COUNTRY_CODE`), and `your-town.html` (playbook list). Put each Brevo form's URL in the form's `action` attribute. The Brevo form URLs are already set. Fields must match each Brevo form exactly: the updates form sends `EMAIL`; the playbook form sends `FIRSTNAME`, `LASTNAME`, `EMAIL`, `CITY`, `ORGANIZATION` and an optional phone (`SMS` digits plus `SMS__COUNTRY_CODE`). After a playbook request, `your-town.html` shows the thank-you and asks "email or phone?" (plus a phone number if none was given), posting again to the same Brevo form with `NOTIFY_BY` (`Email` or `Phone`). If you add a field in Brevo, add the same `name` here. While `action` is empty, the form opens an email to fashionlabsedona@gmail.com instead.
- Sponsors section on the home page is generated from `data/sponsors-2026.csv` (exported from the "Donors Fashion Lab Sedona 2026" Google Sheet). Put logo files in `site/assets/img/sponsors/` named by sponsor (e.g. `fabric-incubator.png`), then run `python3 tools/build_sponsors.py` (it also refreshes the headline sponsor logo strip under the stats at the top of the page); it lists the file names it expects. Sponsors without a logo show a name tile.
- Prior-year photos live in `assets/img/past/<year>/<lab|show|popups>/`.

## Local preview

```bash
python -m http.server 8765 --directory site
```

Then open http://localhost:8765
