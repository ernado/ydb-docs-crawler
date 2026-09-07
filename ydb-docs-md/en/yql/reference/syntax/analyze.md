---
title: "ANALYZE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/analyze?version=v26.1"
doc_path: "en/yql/reference/syntax/analyze"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/analyze.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/analyze.md"
description: "ANALYZE forces the collection of statistics for YDB cost-based optimizer. Syntax. ANALYZE <path_to_table> [ (<column_name> [,...]) ]."
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# ANALYZE

`ANALYZE` forces the collection of statistics for [YDB cost-based optimizer](../../../concepts/query_execution/optimizer.md).

## Syntax

```yql
ANALYZE <path_to_table> [ (<column_name> [, ...]) ]
```

This command forces the synchronous collection of table statistics and column statistics for the specified columns or for all columns if none are specified. `ANALYZE` returns once all the requested statistics have been collected and are up to date.

- `path_to_table` — the path to the table for which statistics should be collected.
- `column_name` — collect column statistics only for the specified columns of the table.

The current set of statistics is described in [Statistics for the Cost-Based Optimizer](../../../concepts/query_execution/optimizer.md#statistics).
