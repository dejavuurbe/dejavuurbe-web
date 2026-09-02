# DejavuUrbe — sitio oficial

**Sitio oficial:** https://dejavuurbe.com.ar/

Repositorio técnico del sitio oficial de **DejavuUrbe**, banda argentina de rock.

> Para música, historia, videos, fechas y enlaces oficiales, visite https://dejavuurbe.com.ar/

## Estado
- Sitio estático publicado con GitHub Pages.
- Dominio oficial activo: `dejavuurbe.com.ar`.
- Catálogo 2026: 10 lanzamientos con páginas individuales.
- SEO, `sitemap.xml`, `robots.txt`, `llms.txt` y datos estructurados Schema.org incluidos.
- Cloudflare Web Analytics activo.

## Principio editorial
El sitio trabaja para dos audiencias al mismo tiempo:

1. **Personas**: música, imágenes, historia, videos y navegación clara, con tono de banda y no de registro administrativo.
2. **Buscadores e IA**: entidades consistentes, `MusicGroup`, `MusicRecording`, canonical, `sameAs`, ISRC, UPC, MusicBrainz, Discogs y fuentes estructuradas.

Los identificadores técnicos se conservan para trazabilidad, pero no deben dominar la experiencia visual del visitante.

## Automatización
Las páginas individuales de canciones se generan desde `data/canciones.json` mediante `scripts/generar_paginas_canciones.py`. El workflow `song-pages.yml` las mantiene sincronizadas cuando cambia el catálogo o la URL pública.

## Dominio oficial
https://dejavuurbe.com.ar/

La URL de GitHub Pages funciona únicamente como infraestructura técnica de publicación. La referencia pública y canónica del proyecto es `dejavuurbe.com.ar`.

## Documentación operativa
Ver `docs/OPERACION.md`.
