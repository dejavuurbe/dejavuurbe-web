#!/usr/bin/env python3
from pathlib import Path
from io import BytesIO
from urllib.request import Request, urlopen
import html
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'canciones.json'
COVERS = ROOT / 'assets' / 'covers'
COVERS.mkdir(parents=True, exist_ok=True)

songs = json.loads(CATALOG.read_text(encoding='utf-8'))
ua = {'User-Agent': 'Mozilla/5.0 DejavuUrbeSite/1.0'}

for song in songs:
    url = song['bandcamp']
    req = Request(url, headers=ua)
    page = urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', page, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', page, re.I)
    if not m:
        raise SystemExit(f"No se encontró og:image en {url}")
    image_url = html.unescape(m.group(1))
    image_data = urlopen(Request(image_url, headers=ua), timeout=30).read()
    with Image.open(BytesIO(image_data)) as im:
        im = im.convert('RGB')
        side = min(im.size)
        left = (im.width - side) // 2
        top = (im.height - side) // 2
        im = im.crop((left, top, left + side, top + side)).resize((600, 600), Image.Resampling.LANCZOS)
        out = COVERS / f"{song['slug']}.webp"
        im.save(out, 'WEBP', quality=84, method=6)
        if out.stat().st_size < 8000:
            raise SystemExit(f"Portada demasiado pequeña: {out} ({out.stat().st_size} bytes)")
        print(f"OK {song['slug']}: {out.stat().st_size} bytes <- {image_url}")

print('OK: 10 portadas sincronizadas desde las páginas oficiales de Bandcamp.')
