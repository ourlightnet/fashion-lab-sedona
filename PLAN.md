# Fashion Lab Sedona — new website plan

Date: 2026-10-12 · Prepared for Adham and Zenka (CEO) · Status: waiting for approval before building

## 1. What I understood

**The goal.** Rebuild fashionlabsedona.com as a new site with two jobs:

1. **Showcase Fashion Lab Sedona** — the 2026 show just happened (Oct 10 at Brady Hall), so the home page becomes the proud recap: this year's photos, the 48-hour Create-a-Thon, the team, the sponsors, the pop-ups, and how to join next year.
2. **Turn Fashion Lab into a template other towns can run** — a second page, reached from a big button on the home page that says **"Do the Fashion Lab in your own town or city!"** It hands another city everything: the money model, the roles, the timeline, the budget, the poster templates, the sample contracts, and an offer of paid consulting (on site or remote).

**Keep the identity of the current site.** Same logo (the orange red-rock "SEDONA" lockup you put in the folder), same fonts (Archivo Black for headlines, Space Grotesk for body), same black / off-white palette with the Sedona orange from the logo as the accent, same photos, same photo credit line, same links that already work (Eventbrite, Typeform model sign-up, Heyzine e-program, Instagram, Facebook).

**The footer** says it is a Dream Machine project: "A Dream Machine project — bringing communities together in joy."

**Photo credit** stays exactly as on the current site: "48 Hour Create-a-Thon Pictures by Karl Mullings KMF Designs Photography" (linked to kfmdesigns.com). Note: the ShootProof galleries spell it "KFM Designs". I will keep the site's wording unless you tell me otherwise.

## 2. The Fashion Lab model (from Zenka's notes, for the template page)

| Piece | How Sedona does it |
|---|---|
| Sensational Sedonans (local celebrity models) | 12 people, each pays $200 for a program ad, walks the runway in 2–3 outfit changes |
| Boutiques / thrift / consignment / fair-trade shops | 3 shops pay $1,500 each to dress the celebrity models |
| Designers | Pay $100 to join the 48-hour Create-a-Thon, show 1–2 looks |
| Core team | 8 organizers, each with a role (see roles list below) |
| Vendor tables | $200 each |
| Donors + sponsors | Underwriters, retail sponsors, in-kind donors |
| The big raffle | Runs the night of the show while the judges decide |
| Prizes | FABRIC Incubator (Tempe) scholarship: $4,000 in courses + mentorship, plus $1,000 cash from Fashion Lab Sedona |
| Tickets | Early bird $30, VIP $100 (from the ticket sales sheet) |

## 3. Source material I found

- **Current site (Squarespace):** home, About, Core Team (9 bios + headshots), Create-a-Thon, Designer Registration, Sponsorship Opportunities, Vendor Table, Program Advertising, Sponsors, 2025 archive. I can pull every image from it.
- **Your folder:** 2 official logos (black box and horizontal strip) + 22 Create-a-Thon / studio photos.
- **ShootProof galleries (KFM Designs):** "FLS Fashion Show" (379 photos, open) and "Fashion Lab Sedona" (email gate; I'll use team@lightnet.org as you said).
- **Google Sheet "Fashion Lab 2026":** Budget tab (2025 actuals, 2026 possible / actual), Roles tab, Calendar tab, Print Assets, To Do, "To Do Differently" lessons, Important Links (Canva sponsor logos, Heyzine, Typeform).
- **SignNow templates (team@lightnet.org):** Vendor Agreement 2026, Sensational Sedonan Agreement 2026, Program Advertising Agreement 2026, Program Advertiser Spec Sheet 2026, Retail Sponsorship Agreement 2026, Underwriter Agreement 2026, Designer Agreement 2025, Sponsor Opportunities cover sheet, Liability & Media Release.

**Privacy rule I will follow:** the sheet also holds ticket buyers' names and emails and sponsor contact details. None of that goes on the site. Only the budget structure and amounts.

## 4. Site map

### Page 1 — Home (Fashion Lab Sedona showcase)
1. Header: logo strip, nav (Home · The Show · Create-a-Thon · Team · Sponsors · Your Town), Instagram/Facebook.
2. Hero: full-bleed runway photo, "Sustainable fashion. Made in 48 hours. Worn by Sedona." + button **Do the Fashion Lab in your own town or city!** + "See the 2026 photos".
3. 2026 recap strip: date, venue, numbers (designers, models, boutiques, raised for the scholarship).
4. Fashion Show photos: curated grid of ~24 from the ShootProof show gallery, lightbox, link to the full gallery.
5. 48 Hour Create-a-Thon pictures: curated grid from your folder + the ShootProof Create-a-Thon gallery, with the credit line.
6. What is Fashion Lab (About copy: textile waste, upcycling, local small-batch).
7. How it works: Create-a-Thon → Runway → Pop-ups, with the prizes.
8. Pop-ups & workshops 2026 (the cards from the current site).
9. Core Team (9 headshots + short bios).
10. Sponsors & donors 2026 (the donor graphic + logos) and a "Sponsor 2027" CTA.
11. Join the community: newsletter sign-up + model sign-up + designer registration links.
12. Footer: Dream Machine line, contact (fashionlabsedona@gmail.com, text line), 2025 archive links.

### Page 2 — Do the Fashion Lab in your own town or city!
1. Hero: "Everything you need to run a Fashion Lab where you live."
2. The model in one picture: who pays what, where the money goes (the table above as a visual).
3. The 8 roles (from the Roles tab): Producer, Pop-ups lead, Website lead, Posters & flyers, Social media, Press, Sponsorship, Models/runway coach … with what each does.
4. The timeline: 6 months out → show week (from the Calendar tab + 2026 real dates).
5. **The budget template:** income and expense lines with Sedona's 2025 actuals as a reference column and an empty "Your town" column; download as a spreadsheet, plus "make a copy" of the Google Sheet template.
6. **Posters & print pack:** Canva templates (poster, flyer, program, tickets, signage) with the Print Assets checklist.
7. **The contracts pack:** one card per agreement (Vendor, Sensational Sedonan, Program Advertising + Spec Sheet, Retail Sponsorship, Underwriter, Designer, Sponsor Opportunities cover sheet, Liability & Media Release), each with a plain-English summary, who signs it, when, and a "View sample PDF" button. The PDFs are the unsigned SignNow templates with a "SAMPLE" watermark.
8. Lessons learned ("Do the same / Do differently" from the sheet).
9. Checklists: print assets, to-do list, show-day run sheet.
10. **Consulting:** "We'll help you run it — on site or remotely, for a fee." with a contact form/email.
11. Footer (same).

## 5. How I'll build it

- **Stack:** plain HTML, CSS and a little JavaScript (lightbox, budget table, contract viewer). No framework, no build step, so anyone on the team can edit it later and it can be hosted anywhere (Vercel, Netlify, GitHub Pages, or imported back into Squarespace as needed).
- **Folder:** `site/` inside this project: `index.html`, `your-town.html`, `assets/` (logos, photos resized for web, contract PDFs, budget spreadsheet).
- **Design:** black header/footer, off-white sections, Sedona orange accent, Archivo Black headlines, Space Grotesk body, lots of photo. Mobile-first.
- **Photos:** download the originals, pick the best, resize to web size. If ShootProof blocks downloads, I'll use the current site's images and your folder, and link out to the galleries.
- **Contracts:** download each template PDF from SignNow in your Chrome, stamp "SAMPLE", embed and offer for download.
- **Budget:** build the template from the Budget tab, export as .xlsx and as a copy-able Google Sheet.
- **Preview:** I'll open it in the browser pane as I go, and I can deploy a preview to Vercel so Zenka can look at it on her phone.

## 6. Decisions I'm assuming (correct me)

1. Consulting has no public price: "Contact us for a quote" with the Fashion Lab email.
2. The budget template shows line items and amounts but not sponsor names.
3. Contracts are shown as unsigned, watermarked samples and are free to download.
4. The new site is a hand-off package. I will not touch the live Squarespace site or the domain.
5. Newsletter sign-up points to the existing list (I'll wire it to Brevo if you want it live, otherwise a mailto).
6. The 2025 archive stays as links to the existing pages/galleries, not rebuilt.

## 7. Order of work

1. Collect assets (site images, folder photos, ShootProof galleries, SignNow PDFs, budget export).
2. Build the shared design system (CSS, header, footer, components).
3. Build the home page.
4. Build the "your own town" page, including the contracts pack and budget.
5. Review on desktop and phone, fix, deploy preview.
6. Hand you the folder and the preview link.
