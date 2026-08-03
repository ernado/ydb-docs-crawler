---
title: "ORDER BY"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/order_by?version=v26.1"
doc_path: "en/yql/reference/syntax/select/order_by"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/order_by.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/order_by.md"
description: "Sorting the SELECT result using a comma-separated list of sorting criteria. As a criteria, you can use a column value or an expression on columns. Ordering by c"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ORDER BY

Sorting the `SELECT` result using a comma-separated list of sorting criteria. As a criteria, you can use a column value or an expression on columns. Ordering by column sequence number is not supported (`ORDER BY N` where `N` is a number).

Each criteria can be followed by the sorting direction:

- `ASC`: Sorting in the ascending order. Applied by default.
- `DESC`: Sorting in the descending order.

Multiple sorting criteria will be applied left-to-right.

## Example

```yql
SELECT key, string_column
FROM my_table
ORDER BY key DESC, LENGTH(string_column) ASC;
```

You can also use `ORDER BY` for [window functions](window.md).
