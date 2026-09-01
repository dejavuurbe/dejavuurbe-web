from pathlib import Path

TOKEN = "9f7d5a440c87436b81c64afc1b21c708"
SNIPPET = f"<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{\"token\": \"{TOKEN}\"}}'></script><!-- End Cloudflare Web Analytics -->"

changed = 0
for path in Path('.').rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    if 'static.cloudflareinsights.com/beacon.min.js' in text:
        continue
    if '</body>' not in text:
        raise SystemExit(f'No se encontró </body> en {path}')
    text = text.replace('</body>', SNIPPET + '\n</body>')
    path.write_text(text, encoding='utf-8')
    changed += 1

print(f'Cloudflare Web Analytics: {changed} archivo(s) actualizado(s).')
