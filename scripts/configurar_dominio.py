from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'data' / 'site.json').read_text(encoding='utf-8'))
base = config['public_base'].rstrip('/')
known = {
    'https://dejavuurbe.com.ar',
    'https://dejavuurbe.github.io/dejavuurbe-web'
}

# Reemplazar URL base en HTML sin tocar enlaces externos.
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    new = text
    for old in known:
        new = new.replace(old, base)
    if new != text:
        path.write_text(new, encoding='utf-8')

# Sitemap completo y coherente con el dominio público activo.
paths = [
    '/', '/banda/', '/musica/', '/videos/', '/prensa/', '/enlaces/', '/contacto/',
    '/musica/ya-no-puedo-evitarte/', '/musica/cada-noche/',
    '/musica/balada-para-un-corto-amor/', '/musica/el-fantasma/', '/musica/brilla/',
    '/musica/dos-extranos/', '/musica/luna/', '/musica/triste-cancion/',
    '/musica/despiertame/', '/musica/luna-acustico/'
]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in paths:
    sitemap.append(f'<url><loc>{base}{p}</loc></url>')
sitemap.append('</urlset>')
(ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n', encoding='utf-8')

print(f'Dominio público sincronizado: {base}')
