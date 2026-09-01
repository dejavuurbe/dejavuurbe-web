#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
index = root / 'index.html'
css = root / 'assets/css/styles.css'

html = index.read_text(encoding='utf-8')
old = '<section class="hero" id="inicio"><div class="wrap hero-content"><div class="eyebrow">Rock argentino · Buenos Aires</div><h1>DEJAVU<span>URBE</span></h1><p class="lead">Canciones que atravesaron años, escenarios y silencios. DejavuUrbe volvió a encontrarse para hacerlas sonar otra vez y abrir una nueva etapa.</p><div class="actions"><a class="btn btn-primary" href="musica/">Escuchar música</a><a class="btn" href="banda/">Conocer la historia</a></div></div></section>'
new = '''<section class="hero" id="inicio"><div class="wrap hero-stage"><div class="hero-content"><div class="eyebrow">Rock argentino · Buenos Aires</div><h1>DEJAVU<span>URBE</span></h1><p class="lead">Canciones que atravesaron años, escenarios y silencios. DejavuUrbe volvió a encontrarse para hacerlas sonar otra vez y abrir una nueva etapa.</p><div class="actions"><a class="btn btn-primary" href="musica/">Escuchar música</a><a class="btn" href="banda/">Conocer la historia</a></div></div><div class="hero-covers" aria-label="Lanzamientos de DejavuUrbe"><a class="hero-cover hero-cover-main" href="musica/despiertame/"><img src="assets/covers/despiertame.webp" alt="Portada de Despiértame de DejavuUrbe" width="600" height="600" fetchpriority="high"></a><a class="hero-cover hero-cover-left" href="musica/balada-para-un-corto-amor/"><img src="assets/covers/balada-para-un-corto-amor.webp" alt="Portada de Balada para un corto amor de DejavuUrbe" width="600" height="600"></a><a class="hero-cover hero-cover-right" href="musica/luna.webp" aria-hidden="true" tabindex="-1"></a><a class="hero-cover hero-cover-right" href="musica/luna/"><img src="assets/covers/luna.webp" alt="Portada de Luna de DejavuUrbe" width="600" height="600"></a></div></div></section>'''
# Remove an accidental placeholder if this script was used from an older draft.
new = new.replace('<a class="hero-cover hero-cover-right" href="musica/luna.webp" aria-hidden="true" tabindex="-1"></a>', '')

if 'class="wrap hero-stage"' not in html:
    if old not in html:
        raise SystemExit('No se encontró el hero esperado; no se modifica el archivo.')
    html = html.replace(old, new, 1)
    index.write_text(html, encoding='utf-8')

styles = css.read_text(encoding='utf-8')
marker = '/* hero-cover-montage-v1 */'
if marker not in styles:
    styles += '''\n/* hero-cover-montage-v1 */
.hero-stage{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1fr) minmax(390px,.78fr);align-items:center;gap:52px;min-height:82vh;padding:82px 0}.hero-stage .hero-content{padding:0;max-width:680px}.hero-covers{position:relative;min-height:560px;perspective:1100px;filter:drop-shadow(0 30px 42px rgba(0,0,0,.52))}.hero-cover{position:absolute;display:block;width:min(63%,360px);aspect-ratio:1;border:1px solid rgba(255,255,255,.16);background:#111;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.58);transition:transform .28s ease,border-color .28s ease,filter .28s ease}.hero-cover img{width:100%;height:100%;object-fit:cover}.hero-cover-main{z-index:3;right:8%;top:12%;transform:rotate(1.5deg)}.hero-cover-left{z-index:2;left:0;top:27%;transform:rotate(-8deg) scale(.87);filter:brightness(.72)}.hero-cover-right{z-index:1;right:-9%;top:31%;transform:rotate(8deg) scale(.84);filter:brightness(.67)}.hero-cover:hover,.hero-cover:focus-visible{z-index:5;border-color:var(--fire);filter:brightness(1);transform:rotate(0) scale(1.035)}.hero-covers:after{content:"CATÁLOGO 2026";position:absolute;right:2%;bottom:8%;z-index:6;font-size:.72rem;font-weight:900;letter-spacing:.24em;color:#ff8a5f;background:rgba(8,8,8,.8);border-left:3px solid var(--fire);padding:8px 10px}.hero .wrap{max-width:var(--max)}
@media(max-width:1000px){.hero-stage{grid-template-columns:minmax(0,1fr) 340px;gap:20px;min-height:72vh}.hero-covers{min-height:430px}.hero-cover{width:265px}.hero-cover-main{right:4%}.hero-cover-left{left:0}.hero-cover-right{right:-8%}}
@media(max-width:760px){.hero-stage{display:block;min-height:auto;padding:72px 0 52px}.hero-stage .hero-content{max-width:650px}.hero-covers{min-height:330px;margin-top:34px;width:min(100%,520px)}.hero-cover{width:220px}.hero-cover-main{right:20%;top:0}.hero-cover-left{left:1%;top:55px}.hero-cover-right{right:0;top:70px}.hero-covers:after{bottom:2%;right:0}}
@media(max-width:480px){.hero-covers{min-height:270px}.hero-cover{width:175px}.hero-cover-main{right:17%}.hero-cover-left{left:0;top:48px}.hero-cover-right{right:-2%;top:58px}.hero-covers:after{font-size:.62rem;letter-spacing:.16em}}
@media(prefers-reduced-motion:reduce){.hero-cover{transition:none}.hero-cover:hover,.hero-cover:focus-visible{transform:none}}
'''
    css.write_text(styles, encoding='utf-8')

print('OK: hero visual enriquecido con portadas oficiales.')
