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
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang", "")
        if tag == "title":
            self.title = True
        if tag == "h1":
            self.h1 += 1
        if data.get("id"):
            self.ids.add(data["id"])
        attribute = {"a": "href", "img": "src", "script": "src", "link": "href"}.get(tag)
        if tag == "form":
            attribute = "action"
        if tag == "meta" and data.get("property") == "og:image":
            attribute = "content"
        if attribute and data.get(attribute):
            self.links.append(data[attribute])


def local_target(url, page):
    path = urlsplit(url).path
    if not path or path.startswith("//"):
        return None
    candidate = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    if path.endswith("/"):
        candidate /= "index.html"
    return candidate.resolve()


def main():
    failures = []
    pages = [ROOT / "index.html", *sorted((ROOT / "uk").rglob("*.html")), *sorted((ROOT / "en").rglob("*.html"))]
    inspections = {}
    for page in pages:
        parser = Inspector()
        parser.feed(page.read_text(encoding="utf-8"))
        inspections[page.resolve()] = parser
        if not parser.title:
            failures.append(f"Missing title: {page.relative_to(ROOT)}")
        if not parser.lang:
            failures.append(f"Missing lang: {page.relative_to(ROOT)}")
        if page.name != "404.html" and parser.h1 != 1:
            failures.append(f"Expected one H1 ({parser.h1}): {page.relative_to(ROOT)}")
        for url in parser.links:
            if url.startswith(("mailto:", "tel:", "https://", "http://")):
                continue
            target = page.resolve() if url.startswith("#") else local_target(url, page)
            if target is not None and not target.exists():
                failures.append(f"Broken {url} in {page.relative_to(ROOT)}")
                continue
            fragment = urlsplit(url).fragment
            if fragment and target is not None and target.suffix == ".html":
                target_parser = inspections.get(target)
                if target_parser is None:
                    target_parser = Inspector()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    inspections[target] = target_parser
                if fragment not in target_parser.ids:
                    failures.append(f"Missing #{fragment} target for {url} in {page.relative_to(ROOT)}")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"Validated {len(pages)} HTML pages: metadata and local links OK")


if __name__ == "__main__":
    main()
