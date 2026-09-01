#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
base = 'https://dejavuurbe.github.io/dejavuurbe-web/'

pages = [p for p in root.rglob('*.html') if '.git' not in p.parts and 'salir' not in p.parts]

for path in pages:
    rel = path.relative_to(root)
    depth = len(rel.parts) - 1
    prefix = '../' * depth
    text = path.read_text(encoding='utf-8')

    if 'rel="icon"' not in text:
        text = text.replace('</title>', f'</title><link rel="icon" href="{prefix}assets/brand/favicon.svg" type="image/svg+xml">', 1)

    if 'name="theme-color"' not in text:
        text = text.replace('</head>', '<meta name="theme-color" content="#080808"></head>', 1)

    path.write_text(text, encoding='utf-8')
    print(f'OK meta {rel}')

# Portada: entidad estable y tarjeta social reutilizando un arte oficial ya disponible.
index = root / 'index.html'
html = index.read_text(encoding='utf-8')

if 'property="og:image"' not in html:
    html = html.replace(
        '<meta property="og:url" content="https://dejavuurbe.github.io/dejavuurbe-web/">',
        '<meta property="og:url" content="https://dejavuurbe.github.io/dejavuurbe-web/">\n  <meta property="og:image" content="https://dejavuurbe.github.io/dejavuurbe-web/assets/covers/ya-no-puedo-evitarte.webp">\n  <meta property="og:image:alt" content="DejavuUrbe — Ya no puedo evitarte">\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="DejavuUrbe | Sitio oficial">\n  <meta name="twitter:description" content="Rock argentino. Canciones, historia, videos y la etapa actual de DejavuUrbe.">\n  <meta name="twitter:image" content="https://dejavuurbe.github.io/dejavuurbe-web/assets/covers/ya-no-puedo-evitarte.webp">',
        1
    )

html = html.replace(
    '"@type":"MusicGroup","name":"DejavuUrbe"',
    '"@type":"MusicGroup","@id":"https://dejavuurbe.github.io/dejavuurbe-web/#dejavuurbe","name":"DejavuUrbe"',
    1
)
index.write_text(html, encoding='utf-8')

# Música: misma llamada a la acción que en la portada.
music = root / 'musica/index.html'
if music.exists():
    text = music.read_text(encoding='utf-8').replace('Entrar a la canción', 'Escuchar y conocer')
    music.write_text(text, encoding='utf-8')

print('OK: metadatos, entidad principal y CTA de Música normalizados.')
