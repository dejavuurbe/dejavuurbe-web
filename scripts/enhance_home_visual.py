#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
css = root / 'assets/css/styles.css'
styles = css.read_text(encoding='utf-8')

# Mantener el hero actual y reemplazar solo la capa visual del catálogo móvil.
styles = re.sub(r'\n?/\* music-cards-app-v1 \*/.*?/\* end-music-cards-app-v1 \*/\n?', '\n', styles, flags=re.S)
styles += r'''
/* music-cards-app-v1 */
@media(max-width:560px){
  .catalog-visual{
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:12px;
    width:88%;
    max-width:410px;
    margin-inline:auto;
  }
  .catalog-visual .track-card{
    min-width:0;
    padding:6px;
    overflow:hidden;
    border-radius:18px;
    border:1px solid rgba(255,106,42,.5);
    background:linear-gradient(180deg,#111 0%,#0a0a0a 100%);
    box-shadow:0 10px 24px rgba(0,0,0,.28);
  }
  .catalog-visual .track-card:before{display:none}
  .catalog-visual .track-card:after{display:none}
  .catalog-visual .track-cover{
    width:100%;
    height:auto!important;
    aspect-ratio:1/1!important;
    object-fit:cover!important;
    object-position:center!important;
    margin:0;
    border-radius:13px;
    background:#090909;
  }
  .catalog-visual .track-copy{
    padding:10px 6px 8px;
    background:transparent;
  }
  .catalog-visual .track-card small{
    display:block;
    margin:0 0 7px;
    font-size:.58rem;
    line-height:1.1;
    letter-spacing:.09em;
    color:#ff7a2f;
  }
  .catalog-visual .track-card h3{
    margin:0 0 4px;
    font-size:.92rem;
    line-height:1.12;
    color:#f5f5f5;
  }
  .catalog-visual .track-card p{
    margin:0;
    font-size:.69rem;
    line-height:1.2;
    color:#aaa;
  }
  .catalog-visual+.actions{margin-top:24px}
}
@media(max-width:480px){
  .catalog-visual{width:86%;gap:10px}
  .catalog-visual .track-card{border-radius:16px;padding:5px}
  .catalog-visual .track-cover{border-radius:12px}
  .catalog-visual .track-copy{padding:9px 5px 7px}
}
@media(max-width:360px){
  .catalog-visual{width:84%;gap:9px}
  .catalog-visual .track-card h3{font-size:.84rem}
  .catalog-visual .track-card p{font-size:.65rem}
}
/* end-music-cards-app-v1 */
'''
css.write_text(styles, encoding='utf-8')
print('OK: tarjetas musicales móviles redondeadas, cuadradas y con metadata visible.')
