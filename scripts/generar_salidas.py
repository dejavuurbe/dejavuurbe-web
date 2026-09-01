from pathlib import Path
import json, html, re

ROOT = Path(__file__).resolve().parents[1]
tracks = json.loads((ROOT / 'data/canciones.json').read_text(encoding='utf-8'))
analytics = json.loads((ROOT / 'data/analytics.json').read_text(encoding='utf-8'))
token = analytics['token']

TEMPLATE = '''<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Abriendo {platform} | DejavuUrbe</title><link rel="stylesheet" href="{css}"><meta http-equiv="refresh" content="2;url={target_esc}"></head><body><main class="song-hero"><div class="wrap"><div class="eyebrow">DejavuUrbe</div><h1>Abriendo {platform}</h1><p class="lead">Te estamos llevando al enlace oficial.</p><p><a class="btn btn-primary" href="{target_esc}">Continuar ahora</a></p></div></main><!-- Cloudflare Web Analytics --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"{token}"}}'></script><!-- End Cloudflare Web Analytics --><script>window.addEventListener('load',()=>setTimeout(()=>location.replace({target_js}),350));</script></body></html>'''

def write_redirect(path: Path, platform: str, target: str, css: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = TEMPLATE.format(platform=platform, target_esc=html.escape(target, quote=True), target_js=json.dumps(target), token=token, css=css)
    path.write_text(text, encoding='utf-8')

# Rutas globales.
write_redirect(ROOT/'salir/bandcamp/index.html','Bandcamp','https://dejavuurbe.bandcamp.com/','../../assets/css/styles.css')
write_redirect(ROOT/'salir/youtube/index.html','YouTube','https://www.youtube.com/@DejavuUrbe','../../assets/css/styles.css')

# Una ruta de salida por tema hacia Bandcamp para poder medir intención de escucha por canción.
for t in tracks:
    slug = t['slug']
    target = t['bandcamp']
    write_redirect(ROOT/f'salir/bandcamp/{slug}/index.html','Bandcamp',target,'../../../assets/css/styles.css')

    page = ROOT / f'musica/{slug}/index.html'
    if page.exists():
        text = page.read_text(encoding='utf-8')
        direct = re.escape(target)
        local = f'../../salir/bandcamp/{slug}/'
        text2 = re.sub(r'(<a[^>]+href=")'+direct+r'("[^>]*>Escuchar en Bandcamp</a>)', r'\1'+local+r'\2', text, count=1)
        if text2 != text:
            page.write_text(text2, encoding='utf-8')

print('Rutas de salida generadas y enlaces de escucha preparados.')
