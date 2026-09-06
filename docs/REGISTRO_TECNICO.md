# Registro técnico de mantenimiento web — DejavuUrbe

## Regla operativa obligatoria

Cada procedimiento que produzca un resultado correcto debe registrarse aquí con:

1. fecha y objetivo;
2. archivos o configuración afectados;
3. commit o referencia verificable;
4. comprobación automática;
5. comprobación en el dominio oficial;
6. problemas encontrados y forma correcta de repetir el procedimiento.

Un commit aceptado no constituye por sí solo una publicación exitosa. Siempre debe verificarse el resultado en `https://dejavuurbe.com.ar/`.

## Procedimiento general de publicación

1. Revisar el estado actual y el historial reciente antes de modificar archivos.
2. Cambiar únicamente los archivos necesarios.
3. Para imágenes, comprobar firma binaria, MIME, extensión, dimensiones y decodificación completa.
4. Publicar en `main`.
5. Esperar la sincronización de GitHub Pages y Cloudflare.
6. Ejecutar los controles de catálogo, imágenes, descubribilidad y sitio publicado.
7. Abrir o solicitar directamente las URLs del dominio oficial, evitando validar solamente GitHub.
8. Verificar escritorio y móvil si la modificación afecta contenido visible.
9. Si el resultado empeora, revertir únicamente esa modificación.
10. Registrar el resultado estable en este documento.

## Buscadores e inteligencia artificial

La infraestructura vigente incluye:

- `robots.txt` con sitemap oficial;
- `sitemap.xml` con las páginas públicas;
- `llms.txt` como resumen factual legible por asistentes;
- `data/entity.jsonld` como fuente estructurada central;
- JSON-LD en las páginas públicas;
- URLs canónicas y metadatos Open Graph;
- páginas individuales para las diez canciones;
- IndexNow posterior a cambios relevantes;
- Cloudflare Web Analytics;
- páginas internas `/salir/` para medir accesos a plataformas externas.

### Control de coherencia

El script `scripts/verificar_descubribilidad.py` compara:

- dominio oficial;
- URLs y fechas del sitemap;
- catálogo de diez canciones;
- títulos, ISRC y UPC;
- `llms.txt`;
- `data/entity.jsonld`;
- existencia de páginas;
- idioma, título, descripción, viewport y canonical;
- Open Graph;
- validez sintáctica del JSON-LD;
- ausencia de `noindex` en páginas públicas;
- presencia de `noindex` en la página 404.

Se ejecuta desde `.github/workflows/site-check.yml` diariamente y en cada cambio técnico relevante.

## Registro de resultados

### 2026-09-06 — Auditoría integral de descubribilidad

- Creado `scripts/verificar_descubribilidad.py`.
- Integrado en el control automático diario.
- Activado el control ante cada cambio relevante.
- Corregida la comprobación de salud para usar el dominio oficial y no la URL provisional de GitHub Pages.
- Añadido `noindex,follow` y descripción técnica a `404.html`.
- Retiradas tres automatizaciones puntuales de fotografías que ya habían cumplido su función:
  - `add-professional-studio-2026.yml`;
  - `add-studio-profesional-photo.yml`;
  - `fix-studio-2026-layout.yml`.
- Resultado de GitHub Actions: correcto, ejecución 34054160366.
- Resultado publicado:
  - portada, Banda y Música: HTTP 200;
  - `robots.txt`, `sitemap.xml` y `llms.txt`: HTTP 200;
  - `data/entity.jsonld`: HTTP 200 y MIME `application/ld+json`;
  - URL inexistente: HTTP 404 y `noindex,follow`.

### Ajuste externo pendiente en Cloudflare

Cloudflare está anteponiendo reglas administradas al `robots.txt` del repositorio. La respuesta pública permite búsqueda y referencia, pero bloquea diversos rastreadores de IA.

Este comportamiento no se corrige modificando solamente el repositorio. Debe revisarse en el panel de Cloudflare:

1. seleccionar `dejavuurbe.com.ar`;
2. abrir **AI Crawl Control**;
3. revisar **Directives/robots.txt** y **Crawlers**;
4. permitir agentes destinados a búsqueda, respuestas con citas y referencias;
5. conservar el bloqueo de entrenamiento cuando esa sea la política elegida;
6. mantener como objetivo `search=yes`, `ai-train=no` y `use=reference`;
7. guardar;
8. volver a solicitar `https://dejavuurbe.com.ar/robots.txt`;
9. comprobar que no existan reglas contradictorias para los agentes que se decida permitir;
10. registrar aquí la fecha y el resultado.

No cambiar esta configuración sin revisar primero las categorías de cada rastreador, porque búsqueda, asistencia en tiempo real y entrenamiento son usos distintos.
