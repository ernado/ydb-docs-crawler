#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27",
#     "lxml>=5.2",
# ]
# ///
"""Crawl the YDB documentation (https://ydb.tech/docs) into structured Markdown.

The site is a Diplodoc/YFM viewer: every page ships its already-rendered article
HTML plus the full table of contents inside a ``__DATA__ = {...}`` blob in the
server-rendered HTML.  We parse that blob instead of scraping the DOM, which
gives us the clean article body, the page title, the source path in the YDB
repo, and the complete TOC for free.

Usage:
    ./crawl_ydb_docs.py                       # crawl en / v26.1 into ./ydb-docs-md
    ./crawl_ydb_docs.py --lang all            # both English and Russian
    ./crawl_ydb_docs.py --version main --lang ru
    ./crawl_ydb_docs.py --only 'yql/**' --refresh
"""

from __future__ import annotations

import argparse
import asyncio
import fnmatch
import hashlib
import json
import posixpath
import re
import sys
import time
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urljoin, urlparse

import httpx
from lxml import html as lxml_html
from lxml.html import HtmlElement

SITE = "https://ydb.tech"
DOCS_BASE = f"{SITE}/docs/"
DEFAULT_UA = "ydb-docs-crawler/1.0 (+https://ydb.tech/docs)"
ALL_LANGS = ["en", "ru"]
#: Statuses worth another attempt rather than reporting as the page's verdict.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
#: How many times to wait out a rate limit before giving up on a page.
RATE_LIMIT_RETRIES = 6


def rate_limit_delay(exc: BaseException) -> float | None:
    """Seconds to wait if ``exc`` is a rate limit, else None.

    Honours ``Retry-After`` when the server sends one; otherwise backs off
    linearly, which is gentler on a public site than hammering it again.
    """
    response = getattr(exc, "response", None)
    if response is None or response.status_code != 429:
        return None
    retry_after = response.headers.get("retry-after", "")
    try:
        return max(1.0, min(60.0, float(retry_after)))
    except ValueError:
        return 5.0


# --------------------------------------------------------------------------- #
# __DATA__ extraction
# --------------------------------------------------------------------------- #

_DATA_START = "__DATA__ = "
_DATA_END = "\n__LOADED_PAGES"


class PageError(Exception):
    """The viewer returned a page we cannot turn into an article."""


def extract_data(page_html: str) -> dict[str, Any]:
    """Pull the ``__DATA__`` JSON payload out of a server-rendered page."""
    start = page_html.find(_DATA_START)
    if start < 0:
        raise PageError("no __DATA__ payload (not a docs-viewer page?)")
    end = page_html.find(_DATA_END, start)
    if end < 0:
        raise PageError("truncated __DATA__ payload")
    raw = page_html[start + len(_DATA_START) : end].rstrip().rstrip(";")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:  # pragma: no cover - site format change
        raise PageError(f"malformed __DATA__ payload: {exc}") from exc


def page_props(data: dict[str, Any]) -> dict[str, Any]:
    props = (data.get("props") or {}).get("pageProps") or {}
    inner = props.get("data")
    if not isinstance(inner, dict):
        err = data.get("err") or props.get("err")
        raise PageError(f"page has no content payload (err={err!r})")
    return inner


# --------------------------------------------------------------------------- #
# Path helpers
# --------------------------------------------------------------------------- #


def norm_doc_path(path: str) -> str:
    """Normalise a docs path such as ``/docs/en/concepts/`` to ``en/concepts/``."""
    path = path.strip()
    for prefix in (SITE, "https://ydb.tech", "http://ydb.tech"):
        if path.startswith(prefix):
            path = path[len(prefix) :]
    if path.startswith("/docs/"):
        path = path[len("/docs/") :]
    path = path.lstrip("/")
    if path.endswith(".html"):
        path = path[: -len(".html")]
        if posixpath.basename(path) == "index":
            path = posixpath.dirname(path) + "/"
    return path


def doc_path_to_file(path: str) -> str:
    """Map a docs path to the Markdown file we write for it."""
    path = norm_doc_path(path)
    if not path or path.endswith("/"):
        return path + "index.md"
    ext = posixpath.splitext(path)[1].lower()
    if ext and ext not in {".md", ".html"}:
        return path  # an asset, keep verbatim
    if ext == ".md":
        return path
    return path + ".md"


#: Images are served from a build-specific location such as
#: ``docs-assets/ydb-platform--ydb/rev/<sha>/en/concepts/_assets/pic.png``.
#: Stripping that prefix leaves the plain doc path (``en/concepts/_assets/pic.png``).
_ASSET_PREFIX = re.compile(r"^docs-assets/[^/]+/rev/[^/]+/")
_GITHUB_TREE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.*)$")


def strip_asset_prefix(path: str) -> str:
    return _ASSET_PREFIX.sub("", path)


def github_raw_base(tree_url: str | None) -> str | None:
    """Turn ``.../ydb/tree/main/ydb/docs`` into its raw.githubusercontent.com form."""
    match = _GITHUB_TREE.match((tree_url or "").rstrip("/"))
    if not match:
        return None
    owner, repo, ref, path = match.groups()
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"


def image_url(asset_path: str, raw_base: str | None) -> str | None:
    """Map a doc asset path to a stable URL in the documentation source repo.

    ``en/concepts/_assets/pic.png`` lives at ``<repo>/en/core/concepts/_assets/pic.png``
    upstream -- every page on the site reports a ``sourcePath`` of ``<lang>/core/...``.
    Linking there instead of at the site's revision-pinned CDN path keeps the URL
    stable across documentation rebuilds.
    """
    if not raw_base:
        return None
    lang, _, rest = asset_path.partition("/")
    if lang not in ALL_LANGS or not rest:
        return None
    return f"{raw_base}/{lang}/core/{quote(rest, safe='/')}"


def doc_path_to_url(path: str, version: str | None) -> str:
    url = urljoin(DOCS_BASE, quote(norm_doc_path(path), safe="/#?&=%"))
    if version:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}version={quote(version)}"
    return url


# --------------------------------------------------------------------------- #
# HTML -> Markdown
# --------------------------------------------------------------------------- #

INLINE_TAGS = {
    "a",
    "abbr",
    "b",
    "bdi",
    "bdo",
    "big",
    "br",
    "cite",
    "code",
    "data",
    "dfn",
    "em",
    "i",
    "img",
    "kbd",
    "mark",
    "q",
    "s",
    "samp",
    "small",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "time",
    "tt",
    "u",
    "var",
    "wbr",
    "font",
    "nobr",
}
DROP_TAGS = {"script", "style", "svg", "button", "noscript", "template", "iframe"}
DROP_CLASSES = {
    "yfm-anchor",
    "yfm-clipboard-anchor",
    "yfm-code-floating",
    "yfm-clipboard-button",
    "yfm-code-button",
}
NOTE_KINDS = {
    "info": "NOTE",
    "note": "NOTE",
    "tip": "TIP",
    "important": "IMPORTANT",
    "warning": "WARNING",
    "alert": "CAUTION",
    "caution": "CAUTION",
}
#: Titles YFM renders by default for each note kind (en + ru). They add nothing
#: on top of the alert marker itself, so they are dropped.
DEFAULT_NOTE_TITLES = {
    "note",
    "tip",
    "attention",
    "alert",
    "important",
    "warning",
    "caution",
    "примечание",
    "совет",
    "внимание",
    "важно",
    "предупреждение",
}
_WS = re.compile(r"[ \t\r\f\v]*\n[ \t\r\f\v]*|[ \t\r\f\v]{2,}")
_ESCAPE_LINE_START = re.compile(r"^(\s*)([-+*>#]|\d+[.)])(\s)")


def classes(el: HtmlElement) -> set[str]:
    return set((el.get("class") or "").split())


def is_dropped(el: HtmlElement) -> bool:
    if not isinstance(el.tag, str):
        return True  # comments, processing instructions
    if el.tag in DROP_TAGS:
        return True
    return bool(classes(el) & DROP_CLASSES)


def collapse(text: str) -> str:
    return _WS.sub(" ", text)


_ESCAPE_INLINE = re.compile(r"[\\`*\[\]]|<(?=[a-zA-Z/!?])")


def escape_inline(text: str) -> str:
    # Keep escaping light: only characters that would flip meaning mid-line.
    # `_` is left alone because CommonMark ignores intra-word underscores, and
    # escaping it would litter identifiers like `x86_64` with backslashes.
    return _ESCAPE_INLINE.sub(lambda m: "\\" + m.group(0), text)


def indent_block(text: str, prefix: str, first: str | None = None) -> str:
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        pfx = first if (i == 0 and first is not None) else prefix
        out.append((pfx + line).rstrip() if line.strip() else pfx.rstrip())
    return "\n".join(out)


@dataclass
class LinkContext:
    """Everything the converter needs to rewrite hrefs and collect assets."""

    doc_path: str  # docs path of the page being rendered, e.g. "en/concepts/glossary"
    lang: str
    keep_absolute: bool = False
    #: Doc paths that are section landing pages. The site links to them both as
    #: ``en/concepts`` and ``en/concepts/``; both must resolve to index.md.
    index_paths: frozenset[str] = frozenset()
    #: Every doc path in the table of contents, without trailing slashes.
    known_paths: frozenset[str] = frozenset()
    #: Base URL images are linked at; they are never downloaded.
    image_base: str | None = None
    #: image URL -> the doc asset path it came from, for the post-crawl check.
    images: dict[str, str] = field(default_factory=dict)
    #: image URL -> the site URL to fall back to if that link does not resolve.
    image_fallbacks: dict[str, str] = field(default_factory=dict)

    @property
    def out_file(self) -> str:
        return doc_path_to_file(self.doc_path)

    def is_known(self, path: str) -> bool:
        stripped = path.rstrip("/")
        return stripped in self.known_paths or stripped in self.index_paths

    def resolve_unrooted(self, path: str) -> str:
        """Anchor a link that does not start with a language root.

        Article HTML uses root-relative doc paths ("en/concepts/glossary"), but
        landing-page descriptions and links YFM failed to rewrite are relative
        ("yql/reference/", "concepts/datamodel/topic").  Prefer the page-relative
        reading, fall back to the language root, and keep the page-relative one
        when neither names a page we know about.
        """
        slash = "/" if path.endswith("/") else ""
        base = self.doc_path if self.doc_path.endswith("/") else posixpath.dirname(self.doc_path)
        relative = posixpath.normpath(posixpath.join(base, path))
        if self.is_known(relative):
            return relative + slash
        rooted = f"{self.lang}/{path.lstrip('/')}"
        if self.is_known(rooted):
            return rooted
        return relative + slash

    def rewrite(self, href: str, *, is_asset: bool = False) -> str:
        href = (href or "").strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
            return href
        parsed = urlparse(href)
        if parsed.scheme and parsed.netloc:
            if parsed.netloc not in {"ydb.tech", "www.ydb.tech"} or not parsed.path.startswith("/docs"):
                return href
        elif parsed.scheme:
            return href
        if self.keep_absolute:
            return urljoin(DOCS_BASE, href)

        path = norm_doc_path(parsed.path or "")
        if not path:
            return href
        if not _ASSET_PREFIX.match(path) and path.split("/", 1)[0] not in ALL_LANGS:
            path = self.resolve_unrooted(path)
        if not path.endswith("/") and path in self.index_paths:
            path += "/"
        target = doc_path_to_file(path)
        if is_asset:
            # Images are linked, never copied into the output tree.
            asset_path = strip_asset_prefix(target)
            site_url = urljoin(DOCS_BASE, quote(path, safe="/"))
            url = image_url(asset_path, self.image_base) or site_url
            self.images[url] = asset_path
            if url != site_url:
                self.image_fallbacks[url] = site_url
            return url
        rel = posixpath.relpath(target, posixpath.dirname(self.out_file) or ".")
        anchor = f"#{parsed.fragment}" if parsed.fragment else ""
        return quote(rel, safe="/._-#~()!$&'*+,;=:@") + anchor


class MarkdownConverter:
    """Converts Diplodoc-rendered article HTML into Markdown."""

    def __init__(self, ctx: LinkContext) -> None:
        self.ctx = ctx

    # -- entry point ------------------------------------------------------- #

    def convert(self, fragment: str) -> str:
        if not fragment or not fragment.strip():
            return ""
        root = lxml_html.fragment_fromstring(fragment, create_parent="div")
        body = "\n\n".join(self.blocks(root))
        return re.sub(r"\n{3,}", "\n\n", body).strip()

    def convert_inline(self, fragment: str) -> str:
        """Render a one-line fragment, such as a page title, as inline Markdown.

        Titles arrive as HTML and can carry markup with server-generated ids
        (``<code ... id="inline-code-id-hg5gddr3">``) that differ on every
        request, so they must not be passed through verbatim.
        """
        if not fragment or "<" not in fragment:
            return (fragment or "").strip()
        root = lxml_html.fragment_fromstring(fragment, create_parent="div")
        return collapse(self.inline_children(root)).strip()

    # -- block level ------------------------------------------------------- #

    def blocks(self, el: HtmlElement) -> list[str]:
        """Render the children of ``el`` as a list of Markdown blocks."""
        out: list[str] = []
        buf: list[str] = []

        def flush() -> None:
            text = "".join(buf).strip()
            buf.clear()
            if text:
                out.append(self.escape_block_start(text))

        if el.text:
            buf.append(escape_inline(collapse(el.text)))
        for child in el:
            tail = escape_inline(collapse(child.tail or ""))
            if is_dropped(child):
                if tail.strip():
                    buf.append(tail)
                continue
            if child.tag in INLINE_TAGS:
                buf.append(self.inline(child))
                buf.append(tail)
                continue
            flush()
            rendered = self.block(child)
            if rendered.strip():
                out.append(rendered)
            if tail.strip():
                buf.append(tail)
        flush()
        return out

    @staticmethod
    def escape_block_start(text: str) -> str:
        return _ESCAPE_LINE_START.sub(lambda m: f"{m.group(1)}\\{m.group(2)}{m.group(3)}", text)

    def block(self, el: HtmlElement) -> str:
        tag = el.tag
        cls = classes(el)

        if "yfm-note" in cls:
            return self.note(el)
        if "yfm-tabs" in cls:
            return self.tabs(el)
        if "yfm-cut" in cls or tag == "details":
            return self.cut(el)
        if "yfm-code-floating-container" in cls:
            return "\n\n".join(self.blocks(el))
        if "yfm-table" in cls and tag == "div":
            return "\n\n".join(self.blocks(el))

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            text = self.inline_children(el).strip()
            anchor = el.get("id")
            suffix = f" {{#{anchor}}}" if anchor and self.slugify(text) != anchor else ""
            return f"{'#' * level} {text}{suffix}" if text else ""
        if tag == "p":
            text = self.inline_children(el).strip()
            return self.escape_block_start(text)
        if tag == "pre":
            return self.code_block(el)
        if tag in {"ul", "ol"}:
            return self.list_block(el)
        if tag == "dl":
            return self.definition_list(el)
        if tag == "table":
            return self.table(el)
        if tag == "blockquote":
            inner = "\n\n".join(self.blocks(el))
            return indent_block(inner, "> ")
        if tag == "hr":
            return "---"
        if tag == "figure":
            return "\n\n".join(self.blocks(el))
        if tag == "figcaption":
            text = self.inline_children(el).strip()
            return f"*{text}*" if text else ""
        # div/section/article/main/... and anything unknown: recurse
        return "\n\n".join(self.blocks(el))

    # -- YFM widgets ------------------------------------------------------- #

    def note(self, el: HtmlElement) -> str:
        kind = (el.get("note-type") or "").lower()
        if not kind:
            for cl in classes(el):
                if cl.startswith("yfm-accent-"):
                    kind = cl[len("yfm-accent-") :]
        alert = NOTE_KINDS.get(kind, "NOTE")

        title, parts = "", []
        for child in el:
            if is_dropped(child):
                continue
            cls = classes(child)
            if "yfm-note-title" in cls:
                title = self.inline_children(child).strip()
            elif "yfm-note-content" in cls:
                parts.extend(self.blocks(child))
            else:
                rendered = self.block(child)
                if rendered.strip():
                    parts.append(rendered)
        body = "\n\n".join(p for p in parts if p.strip())
        # GitHub alert syntax: the marker line, then the content. A custom title
        # becomes its own paragraph so it does not merge with the first one.
        head = f"[!{alert}]"
        if title and title.lower().rstrip("!.:") not in DEFAULT_NOTE_TITLES | {kind}:
            head += f"\n**{title}**\n"
        return indent_block(f"{head}\n{body}".rstrip(), "> ")

    def tabs(self, el: HtmlElement) -> str:
        titles = [
            self.inline_children(t).strip()
            for t in el.find_class("yfm-tab")
            if "yfm-tab-list" not in classes(t)
        ]
        panels = el.find_class("yfm-tab-panel")
        if not panels:
            return "\n\n".join(self.blocks(el))
        chunks = ["{% list tabs %}", ""]
        for i, panel in enumerate(panels):
            title = panel.get("data-title") or (titles[i] if i < len(titles) else f"Tab {i + 1}")
            body = "\n\n".join(self.blocks(panel)).strip()
            chunks.append(f"- {collapse(title).strip()}")
            chunks.append("")
            if body:
                chunks.append(indent_block(body, "  "))
                chunks.append("")
        chunks.append("{% endlist %}")
        return "\n".join(chunks).rstrip()

    def cut(self, el: HtmlElement) -> str:
        title, parts = "", []
        for child in el:
            if is_dropped(child):
                continue
            cls = classes(child)
            if child.tag == "summary" or "yfm-cut-title" in cls:
                title = self.inline_children(child).strip()
            elif "yfm-cut-content" in cls:
                parts.extend(self.blocks(child))
            else:
                rendered = self.block(child)
                if rendered.strip():
                    parts.append(rendered)
        body = "\n\n".join(p for p in parts if p.strip())
        return f"<details>\n<summary>{title or 'Details'}</summary>\n\n{body}\n\n</details>"

    # -- primitives -------------------------------------------------------- #

    def code_block(self, el: HtmlElement) -> str:
        code = el.find("code")
        node = code if code is not None else el
        lang = ""
        for cl in classes(node) | classes(el):
            if cl in {"hljs", "yfm-code", "code"} or cl.startswith(("hljs-", "yfm-")):
                continue
            if cl.startswith("language-"):
                lang = cl[len("language-") :]
                break
            lang = lang or cl
        text = node.text_content().rstrip("\n")
        fence = "`" * max(3, *(len(m) + 1 for m in re.findall(r"`+", text)), 3)
        return f"{fence}{lang}\n{text}\n{fence}"

    def list_block(self, el: HtmlElement, depth: int = 0) -> str:
        ordered = el.tag == "ol"
        try:
            index = int(el.get("start") or 1)
        except ValueError:
            index = 1
        items: list[str] = []
        for li in el:
            if not isinstance(li.tag, str) or li.tag != "li" or is_dropped(li):
                continue
            body = "\n\n".join(self.blocks(li)).strip()
            marker = f"{index}. " if ordered else "- "
            index += 1
            if not body:
                items.append(marker.rstrip())
                continue
            items.append(indent_block(body, " " * len(marker), first=marker))
        # Tight list when every item is a single line, loose otherwise.
        sep = "\n" if all("\n" not in i for i in items) else "\n\n"
        return sep.join(items)

    def definition_list(self, el: HtmlElement) -> str:
        parts = []
        for child in el:
            if not isinstance(child.tag, str):
                continue
            if child.tag == "dt":
                parts.append(f"**{self.inline_children(child).strip()}**")
            elif child.tag == "dd":
                body = "\n\n".join(self.blocks(child)).strip()
                parts.append(indent_block(body, "  "))
        return "\n\n".join(p for p in parts if p.strip())

    def table(self, el: HtmlElement) -> str:
        rows: list[list[str]] = []
        header: list[str] | None = None
        for section in el.iter("thead", "tbody", "tfoot", "tr"):
            if section.tag != "tr":
                continue
            cells = [c for c in section if isinstance(c.tag, str) and c.tag in {"td", "th"}]
            if not cells:
                continue
            rendered = [self.cell(c) for c in cells]
            is_header = all(c.tag == "th" for c in cells)
            parent = section.getparent()
            if header is None and (is_header or (parent is not None and parent.tag == "thead")):
                header = rendered
            else:
                rows.append(rendered)
        if header is None and not rows:
            return ""
        width = max(len(r) for r in ([header] if header else []) + rows) if (header or rows) else 0
        if header is None:
            header = [""] * width
        pad = lambda r: r + [""] * (width - len(r))
        lines = [
            "| " + " | ".join(pad(header)) + " |",
            "| " + " | ".join(["---"] * width) + " |",
        ]
        lines += ["| " + " | ".join(pad(r)) + " |" for r in rows]
        return "\n".join(lines)

    def cell(self, el: HtmlElement) -> str:
        blocks = [b for b in self.blocks(el) if b.strip()]
        text = "<br>".join(b.replace("\n", "<br>") for b in blocks)
        return text.replace("|", "\\|").strip()

    # -- inline level ------------------------------------------------------ #

    def inline_children(self, el: HtmlElement) -> str:
        parts = [escape_inline(collapse(el.text or ""))]
        for child in el:
            if is_dropped(child):
                parts.append(escape_inline(collapse(child.tail or "")))
                continue
            parts.append(self.inline(child))
            parts.append(escape_inline(collapse(child.tail or "")))
        return "".join(parts)

    def inline(self, el: HtmlElement) -> str:
        tag = el.tag
        if tag == "br":
            return "  \n"
        if tag == "code":
            text = el.text_content()
            ticks = "`" * (max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
            pad = " " if text.startswith("`") or text.endswith("`") else ""
            return f"{ticks}{pad}{text}{pad}{ticks}"
        if tag in {"strong", "b"}:
            inner = self.inline_children(el).strip()
            return f"**{inner}**" if inner else ""
        if tag in {"em", "i", "dfn", "cite", "var"}:
            inner = self.inline_children(el).strip()
            return f"*{inner}*" if inner else ""
        if tag in {"s", "del", "strike"}:
            inner = self.inline_children(el).strip()
            return f"~~{inner}~~" if inner else ""
        if tag in {"kbd", "samp", "tt"}:
            text = el.text_content()
            return f"`{text}`" if text else ""
        if tag == "sup":
            return f"<sup>{self.inline_children(el)}</sup>"
        if tag == "sub":
            return f"<sub>{self.inline_children(el)}</sub>"
        if tag == "img":
            return self.image(el)
        if tag == "a":
            return self.link(el)
        if tag in {"wbr"}:
            return ""
        # span and friends: transparent
        return self.inline_children(el)

    def image(self, el: HtmlElement) -> str:
        src = self.ctx.rewrite(el.get("src") or "", is_asset=True)
        alt = collapse(el.get("alt") or "").strip().replace("]", "\\]")
        title = collapse(el.get("title") or "").strip()
        title_part = f' "{title}"' if title else ""
        return f"![{alt}]({self.link_target(src)}{title_part})"

    def link(self, el: HtmlElement) -> str:
        text = self.inline_children(el).strip()
        href = el.get("href")
        if not href:
            return text
        target = self.ctx.rewrite(href)
        if not text:
            return f"<{target}>" if target else ""
        title = collapse(el.get("title") or "").strip()
        title_part = f' "{title}"' if title else ""
        return f"[{text}]({self.link_target(target)}{title_part})"

    @staticmethod
    def link_target(target: str) -> str:
        if not target:
            return ""
        return f"<{target}>" if re.search(r"[ ()]", target) else target

    @staticmethod
    def slugify(text: str) -> str:
        slug = re.sub(r"[^\w\- ]+", "", text.lower(), flags=re.UNICODE)
        return re.sub(r"[\s_]+", "-", slug).strip("-")


# --------------------------------------------------------------------------- #
# TOC
# --------------------------------------------------------------------------- #


def walk_toc(items: Iterable[dict[str, Any]], depth: int = 0) -> Iterator[tuple[int, dict[str, Any]]]:
    for item in items or []:
        if not isinstance(item, dict):
            continue
        yield depth, item
        yield from walk_toc(item.get("items") or [], depth + 1)


def toc_paths(toc: dict[str, Any]) -> list[str]:
    seen: dict[str, None] = {}
    for _, item in walk_toc(toc.get("items") or []):
        href = item.get("href")
        if not isinstance(href, str) or href.startswith(("http://", "https://")):
            continue
        seen.setdefault(norm_doc_path(href.split("#")[0]), None)
    return list(seen)


def toc_index_paths(toc: dict[str, Any]) -> frozenset[str]:
    """Section landing pages, without their trailing slash (``en/concepts``)."""
    return frozenset(p.rstrip("/") for p in toc_paths(toc) if p.endswith("/"))


def render_summary(toc: dict[str, Any], lang: str) -> str:
    lines = [f"# {toc.get('title') or 'Contents'}", ""]
    for depth, item in walk_toc(toc.get("items") or []):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        href = item.get("href")
        href = href if isinstance(href, str) else None
        pad = "  " * depth
        if href and not href.startswith(("http://", "https://")):
            rel = doc_path_to_file(href.split("#")[0])
            lines.append(f"{pad}- [{name}]({quote(rel, safe='/._-')})")
        elif href:
            lines.append(f"{pad}- [{name}]({href})")
        else:
            lines.append(f"{pad}- {name}")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Page rendering
# --------------------------------------------------------------------------- #


def yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return '""'
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def front_matter(meta: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in meta.items():
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {yaml_scalar(v)}" for v in value)
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def render_leading(props: dict[str, Any], conv: MarkdownConverter) -> str:
    """Render an index.yaml-style landing page (title + description + link cards)."""
    data = props.get("data") or {}
    parts: list[str] = []
    for desc in data.get("description") or []:
        parts.append(conv.convert(f"<p>{desc}</p>") if "<" in desc else desc.strip())
    for section in data.get("links") or []:
        title = (section.get("title") or "").strip()
        href = section.get("href")
        body = (section.get("description") or "").strip()
        if href:
            link = conv.ctx.rewrite(href)
            entry = f"- [{title}]({MarkdownConverter.link_target(link)})"
        else:
            entry = f"- **{title}**"
        if body:
            entry += f" — {body}"
        parts.append(entry)
    # Merge consecutive link bullets into single lists.
    merged: list[str] = []
    for part in parts:
        if part.startswith("- ") and merged and merged[-1].startswith("- "):
            merged[-1] += "\n" + part
        else:
            merged.append(part)
    return "\n\n".join(p for p in merged if p.strip())


@dataclass
class RenderedPage:
    doc_path: str
    out_file: str
    title: str
    markdown: str
    source_path: str | None
    vcs_url: str | None
    description: str | None
    links: list[str]
    images: dict[str, str]
    image_fallbacks: dict[str, str]


def render_page(
    doc_path: str,
    props: dict[str, Any],
    *,
    lang: str,
    version: str,
    keep_absolute: bool,
    with_front_matter: bool,
    index_paths: frozenset[str] = frozenset(),
    known_paths: frozenset[str] = frozenset(),
) -> RenderedPage:
    ctx = LinkContext(
        doc_path=doc_path,
        lang=lang,
        keep_absolute=keep_absolute,
        index_paths=index_paths,
        known_paths=known_paths,
        image_base=github_raw_base(props.get("githubUrlPrefix")),
    )
    conv = MarkdownConverter(ctx)
    meta = props.get("meta") or {}

    html_body = props.get("html")
    if isinstance(html_body, str) and html_body.strip():
        body = conv.convert(html_body)
        title = conv.convert_inline(props.get("title") or "")
    else:
        data = props.get("data") or {}
        body = render_leading(props, conv)
        title = conv.convert_inline(data.get("title") or props.get("title") or "")
        meta = data.get("meta") or meta

    if not title:
        first = re.match(r"#\s+(.+)", body or "")
        title = first.group(1).strip() if first else doc_path

    # Diplodoc puts the H1 in the body already for most pages; only add one when missing.
    if body and not re.match(r"#\s", body.lstrip()):
        body = f"# {title}\n\n{body}" if title else body

    source_path = meta.get("sourcePath") or meta.get("vcsPath")
    header = ""
    if with_front_matter:
        header = (
            front_matter(
                {
                    "title": title,
                    "url": doc_path_to_url(doc_path, version),
                    "doc_path": doc_path,
                    "version": version,
                    "lang": lang,
                    "source_path": source_path,
                    "vcs_url": props.get("vcsUrl"),
                    "description": meta.get("description"),
                    # No timestamp: the docs revision already identifies the build,
                    # and a clock reading would make every re-scrape a full rewrite.
                    "revision": props.get("revision"),
                }
            )
            + "\n\n"
        )

    internal_links = sorted(
        {
            norm_doc_path(m)
            for m in re.findall(r'href="([^"]+)"', props.get("html") or "")
            if not m.startswith(("http://", "https://", "#", "mailto:", "tel:"))
        }
    )
    return RenderedPage(
        doc_path=doc_path,
        out_file=ctx.out_file,
        title=title,
        markdown=header + (body.strip() + "\n" if body.strip() else ""),
        source_path=source_path,
        vcs_url=props.get("vcsUrl"),
        description=meta.get("description"),
        links=internal_links,
        images=dict(ctx.images),
        image_fallbacks=dict(ctx.image_fallbacks),
    )


# --------------------------------------------------------------------------- #
# Crawler
# --------------------------------------------------------------------------- #


@dataclass
class Stats:
    fetched: int = 0
    throttled: int = 0
    cached: int = 0
    written: int = 0
    unchanged: int = 0
    failed: int = 0


class Crawler:
    """Crawls one language of the documentation into ``args.out``."""

    def __init__(self, args: argparse.Namespace, lang: str, stats: Stats | None = None) -> None:
        self.args = args
        self.lang = lang
        self.out = Path(args.out).resolve()
        self.cache_dir = Path(args.cache_dir).resolve() if args.cache_dir else self.out / ".cache"
        self.stats = stats if stats is not None else Stats()
        self.seen: set[str] = set()
        self.manifest: list[dict[str, Any]] = []
        self.images: dict[str, str] = {}
        self.image_fallbacks: dict[str, str] = {}
        #: image URL -> the output files that reference it
        self.image_pages: dict[str, set[str]] = {}
        self.failures: list[tuple[str, str]] = []
        self.index_paths: frozenset[str] = frozenset()
        self.known_paths: frozenset[str] = frozenset()
        self.revision = "unknown"
        self._lock = asyncio.Lock()
        self._log_lock = asyncio.Lock()
        self._done = 0
        self._total = 0

    # -- io ---------------------------------------------------------------- #

    def cache_file(self, doc_path: str) -> Path:
        digest = hashlib.sha1(f"{doc_path}|{self.args.version}".encode()).hexdigest()
        return self.cache_dir / self.revision / f"{digest}.json"

    async def fetch(self, client: httpx.AsyncClient, doc_path: str) -> dict[str, Any]:
        """Return the page's ``pageProps.data``, using the on-disk cache when allowed."""
        cache = self.cache_file(doc_path)
        if not self.args.refresh and cache.is_file():
            try:
                self.stats.cached += 1
                return json.loads(cache.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self.stats.cached -= 1

        url = doc_path_to_url(doc_path, self.args.version)
        last: Exception | None = None
        attempt = throttled = 0
        while True:
            try:
                resp = await client.get(url)
                if resp.status_code in RETRY_STATUSES:
                    raise httpx.HTTPStatusError(
                        f"HTTP {resp.status_code}", request=resp.request, response=resp
                    )
                resp.raise_for_status()
                props = page_props(extract_data(resp.text))
                self.stats.fetched += 1
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
                if self.args.delay:
                    await asyncio.sleep(self.args.delay)
                return props
            except (httpx.HTTPError, PageError) as exc:
                last = exc
                delay = rate_limit_delay(exc)
                if delay is not None:
                    # Being throttled says nothing about the page, so it gets its
                    # own budget: giving up here would report a rate limit as if
                    # it were the page's real status.
                    throttled += 1
                    if throttled > RATE_LIMIT_RETRIES:
                        break
                    self.stats.throttled += 1
                    await asyncio.sleep(delay)
                    continue
                attempt += 1
                if attempt > self.args.retries:
                    break
                await asyncio.sleep(min(2**attempt, 10) * 0.5)
        raise PageError(f"{url}: {last}")

    def write(self, path: Path, content: str | bytes) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8") if isinstance(content, str) else content
        if path.is_file() and path.read_bytes() == data:
            self.stats.unchanged += 1
            return False
        path.write_bytes(data)
        self.stats.written += 1
        return True

    async def log(self, message: str) -> None:
        async with self._log_lock:
            print(message, file=sys.stderr, flush=True)

    # -- crawl ------------------------------------------------------------- #

    def selected(self, doc_path: str) -> bool:
        prefix = f"{self.lang}/"
        if doc_path != self.lang and not doc_path.startswith(prefix):
            return False
        if not self.args.only:
            return True
        rel = doc_path[len(prefix) :] if doc_path.startswith(prefix) else ""
        return any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(rel + "/", pat) for pat in self.args.only)

    async def run(self) -> int:
        limits = httpx.Limits(max_connections=self.args.jobs * 2, max_keepalive_connections=self.args.jobs)
        headers = {"User-Agent": self.args.user_agent, "Accept-Language": self.lang}
        timeout = httpx.Timeout(self.args.timeout)
        async with httpx.AsyncClient(
            headers=headers, timeout=timeout, limits=limits, follow_redirects=True, http2=False
        ) as client:
            root = f"{self.lang}/"
            await self.log(f"→ fetching table of contents from {doc_path_to_url(root, self.args.version)}")
            self.args.refresh, keep = True, self.args.refresh
            try:
                props = await self.fetch(client, root)
            finally:
                self.args.refresh = keep
            self.revision = props.get("revision") or "unknown"
            toc = props.get("toc") or {}
            available = props.get("docVersions") or []
            if self.args.version and available and self.args.version not in available:
                await self.log(f"! warning: version {self.args.version!r} not in {available}")

            self.index_paths = toc_index_paths(toc)
            self.known_paths = frozenset(p.rstrip("/") for p in toc_paths(toc))
            paths = [p for p in toc_paths(toc) if self.selected(p)]
            if root not in paths and self.selected(root):
                paths.insert(0, root)
            await self.log(f"→ revision {self.revision}, {len(paths)} pages selected")
            if self.args.limit:
                paths = paths[: self.args.limit]

            self.out.mkdir(parents=True, exist_ok=True)
            self.write(
                self.out / f"toc.{self.lang}.json", json.dumps(toc, ensure_ascii=False, indent=2) + "\n"
            )
            self.write(self.out / f"SUMMARY.{self.lang}.md", render_summary(toc, self.lang))

            queue: asyncio.Queue[str] = asyncio.Queue()
            for path in paths:
                if path not in self.seen:
                    self.seen.add(path)
                    self._total += 1
                    queue.put_nowait(path)

            workers = [asyncio.create_task(self.worker(client, queue)) for _ in range(self.args.jobs)]
            await queue.join()
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        self.manifest.sort(key=lambda m: m["doc_path"])
        return len(self.failures)

    async def worker(self, client: httpx.AsyncClient, queue: asyncio.Queue[str]) -> None:
        while True:
            doc_path = await queue.get()
            try:
                await self.process(client, queue, doc_path)
            except PageError as exc:
                self.stats.failed += 1
                self.failures.append((doc_path, str(exc)))
                await self.log(f"  ! {doc_path}: {exc}")
            except Exception as exc:  # pragma: no cover - defensive
                self.stats.failed += 1
                self.failures.append((doc_path, repr(exc)))
                await self.log(f"  ! {doc_path}: {exc!r}")
            finally:
                queue.task_done()

    async def process(self, client: httpx.AsyncClient, queue: asyncio.Queue[str], doc_path: str) -> None:
        props = await self.fetch(client, doc_path)
        page = render_page(
            doc_path,
            props,
            lang=self.lang,
            version=self.args.version,
            keep_absolute=self.args.absolute_links,
            with_front_matter=not self.args.no_front_matter,
            index_paths=self.index_paths,
            known_paths=self.known_paths,
        )
        target = self.out / page.out_file
        changed = self.write(target, page.markdown)

        async with self._lock:
            self._done += 1
            done, total = self._done, self._total
            self.manifest.append(
                {
                    "doc_path": doc_path,
                    "url": doc_path_to_url(doc_path, self.args.version),
                    "file": page.out_file,
                    "title": page.title,
                    "description": page.description,
                    "source_path": page.source_path,
                    "vcs_url": page.vcs_url,
                    "bytes": len(page.markdown.encode("utf-8")),
                }
            )
            self.images.update(page.images)
            self.image_fallbacks.update(page.image_fallbacks)
            for url in page.images:
                self.image_pages.setdefault(url, set()).add(page.out_file)
            if self.args.follow_links:
                for link in page.links:
                    target_path = link.split("#")[0]
                    if not target_path or posixpath.splitext(target_path)[1]:
                        continue
                    if target_path in self.seen or not self.selected(target_path):
                        continue
                    self.seen.add(target_path)
                    self._total += 1
                    queue.put_nowait(target_path)

        mark = "+" if changed else "="
        await self.log(f"  {mark} [{done}/{total}] {page.out_file}")


# --------------------------------------------------------------------------- #
# Post-processing
# --------------------------------------------------------------------------- #

_MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")


def check_links(out: Path, files: Iterable[str]) -> list[dict[str, str]]:
    """Report relative links that do not resolve to a file we wrote."""
    broken: list[dict[str, str]] = []
    for rel in files:
        path = out / rel
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for match in _MD_LINK.finditer(text):
            target = unquote(match.group(1))
            if target.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:")):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                broken.append({"file": rel, "link": match.group(1)})
    return broken


async def url_ok(client: httpx.AsyncClient, url: str) -> str | None:
    """Return None if the URL resolves, otherwise a short reason why it does not."""
    try:
        resp = await client.head(url, follow_redirects=True)
        if resp.status_code == 405:  # some hosts reject HEAD
            resp = await client.get(url, follow_redirects=True)
    except httpx.HTTPError as exc:
        return repr(exc)
    return None if resp.status_code < 400 else str(resp.status_code)


async def check_images(
    client: httpx.AsyncClient,
    images: dict[str, str],
    fallbacks: dict[str, str],
    jobs: int,
) -> tuple[list[dict[str, str]], dict[str, str]]:
    """Verify every distinct image URL, falling back to the site where needed.

    Image URLs are derived from the documentation source layout rather than
    copied verbatim from the page, and that mapping does not hold for every
    single asset, so each one is checked. Anything that fails is retried at the
    URL the site itself serves; only if that fails too is the image reported
    broken.

    Returns the still-broken images and the ``url -> replacement`` map to apply.
    """
    broken: list[dict[str, str]] = []
    replacements: dict[str, str] = {}
    sem = asyncio.Semaphore(max(1, min(jobs, 8)))

    async def one(url: str, asset: str) -> None:
        async with sem:
            reason = await url_ok(client, url)
            if reason is None:
                return
            fallback = fallbacks.get(url)
            if fallback and await url_ok(client, fallback) is None:
                replacements[url] = fallback
                return
            broken.append({"asset": asset, "url": url, "status": reason})

    await asyncio.gather(*(one(url, asset) for url, asset in sorted(images.items())))
    return sorted(broken, key=lambda b: b["asset"]), replacements


def apply_replacements(out: Path, replacements: dict[str, str], pages: dict[str, set[str]]) -> int:
    """Swap image URLs in the pages that reference them."""
    affected: set[str] = set()
    for url in replacements:
        affected |= pages.get(url, set())
    for rel in sorted(affected):
        path = out / rel
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for url, replacement in replacements.items():
            text = text.replace(f"({url})", f"({replacement})")
        path.write_text(text, encoding="utf-8")
    return len(affected)


def prune(out: Path, langs: Iterable[str], keep: set[str]) -> list[str]:
    """Delete files under the crawled language roots that this run did not produce.

    Without this a mirror keeps serving pages the upstream docs have deleted.
    Only the language roots are touched, so the manifest, the TOCs and the cache
    at the top level are never at risk.
    """
    removed: list[str] = []
    for lang in langs:
        root = out / lang
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(out).as_posix()
            if rel not in keep:
                path.unlink()
                removed.append(rel)
        # Clear the directories the deletions emptied, deepest first.
        for path in sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    return removed


async def crawl_all(args: argparse.Namespace) -> int:
    out = Path(args.out).resolve()
    stats = Stats()
    languages: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    pages: list[dict[str, Any]] = []
    images: dict[str, str] = {}
    image_fallbacks: dict[str, str] = {}
    image_pages: dict[str, set[str]] = {}

    produced: set[str] = set()
    for lang in args.lang:
        print(f"\n=== {lang} ===", file=sys.stderr)
        crawler = Crawler(args, lang, stats)
        await crawler.run()
        for entry in crawler.manifest:
            entry["lang"] = lang
        pages.extend(crawler.manifest)
        produced |= {entry["file"] for entry in crawler.manifest}
        # A page that failed this run may just be a hiccup on the other end, so
        # its file stays. Pages genuinely removed upstream leave the table of
        # contents, are never requested, never fail, and are pruned normally.
        produced |= {doc_path_to_file(path) for path, _ in crawler.failures}
        images.update(crawler.images)
        image_fallbacks.update(crawler.image_fallbacks)
        for url, files in crawler.image_pages.items():
            image_pages.setdefault(url, set()).update(files)
        failures.extend({"lang": lang, "doc_path": p, "error": e} for p, e in crawler.failures)
        languages.append(
            {
                "lang": lang,
                "revision": crawler.revision,
                "page_count": len(crawler.manifest),
                "toc": f"toc.{lang}.json",
                "summary": f"SUMMARY.{lang}.md",
            }
        )

    # A partial crawl always has dangling links, so the check only means
    # something once the whole tree has been fetched.
    partial = bool(args.only or args.limit)
    if args.min_pages and len(pages) < args.min_pages:
        print(
            f"\nabort: crawled {len(pages)} pages, expected at least {args.min_pages}; "
            "leaving the existing output untouched",
            file=sys.stderr,
        )
        return 1

    removed: list[str] = []
    if args.prune:
        if partial:
            print("note: --prune ignored, this is a partial crawl", file=sys.stderr)
        else:
            removed = prune(out, args.lang, produced)

    # Sorted so the report does not depend on the order the workers finished in.
    files = sorted(p["file"] for p in pages)
    broken = check_links(out, files) if args.check_links and not partial else []
    bad_images: list[dict[str, str]] = []
    replacements: dict[str, str] = {}
    if args.check_links and images:
        print(f"\nverifying {len(images)} image links", file=sys.stderr)
        async with httpx.AsyncClient(
            headers={"User-Agent": args.user_agent}, timeout=httpx.Timeout(args.timeout)
        ) as client:
            bad_images, replacements = await check_images(client, images, image_fallbacks, args.jobs)
        if replacements:
            touched = apply_replacements(out, replacements, image_pages)
            print(
                f"→ {len(replacements)} images not in the source repo, "
                f"linked at the site instead ({touched} pages updated)",
                file=sys.stderr,
            )

    index = {
        "site": DOCS_BASE,
        "version": args.version,
        "languages": languages,
        # No crawl timestamp: it would make every re-scrape a change even when
        # the documentation itself is untouched.
        "page_count": len(pages),
        "pages": sorted(pages, key=lambda m: (m["lang"], m["doc_path"])),
        "image_count": len(images),
        "images_linked_at_site": sorted(images[url] for url in replacements),
        "failures": sorted(failures, key=lambda f: (f["lang"], f["doc_path"])),
        "broken_links": broken,
        "broken_images": bad_images,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"\ndone: {len(pages)} pages "
        f"(fetched {stats.fetched}, cached {stats.cached}, written {stats.written}, "
        f"unchanged {stats.unchanged}, throttled {stats.throttled}, failed {stats.failed}) → {out}",
        file=sys.stderr,
    )
    if removed:
        print(f"pruned {len(removed)} stale files:", file=sys.stderr)
        for rel in removed[:20]:
            print(f"  - {rel}", file=sys.stderr)
    if broken:
        print(f"broken internal links: {len(broken)} (see index.json)", file=sys.stderr)
    if bad_images:
        print(f"broken image links: {len(bad_images)} (see index.json)", file=sys.stderr)
        for img in bad_images[:10]:
            print(f"  - {img['asset']}: {img['status']}", file=sys.stderr)
    if failures:
        print(f"failures ({len(failures)}):", file=sys.stderr)
        for f in failures[:20]:
            print(f"  - [{f['lang']}] {f['doc_path']}: {f['error'].splitlines()[0]}", file=sys.stderr)
    return 1 if (failures and args.strict) else 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Crawl ydb.tech/docs into structured Markdown files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--version", default="v26.1", help="documentation version (e.g. v26.1, main)")
    p.add_argument(
        "--lang",
        action="append",
        choices=["en", "ru", "all"],
        help="documentation language; repeatable, or 'all' for every language (default: en)",
    )
    p.add_argument("-o", "--out", default="ydb-docs-md", help="output directory")
    p.add_argument("-j", "--jobs", type=int, default=8, help="concurrent requests")
    p.add_argument("--delay", type=float, default=0.0, help="seconds to sleep after each fetch")
    p.add_argument("--timeout", type=float, default=30.0, help="per-request timeout, seconds")
    p.add_argument("--retries", type=int, default=3, help="retries per page")
    p.add_argument("--limit", type=int, default=0, help="stop after N pages (0 = no limit)")
    p.add_argument(
        "--only",
        action="append",
        metavar="GLOB",
        help="only crawl paths matching this glob, relative to the language root (e.g. 'yql/**'); repeatable",
    )
    p.add_argument("--refresh", action="store_true", help="ignore the HTTP cache and refetch everything")
    p.add_argument("--cache-dir", default=None, help="cache location (default: <out>/.cache)")
    p.add_argument(
        "--no-follow-links",
        dest="follow_links",
        action="store_false",
        help="only crawl pages listed in the table of contents",
    )
    p.add_argument(
        "--no-front-matter",
        action="store_true",
        help="write bare Markdown without the YAML front matter block",
    )
    p.add_argument(
        "--absolute-links",
        action="store_true",
        help="keep links pointing at ydb.tech instead of rewriting them to local .md files",
    )
    p.add_argument(
        "--prune",
        action="store_true",
        help="delete files under the crawled language roots that this run did not produce, "
        "so pages removed upstream disappear from the mirror (ignored for partial crawls)",
    )
    p.add_argument(
        "--min-pages",
        type=int,
        default=0,
        help="abort without touching the output if fewer than N pages were crawled",
    )
    p.add_argument(
        "--no-check-links",
        dest="check_links",
        action="store_false",
        help="skip the post-crawl internal link check",
    )
    p.add_argument("--strict", action="store_true", help="exit non-zero if any page failed")
    p.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent header")
    args = p.parse_args(argv)
    langs = args.lang or ["en"]
    args.lang = ALL_LANGS if "all" in langs else list(dict.fromkeys(langs))
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    started = time.monotonic()
    try:
        code = asyncio.run(crawl_all(args))
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130
    print(f"elapsed: {time.monotonic() - started:.1f}s", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
