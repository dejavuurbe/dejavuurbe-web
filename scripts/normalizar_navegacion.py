#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]

pages = [p for p in root.rglob('*.html') if '.git' not in p.parts and 'salir' not in p.parts]

for path in pages:
    rel = path.relative_to(root)
    depth = len(rel.parts) - 1
    prefix = '../' * depth
    home_href = '#inicio' if rel.as_posix() == 'index.html' else prefix
    nav = (
        f'<header class="site-header"><div class="wrap nav">'
        f'<a class="brand" href="{home_href}">DEJAVUURBE</a>'
        f'<nav class="nav-links" aria-label="Navegación principal">'
        f'<a href="{prefix}banda/">Banda</a>'
        f'<a href="{prefix}musica/">Música</a>'
        f'<a href="{prefix}videos/">Videos</a>'
        f'<a href="{prefix}prensa/">En vivo</a>'
        f'<a href="{prefix}enlaces/">Enlaces</a>'
        f'<a href="{prefix}contacto/">Contacto</a>'
        f'</nav></div></header>'
    )
    text = path.read_text(encoding='utf-8')
    new, n = re.subn(r'<header class="site-header">.*?</header>', nav, text, count=1, flags=re.S)
    if n:
        path.write_text(new, encoding='utf-8')
        print(f'OK {rel}')
    else:
        print(f'SIN HEADER {rel}')

# Mantener una única navegación coherente en todas las páginas públicas.
