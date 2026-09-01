from pathlib import Path

p = Path('index.html')
text = p.read_text(encoding='utf-8')
old = '''<section id="banda"><div class="wrap intro-grid"><div><div class="eyebrow">La banda</div><h2>Una historia que volvió a ponerse en movimiento.</h2><p>DejavuUrbe nació alrededor de canciones propias, ensayos y escenarios. En 2002 ese repertorio tomó forma en un disco físico; años después, las canciones siguieron ahí, esperando otro momento.</p><p>Ese momento llegó en 2025. La banda volvió a reunirse, recuperó su repertorio y comenzó una etapa nueva: presentaciones, material audiovisual y diez canciones publicadas nuevamente en 2026.</p><div class="actions"><a class="btn" href="banda/">Leer la historia</a></div></div><div class="timeline" id="historia"><div><strong>2002</strong>Las canciones toman forma en el disco <em>Dejavu urbe</em>.</div><div><strong>2025</strong>La banda vuelve a encontrarse y a tocar.</div><div><strong>2026</strong>Diez canciones regresan al presente.</div></div></div></section>'''
new = '''<section id="banda"><div class="wrap"><div class="eyebrow">La banda</div><h2>Una historia que volvió a ponerse en movimiento.</h2><p class="lead">DejavuUrbe nació en 1999 alrededor de canciones propias, tuvo una primera etapa a comienzos de los 2000 y volvió a reunirse en 2025 para retomar su repertorio desde el presente y seguir creando música nueva.</p><div class="actions"><a class="btn" href="banda/">Conocer la historia</a></div></div></section>'''
if old not in text:
    raise SystemExit('No se encontró el bloque histórico esperado; no se realizaron cambios.')
p.write_text(text.replace(old, new, 1), encoding='utf-8')
print('Historia de portada compactada correctamente.')
