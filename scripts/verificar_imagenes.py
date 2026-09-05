#!/usr/bin/env python3
"""Comprueba que cada imagen usada por HTML existe y coincide con su MIME/extensión."""

from __future__ import annotations

import base64
import hashlib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MIME_BY_EXT = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".avif": "image/avif",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
}


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        source = dict(attrs).get("src")
        if source:
            self.sources.append(source.strip())


def identify(data: bytes) -> str | None:
    stripped = data.lstrip()
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if len(data) >= 16 and data[4:8] == b"ftyp" and data[8:12] in {b"avif", b"avis", b"mif1"}:
        return "image/avif"
    if stripped.startswith(b"<svg") or (stripped.startswith(b"<?xml") and b"<svg" in stripped[:1024]):
        return "image/svg+xml"
    return None


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    i = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        if i + 2 > len(data):
            break
        length = int.from_bytes(data[i:i + 2], "big")
        if length < 2 or i + length > len(data):
            return None
        if marker in sof and length >= 7:
            height = int.from_bytes(data[i + 3:i + 5], "big")
            width = int.from_bytes(data[i + 5:i + 7], "big")
            return width, height
        i += length
    return None


def dimensions(data: bytes, mime: str) -> tuple[int, int] | None:
    if mime == "image/jpeg":
        return jpeg_dimensions(data)
    if mime == "image/png" and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if mime == "image/gif" and len(data) >= 10:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    if mime == "image/webp" and len(data) >= 30:
        chunk = data[12:16]
        if chunk == b"VP8X":
            return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if chunk == b"VP8 " and data[23:26] == b"\x9d\x01\x2a":
            return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(data[28:30], "little") & 0x3FFF
        if chunk == b"VP8L" and data[20] == 0x2F:
            bits = int.from_bytes(data[21:25], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if mime == "image/avif":
        pos = data.find(b"ispe")
        if pos >= 0 and pos + 16 <= len(data):
            return int.from_bytes(data[pos + 8:pos + 12], "big"), int.from_bytes(data[pos + 12:pos + 16], "big")
    if mime == "image/svg+xml":
        return 1, 1
    return None


def inspect_image(label: str, data: bytes, expected_mime: str) -> str:
    actual = identify(data)
    if actual != expected_mime:
        raise ValueError(f"{label}: se esperaba {expected_mime}, contenido real {actual or 'desconocido'}")
    size = dimensions(data, actual)
    if not size or size[0] <= 0 or size[1] <= 0:
        raise ValueError(f"{label}: no se pudieron validar dimensiones positivas")
    digest = hashlib.sha256(data).hexdigest()[:12]
    return f"{label}: {actual}, {size[0]}x{size[1]}, sha256={digest}"


def decode_data_uri(source: str) -> tuple[str, bytes]:
    match = re.fullmatch(r"data:([^;,]+)(;base64)?,(.*)", source, flags=re.DOTALL)
    if not match:
        raise ValueError("data URI inválido")
    mime, encoded, payload = match.groups()
    if encoded:
        return mime.lower(), base64.b64decode(payload, validate=True)
    return mime.lower(), unquote(payload).encode("latin-1")


def main() -> int:
    errors: list[str] = []
    checked: dict[str, str] = {}
    html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    for html_file in html_files:
        parser = ImageParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for source in parser.sources:
            if source.startswith("data:"):
                key = f"{html_file.relative_to(ROOT)}:data:{hashlib.sha256(source.encode()).hexdigest()[:12]}"
                if key in checked:
                    continue
                try:
                    mime, data = decode_data_uri(source)
                    checked[key] = inspect_image(key, data, mime)
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{key}: {exc}")
                continue
            parsed = urlparse(source)
            if parsed.scheme or parsed.netloc:
                continue
            relative = unquote(parsed.path)
            candidate = (ROOT / relative.lstrip("/")) if relative.startswith("/") else (html_file.parent / relative)
            try:
                path = candidate.resolve()
                path.relative_to(ROOT)
            except ValueError:
                errors.append(f"{html_file.relative_to(ROOT)}: ruta fuera del repositorio: {source}")
                continue
            key = path.relative_to(ROOT).as_posix()
            if key in checked:
                continue
            if not path.is_file():
                errors.append(f"{key}: archivo inexistente (referido desde {html_file.relative_to(ROOT)})")
                continue
            expected = MIME_BY_EXT.get(path.suffix.lower())
            if not expected:
                errors.append(f"{key}: extensión de imagen no admitida")
                continue
            try:
                checked[key] = inspect_image(key, path.read_bytes(), expected)
            except Exception as exc:  # noqa: BLE001
                errors.append(str(exc))

    for line in checked.values():
        print(f"OK {line}")
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(checked)} imágenes únicas verificadas en {len(html_files)} páginas HTML")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

