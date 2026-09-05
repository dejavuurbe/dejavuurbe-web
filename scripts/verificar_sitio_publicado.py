#!/usr/bin/env python3
"""Audita el dominio publicado: páginas, metadatos, recursos técnicos y 404."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://dejavuurbe.com.ar/"
HEADERS = {"User-Agent": "DejavuUrbe-SiteCheck/1.0 (+https://dejavuurbe.com.ar/)"}


def request(url: str, attempts: int = 3) -> tuple[int, str, str, bytes]:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.status, response.geturl(), response.headers.get("Content-Type", ""), response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read()
            if exc.code < 500 and exc.code != 429:
                return exc.code, exc.geturl(), exc.headers.get("Content-Type", ""), body
            last = exc
        except (OSError, urllib.error.URLError) as exc:
            last = exc
        if attempt + 1 < attempts:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: sin respuesta utilizable tras {attempts} intentos: {last}")


def assert_html(url: str) -> None:
    status, final_url, content_type, body = request(url)
    assert status == 200, f"{url}: HTTP {status}"
    assert "text/html" in content_type.lower(), f"{url}: Content-Type {content_type}"
    text = body.decode("utf-8")
    canonicals = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', text, flags=re.I)
    if not canonicals:
        canonicals = re.findall(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', text, flags=re.I)
    assert canonicals == [url], f"{url}: canonical inesperado {canonicals}"
    blocks = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, flags=re.I | re.S)
    assert blocks, f"{url}: falta JSON-LD"
    for block in blocks:
        json.loads(block)
    assert urlsplit(final_url).netloc == "dejavuurbe.com.ar", f"{url}: redirección inesperada a {final_url}"
    print(f"OK página {url}")


def main() -> int:
    local_tree = ET.parse(ROOT / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text.strip() for node in local_tree.findall("sm:url/sm:loc", namespace) if node.text]
    assert urls and len(urls) == len(set(urls)), "sitemap.xml local vacío o con URLs duplicadas"

    status, _, content_type, remote_sitemap = request(urljoin(BASE, "sitemap.xml"))
    assert status == 200 and "xml" in content_type.lower(), f"sitemap publicado inválido: HTTP {status}, {content_type}"
    remote_root = ET.fromstring(remote_sitemap)
    remote_urls = [node.text.strip() for node in remote_root.findall("sm:url/sm:loc", namespace) if node.text]
    assert remote_urls == urls, "el sitemap publicado no coincide con el repositorio"
    assert b"<lastmod>2026-09-05</lastmod>" in remote_sitemap, "el sitemap publicado aún no contiene la actualización del 2026-09-05"
    print(f"OK sitemap publicado: {len(urls)} URLs")

    for url in urls:
        assert_html(url)

    technical = {
        "robots.txt": "text/plain",
        "llms.txt": "text/plain",
        "data/identity.json": "json",
        "data/canciones.json": "json",
        "data/entity.jsonld": "json",
        "site.webmanifest": "json",
    }
    for path, kind in technical.items():
        url = urljoin(BASE, path)
        status, _, content_type, body = request(url)
        assert status == 200, f"{url}: HTTP {status}"
        if kind == "json":
            json.loads(body.decode("utf-8"))
        else:
            text = body.decode("utf-8")
            if path == "robots.txt":
                assert urljoin(BASE, "sitemap.xml") in text, "robots.txt no declara el sitemap"
            if path == "llms.txt":
                assert "# DejavuUrbe" in text, "llms.txt no identifica a DejavuUrbe"
        print(f"OK recurso {url} ({content_type})")

    key = "c6383b912d2d4c1697d3a14b7f5bd933"
    key_url = urljoin(BASE, f"{key}.txt")
    status, _, _, body = request(key_url)
    assert status == 200 and body.decode("utf-8").strip() == key, "clave pública de IndexNow inválida"
    print(f"OK clave IndexNow {key_url}")

    status, final_url, _, _ = request("https://www.dejavuurbe.com.ar/")
    assert status == 200 and final_url == BASE, f"www no redirige al dominio canónico: {final_url}"
    print("OK redirección www → dominio canónico")

    missing = urljoin(BASE, "comprobacion-404-dejavuurbe/")
    status, _, _, body = request(missing)
    assert status == 404, f"la URL inexistente respondió HTTP {status}"
    assert "Página no encontrada" in body.decode("utf-8"), "la página 404 personalizada no se mostró"
    print("OK respuesta 404 personalizada")
    print("OK: auditoría del sitio publicado completada")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, RuntimeError, ValueError, json.JSONDecodeError, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

