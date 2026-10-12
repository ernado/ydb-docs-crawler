---
title: "WHERE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/where?version=v26.1"
doc_path: "en/yql/reference/syntax/select/where"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/where.md"
description: "Filtering rows in the SELECT result based on a condition in row-oriented or column-oriented. Example. SELECT key FROM my_table WHERE value > 0; Warning."
revision: "665607947c838b4f199a3b30499a54d29413ee4f"
---

# WHERE

Filtering rows in the `SELECT` result based on a condition in [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) or [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables).

## Example

```yql
SELECT key FROM my_table
WHERE value > 0;
```

> [!WARNING]
> Correlated subqueries in `WHERE` are not supported: a subquery cannot refer to columns or table aliases from an outer query. To select rows that have matching rows in another table, use [`LEFT SEMI JOIN`](../correlated-subqueries.md#exists). To select rows without matches, use [`LEFT ONLY JOIN`](../correlated-subqueries.md#not-exists).
