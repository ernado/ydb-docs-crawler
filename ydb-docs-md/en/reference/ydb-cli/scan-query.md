---
title: "Running scan queries"
url: "https://ydb.tech/docs/en/reference/ydb-cli/scan-query?version=v26.1"
doc_path: "en/reference/ydb-cli/scan-query"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/scan-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/scan-query.md"
description: "Running scan queries. Warning. This functionality is deprecated. Use standard query execution methods. See Query execution."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Running scan queries

> [!WARNING]
> This functionality is deprecated. Use standard query execution methods.
>  See [Query execution](sql.md).

To run a query via [Scan Queries](../../concepts/query_execution/scan_query.md) using YDB CLI, add the `-t scan` flag to the `ydb table query execute` command.

Run a query against the data:

```bash
ydb table query execute -t scan \
 --query "SELECT season_id, episode_id, title \
 FROM episodes \
 WHERE series_id = 1 AND season_id > 1 \
 ORDER BY season_id, episode_id \
 LIMIT 3"
```

Where:

- `--query` — query text.

Result:

```text
┌───────────┬────────────┬──────────────────────────────┐
| season_id | episode_id | title |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 1 | "The Work Outing" |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 2 | "Return of the Golden Child" |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 3 | "Moss and the German" |
└───────────┴────────────┴──────────────────────────────┘
```
