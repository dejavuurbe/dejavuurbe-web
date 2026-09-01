#!/usr/bin/env python3
"""Verifica que data/canciones.json y las páginas públicas del catálogo estén sincronizadas.

No modifica archivos. Está pensado para GitHub Actions y mantenimiento automatizado.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "canciones.json"
SITE = ROOT / "data" / "site.json"


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(1)


def main() -> None:
    try:
        songs = json.loads(DATA.read_text(encoding="utf-8"))
        site = json.loads(SITE.read_text(encoding="utf-8"))
        base = site["public_base"].rstrip("/")
    except Exception as exc:
        fail(f"No se pudieron leer los datos del sitio: {exc}")

    if len(songs) != 10:
        fail(f"Se esperaban 10 canciones y hay {len(songs)}")

    seen_slugs = set()
    seen_isrc = set()
    seen_upc = set()
    required = {"titulo", "slug", "fecha", "upc", "isrc", "bandcamp", "musicbrainz_release", "musicbrainz_recording", "cover_file", "cover_alt"}

    for song in songs:
        missing = required - set(song)
        if missing:
            fail(f"Faltan campos en {song.get('titulo', '<sin título>')}: {sorted(missing)}")

        slug = song["slug"]
        if slug in seen_slugs:
            fail(f"Slug duplicado: {slug}")
        if song["isrc"] in seen_isrc:
            fail(f"ISRC duplicado: {song['isrc']}")
        if song["upc"] in seen_upc:
            fail(f"UPC duplicado: {song['upc']}")
        if not song["cover_file"].endswith(".webp"):
            fail(f"La portada de {song['titulo']} debe mapear a WebP")
        seen_slugs.add(slug)
        seen_isrc.add(song["isrc"])
        seen_upc.add(song["upc"])

        page = ROOT / "musica" / slug / "index.html"
        if not page.exists():
            fail(f"Falta la página {page.relative_to(ROOT)}")
        text = page.read_text(encoding="utf-8")
        checks = [
            song["titulo"], song["isrc"], song["upc"],
            f"{base}/musica/{slug}/",
            '"@type":"MusicRecording"',
            song["bandcamp"], song["musicbrainz_recording"],
        ]
        for value in checks:
            if value not in text:
                fail(f"{page.relative_to(ROOT)} no contiene: {value}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for song in songs:
        url = f"{base}/musica/{song['slug']}/"
        if url not in sitemap:
            fail(f"El sitemap no contiene {url}")

    print(f"OK: catálogo, páginas, sitemap y mapeo visual sincronizados con {base}.")


if __name__ == "__main__":
    main()
