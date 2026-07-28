# YDB docs → Markdown

`crawl_ydb_docs.py` scrapes <https://ydb.tech/docs> into a tree of structured Markdown
files. Re-run it any time; it is incremental and only rewrites what changed.

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
| `--no-assets` | skip image downloads |
| `--no-front-matter` | plain Markdown without the YAML header |
| `--absolute-links` | keep links pointing at ydb.tech instead of local `.md` files |
| `--no-follow-links` | only crawl what the table of contents lists |
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

Links are rewritten to relative `.md` paths and images are downloaded next to
the pages that use them, mirroring the upstream repository layout.

## Output

```
ydb-docs-md/
  en/…/*.md          one file per page (index.md for section landing pages)
  en/…/_assets/*     images
  ru/…               same for Russian
  SUMMARY.en.md      the table of contents as a nested link list
  toc.en.json        the raw TOC
  index.json         manifest: every page, its URL, title, upstream source path,
                     plus crawl failures and broken internal links
  .cache/            per-revision page cache; delete it or pass --refresh to bust
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

## Known upstream breakage

A handful of pages and images 404 on ydb.tech itself (`en/concepts/topic`,
`maintenance/manual/static-config`, the DBeaver plugin screenshots, a few
Russian SDK recipes). They are reported under `failures` and `broken_links` in
`index.json` and are not crawler bugs.

## License

Apache-2.0. See [LICENSE](LICENSE).

The crawled documentation itself belongs to the YDB project and stays under its
own license.
