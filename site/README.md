# Fashion Lab Sedona — website

Static site, no build step. Open `index.html` in a browser or host the `site/` folder anywhere (Vercel, Netlify, GitHub Pages, any web host).

## Pages

- `index.html` — Fashion Lab Sedona showcase (2026 recap, photos, Create-a-Thon, about, pop-ups, team, sponsors, join).
- `your-town.html` — "Do the Fashion Lab in your own town or city!": money model, 8 roles, timeline, budget template, print pack, contract pack, lessons, consulting.

## Folders

- `assets/css/style.css` — all styles. Colors and fonts are CSS variables at the top.
- `assets/js/main.js` — mobile menu, photo lightbox, contract viewer, budget calculator, newsletter placeholder.
- `assets/img/show/` — 2026 Fashion Show photos (KFM Designs, proofing watermark).
- `assets/img/lab/` — 2026 Create-a-Thon photos (KFM Designs, proofing watermark).
- `assets/img/folder/` — Create-a-Thon phone photos from the shared folder.
- `assets/img/team/`, `assets/img/site/` — headshots and graphics from the old Squarespace site.
- `assets/docs/fashion-lab-budget-template.xlsx` — downloadable budget with formulas, roles and timeline tabs.

## Editing

- Contracts live at the bottom of `your-town.html` inside `<template id="doc-...">` blocks. Edit the text there; the cards open them.
- Budget numbers are in the table in `your-town.html`; the `data-sedona` attribute on each input is what the "Fill with Sedona 2026" button uses.
- Newsletter form is a placeholder (opens an email). Point it at Brevo or another list when ready.

## Local preview

```bash
python -m http.server 8765 --directory site
```

Then open http://localhost:8765
