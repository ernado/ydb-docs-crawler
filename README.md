# YDB docs → Markdown

`crawl_ydb_docs.py` scrapes <https://ydb.tech/docs> into a tree of structured Markdown
files. Re-run it any time; it is incremental and only rewrites what changed.

The result is committed to this repository under [`ydb-docs-md/`](ydb-docs-md), and
a [weekly workflow](.github/workflows/scrape.yml) re-scrapes and commits the diff.

## Usage

```sh
uv run crawl_ydb_docs.py --lang all            # en + ru, version v26.1 → ./ydb-docs-md
uv run crawl_ydb_docs.py                       # en only
uv run crawl_ydb_docs.py --version main
uv run crawl_ydb_docs.py --only 'yql/**' --refresh
```

The script carries its own dependencies via PEP 723 inline metadata, so `uv run`
needs nothing installed beforehand. `./crawl_ydb_docs.py` works too (shebang).

Useful flags — `--help` lists them all:

| Flag | Effect |
| --- | --- |
| `--lang en\|ru\|all` | repeatable; default `en` |
| `--version v26.1` | any version the site offers (`main`, `v25.4`, …) |
| `-o, --out DIR` | output directory (default `ydb-docs-md`) |
| `-j, --jobs N` | concurrent requests (default 8) |
| `--only GLOB` | crawl a subtree, glob relative to the language root; repeatable |
| `--refresh` | ignore the on-disk cache and refetch |
| `--prune` | delete pages that vanished upstream (ignored for partial crawls) |
| `--min-pages N` | abort without touching the output if the crawl came back short |
| `--no-front-matter` | plain Markdown without the YAML header |
| `--absolute-links` | keep links pointing at ydb.tech instead of local `.md` files |
| `--no-follow-links` | only crawl what the table of contents lists |
| `--no-check-links` | skip the post-crawl link and image verification |
| `--strict` | exit non-zero if any page failed |

## How it works

The site runs the Diplodoc/YFM viewer. Every server-rendered page embeds a
`__DATA__ = {...}` blob containing the already-rendered article HTML, the page
title, its source path in `ydb-platform/ydb`, and the **complete** table of
contents. The crawler parses that blob rather than scraping the DOM, so it gets
clean content without the site chrome and learns every page URL from the first
request.

Pages are then converted to Markdown with a converter that understands the YFM
constructs the docs use:

- `{% list tabs %}` blocks for tabbed content
- GitHub alerts (`> [!NOTE]`, `> [!WARNING]`, …) for `{% note %}` blocks
- `<details>` for cuts
- fenced code blocks with the original language, GFM tables, nested lists
- `{#anchor}` suffixes on headings whose id does not match the slug, so
  in-page links keep working

Links are rewritten to relative `.md` paths. Images are **linked, not copied** —
70 MB of screenshots do not belong in a git history. They point at the
documentation source repository:

    en/concepts/_assets/pic.png
    → https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/concepts/_assets/pic.png

That URL is stable across documentation rebuilds, whereas the site serves images
from a path containing the build SHA, which would rewrite every image link on
every rebuild. The mapping is verified rather than assumed: each distinct image
URL is checked after the crawl, and the handful that do not resolve upstream
fall back to the site's own URL (listed under `images_linked_at_site` in
`index.json`).

## Output

```
ydb-docs-md/
  en/…/*.md          one file per page (index.md for section landing pages)
  ru/…               same for Russian
  SUMMARY.en.md      the table of contents as a nested link list
  toc.en.json        the raw TOC
  index.json         manifest: every page, its URL, title, upstream source path,
                     plus crawl failures, broken links and broken images
  .cache/            per-revision page cache, not committed; --refresh busts it
```

Each file carries YAML front matter:

```yaml
---
title: "YDB glossary"
url: "https://ydb.tech/docs/en/concepts/glossary?version=v26.1"
doc_path: "en/concepts/glossary"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/glossary.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/glossary.md"
description: "…"
revision: "e9f5418…"
---
```

The pages carry no timestamp on purpose: `revision` already identifies the docs
build, so re-scraping an unchanged site produces a byte-identical tree and an
empty diff.

## Weekly re-scrape

[`scrape.yml`](.github/workflows/scrape.yml) runs every Monday and commits
whatever changed. Two properties make that safe to run unattended:

- **An unchanged site produces no commit.** Nothing in the output records the
  wall clock, so a re-scrape of the same docs revision is byte-identical.
- **A broken scrape cannot destroy the mirror.** `--min-pages 1200` aborts
  before writing anything if the crawl comes back short, `--prune` only runs
  after that guard passes, and a page whose fetch failed is never pruned — a
  hiccup at the other end must not delete good documentation.

Rate limiting gets its own retry budget (honouring `Retry-After`) so a 429 is
waited out rather than recorded as the page's status, which would otherwise show
up as phantom churn in the manifest.

It can also be triggered by hand from the Actions tab, with a version and
language to crawl.

## Known upstream breakage

A handful of pages 404 on ydb.tech itself (`en/concepts/topic`,
`maintenance/manual/static-config`, a few Russian SDK recipes), and some pages
link to images that were never published. They are reported under `failures`,
`broken_links` and `broken_images` in `index.json` and are not crawler bugs.

## License

Apache-2.0. See [LICENSE](LICENSE).

The crawled documentation itself belongs to the YDB project and stays under its
own license.
