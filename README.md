# DejavuUrbe — sitio oficial

Sitio oficial de **DejavuUrbe**, proyecto argentino de rock.

## Estado
- Sitio estático publicado con GitHub Pages.
- Catálogo 2026: 10 lanzamientos con páginas individuales.
- SEO, `sitemap.xml`, `robots.txt`, `llms.txt` y datos estructurados Schema.org incluidos.
- Cloudflare Web Analytics activo.
- Mantenimiento previsto directamente mediante GitHub y ChatGPT.

## Principio editorial
El sitio trabaja para dos audiencias al mismo tiempo:

1. **Personas**: música, imágenes, historia, videos y navegación clara, con tono de banda y no de registro administrativo.
2. **Buscadores e IA**: entidades consistentes, `MusicGroup`, `MusicRecording`, canonical, `sameAs`, ISRC, UPC, MusicBrainz, Discogs y fuentes estructuradas.

Los identificadores técnicos se conservan para trazabilidad, pero no deben dominar la experiencia visual del visitante.

## Automatización
Las páginas individuales de canciones se generan desde `data/canciones.json` mediante `scripts/generar_paginas_canciones.py`. El workflow `song-pages.yml` las mantiene sincronizadas cuando cambia el catálogo o la URL pública.

## Sitio provisional
https://dejavuurbe.github.io/dejavuurbe-web/

## Dominio definitivo
`dejavuurbe.com.ar` se conectará cuando NIC Argentina confirme la registración. Hasta entonces no se debe crear `CNAME` ni modificar DNS.

## Documentación operativa
Ver `docs/OPERACION.md`.
