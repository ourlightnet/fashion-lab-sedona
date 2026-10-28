"""Build the sponsors section of site/index.html, the Shop Our Sponsors page
(site/sponsors.html) and the Partners page (site/partners.html) from
data/sponsors-2026.csv.

On the home page only Headline Sponsors show their name under the logo; every
other logo shows its name and description on hover. The Partners page prints
every name and description in full.

The CSV is exported from the "Donors Fashion Lab Sedona 2026" Google Sheet
(File > Download > CSV). Logos are picked up from site/assets/img/sponsors/
by slug (e.g. fabric-incubator.png); a sponsor without a logo file shows a
name tile instead. Run:  python3 tools/build_sponsors.py
"""
import csv, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / 'data' / 'sponsors-2026.csv'
INDEX = ROOT / 'site' / 'index.html'
PARTNERS = ROOT / 'site' / 'partners.html'
SPONSORS = ROOT / 'site' / 'sponsors.html'
LOGOS = ROOT / 'site' / 'assets' / 'img' / 'sponsors'
START, END = '<!-- SPONSORS:START -->', '<!-- SPONSORS:END -->'
# Compact strip of headline sponsor logos near the top of the page.
STRIP_START, STRIP_END = '<!-- HEADLINE-STRIP:START -->', '<!-- HEADLINE-STRIP:END -->'

# Section order, heading and display size on the page.
GROUPS = [
    ('Headline Sponsor', 'Headline Sponsors', 'xl'),
    ('Event Sponsor', 'Event Sponsors', 'md'),
    ('Event Collaborator', 'Event Collaborators', 'md'),
    ('Production Partner', 'Production Partner', 'md'),
    ('Vendor', 'Vendors', 'sm'),
    ('Raffle Donor', 'Raffle Donors', 'sm'),
    ('Donor & Community Supporter', 'Donors & Community Supporters', 'sm'),
]
# Names as they should read on the site, where the sheet has a working label.
RENAME = {
    '"d+b … Productions" (round logo)': 'Downtown Browne Productions',
    'Sedona Superhum Juice': 'Sedona Superhuman Juice',
}

def slug(name):
    name = re.sub(r"['’]", '', name.lower()).replace('&', 'and').replace('é', 'e')
    return re.sub(r'[^a-z0-9]+', '-', name).strip('-')

def logo_for(name):
    for ext in ('svg', 'png', 'webp', 'jpg', 'jpeg'):
        p = LOGOS / f'{slug(name)}.{ext}'
        if p.exists():
            return f'assets/img/sponsors/{p.name}'
    return None

def link(url):
    url = url.strip()
    if url and not re.match(r'^(https?:|mailto:)', url):
        url = 'https://' + url
    return url

def card(row, size, roll=False):
    """A logo card. roll=True hides the name and shows name + description on hover."""
    name = RENAME.get(row['Name'], row['Name']).strip()
    url, desc = link(row['Link']), row['Description'].strip()
    logo = logo_for(name)
    e = html.escape
    mark = (f'<img src="{logo}" alt="{e(name)}" loading="lazy">' if logo
            else f'<span class="sp-card__name-tile">{e(name)}</span>')
    text = (f'<span class="sp-card__name">{e(name)}</span>'
            + (f'<span class="sp-card__desc">{e(desc)}</span>' if desc else ''))
    if roll:
        inner = f'<span class="sp-card__logo">{mark}</span><span class="sp-card__roll">{text}</span>'
        cls = f'sp-card sp-card--{size} sp-card--roll'
    else:
        inner = f'<span class="sp-card__logo">{mark}</span>{text}'
        cls = f'sp-card sp-card--{size}'
    attrs = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
    tag = f'<a class="{cls}" href="{e(url)}"{attrs}>' if url else f'<div class="{cls}" tabindex="0">'
    close = '</a>' if url else '</div>'
    return f'          {tag}{inner}{close}'

def strip_item(row):
    name = RENAME.get(row['Name'], row['Name']).strip()
    url, logo, e = link(row['Link']), logo_for(name), html.escape
    mark = (f'<img src="{logo}" alt="{e(name)}" loading="lazy">' if logo
            else f'<span class="sp-strip__name">{e(name)}</span>')
    attrs = ' target="_blank" rel="noopener"' if url.startswith('http') else ''
    if url:
        return f'          <a class="sp-strip__item" href="{e(url)}" title="{e(name)}"{attrs}>{mark}</a>'
    return f'          <span class="sp-strip__item" title="{e(name)}">{mark}</span>'

def replace_between(page, start, end, body):
    s, t = page.index(start), page.index(end) + len(end)
    return page[:s] + body + page[t:]

def groups_html(rows, partners_page=False):
    out = []
    for cat, heading, size in GROUPS:
        members = [r for r in rows if r['Category'].strip() == cat]
        if not members:
            continue
        headline = cat == GROUPS[0][0]
        if partners_page and not headline:
            size = 'md'  # full name + description on every card
        roll = not partners_page and not headline
        out.append(f'      <div class="sp-group reveal">\n        <h3 class="sponsor-title">{html.escape(heading)}</h3>\n        <div class="sp-grid sp-grid--{size}">')
        out += [card(r, size, roll) for r in members]
        out.append('        </div>\n      </div>')
    return out

def build():
    rows = [r for r in csv.DictReader(open(CSV, encoding='utf-8')) if r.get('Name', '').strip()]
    out = [START, *groups_html(rows), '      ' + END]
    page = replace_between(INDEX.read_text(encoding='utf-8'), START, END, '\n'.join(out))
    headline = [strip_item(r) for r in rows if r['Category'].strip() == GROUPS[0][0]]
    strip = [STRIP_START, '        <div class="sp-strip__logos">', *headline, '        </div>', '        ' + STRIP_END]
    page = replace_between(page, STRIP_START, STRIP_END, '\n'.join(strip))
    partners = PARTNERS.read_text(encoding='utf-8')
    partners = replace_between(partners, START, END, '\n'.join([START, *groups_html(rows, True), '      ' + END]))
    PARTNERS.write_text(partners, encoding='utf-8')
    sponsors = SPONSORS.read_text(encoding='utf-8')
    SPONSORS.write_text(replace_between(sponsors, START, END, '\n'.join(out)), encoding='utf-8')
    INDEX.write_text(page, encoding='utf-8')
    missing = [RENAME.get(r['Name'], r['Name']) for r in rows if not logo_for(RENAME.get(r['Name'], r['Name']))]
    print(f'{len(rows)} sponsors; {len(rows) - len(missing)} with logos')
    print('Logo file names expected (in site/assets/img/sponsors/):')
    for n in missing:
        print(f'  {slug(n)}.png  ({n})')

if __name__ == '__main__':
    build()
