from pathlib import Path
import json
from datetime import datetime
from html import escape

ROOT = Path(__file__).resolve().parents[1]
SONGS = json.loads((ROOT / 'data/canciones.json').read_text(encoding='utf-8'))
SITE = json.loads((ROOT / 'data/site.json').read_text(encoding='utf-8'))
BASE = SITE['public_base'].rstrip('/')
TOKEN = '9f7d5a440c87436b81c64afc1b21c708'

TEXTOS = {
    'ya-no-puedo-evitarte': 'Una canción de rock en español construida sobre un conflicto directo, una frase central contundente y una ejecución de banda.',
    'balada-para-un-corto-amor': 'La faceta más melódica del repertorio: una balada rock sostenida por la canción, la emoción y el trabajo de banda.',
    'despiertame': 'Una canción atravesada por pérdida, recuerdo y la necesidad de salir de un estado emocional que se vuelve irreal.'
}

def fecha_humana(value):
    d = datetime.strptime(value, '%Y-%m-%d')
    meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    return f'{d.day} de {meses[d.month-1]} de {d.year}'

def page(song):
    title = escape(song['titulo'])
    slug = song['slug']
    canonical = f'{BASE}/musica/{slug}/'
    description = TEXTOS.get(slug, f'{title}, canción de DejavuUrbe publicada en 2026. Escuchá el tema y consultá información oficial de la grabación.')
    schema = {
        '@context':'https://schema.org','@type':'MusicRecording','name':song['titulo'],
        'byArtist':{'@type':'MusicGroup','name':'DejavuUrbe','url':f'{BASE}/'},
        'datePublished':song['fecha'],'isrcCode':song['isrc'],'url':canonical,
        'sameAs':[song['bandcamp'],song['musicbrainz_recording']]
    }
    schema_json = json.dumps(schema, ensure_ascii=False, separators=(',',':'))
    return f'''<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} — DejavuUrbe | Canción oficial</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="../../assets/css/styles.css"><meta property="og:type" content="music.song"><meta property="og:title" content="{title} — DejavuUrbe"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{canonical}"><script type="application/ld+json">{schema_json}</script></head><body><header class="site-header"><div class="wrap nav"><a class="brand" href="../../">DEJAVUURBE</a><nav class="nav-links"><a href="../../banda/">Banda</a><a href="../../musica/">Música</a><a href="../../videos/">Videos</a><a href="../../enlaces/">Enlaces</a></nav></div></header><main><section class="song-hero song-hero-human"><div class="wrap"><div class="breadcrumb"><a href="../../">Inicio</a> / <a href="../">Música</a></div><div class="eyebrow">DejavuUrbe · 2026</div><h1>{title}</h1><p class="lead">{escape(description)}</p><div class="actions"><a class="btn btn-primary" href="../../salir/bandcamp/{slug}/">Escuchar en Bandcamp</a><a class="btn" href="../">Ver más canciones</a></div></div></section><section><div class="wrap song-layout song-human-layout"><div class="prose"><div class="eyebrow">La canción</div><h2>{title}</h2><p>Forma parte del repertorio publicado por DejavuUrbe en 2026 y de la etapa actual de la banda.</p><p class="technical-note">Los identificadores y enlaces de referencia se mantienen disponibles para documentación, buscadores e información musical.</p></div><aside class="data-card technical-card"><div class="eyebrow">Datos de la grabación</div><div class="data-row"><span>Artista</span><strong>DejavuUrbe</strong></div><div class="data-row"><span>Publicación</span><strong>{fecha_humana(song['fecha'])}</strong></div><div class="data-row"><span>ISRC</span><strong>{song['isrc']}</strong></div><div class="data-row"><span>UPC</span><strong>{song['upc']}</strong></div><div class="data-row"><span>Fonograma</span><strong>℗ 2026 DejavuUrbe</strong></div><div class="song-nav"><a href="{song['musicbrainz_release']}">MusicBrainz · lanzamiento</a><a href="{song['musicbrainz_recording']}">MusicBrainz · grabación</a></div></aside></div></section></main><footer class="footer"><div class="wrap"><strong>DEJAVUURBE</strong><br>Rock argentino · Buenos Aires</div></footer><!-- Cloudflare Web Analytics --><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token":"{TOKEN}"}}'></script><!-- End Cloudflare Web Analytics --></body></html>'''

for song in SONGS:
    out = ROOT / 'musica' / song['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(song), encoding='utf-8')
    print(out.relative_to(ROOT))
