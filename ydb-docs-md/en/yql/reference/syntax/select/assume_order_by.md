---
title: "ASSUME ORDER BY"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/assume_order_by?version=v26.1"
doc_path: "en/yql/reference/syntax/select/assume_order_by"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/assume_order_by.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/assume_order_by.md"
description: "Checking that the SELECT result is sorted by the value in the specified column or multiple columns. The result of such a SELECT statement is treated as sorted,"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ASSUME ORDER BY

Checking that the `SELECT` result is sorted by the value in the specified column or multiple columns. The result of such a `SELECT` statement is treated as sorted, but without actually running a sort. Sort check is performed at the query execution stage.

As in case of `ORDER BY`, it supports setting the sort order using the keywords `ASC` (ascending order) and `DESC` (descending order). Expressions are not supported in `ASSUME ORDER BY`.

## Examples

```yql
SELECT key || "suffix" as key, -CAST(subkey as Int32) as subkey
FROM my_table
ASSUME ORDER BY key, subkey DESC;
```
