---
title: "DISTINCT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/distinct?version=v26.1"
doc_path: "en/yql/reference/syntax/select/distinct"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/distinct.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/distinct.md"
description: "Selecting unique rows. Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DISTINCT

Selecting unique rows.

> [!NOTE]
> Applying `DISTINCT` to calculated values is not currently implemented. For this purpose, use a subquery or the clause [`GROUP BY ... AS ...`](group-by.md).

## Example

```yql
SELECT DISTINCT value -- only unique values from the table
FROM my_table;
```

The `DISTINCT` keyword can also be used to apply [aggregate functions](../../builtins/aggregation.md) only to distinct values. For more information, see the documentation for [GROUP BY](group-by.md).

Removes duplicate rows from the result. Applies after the clause [`GROUP BY ... AS ...`](group-by.md).
