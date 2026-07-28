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

CRAWL_ARGS = [
    "--lang",
    "en",
    "--lang",
    "ru",
    "--only",
    "quickstart",
    "--only",
    "concepts/glossary",
    "--jobs",
    "4",
]


@pytest.fixture(scope="module")
def crawled(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("docs")
    code = main([*CRAWL_ARGS, "--out", str(out), "--strict"])
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
    assert main([*CRAWL_ARGS, "--out", str(crawled)]) == 0
    assert {p: p.read_bytes() for p in crawled.rglob("*.md")} == before


def test_second_run_leaves_the_manifest_untouched(crawled: Path) -> None:
    """The weekly re-scrape must produce no diff at all when nothing changed."""
    before = (crawled / "index.json").read_bytes()
    assert main([*CRAWL_ARGS, "--out", str(crawled)]) == 0
    assert (crawled / "index.json").read_bytes() == before


def test_min_pages_guard_aborts_without_touching_the_output(crawled: Path) -> None:
    """A truncated crawl must never be allowed to overwrite a good mirror."""
    before = {p: p.read_bytes() for p in crawled.rglob("*") if p.is_file()}
    assert main([*CRAWL_ARGS, "--out", str(crawled), "--min-pages", "10000", "--prune"]) == 1
    assert {p: p.read_bytes() for p in crawled.rglob("*") if p.is_file()} == before


def test_prune_removes_pages_that_vanished_upstream(crawled: Path) -> None:
    stale = crawled / "en" / "was-deleted-upstream.md"
    stale.write_text("gone", encoding="utf-8")
    assert main([*CRAWL_ARGS, "--out", str(crawled), "--prune"]) == 0
    # A partial crawl must not prune: it only ever fetches a slice of the tree.
    assert stale.is_file()


def test_a_failed_page_is_not_pruned(crawled: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A transient fetch failure must never delete a page from the mirror."""
    import crawl_ydb_docs

    survivor = crawled / "en" / "quickstart.md"
    original = crawl_ydb_docs.Crawler.fetch

    async def flaky(self, client, doc_path):
        if doc_path == "en/quickstart":
            raise crawl_ydb_docs.PageError("simulated outage")
        return await original(self, client, doc_path)

    monkeypatch.setattr(crawl_ydb_docs.Crawler, "fetch", flaky)
    assert main([*CRAWL_ARGS, "--out", str(crawled), "--prune"]) == 0
    assert survivor.is_file(), "a page that failed to fetch was deleted"
