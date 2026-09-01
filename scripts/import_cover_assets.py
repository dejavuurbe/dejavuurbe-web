#!/usr/bin/env python3
"""Reconstruye las portadas WebP desde fragmentos base64 temporales.

Tolera cortes arbitrarios entre fragmentos: concatena el flujo, elimina padding
intermedio y vuelve a aplicar padding únicamente al final antes de decodificar.
Tras extraer las 10 portadas, elimina los fragmentos temporales.
"""
from pathlib import Path
from io import BytesIO
import base64
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
IMPORT_DIR = ROOT / "assets" / "import"
COVERS_DIR = ROOT / "assets" / "covers"
EXPECTED = {
    "ya-no-puedo-evitarte.webp", "cada-noche.webp",
    "balada-para-un-corto-amor.webp", "dos-extranos.webp",
    "brilla.webp", "el-fantasma.webp", "triste-cancion.webp",
    "luna.webp", "despiertame.webp", "luna-acustico.webp",
}

parts = sorted(IMPORT_DIR.glob("covers.b64.*"))
if len(parts) != 5:
    raise SystemExit(f"Se esperaban 5 fragmentos y se encontraron {len(parts)}")

raw = "".join(p.read_text(encoding="utf-8") for p in parts)
raw = re.sub(r"\s+", "", raw)
# El material temporal pudo quedar cortado en unidades no múltiplo de cuatro.
# Se retira padding intermedio y se reconstruye un único flujo base64.
raw = raw.replace("=", "")
raw += "=" * ((4 - len(raw) % 4) % 4)
try:
    archive = base64.b64decode(raw, validate=True)
except Exception as exc:
    raise SystemExit(f"No se pudo reconstruir el flujo base64: {exc}")

COVERS_DIR.mkdir(parents=True, exist_ok=True)
try:
    with zipfile.ZipFile(BytesIO(archive)) as zf:
        names = {Path(name).name for name in zf.namelist() if not name.endswith("/")}
        if names != EXPECTED:
            raise SystemExit(f"Contenido inesperado del ZIP: {sorted(names)}")
        for info in zf.infolist():
            if not info.is_dir():
                (COVERS_DIR / Path(info.filename).name).write_bytes(zf.read(info))
except zipfile.BadZipFile as exc:
    raise SystemExit(f"No se pudo reconstruir el ZIP de portadas: {exc}")

for path in parts:
    path.unlink()

files = {p.name for p in COVERS_DIR.glob("*.webp")}
if not EXPECTED.issubset(files):
    raise SystemExit("No quedaron disponibles las diez portadas esperadas")

print("OK: 10 portadas oficiales integradas en assets/covers y fragmentos temporales eliminados.")
