# Integración de perfiles de streaming — DejavuUrbe

## Objetivo

Cuando la nueva distribuidora publique el catálogo, la web debe incorporar los perfiles oficiales de DejavuUrbe en las plataformas musicales sin inventar ni anticipar URLs.

## Regla principal

Cada perfil debe verificarse antes de publicarse. Un enlace se considera confirmado cuando proviene de la distribuidora, de la plataforma o de una búsqueda manual inequívoca que muestre el catálogo correcto de DejavuUrbe.

## Flujo de incorporación

1. Recibir o localizar los cuatro perfiles oficiales de artista.
2. Confirmar que el perfil muestra DejavuUrbe y el catálogo correcto.
3. Registrar cada URL en `data/plataformas.json`.
4. Añadir esos perfiles a `sameAs` del `MusicGroup` principal.
5. Mostrar los perfiles en `/enlaces/` y `/musica/`.
6. Añadir, cuando existan, enlaces directos de cada lanzamiento a las páginas individuales de canción.
7. Incorporar los perfiles confirmados a `llms.txt` y demás recursos de trazabilidad.

## Separación entre perfil de artista y enlace de canción

No deben confundirse:

- **Perfil de artista:** URL estable del perfil de DejavuUrbe en una plataforma.
- **Enlace de lanzamiento/canción:** URL específica de un single o grabación.

El perfil de artista se usa como señal de identidad (`sameAs`). El enlace de canción se usa en la página individual del tema.

## Prevención de errores

No reutilizar URLs antiguas sin confirmar que pertenezcan al perfil correcto. No asumir que una plataforma conservará el mismo identificador usado por una distribuidora anterior. Si aparece más de un perfil con el nombre DejavuUrbe, comprobar catálogo, portada, fechas e ISRC antes de decidir cuál es el oficial.

## Resultado esperado

La web oficial debe terminar funcionando como punto de unión entre:

DejavuUrbe → perfil oficial de artista → canción → ISRC/UPC → MusicBrainz/Discogs/Bandcamp/YouTube y demás plataformas confirmadas.
