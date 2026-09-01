from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = 'Escuchar en Bandcamp'
NEW = 'Escuchar canción'

changed = 0
for path in sorted((ROOT / 'musica').glob('*/index.html')):
    text = path.read_text(encoding='utf-8')
    if OLD not in text:
        continue
    text = text.replace(OLD, NEW)
    path.write_text(text, encoding='utf-8')
    changed += 1
    print(path.relative_to(ROOT))

print(f'Páginas actualizadas: {changed}')
