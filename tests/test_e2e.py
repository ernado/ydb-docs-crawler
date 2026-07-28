"""End-to-end test: crawl a small slice of the live ydb.tech documentation.

Marked ``e2e`` because it needs network access. Run the rest with
``pytest -m "not e2e"``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from crawl_ydb_docs import main

pytestmark = pytest.mark.e2e


@pytest.fixture(scope="module")
def crawled(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("docs")
    code = main(
        [
            "--lang",
            "en",
            "--lang",
            "ru",
            "--only",
            "quickstart",
            "--only",
            "concepts/glossary",
            "--out",
            str(out),
            "--jobs",
            "4",
            "--strict",
        ]
    )
    assert code == 0, "crawl reported failures"
    return out


def test_pages_are_written_for_both_languages(crawled: Path) -> None:
    for lang in ("en", "ru"):
        page = crawled / lang / "quickstart.md"
        assert page.is_file(), f"{page} missing"
        assert page.stat().st_size > 1000


def test_front_matter_describes_the_source(crawled: Path) -> None:
    text = (crawled / "en" / "concepts" / "glossary.md").read_text(encoding="utf-8")
    head, body = text.split("---\n", 2)[1:]
    assert 'doc_path: "en/concepts/glossary"' in head
    assert 'url: "https://ydb.tech/docs/en/concepts/glossary?version=v26.1"' in head
    assert 'source_path: "en/core/concepts/glossary.md"' in head
    assert body.lstrip().startswith("# ")


def test_content_is_markdown_not_html(crawled: Path) -> None:
    text = (crawled / "en" / "quickstart.md").read_text(encoding="utf-8")
    assert "## Install and start YDB" in text
    assert "```bash" in text
    assert "{% list tabs %}" in text
    for leaked in ("<div", "<span", "yfm-anchor", "hljs"):
        assert leaked not in text, f"{leaked!r} leaked into the Markdown"


def test_links_resolve_to_files_on_disk(crawled: Path) -> None:
    text = (crawled / "en" / "quickstart.md").read_text(encoding="utf-8")
    assert "(concepts/glossary.md#cluster)" in text
    assert (crawled / "en" / "concepts" / "glossary.md").is_file()


def test_manifest_and_summary(crawled: Path) -> None:
    index = json.loads((crawled / "index.json").read_text(encoding="utf-8"))
    assert index["version"] == "v26.1"
    assert index["page_count"] == len(index["pages"]) >= 4
    assert not index["failures"]
    assert {lang["lang"] for lang in index["languages"]} == {"en", "ru"}
    assert len(index["languages"][0]["revision"]) == 40

    by_path = {page["doc_path"]: page for page in index["pages"]}
    assert by_path["en/quickstart"]["file"] == "en/quickstart.md"
    assert by_path["en/quickstart"]["title"]

    for lang in ("en", "ru"):
        summary = (crawled / f"SUMMARY.{lang}.md").read_text(encoding="utf-8")
        assert f"({lang}/concepts/glossary.md)" in summary
        assert json.loads((crawled / f"toc.{lang}.json").read_text(encoding="utf-8"))["items"]


def test_second_run_is_incremental(crawled: Path) -> None:
    """Re-running must be a no-op: same inputs, byte-identical output."""
    before = {p: p.read_bytes() for p in crawled.rglob("*.md")}
    assert (
        main(
            [
                "--lang",
                "en",
                "--lang",
                "ru",
                "--only",
                "quickstart",
                "--only",
                "concepts/glossary",
                "--out",
                str(crawled),
                "--jobs",
                "4",
            ]
        )
        == 0
    )
    assert {p: p.read_bytes() for p in crawled.rglob("*.md")} == before
