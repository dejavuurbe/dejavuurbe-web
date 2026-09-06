#!/usr/bin/env python3
"""Audita indexación, metadatos y fuentes legibles por buscadores e IA.

No modifica archivos. Falla ante divergencias entre el sitemap, el catálogo,
los datos estructurados, llms.txt y las páginas públicas.
"""
from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://dejavuurbe.com.ar"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


class HeadAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.jsonld: list[str] = []
        self._jsonld = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = {str(k).lower(): str(v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._jsonld = True
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._jsonld:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._jsonld:
            self.jsonld.append("".join(self._buffer))
            self._jsonld = False


def meta_value(parser: HeadAudit, *, name: str = "", prop: str = "") -> str:
    for item in parser.meta:
        if name and item.get("name", "").lower() == name.lower():
            return item.get("content", "").strip()
        if prop and item.get("property", "").lower() == prop.lower():
            return item.get("content", "").strip()
    return ""


def local_page(url: str) -> Path:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "dejavuurbe.com.ar":
        fail(f"URL no canónica en sitemap: {url}")
    relative = parsed.path.strip("/")
    return ROOT / relative / "index.html" if relative else ROOT / "index.html"


def audit_page(url: str) -> None:
    page = local_page(url)
    if not page.is_file():
        fail(f"El sitemap apunta a un archivo inexistente: {page.relative_to(ROOT)}")
    raw = page.read_text(encoding="utf-8")
    parser = HeadAudit()
    parser.feed(raw)

    if 'lang="es-AR"' not in raw and "lang='es-AR'" not in raw:
        fail(f"{page.relative_to(ROOT)} no declara es-AR")
    if not parser.title.strip():
        fail(f"{page.relative_to(ROOT)} no tiene title")
    if not meta_value(parser, name="description"):
        fail(f"{page.relative_to(ROOT)} no tiene meta description")
    if not meta_value(parser, name="viewport"):
        fail(f"{page.relative_to(ROOT)} no tiene viewport")

    canonicals = [
        item.get("href", "").rstrip("/") + "/"
        for item in parser.links
        if item.get("rel", "").lower() == "canonical"
    ]
    expected = url.rstrip("/") + "/"
    if canonicals != [expected]:
        fail(f"Canonical incorrecta en {page.relative_to(ROOT)}: {canonicals!r}")

    robots = meta_value(parser, name="robots").lower()
    if "noindex" in robots:
        fail(f"Página pública marcada noindex: {page.relative_to(ROOT)}")

    for prop in ("og:title", "og:description", "og:url", "og:image"):
        if not meta_value(parser, prop=prop):
            fail(f"{page.relative_to(ROOT)} no tiene {prop}")

    for payload in parser.jsonld:
        try:
            json.loads(payload)
        except json.JSONDecodeError as exc:
            fail(f"JSON-LD inválido en {page.relative_to(ROOT)}: {exc}")


def main() -> None:
    site = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
    if site.get("public_base", "").rstrip("/") != BASE:
        fail("data/site.json no usa el dominio oficial")

    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    nodes = tree.findall("sm:url", ns)
    urls: list[str] = []
    for node in nodes:
        location = node.findtext("sm:loc", default="", namespaces=ns).strip()
        modified = node.findtext("sm:lastmod", default="", namespaces=ns).strip()
        if not location or not modified:
            fail("Todas las entradas del sitemap deben tener loc y lastmod")
        try:
            stamp = date.fromisoformat(modified)
        except ValueError:
            fail(f"lastmod inválido para {location}: {modified}")
        if stamp > date.today():
            fail(f"lastmod futuro para {location}: {modified}")
        urls.append(location)

    if len(urls) != len(set(urls)):
        fail("El sitemap contiene URLs duplicadas")

    songs = json.loads((ROOT / "data/canciones.json").read_text(encoding="utf-8"))
    expected_song_urls = {f"{BASE}/musica/{song['slug']}/" for song in songs}
    if not expected_song_urls.issubset(set(urls)):
        fail("El sitemap no contiene todas las páginas de canciones")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    entity = json.loads((ROOT / "data/entity.jsonld").read_text(encoding="utf-8"))
    if "DejavuUrbe" not in llms or BASE not in llms:
        fail("llms.txt no identifica claramente la fuente oficial")
    if not isinstance(entity, dict) or "@graph" not in entity:
        fail("data/entity.jsonld debe contener un @graph")

    serialized_entity = json.dumps(entity, ensure_ascii=False)
    for song in songs:
        for field in ("titulo", "isrc", "upc"):
            value = str(song[field])
            if value not in llms:
                fail(f"llms.txt no contiene {field}: {value}")
            if value not in serialized_entity:
                fail(f"entity.jsonld no contiene {field}: {value}")

    for url in urls:
        audit_page(url)

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://dejavuurbe.com.ar/sitemap.xml" not in robots:
        fail("robots.txt no anuncia el sitemap oficial")

    not_found = (ROOT / "404.html").read_text(encoding="utf-8").lower()
    if 'name="robots"' not in not_found or "noindex" not in not_found:
        fail("404.html debe declarar noindex")

    print(
        f"OK: {len(urls)} URLs públicas, {len(songs)} canciones, "
        "metadatos, sitemap, llms.txt y JSON-LD coherentes."
    )


if __name__ == "__main__":
    main()
