# Protocolo operativo del sitio DejavuUrbe

Este repositorio es la fuente principal del sitio oficial de DejavuUrbe.

## Principios
- Mantener arquitectura estática y simple compatible con GitHub Pages.
- No mezclar autoría de composiciones con titularidad de fonogramas.
- No publicar datos personales sensibles ni documentación privada.
- Priorizar fuentes maestras del proyecto para historia, catálogo, registros y créditos.
- Mantener títulos de canciones con ortografía normalizada en pantalla y slugs simples en URL.

## Flujo normal de actualización
1. Leer la información nueva y contrastarla con los documentos maestros del proyecto.
2. Modificar directamente los archivos correspondientes en `main` cuando el cambio sea de bajo riesgo.
3. Mantener `sitemap.xml` actualizado al crear nuevas páginas públicas.
4. Mantener Schema.org y metadatos SEO coherentes con el contenido visible.
5. Verificar que los enlaces relativos funcionen tanto en GitHub Pages como en el futuro dominio propio.

## Estructura
- `/index.html`: portada oficial.
- `/musica/<slug>/index.html`: páginas individuales de canciones.
- `/assets/css/styles.css`: estilos globales.
- `/data/canciones.json`: catálogo estructurado.
- `/sitemap.xml`: URLs indexables.
- `/robots.txt`: directivas para buscadores.

## Dominio
Hasta que NIC Argentina confirme el registro de `dejavuurbe.com.ar`, no crear `CNAME` ni modificar DNS. El sitio provisional continúa alojado en GitHub Pages.

## Actualizaciones futuras solicitables a ChatGPT
- Agregar entrevista o nota de prensa.
- Crear una página de nuevo lanzamiento.
- Corregir biografía, fechas o enlaces.
- Incorporar videos.
- Actualizar distribución o perfiles oficiales.
- Ampliar datos estructurados y SEO.

Los cambios normales deben resolverse desde GitHub sin exigir edición manual al usuario.