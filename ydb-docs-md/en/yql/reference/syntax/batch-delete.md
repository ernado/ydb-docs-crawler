---
title: "BATCH DELETE FROM"
url: "https://ydb.tech/docs/en/yql/reference/syntax/batch-delete?version=v26.1"
doc_path: "en/yql/reference/syntax/batch-delete"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/batch-delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/batch-delete.md"
description: "Tip. Before diving into BATCH DELETE FROM, it is recommended to familiarize yourself with the standard DELETE FROM."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# BATCH DELETE FROM

> [!TIP]
> Before diving into `BATCH DELETE FROM`, it is recommended to familiarize yourself with the standard [DELETE FROM](delete.md).

`BATCH DELETE FROM` allows to delete records in large tables while minimizing the risk of lock invalidation and transaction rollback by weakening guarantees. Specifically, data deletion is performed as a series of transactions for each [partition](../../../concepts/datamodel/table.md#partitioning) of the specified table separately, processing 10 000 rows per iteration. Each query processes up to 10 partitions concurrently.

This query, like the standard `DELETE FROM`, executes synchronously and returns a status. If an error occurs or the client disconnects, data deletion stops, and applied changes are not rolled back.

The semantics are inherited from the standard `DELETE FROM` with the following restrictions:

- Supported only for [row-oriented tables](../../../concepts/glossary.md#row-oriented-table).
- Supported only for queries with [implicit transaction control](../../../concepts/transactions.md#implicit).
- The use of subqueries and multiple statements in a single query is prohibited.
- The `RETURNING` clause is unavailable.

## Example

```yql
BATCH DELETE FROM my_table
WHERE Key1 > 1 AND Key2 >= "One";
```
