"""Unit tests for the HTML -> Markdown conversion and path handling."""

from __future__ import annotations

import json

import pytest

from crawl_ydb_docs import (
    LinkContext,
    MarkdownConverter,
    PageError,
    doc_path_to_file,
    doc_path_to_url,
    extract_data,
    front_matter,
    norm_doc_path,
    page_props,
    render_summary,
    strip_asset_prefix,
    toc_index_paths,
    toc_paths,
)


def convert(html: str, doc_path: str = "en/concepts/glossary", **kwargs) -> str:
    ctx = LinkContext(doc_path=doc_path, lang=doc_path.split("/")[0], **kwargs)
    return MarkdownConverter(ctx).convert(html)


# --------------------------------------------------------------------------- #
# paths
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("en/concepts/glossary", "en/concepts/glossary"),
        ("/docs/en/concepts/", "en/concepts/"),
        ("https://ydb.tech/docs/en/quickstart", "en/quickstart"),
        ("en/concepts/glossary.html", "en/concepts/glossary"),
        ("en/concepts/index.html", "en/concepts/"),
    ],
)
def test_norm_doc_path(raw: str, expected: str) -> None:
    assert norm_doc_path(raw) == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("en/quickstart", "en/quickstart.md"),
        ("en/concepts/", "en/concepts/index.md"),
        ("en/", "en/index.md"),
        ("en/_assets/pic.png", "en/_assets/pic.png"),
    ],
)
def test_doc_path_to_file(path: str, expected: str) -> None:
    assert doc_path_to_file(path) == expected


def test_doc_path_to_url_adds_version() -> None:
    assert doc_path_to_url("en/quickstart", "v26.1") == "https://ydb.tech/docs/en/quickstart?version=v26.1"
    assert doc_path_to_url("en/", None) == "https://ydb.tech/docs/en/"


def test_strip_asset_prefix() -> None:
    raw = "docs-assets/ydb-platform--ydb/rev/abc123/en/concepts/_assets/pic.png"
    assert strip_asset_prefix(raw) == "en/concepts/_assets/pic.png"
    assert strip_asset_prefix("en/_assets/pic.png") == "en/_assets/pic.png"


# --------------------------------------------------------------------------- #
# __DATA__ payload
# --------------------------------------------------------------------------- #


def test_extract_data_roundtrip() -> None:
    payload = {"props": {"pageProps": {"data": {"title": "T", "html": "<p>hi</p>"}}}}
    page = f"<html><script>__DATA__ = {json.dumps(payload)};\n__LOADED_PAGES = [];</script></html>"
    assert page_props(extract_data(page))["title"] == "T"


def test_extract_data_without_payload() -> None:
    with pytest.raises(PageError):
        extract_data("<html><body>404</body></html>")


def test_page_props_rejects_error_page() -> None:
    page = '<script>__DATA__ = {"err": {"code": 404}, "props": {}};\n__LOADED_PAGES = [];</script>'
    with pytest.raises(PageError):
        page_props(extract_data(page))


# --------------------------------------------------------------------------- #
# conversion
# --------------------------------------------------------------------------- #


def test_heading_drops_anchor_link_and_keeps_custom_id() -> None:
    html = (
        '<h2 id="key-terminology">'
        '<a href="en/concepts/glossary#key-terminology" class="yfm-anchor" aria-hidden="true"></a>'
        "Key terminology</h2>"
        '<h2 id="install">Install and start YDB</h2>'
    )
    md = convert(html)
    assert "## Key terminology" in md
    assert "yfm-anchor" not in md
    # The slug matches, so no explicit anchor is needed...
    assert "{#key-terminology}" not in md
    # ...but a mismatching id must be preserved for in-page links.
    assert "## Install and start YDB {#install}" in md


def test_code_block_keeps_language_and_strips_highlighting() -> None:
    html = (
        '<div class="yfm-code-floating-container">'
        '<pre><code class="hljs bash"><span class="hljs-built_in">mkdir</span> ~/ydbd</code></pre>'
        '<div class="yfm-code-floating"><button>copy</button></div>'
        "</div>"
    )
    assert convert(html) == "```bash\nmkdir ~/ydbd\n```"


def test_note_becomes_github_alert() -> None:
    html = (
        '<div class="yfm-note yfm-accent-warning" note-type="warning">'
        '<p class="yfm-note-title">Attention!</p>'
        '<div class="yfm-note-content"><p>Mind the gap.</p></div></div>'
    )
    assert convert(html) == "> [!WARNING]\n> Mind the gap."


def test_note_keeps_custom_title() -> None:
    html = (
        '<div class="yfm-note yfm-accent-info" note-type="info">'
        '<p class="yfm-note-title">Size limits</p>'
        '<div class="yfm-note-content"><p>Body.</p></div></div>'
    )
    assert convert(html) == "> [!NOTE]\n> **Size limits**\n>\n> Body."


def test_tabs_become_yfm_list_tabs() -> None:
    html = (
        '<div class="yfm-tabs">'
        '<div class="yfm-tab-list"><div class="yfm-tab yfm-tab-group">Linux</div></div>'
        '<div class="yfm-tab-panel" data-title="Linux"><p>Run it.</p></div>'
        '<div class="yfm-tab-panel" data-title="Docker"><p>Pull it.</p></div>'
        "</div>"
    )
    md = convert(html)
    assert md.startswith("{% list tabs %}")
    assert md.endswith("{% endlist %}")
    assert "- Linux\n\n  Run it." in md
    assert "- Docker\n\n  Pull it." in md


def test_cut_becomes_details() -> None:
    html = (
        '<div class="yfm-cut"><div class="yfm-cut-title">More</div>'
        '<div class="yfm-cut-content"><p>Hidden.</p></div></div>'
    )
    assert convert(html) == "<details>\n<summary>More</summary>\n\nHidden.\n\n</details>"


def test_table_becomes_gfm() -> None:
    html = (
        "<table><thead><tr><th>Name</th><th>Description</th></tr></thead>"
        "<tbody><tr><td><code>--timeout</code></td><td>Deadline | limit</td></tr></tbody></table>"
    )
    assert convert(html) == ("| Name | Description |\n| --- | --- |\n| `--timeout` | Deadline \\| limit |")


def test_nested_lists_are_indented() -> None:
    html = "<ol><li><p>Outer</p><ul><li>Inner</li></ul></li></ol>"
    assert convert(html) == "1. Outer\n\n   - Inner"


def test_intra_word_underscores_are_not_escaped() -> None:
    assert convert("<p>Use x86_64 Linux</p>") == "Use x86_64 Linux"


def test_inline_code_with_backticks() -> None:
    assert convert("<p><code>a`b</code></p>") == "``a`b``"


# --------------------------------------------------------------------------- #
# link rewriting
# --------------------------------------------------------------------------- #


def test_links_are_rewritten_to_relative_markdown() -> None:
    html = '<p><a href="en/quickstart#install">Quick start</a></p>'
    assert convert(html) == "[Quick start](../quickstart.md#install)"


def test_external_links_are_left_alone() -> None:
    html = '<p><a href="https://example.com/x">x</a></p>'
    assert convert(html) == "[x](https://example.com/x)"


def test_section_landing_pages_resolve_to_index() -> None:
    html = '<p><a href="en/devops">DevOps</a></p>'
    md = convert(html, index_paths=frozenset({"en/devops"}))
    assert md == "[DevOps](../devops/index.md)"


def test_unrooted_link_prefers_a_known_page_relative_target() -> None:
    html = '<p><a href="topology">Topology</a></p>'
    md = convert(html, known_paths=frozenset({"en/concepts/topology"}))
    assert md == "[Topology](topology.md)"


def test_unrooted_link_falls_back_to_the_language_root() -> None:
    # ydb.tech itself serves this one as a broken root-relative link.
    html = '<p><a href="concepts/datamodel/topic">Topics</a></p>'
    md = convert(
        html,
        doc_path="en/yql/reference/syntax/alter-topic",
        known_paths=frozenset({"en/concepts/datamodel/topic"}),
    )
    assert md == "[Topics](../../../concepts/datamodel/topic.md)"


def test_images_are_collected_and_rewritten() -> None:
    ctx = LinkContext(doc_path="en/quickstart", lang="en")
    html = '<p><img src="docs-assets/svc/rev/abc/en/_assets/ui.png" alt="Web UI"></p>'
    md = MarkdownConverter(ctx).convert(html)
    assert md == "![Web UI](_assets/ui.png)"
    assert ctx.assets == {"en/_assets/ui.png": "docs-assets/svc/rev/abc/en/_assets/ui.png"}


def test_absolute_links_mode_keeps_the_site_urls() -> None:
    html = '<p><a href="en/quickstart">Quick start</a></p>'
    md = convert(html, keep_absolute=True)
    assert md == "[Quick start](https://ydb.tech/docs/en/quickstart)"


# --------------------------------------------------------------------------- #
# toc / front matter
# --------------------------------------------------------------------------- #


TOC = {
    "title": "YDB",
    "items": [
        {"name": "Quick start", "href": "en/quickstart"},
        {
            "name": "Concepts",
            "href": "en/concepts/",
            "items": [{"name": "Glossary", "href": "en/concepts/glossary"}],
        },
        {"name": 2024, "href": "en/public-materials/videos/2024"},
    ],
}


def test_toc_paths_are_flattened_and_deduped() -> None:
    assert toc_paths(TOC) == [
        "en/quickstart",
        "en/concepts/",
        "en/concepts/glossary",
        "en/public-materials/videos/2024",
    ]


def test_toc_index_paths() -> None:
    assert toc_index_paths(TOC) == frozenset({"en/concepts"})


def test_render_summary_nests_and_stringifies_numeric_names() -> None:
    summary = render_summary(TOC, "en")
    assert "- [Quick start](en/quickstart.md)" in summary
    assert "  - [Glossary](en/concepts/glossary.md)" in summary
    assert "- [2024](en/public-materials/videos/2024.md)" in summary


def test_front_matter_quotes_and_skips_empty_values() -> None:
    fm = front_matter({"title": 'He said "hi"', "empty": None, "list": ["a", "b"]})
    assert fm == '---\ntitle: "He said \\"hi\\""\nlist:\n  - "a"\n  - "b"\n---'
