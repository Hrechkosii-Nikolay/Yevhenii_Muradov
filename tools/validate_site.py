#!/usr/bin/env python3
"""Lightweight local checks for generated HTML and internal assets."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.title = False
        self.lang = ""
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang", "")
        if tag == "title":
            self.title = True
        if tag == "h1":
            self.h1 += 1
        attribute = {"a": "href", "img": "src", "script": "src", "link": "href"}.get(tag)
        if attribute and data.get(attribute):
            self.links.append(data[attribute])


def local_target(url):
    path = urlsplit(url).path
    if not path or path.startswith("//"):
        return None
    candidate = ROOT / path.lstrip("/")
    if path.endswith("/"):
        candidate /= "index.html"
    return candidate


def main():
    failures = []
    pages = [ROOT / "index.html", *sorted((ROOT / "uk").rglob("*.html")), *sorted((ROOT / "en").rglob("*.html"))]
    for page in pages:
        parser = Inspector()
        parser.feed(page.read_text(encoding="utf-8"))
        if not parser.title:
            failures.append(f"Missing title: {page.relative_to(ROOT)}")
        if not parser.lang:
            failures.append(f"Missing lang: {page.relative_to(ROOT)}")
        if page.name != "404.html" and parser.h1 != 1:
            failures.append(f"Expected one H1 ({parser.h1}): {page.relative_to(ROOT)}")
        for url in parser.links:
            if url.startswith(("#", "mailto:", "tel:", "https://", "http://")):
                continue
            target = local_target(url)
            if target is not None and not target.exists():
                failures.append(f"Broken {url} in {page.relative_to(ROOT)}")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"Validated {len(pages)} HTML pages: metadata and local links OK")


if __name__ == "__main__":
    main()
