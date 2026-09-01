from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if 'desktop-tuning.css' in text:
        continue
    rel_depth = len(path.relative_to(ROOT).parts) - 1
    prefix = '../' * rel_depth
    target = f'<link rel="stylesheet" href="{prefix}assets/css/styles.css">'
    addition = target + f'<link rel="stylesheet" href="{prefix}assets/css/desktop-tuning.css">'
    if target in text:
        path.write_text(text.replace(target, addition, 1), encoding='utf-8')
        print(f'Actualizado: {path.relative_to(ROOT)}')
