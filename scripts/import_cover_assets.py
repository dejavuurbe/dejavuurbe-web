#!/usr/bin/env python3
"""Reconstruye las portadas WebP desde fragmentos base64 temporales.

Los fragmentos se guardan como texto para permitir una importación controlada desde
herramientas que no adjuntan binarios directamente al repositorio. Cada fragmento
puede ser una unidad base64 independiente; se decodifican por separado y luego se
rearma el ZIP binario. Tras extraer las 10 portadas, elimina los fragmentos.
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

chunks = []
for part in parts:
    payload = part.read_text(encoding="utf-8").strip()
    try:
        chunks.append(base64.b64decode(payload, validate=True))
    except Exception as exc:
        raise SystemExit(f"Base64 inválido en {part.name}: {exc}")
archive = b"".join(chunks)

COVERS_DIR.mkdir(parents=True, exist_ok=True)
try:
    with zipfile.ZipFile(BytesIO(archive)) as zf:
        names = {Path(name).name for name in zf.namelist() if not name.endswith("/")}
        if names != EXPECTED:
            raise SystemExit(f"Contenido inesperado del ZIP: {sorted(names)}")
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = Path(info.filename).name
            (COVERS_DIR / name).write_bytes(zf.read(info))
except zipfile.BadZipFile as exc:
    raise SystemExit(f"No se pudo reconstruir el ZIP de portadas: {exc}")

for path in parts:
    path.unlink()

files = {p.name for p in COVERS_DIR.glob("*.webp")}
if not EXPECTED.issubset(files):
    raise SystemExit("No quedaron disponibles las diez portadas esperadas")

print("OK: 10 portadas oficiales integradas en assets/covers y fragmentos temporales eliminados.")
