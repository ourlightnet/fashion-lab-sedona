"""Build the playbook request map (site/playbook-map.html) from a Brevo export.

Playbook requests from your-town.html land in Brevo. To update the map:
  1. In Brevo, open Contacts, filter to the playbook list and export it as CSV.
  2. Save the file as data/playbook-requests.csv (it is git-ignored: it holds
     names, emails and phones, which never go in the repo or on the site).
  3. Run:  python3 tools/build_request_map.py

Only towns and counts are written to site/assets/data/playbook-requests.js.
Towns are looked up once on OpenStreetMap (Nominatim) and remembered in
data/city-coords.csv; fix a wrong spot by editing its lat/lon there. A town
that can't be found is listed at the end so you can add it by hand.
"""
import csv, json, sys, time, urllib.parse, urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORT = ROOT / 'data' / 'playbook-requests.csv'
COORDS = ROOT / 'data' / 'city-coords.csv'
OUT = ROOT / 'site' / 'assets' / 'data' / 'playbook-requests.js'
CITY_COLUMNS = ('CITY', 'TOWN OR CITY', 'VILLE')
UA = 'fashion-lab-sedona-site (fashionlabsedona@gmail.com)'

def key(city):
    return ' '.join(city.replace('.', ' ').split()).casefold()

def read_export(path):
    text = path.read_text(encoding='utf-8-sig')
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=',;\t')
    rows = list(csv.DictReader(text.splitlines(), dialect=dialect))
    if not rows:
        return []
    col = next((c for c in rows[0] if c and c.strip().upper() in CITY_COLUMNS), None)
    if not col:
        sys.exit(f'No city column in {path.name}. Columns: {", ".join(rows[0])}')
    return [r[col].strip() for r in rows if r.get(col, '').strip()]

def read_coords():
    if not COORDS.exists():
        return {}
    with COORDS.open(encoding='utf-8') as f:
        return {r['query']: r for r in csv.DictReader(f)}

def write_coords(coords):
    with COORDS.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['query', 'name', 'lat', 'lon'])
        w.writeheader()
        for k in sorted(coords):
            w.writerow(coords[k])

def geocode(city):
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(
        {'q': city, 'format': 'json', 'limit': 1, 'addressdetails': 1, 'accept-language': 'en'})
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        hits = json.load(r)
    time.sleep(1.1)  # Nominatim allows one request a second
    if not hits:
        return None
    a = hits[0].get('address', {})
    town = a.get('city') or a.get('town') or a.get('village') or a.get('hamlet') or hits[0]['name']
    region = a.get('state') if a.get('country_code') == 'us' else a.get('country')
    return {'name': ', '.join(p for p in (town, region) if p), 'lat': hits[0]['lat'], 'lon': hits[0]['lon']}

def main():
    if not EXPORT.exists():
        sys.exit(f'Export the playbook list from Brevo and save it as {EXPORT.relative_to(ROOT)}')
    cities = read_export(EXPORT)
    coords = read_coords()
    places, missing = {}, []
    for city in cities:
        k = key(city)
        if k not in coords:
            hit = geocode(city)
            coords[k] = {'query': k, **(hit or {'name': city, 'lat': '', 'lon': ''})}
        c = coords[k]
        if not c['lat']:
            missing.append(city)
            continue
        p = places.setdefault(c['name'], {'name': c['name'], 'lat': round(float(c['lat']), 4), 'lon': round(float(c['lon']), 4), 'count': 0})
        p['count'] += 1
    write_coords(coords)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = {'updated': date.today().isoformat(), 'total': len(cities), 'unmapped': len(missing),
            'places': sorted(places.values(), key=lambda p: (-p['count'], p['name']))}
    OUT.write_text('// Built by tools/build_request_map.py from the Brevo export. Towns and counts only.\n'
                   'window.PLAYBOOK_REQUESTS = ' + json.dumps(data, indent=1, ensure_ascii=False) + ';\n', encoding='utf-8')
    print(f'{len(cities)} requests from {len(places)} places written to {OUT.relative_to(ROOT)}')
    if missing:
        print('Not found (add lat/lon in data/city-coords.csv and run again):')
        for m in sorted(set(missing)):
            print('  ' + m)

if __name__ == '__main__':
    main()
