#!/usr/bin/env python3
"""Format generated HTML while preserving original start-tag spelling."""

import re
from html.parser import HTMLParser


VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

BLOCK_TAGS = {
    "html", "head", "body", "header", "footer", "main", "nav", "section",
    "article", "aside", "div", "form", "figure", "figcaption", "details",
    "dialog", "fieldset", "dl", "ol", "ul", "li", "table", "thead",
    "tbody", "tfoot", "tr", "blockquote",
}

TEXT_TAGS = {
    "title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "label",
    "button", "address", "summary", "dt", "dd", "textarea", "option",
}

LINE_TAGS = {
    "a", "button", "script", "meta", "link", "img", "input", "iframe",
    "title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "label",
    "address", "summary", "dt", "dd", "textarea", "option",
}


class Node:
    def __init__(self, kind, raw="", tag=""):
        self.kind = kind
        self.raw = raw
        self.tag = tag
        self.children = []


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node("root")
        self.stack = [self.root]

    def append(self, node):
        self.stack[-1].children.append(node)

    def handle_decl(self, decl):
        self.append(Node("raw", f"<!{decl}>"))

    def handle_comment(self, data):
        self.append(Node("raw", f"<!--{data}-->"))

    def handle_starttag(self, tag, attrs):
        node = Node("element", self.get_starttag_text(), tag.lower())
        self.append(node)
        if node.tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.append(Node("void", self.get_starttag_text(), tag.lower()))

    def handle_endtag(self, tag):
        wanted = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == wanted:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.append(Node("text", data))

    def handle_entityref(self, name):
        self.append(Node("text", f"&{name};"))

    def handle_charref(self, name):
        self.append(Node("text", f"&#{name};"))

    def handle_pi(self, data):
        self.append(Node("raw", f"<?{data}>") )


def inline_html(node):
    if node.kind in {"text", "raw"}:
        return node.raw
    if node.kind == "void" or node.tag in VOID_TAGS:
        return node.raw
    inner = "".join(inline_html(child) for child in node.children)
    return f"{node.raw}{inner}</{node.tag}>"


def compact_inline(nodes):
    value = "".join(inline_html(node) for node in nodes)
    return re.sub(r"\s+", " ", value).strip()


def meaningful(node):
    return node.kind != "text" or bool(node.raw.strip())


def structural(node):
    return node.kind == "element" and node.tag in BLOCK_TAGS


def format_node(node, depth=0):
    indent = "  " * depth
    if node.kind == "raw":
        return [f"{indent}{node.raw.strip()}"]
    if node.kind == "text":
        text = re.sub(r"\s+", " ", node.raw).strip()
        return [f"{indent}{text}"] if text else []
    if node.kind == "void" or node.tag in VOID_TAGS:
        return [f"{indent}{node.raw}"]

    children = [child for child in node.children if meaningful(child)]
    closing = f"</{node.tag}>"
    if not children and node.tag in BLOCK_TAGS:
        return [f"{indent}{node.raw}", f"{indent}{closing}"]
    if node.tag in TEXT_TAGS or not children:
        return [f"{indent}{node.raw}{compact_inline(children)}{closing}"]

    lines = [f"{indent}{node.raw}"]
    inline_group = []

    def flush_inline():
        if not inline_group:
            return
        value = compact_inline(inline_group)
        if value:
            lines.append(f"{'  ' * (depth + 1)}{value}")
        inline_group.clear()

    for child in children:
        separate = structural(child)
        if node.tag == "head" and child.kind == "element":
            separate = True
        if child.kind == "element" and child.tag in LINE_TAGS:
            separate = True
        if separate:
            flush_inline()
            lines.extend(format_node(child, depth + 1))
        else:
            inline_group.append(child)
    flush_inline()
    lines.append(f"{indent}{closing}")
    return lines


def format_html(source):
    parser = TreeBuilder()
    parser.feed(source)
    parser.close()
    lines = []
    for node in parser.root.children:
        if meaningful(node):
            lines.extend(format_node(node))
    return "\n".join(lines) + "\n"

