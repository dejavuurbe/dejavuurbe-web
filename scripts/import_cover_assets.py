#!/usr/bin/env python3
"""Reconstruye las portadas WebP desde fragmentos base64 temporales.

Los fragmentos se guardan como texto para permitir una importación controlada desde
herramientas que no adjuntan binarios directamente al repositorio. Tras extraer las
10 portadas, elimina los fragmentos para que no queden publicados.
"""
from pathlib import Path
from io import BytesIO
import base64
import zipfile

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "assets" / "import"
COVERS_DIR = ROOT / "assets" / "covers"
EXPECTED = {
    "ya-no-puedo-evitarte.webp",
    "cada-noche.webp",
    "balada-para-un-corto-amor.webp",
    "dos-extranos.webp",
    "brilla.webp",
    "el-fantasma.webp",
    "triste-cancion.webp",
    "luna.webp",
    "despiertame.webp",
    "luna-acustico.webp",
}

parts = sorted(IMPORT_DIR.glob("covers.b64.*"))
if len(parts) != 5:
    raise SystemExit(f"Se esperaban 5 fragmentos y se encontraron {len(parts)}")

payload = "".join(p.read_text(encoding="utf-8").strip() for p in parts)
try:
    archive = base64.b64decode(payload, validate=True)
except Exception as exc:
    raise SystemExit(f"Base64 inválido: {exc}")

COVERS_DIR.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(BytesIO(archive)) as zf:
    names = {Path(name).name for name in zf.namelist() if not name.endswith("/")}
    if names != EXPECTED:
        raise SystemExit(f"Contenido inesperado del ZIP: {sorted(names)}")
    for info in zf.infolist():
        if info.is_dir():
            continue
        name = Path(info.filename).name
        target = COVERS_DIR / name
        target.write_bytes(zf.read(info))

for path in parts:
    path.unlink()

files = {p.name for p in COVERS_DIR.glob("*.webp")}
if not EXPECTED.issubset(files):
    raise SystemExit("No quedaron disponibles las diez portadas esperadas")

print("OK: 10 portadas oficiales integradas en assets/covers y fragmentos temporales eliminados.")
