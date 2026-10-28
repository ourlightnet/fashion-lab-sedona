# Fashion Lab Sedona — website

Static site, no build step. Open `index.html` in a browser or host the `site/` folder anywhere (Vercel, Netlify, GitHub Pages, any web host).

## Pages

- `index.html` — Fashion Lab Sedona showcase (2026 recap, photos, Create-a-Thon, about, pop-ups, team, sponsors, join).
- `your-town.html` — "Do the Fashion Lab in your own town or city!" teaser: what's in the playbook, plus a sign-up form. The full playbook is `playbook.html`.
- `get-started.html` (short links `/get-started`, `/getting-started`, `/welcome`) — hidden landing page people reach after the playbook sign-up: the free playbook, or Rocket Fuel: five one-hour sessions with the team at $125 an hour ($625) (paid through a Stripe payment link), or Full Support for Maiden Voyage: on-site support from $1,000 by estimate (Calendly call). Not in menus or sitemap, `noindex`.
- `playbook.html` (short link `/playbook`, via `playbook/`) — the full playbook (money model, roles, timeline, budget, print pack, contracts, consulting). Hidden: shared only by direct link with people who sign up; not in menus, footer or sitemap, and `noindex`. Budget spreadsheet in `assets/docs/`.
- `designer-waitlist.html`, `model-waitlist.html` — 2027 waitlist sign-up pages (first name, last name, email, phone), with photos below. The home page, Get Involved, designers page and footers link here.
- `get-involved.html` — five ways to help (donate materials, volunteer, design for 2027, give, run a Fashion Lab in your town), the 2027 designer and model waitlists (`#designer-waitlist`, `#model-waitlist`), nominations and the updates form. The menu's "Get Involved" item points here.
- `popups.html` — past pop-ups and workshops.
- `2025.html`, `2024.html` — prior years' photos (Prior Years menu).
- `videos.html` — the YouTube videos.
- `photos-2026.html` — 2026 photos hub (big group shot, one card per event). Event pages: `createathon-2026.html` (Day 1 and Day 2), `show-2026.html` (Karl Mullings), `photographers-2026.html` (About menu: the 2026 photographers, videographers and social media team, portraits in `assets/img/collab/`), `show-2026-leah.html` (Leah Joy Love, links to her Pixieset gallery until her photos are added), `afterparty-2026.html`, and `galleries-2026.html` (links to both photographers' full galleries). Every 2026 page ends with links to the 2025 and 2024 photos. Photos are culled to one shot per person and live in `assets/img/2026/<event>/`.
- `designers.html` — the 2026 Create-a-Thon designers (photos in `assets/img/designers/`). `designers-2026/` forwards the old Squarespace address there.
- `sedonans.html` — the 2026 Sensational Sedonans from the E-Program (photos in `assets/img/sedonans/`, cropped from the E-Program PDF).
- `updates/` — sign-up page for Fashion Lab updates (fashionlabsedona.com/updates). `newsletter/` redirects there.
- `playbook-map.html` — team map of where playbook requests come from (not in the menu, not indexed). Rebuild it from a Brevo export with `python3 tools/build_request_map.py`; see the top of that script.
- `about.html` — About us: the story year by year (2024, 2025, 2026, heading into 2027) with each year's core team. 2025 headshots in `assets/img/team/2025/`, cropped from the 2025 E-Program. Every "About us" menu link points here.
- `shop.html` — Shop Our Sponsors: 2026 Headline Sponsors The Closet Concierge (Betsy Klein's shop, address and directions; they ran the VIP room and dressed the Sensational Sedonans) and FABRIC Incubator (photo in `assets/img/collab/fabric-incubator.jpg`), then the raffle donors with shops (Cielo Connection, Village Yoga, Sedona Active Wear, Shine, Mermaid Heaven), each with logo, description and a 2026 donor sticker, and Sensational Sedonan shops (Belle &amp; Star) with a Sensational Sedonan sticker. In the main menu and footer.
- `press.html` — press page: news coverage, fast facts, boilerplate, logos and photos, press contact. Add new clippings to the `press-list` at the top; PDF copies of articles go in `assets/press/`.

## Folders

- `assets/css/style.css` — all styles. Colors and fonts are CSS variables at the top.
- `assets/js/main.js` — mobile menu, photo lightbox, sign-up forms (Brevo).
- `assets/img/show/` — 2026 Fashion Show photos (KFM Designs, proofing watermark).
- `assets/img/lab/` — 2026 Create-a-Thon photos (KFM Designs, proofing watermark).
- `assets/img/folder/` — Create-a-Thon phone photos from the shared folder.
- `assets/img/team/`, `assets/img/site/` — headshots and graphics from the old Squarespace site.

## Editing

- Sign-up forms are `<form class="signup">` in `index.html` and `updates/index.html` (the Fashion Lab Sedona Mailing List, same Brevo form), `designer-waitlist.html` and `model-waitlist.html` (2027 waitlists, sending `FIRSTNAME`, `LASTNAME`, `EMAIL`, `SMS` and `SMS__COUNTRY_CODE`), and `your-town.html` (playbook list). Put each Brevo form's URL in the form's `action` attribute. The Brevo form URLs are already set. Fields must match each Brevo form exactly: the updates form sends `EMAIL`; the playbook form sends `FIRSTNAME`, `LASTNAME`, `EMAIL`, `CITY`, `ORGANIZATION` and a phone (`SMS` digits plus `SMS__COUNTRY_CODE`). The playbook form also sends `CONTACT_METHOD_PREFERENCE` (a Text attribute in Brevo): the ticked boxes joined with commas, any of `SMS Phone Text`, `WhatsApp`, `Email`, at least one required. The phone (`SMS`, `SMS__COUNTRY_CODE`) and a consent box (`SMS_CONSENT` = `Yes`) only show, and are only required and sent, when SMS Phone Text or WhatsApp is ticked; and after it is sent people go straight to `get-started.html`. If you add a field in Brevo, add the same `name` here. While `action` is empty, the form opens an email to info@fashionlabsedona.com instead.
- Sponsors section on the home page is generated from `data/sponsors-2026.csv` (exported from the "Donors Fashion Lab Sedona 2026" Google Sheet). Put logo files in `site/assets/img/sponsors/` named by sponsor (e.g. `fabric-incubator.png`), then run `python3 tools/build_sponsors.py` (it also refreshes the headline sponsor logo strip under the stats at the top of the page); it lists the file names it expects. Sponsors without a logo show a name tile.
- Link previews and SEO: every page has a block between `<!-- SEO:START -->` and `<!-- SEO:END -->` in `<head>` (canonical link, Open Graph and Twitter tags, the Google Analytics loader), and a 1200x630 preview picture in `assets/img/og/` (what shows when someone texts or posts the link). Both are made by `python3 tools/build_seo.py` from the page's `<title>` and meta description; the photo and headline for each page are in the `PAGES` list at the top of the script. Add a new page there and re-run; it also rewrites `sitemap.xml`. `robots.txt` points search engines to the sitemap.
- Google Analytics: paste the GA4 Measurement ID (`G-...`) into `assets/js/analytics.js`. While it is empty nothing is tracked.
- Prior-year photos live in `assets/img/past/<year>/<lab|show|popups>/`.

## Local preview

```bash
python -m http.server 8765 --directory site
```

Then open http://localhost:8765
