---
title: "BATCH UPDATE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/batch-update?version=v26.1"
doc_path: "en/yql/reference/syntax/batch-update"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/batch-update.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/batch-update.md"
description: "Tip. Before diving into BATCH UPDATE, it is recommended to familiarize yourself with the standard UPDATE."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# BATCH UPDATE

> [!TIP]
> Before diving into `BATCH UPDATE`, it is recommended to familiarize yourself with the standard [UPDATE](update.md).

`BATCH UPDATE` allows to update records in large tables while minimizing the risk of lock invalidation and transaction rollback by weakening guarantees. Specifically, data updates are performed as a series of transactions for each [partition](../../../concepts/datamodel/table.md#partitioning) of the specified table separately, processing 10 000 rows per iteration. Each query processes up to 10 partitions concurrently.

This query, like the standard `UPDATE`, executes synchronously and returns a status. If an error occurs or the client disconnects, the data update stops, and the applied changes are not rolled back.

The semantics are inherited from the standard `UPDATE` with the following restrictions:

- Supported only for [row-oriented tables](../../../concepts/glossary.md#row-oriented-table).
- Supported only for queries with [implicit transaction control](../../../concepts/transactions.md#implicit).
- Only idempotent updates are supported: expressions following `SET` should not depend on the current values of the columns being modified.
- The use of subqueries and multiple statements in a single query is prohibited.
- The `RETURNING` clause is unavailable.

## Example

```yql
BATCH UPDATE my_table
SET Value1 = "foo", Value2 = 0
WHERE Key1 > 1;
```
