from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
songs = json.loads((ROOT / 'data/canciones.json').read_text(encoding='utf-8'))

for song in songs:
    path = ROOT / 'musica' / song['slug'] / 'index.html'
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    old = f'href="../../salir/bandcamp/{song["slug"]}/"'
    new = f'href="{song["bandcamp"]}"'
    if old in text:
        path.write_text(text.replace(old, new), encoding='utf-8')
        print(f'Actualizado: {path.relative_to(ROOT)}')
    else:
        print(f'Sin cambio: {path.relative_to(ROOT)}')
