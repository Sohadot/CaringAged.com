#!/usr/bin/env python3
"""Static quality checks: HTML links, SEO boundaries and editorial safeguards."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "/": ROOT / "index.html",
    "/sources/": ROOT / "sources" / "index.html",
    "/acquire/": ROOT / "acquire" / "index.html",
}

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.h1 = 0
        self.canonical = []
        self.robots = []
        self.ld = []
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        if tag == "meta" and a.get("name") == "robots":
            self.robots.append(a.get("content", "").lower())
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_data(self, data):
        if self._in_ld:
            self.ld.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False

def verify():
    errors = []
    for page_url, filename in PAGES.items():
        if not filename.is_file():
            errors.append(f"Missing page: {filename}")
            continue
        html = filename.read_text(encoding="utf-8")
        doc = Document()
        doc.feed(html)
        if doc.h1 != 1:
            errors.append(f"{page_url}: expected one H1, found {doc.h1}")
        if len(doc.ids) != len(set(doc.ids)):
            errors.append(f"{page_url}: duplicate id")
        for href in doc.links:
            if not href:
                errors.append(f"{page_url}: empty link")
                continue
            parsed = urlparse(href)
            if parsed.scheme or href.startswith("mailto:"):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in doc.ids:
                    errors.append(f"{page_url}: missing fragment {href}")
                continue
            path = parsed.path
            if path.startswith("/"):
                if path not in PAGES:
                    errors.append(f"{page_url}: unrecognised internal path {href}")
                elif parsed.fragment:
                    target = Document()
                    target.feed(PAGES[path].read_text(encoding="utf-8"))
                    if parsed.fragment not in target.ids:
                        errors.append(f"{page_url}: missing target {href}")
        if page_url == "/acquire/":
            if not any("noindex" in x for x in doc.robots):
                errors.append("Acquisition page must be noindex")
        else:
            expected = "https://caringaged.com" + page_url
            if expected not in doc.canonical:
                errors.append(f"{page_url}: canonical missing or mismatched")
            if any("noindex" in x for x in doc.robots):
                errors.append(f"{page_url}: public page marked noindex")
        for raw in doc.ld:
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{page_url}: invalid JSON-LD: {exc}")
    sitemap = ET.parse(ROOT / "sitemap.xml")
    locs = [x.text for x in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if set(locs) != {"https://caringaged.com/", "https://caringaged.com/sources/"}:
        errors.append(f"Sitemap scope incorrect: {locs}")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://caringaged.com/sitemap.xml" not in robots:
        errors.append("robots.txt needs sitemap declaration")
    if "noindex" not in (ROOT / "acquire" / "index.html").read_text(encoding="utf-8"):
        errors.append("Noindex marker missing")
    for page in ("index.html", "sources/index.html"):
        txt = (ROOT / page).read_text(encoding="utf-8")
        if "https://" not in txt:
            errors.append(f"Evidence URLs absent: {page}")
    if errors:
        print("QUALITY GATE FAILED")
        for error in errors:
            print(" -", error)
        raise SystemExit(1)
    print("QUALITY GATE PASSED: 3 pages, internal links, canonical URLs, JSON-LD, sitemap and acquisition noindex.")

if __name__ == "__main__":
    verify()
