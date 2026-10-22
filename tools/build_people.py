"""Build the People directory (site/people.html): everyone involved in
Fashion Lab Sedona 2026 on one big page, sponsors first.

Everything is pulled from content already on the site, so re-run this after
changing any of the sources:
  - Sponsors, vendors and raffle donors: data/sponsors-2026.csv (same as
    tools/build_sponsors.py, same logos).
  - Core team: the TEAM section of site/index.html.
  - Designers: site/designers.html.
  - Sensational Sedonans: site/sedonans.html.
  - Photographers, collaborators, award winners and press: the short lists
    below (they mirror photographers-2026.html, sedona-dance-academy.html,
    winners-2026.html and press.html).

Run:  python3 tools/build_people.py
"""
import csv, html, re
from pathlib import Path

import build_sponsors as sp

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
PAGE = SITE / 'people.html'
START, END = '<!-- PEOPLE:START -->', '<!-- PEOPLE:END -->'
e = html.escape

# Sponsor groups in page order: (CSV category, heading, card size).
SPONSOR_GROUPS = [
    ('Headline Sponsor', 'Headline Sponsors', 'xl'),
    ('Event Sponsor', 'Event Sponsors', 'md'),
    ('Vendor', 'Vendors', 'sm'),
    ('Raffle Donor', 'Raffle Donors', 'sm'),
]

# (name, role, photo or logo, link)
PHOTOGRAPHERS = [
    ('Karl Mullings', 'KFM Designs Photography. Create-a-Thon and runway photos.', 'assets/img/collab/karl-mullings.jpg', 'photographers-2026.html#karl'),
    ('Leah Joy Love', 'Leah Joy Love Photography. Runway photos.', 'assets/img/collab/leah-joy-love.jpg', 'photographers-2026.html#leah'),
    ('Angelo LaMarco', 'Sedona Media Services. Filmed the show.', 'assets/img/sponsors/sedona-media-services.png', 'photographers-2026.html#sedona-media'),
    ('The Closet Concierge', 'Social media, from the Create-a-Thon to the runway.', 'assets/img/sponsors/the-closet-concierge.png', 'photographers-2026.html#closet-concierge'),
]
COLLABORATORS = [
    ('Sedona Dance Academy', 'Event collaboration. The dancers on the runway.', 'assets/img/sponsors/sedona-dance-academy.png', 'sedona-dance-academy.html'),
    ('Danielle Johnson', 'Sedona Dance Project. Choreographed the Sedona Dance Academy girls.', 'assets/img/collab/danielle-johnson.jpg', 'sedona-dance-academy.html'),
    ('The Closet Concierge', 'The boutique that dressed the Sensational Sedonans.', 'assets/img/sponsors/the-closet-concierge.png', 'https://theclosetconcierge.shop'),
    ('Ultimate Light Mission', 'Home of the Create-a-Thon and the pop-ups.', 'assets/img/sponsors/ultimate-light-mission.png', 'https://ultimatelightmission.com'),
    ('FABRIC Incubator', 'Tempe fashion incubator. The scholarship prize.', 'assets/img/sponsors/fabric-incubator.png', 'https://fabricincubator.com'),
]
WINNERS = [
    ('Jesselynn Desmond', 'Sustainable Design Award. $1,000 and $4,000 in FABRIC credits.', 'designers.html#jesselynn-desmond'),
    ('Inok Alrutz', 'Extra $4,000 FABRIC scholarship.', 'designers.html#inok-alrutz'),
    ('Hollie Laban', '$750 cash prize from an anonymous donor.', 'designers.html#hollie-laban'),
]
PRESS = [
    ('Sedona Red Rock News', 'Fashion show brings imagination to runway (Oct 2026).', 'https://www.redrocknews.com/2026/10/17/fashion-show-brings-imagination-to-runway/'),
    ('Verde Independent', 'Kudos coverage, 2024 to 2026.', 'press.html#news'),
    ('Sedona.biz', 'Fashion Lab Sedona takes on fast fashion (Sept 2026).', 'https://sedona.biz/fashion-lab-sedona-takes-on-fast-fashion-with-a-runway-made-in-sedona/'),
]


def text(fragment):
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def articles(page):
    """(id, name, img, tagline) for each <article class="designer..."> on a page.

    The tagline is the first bold-italic business name in the bio (Sedonans) or
    the first link label (designers, unused for now), since free-text bios don't trim well."""
    src = (SITE / page).read_text(encoding='utf-8')
    out = []
    for m in re.finditer(r'<article class="designer[^"]*" id="([^"]+)">(.*?)</article>', src, re.S):
        aid, body = m.groups()
        img = re.search(r'<img[^>]+src="([^"]+)"', body)
        name = text(re.search(r'<h3>(.*?)</h3>', body, re.S).group(1))
        biz = re.search(r'<strong><em>(.*?)</em></strong>', body, re.S)
        lnk = re.search(r'class="designer__links"><li><a[^>]*>(.*?)</a>', body, re.S)
        tag = text(biz.group(1)) if biz else text(lnk.group(1)) if lnk else ''
        out.append((aid, name, img.group(1) if img else None, tag))
    return out


def team():
    src = (SITE / 'index.html').read_text(encoding='utf-8')
    block = src[src.index('id="team"'):]
    block = block[:block.index('</section>')]
    out = []
    for m in re.finditer(r'<figure><img src="([^"]+)"[^>]*><figcaption><strong>(.*?)</strong><span>(.*?)</span>', block):
        img, name, role = m.groups()
        out.append((text(name), text(role), img, 'index.html#team'))
    return out


def person(name, role, img, url, kind='photo'):
    ext = url.startswith('http')
    attrs = ' target="_blank" rel="noopener"' if ext else ''
    pic = (f'<img src="{e(img)}" alt="" loading="lazy">' if img
           else f'<span class="dir-card__initials">{e("".join(w[0] for w in name.split()[:2]))}</span>')
    return (f'          <a class="dir-card dir-card--{kind}" href="{e(url)}"{attrs} data-name="{e(name.lower())}">'
            f'<span class="dir-card__pic">{pic}</span>'
            f'<span class="dir-card__text"><strong>{e(name)}</strong><span>{e(role)}</span></span></a>')


def section(sid, eyebrow, heading, cards, note='', sand=False):
    cls = 'section section--sand' if sand else 'section'
    out = [f'  <section class="{cls} dir-section" id="{sid}">', '    <div class="wrap">',
           '      <div class="section-head">', f'        <span class="eyebrow">{e(eyebrow)}</span>',
           f'        <h2>{e(heading)} <span class="dir-count">{len(cards)}</span></h2>']
    if note:
        out.append(f'        <p class="lead">{note}</p>')
    out += ['      </div>', '      <div class="dir-grid">', *cards, '      </div>', '    </div>', '  </section>']
    return out


def sponsors_section(rows):
    out = ['  <section class="section dir-section" id="sponsors">', '    <div class="wrap">',
           '      <div class="section-head">', '        <span class="eyebrow">Thank you</span>',
           f'        <h2>Sponsors &amp; donors <span class="dir-count">{len(rows)}</span></h2>',
           '        <p class="lead">The businesses, foundations and neighbors who made 2026 possible. Full details on the <a href="partners.html">Partners page</a>.</p>',
           '      </div>']
    for cat, heading, size in SPONSOR_GROUPS:
        members = [r for r in rows if r['Category'].strip() == cat]
        if not members:
            continue
        cards = []
        for r in members:
            c = sp.card(r, size).replace('class="sp-card', f'data-name="{e(sp.RENAME.get(r["Name"], r["Name"]).strip().lower())}" class="sp-card', 1)
            cards.append(c)
        out += ['      <div class="sp-group dir-group">',
                f'        <h3 class="sponsor-title">{e(heading)}</h3>',
                f'        <div class="sp-grid sp-grid--{size}">', *cards, '        </div>', '      </div>']
    out += ['    </div>', '  </section>']
    return out


def build():
    rows = [r for r in csv.DictReader(open(sp.CSV, encoding='utf-8')) if r.get('Name', '').strip()]
    designers = articles('designers.html')
    sedonans = articles('sedonans.html')
    sections = [
        ('sponsors', 'Sponsors', sponsors_section(rows)),
        ('team', 'Core team', section('team', 'Core team', 'The people who make it happen',
            [person(*t) for t in team()], sand=True)),
        ('designers', 'Designers', section('designers', '48 Hour Create-a-Thon', 'Designers 2026',
            [person(n, 'Create-a-Thon designer', i, f'designers.html#{a}') for a, n, i, b in designers],
            'The makers who designed and sewed the looks. <a href="winners-2026.html">See the award winners</a>.')),
        ('winners', 'Winners', section('winners', 'Sustainable Design Award', 'Award winners 2026',
            [person(n, r, next((i for a, nn, i, b in designers if nn == n), None), u) for n, r, u in WINNERS], sand=True)),
        ('sedonans', 'Sensational Sedonans', section('sedonans', 'On the runway', 'Sensational Sedonans',
            [person(n, b or 'Sensational Sedonan', i, f'sedonans.html#{a}') for a, n, i, b in sedonans],
            'Local business owners and community members who walked the runway.')),
        ('photographers', 'Photo &amp; video', section('photographers', 'Behind the lens', 'Photographers & videographers',
            [person(*p) for p in PHOTOGRAPHERS], sand=True)),
        ('collaborators', 'Collaborators', section('collaborators', 'Event collaboration', 'Collaborators',
            [person(*c, kind='logo') if c[2] and 'sponsors/' in c[2] else person(*c) for c in COLLABORATORS])),
        ('press', 'Press', section('press', 'In the news', 'Press',
            [person(n, r, None, u) for n, r, u in PRESS],
            'Writing about Fashion Lab Sedona? See the <a href="press.html">press page</a>.', sand=True)),
    ]
    jump = ['  <nav class="dir-jump" aria-label="Directory sections">', '    <div class="wrap">',
            '      <label class="dir-search"><span class="sr-only">Search the directory</span><input type="search" id="dir-search" placeholder="Search names…" autocomplete="off"></label>',
            '      <div class="dir-jump__links">']
    jump += [f'        <a href="#{sid}">{label}</a>' for sid, label, _ in sections]
    jump += ['      </div>', '    </div>', '  </nav>']
    body = [START, *jump]
    for _, _, lines in sections:
        body += lines
    body += ['  <p class="dir-empty" id="dir-empty" hidden>No one by that name. Try fewer letters.</p>', '  ' + END]
    src = PAGE.read_text(encoding='utf-8')
    PAGE.write_text(sp.replace_between(src, START, END, '\n'.join(body)), encoding='utf-8')
    total = len(rows) + len(team()) + len(designers) + len(sedonans) + len(PHOTOGRAPHERS) + len(COLLABORATORS) + len(PRESS)
    print(f'people.html: {total} entries ({len(rows)} sponsors, {len(designers)} designers, {len(sedonans)} Sedonans)')


if __name__ == '__main__':
    build()
