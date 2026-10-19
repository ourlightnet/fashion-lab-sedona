"""Build the link previews and SEO tags for every page.

For each page in PAGES this:
  - draws a 1200x630 preview image (the picture shown when someone texts or
    posts a link) into site/assets/img/og/<name>.jpg, from the page's photo,
    the logo and a short headline;
  - writes the page's preview and SEO tags (canonical, Open Graph, Twitter
    card) and the Google Analytics loader between the SEO markers in <head>,
    using the page's own <title> and meta description;
  - rewrites site/sitemap.xml.

Google Analytics: put the Measurement ID in site/assets/js/analytics.js.

To add a page, add a line to PAGES and run:  python3 tools/build_seo.py
Pages not in PAGES (playbook, get-started, playbook-map, the redirect folders) are left alone.
"""
import html, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
OG_DIR = SITE / 'assets' / 'img' / 'og'
FONTS = ROOT / 'tools' / 'fonts'
BASE_URL = 'https://fashionlabsedona.com/'
START, END = '<!-- SEO:START -->', '<!-- SEO:END -->'
W, H = 1200, 630
ORANGE, DEEP, PAPER = (232, 93, 26), (178, 52, 10), (250, 250, 250)

# file, preview image name, photo (under assets/img), kicker, headline, focus.
# focus is where to keep the photo centred when it is cropped (0 = top/left,
# 1 = bottom/right): (x, y).
PAGES = [
    ('index.html', 'home', 'show/11201.jpg', 'Sedona, Arizona', 'Sustainable fashion. Made in 48 hours.', (.5, .5)),
    ('show-2026.html', 'show-2026', '2026/show-karl/22.jpg', 'Photos by Karl Mullings', 'The Show 2026', (.5, .3)),
    ('show-2026-leah.html', 'show-2026-leah', '2026/show-leah/37.jpg', 'Photos by Leah Joy Love', 'The Show 2026', (.5, .3)),
    ('createathon-2026.html', 'createathon-2026', '2026/createathon-day2/01.jpg', 'Day 1 and Day 2', '48 Hour Create-a-Thon 2026', (.5, .5)),
    ('afterparty-2026.html', 'afterparty-2026', '2026/afterparty/02.jpg', 'Fashion Lab Sedona', 'After Party 2026', (.5, .35)),
    ('photos-2026.html', 'photos-2026', 'show/11185.jpg', 'Show, Create-a-Thon, After Party', '2026 Photos', (.5, .3)),
    ('galleries-2026.html', 'galleries-2026', '2026/show-karl/75.jpg', 'Karl Mullings and Leah Joy Love', '2026 Full Galleries', (.5, .5)),
    ('winners-2026.html', 'winners-2026', 'designers/jesselynn-desmond-runway.jpg', 'Sustainable Design Award', '2026 Winners', (.5, .3)),
    ('designers.html', 'designers', 'lab/0262.jpg', 'Upcycled in 48 hours', 'Meet the 2026 Designers', (.5, .4)),
    ('sedonans.html', 'sedonans', 'show/10883.jpg', 'Local celebrity models', 'Sensational Sedonans 2026', (.5, .25)),
    ('sedona-dance-academy.html', 'sedona-dance-academy', '2026/sedona-dance-academy/03.jpg', 'Event Collaboration', 'Sedona Dance Academy', (.5, .3)),
    ('get-involved.html', 'get-involved', 'lab/0164.jpg', 'Design, model, volunteer, give', 'Get Involved', (.5, .5)),
    ('designer-waitlist.html', 'designer-waitlist', 'lab/0603.jpg', 'Designer waitlist', 'Design for Fashion Lab 2027', (.5, .3)),
    ('model-waitlist.html', 'model-waitlist', 'show/10965.jpg', 'Model waitlist', 'Walk the runway in 2027', (.5, .3)),
    ('your-town.html', 'your-town', 'lab/0548.jpg', 'The Fashion Lab playbook', 'Do the Fashion Lab in your own town!', (.5, .5)),
    ('updates/index.html', 'updates', 'show/10941.jpg', 'Mailing list', 'Get Fashion Lab updates', (.5, .3)),
    ('popups.html', 'popups', 'site/popup-sewing.jpg', 'Sewing, dyeing, modeling and more', 'Pop-Ups and Workshops', (.5, .5)),
    ('videos.html', 'videos', '2026/show-karl/01.jpg', 'Highlights and sizzle reel', 'Videos', (.5, .3)),
    ('partners.html', 'partners', 'show/11203.jpg', 'Sponsors, donors and collaborators', 'Our Partners', (.5, .5)),
    ('press.html', 'press', 'site/lead.jpg', 'News, fast facts, logos, photos', 'Press', (.5, .5)),
    ('2025.html', '2025', 'past/2025/show/01.jpg', 'Prior years', 'Fashion Lab 2025', (.5, .3)),
    ('2024.html', '2024', 'past/2024/show/02.jpg', 'Prior years', 'Fashion Lab 2024', (.5, .3)),
]


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def wrap(draw, text, fnt, width):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if draw.textlength(trial, font=fnt) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def fit_headline(draw, text, width, max_lines=3):
    for size in range(78, 34, -2):
        fnt = font('ArchivoBlack.ttf', size)
        lines = wrap(draw, text, fnt, width)
        if len(lines) <= max_lines and all(draw.textlength(l, font=fnt) <= width for l in lines):
            return fnt, lines
    return fnt, lines


def draw_text_panel(card, x, width, bottom, kicker, headline, shadow=False):
    """Kicker, headline and site name, stacked up from `bottom`."""
    d = ImageDraw.Draw(card)
    hf, lines = fit_headline(d, headline, width)
    kf = font('SpaceGrotesk-Bold.ttf', 26)
    uf = font('SpaceGrotesk-Medium.ttf', 24)
    lh = int(hf.size * 1.08)
    y = bottom - 24 - 30                       # site name line
    url_y = y
    y -= 26 + lh * len(lines)                  # headline block
    head_y = y
    y -= 20 + 30                               # kicker
    kick_y = y
    d.rectangle([x, kick_y - 22, x + 64, kick_y - 14], fill=ORANGE)
    d.text((x, kick_y), kicker.upper(), font=kf, fill=ORANGE if not shadow else (255, 154, 60))
    for i, l in enumerate(lines):
        d.text((x, head_y + i * lh), l, font=hf, fill=PAPER)
    d.text((x, url_y), 'fashionlabsedona.com', font=uf, fill=(220, 220, 220))


def build_card(photo, kicker, headline, focus, out):
    src = Image.open(SITE / 'assets' / 'img' / photo).convert('RGB')
    logo = Image.open(SITE / 'assets' / 'img' / 'logo-box.jpg').convert('RGB')
    # Trim the logo's white margin so only the black box shows.
    logo = logo.crop(ImageOps.invert(logo).getbbox())
    portrait = src.width / src.height < 1.3
    if portrait:
        # Black panel on the left with the text, photo on the right.
        pw = 560
        card = Image.new('RGB', (W, H), (0, 0, 0))
        card.paste(ImageOps.fit(src, (W - pw, H), Image.LANCZOS, centering=focus), (pw, 0))
        d = ImageDraw.Draw(card)
        d.rectangle([pw - 6, 0, pw, H], fill=ORANGE)
        lg = logo.resize((300, round(300 * logo.height / logo.width)), Image.LANCZOS)
        card.paste(lg, (56, 56))
        draw_text_panel(card, 56, pw - 56 - 48, H - 30, kicker, headline)
    else:
        # Photo across the whole card, darkened at the bottom for the text.
        card = ImageOps.fit(src, (W, H), Image.LANCZOS, centering=focus)
        shade = Image.new('L', (1, H))
        for yy in range(H):
            t = max(0, (yy - H * .25) / (H * .60))
            shade.putpixel((0, yy), int(min(1, t) * 242))
        card = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), card, shade.resize((W, H)))
        lg = logo.resize((240, round(240 * logo.height / logo.width)), Image.LANCZOS)
        card.paste(lg, (48, 44))
        draw_text_panel(card, 56, 900, H - 26, kicker, headline, shadow=True)
        ImageDraw.Draw(card).rectangle([0, H - 8, W, H], fill=ORANGE)
    card.save(out, 'JPEG', quality=85, optimize=True, progressive=True)


def page_url(file):
    if file == 'index.html':
        return BASE_URL
    if file.endswith('/index.html'):
        return BASE_URL + file[:-len('index.html')]
    return BASE_URL + file


def meta_block(file, name, text, kicker, headline):
    title = re.search(r'<title>(.*?)</title>', text, re.S).group(1).strip()
    m = re.search(r'<meta name="description" content="([^"]*)"', text)
    desc = m.group(1) if m else ''
    url, img = page_url(file), f'{BASE_URL}assets/img/og/{name}.jpg'
    alt = html.escape(f'{headline} — Fashion Lab Sedona', quote=True)
    depth = '' if '/' not in file or '<base href="../">' in text else '../'
    return '\n'.join([
        START,
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Fashion Lab Sedona">',
        '<meta property="og:locale" content="en_US">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:type" content="image/jpeg">',
        f'<meta property="og:image:width" content="{W}">',
        f'<meta property="og:image:height" content="{H}">',
        f'<meta property="og:image:alt" content="{alt}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{img}">',
        f'<meta name="twitter:image:alt" content="{alt}">',
        f'<script src="{depth}assets/js/analytics.js" async></script>',
        END,
    ])


def update_page(file, block):
    path = SITE / file
    text = path.read_text()
    if START in text:
        text = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        # Drop the old hand-written preview tags, then add the block before </head>.
        text = re.sub(r'<meta property="og:[^"]*" content="[^"]*">\n', '', text)
        text = text.replace('</head>', block + '\n</head>', 1)
    path.write_text(text)


def lastmod(file):
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f'site/{file}'],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return out or None


def write_sitemap():
    rows = []
    for file, *_ in PAGES:
        mod = lastmod(file)
        rows.append('  <url><loc>%s</loc>%s</url>' % (
            page_url(file), f'<lastmod>{mod}</lastmod>' if mod else ''))
    (SITE / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(rows) + '\n</urlset>\n')


def main():
    OG_DIR.mkdir(exist_ok=True)
    for file, name, photo, kicker, headline, focus in PAGES:
        build_card(photo, kicker, headline, focus, OG_DIR / f'{name}.jpg')
        text = (SITE / file).read_text()
        update_page(file, meta_block(file, name, text, kicker, headline))
        print(f'{file:28} -> assets/img/og/{name}.jpg')
    write_sitemap()
    print('sitemap.xml:', len(PAGES), 'pages')


if __name__ == '__main__':
    main()
