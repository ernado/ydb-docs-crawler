---
title: "REPLACE INTO"
url: "https://ydb.tech/docs/en/yql/reference/syntax/replace_into?version=v26.1"
doc_path: "en/yql/reference/syntax/replace_into"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/replace_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/replace_into.md"
description: "Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# REPLACE INTO

> [!WARNING]
> Currently, mixing [column-oriented tables](../../../concepts/glossary.md#column-oriented-table) and [row-oriented tables](../../../concepts/glossary.md#row-oriented-table) in a single transaction is supported only if the transaction performs read operations; no writes are allowed. Support for read-write transactions involving both table types is under development.
>
> If a write transaction includes both types of tables, it fails with the following error: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Saves data to a table, overwriting the rows based on the primary key. If the given primary key is missing, a new row is added to the table. If the given `PRIMARY_KEY` exists, the row is overwritten. The values of columns not involved in the operation are replaced by their default values.

> [!NOTE]
> Unlike [`INSERT INTO`](insert_into.md) and [`UPDATE`](update.md), the queries [`UPSERT INTO`](upsert_into.md) and `REPLACE INTO` don't need to pre-fetch the data, hence they run faster.

## Examples

- Setting values for `REPLACE INTO` using `VALUES`.

  ```yql
  REPLACE INTO my_table (Key1, Key2, Value2) VALUES
      (1u, "One", 101),
      (2u, "Two", 102);
  COMMIT;
  ```

- Fetching values for `REPLACE INTO` using a `SELECT`.

  ```yql
  REPLACE INTO my_table
  SELECT Key AS Key1, "Empty" AS Key2, Value AS Value1
  FROM my_table1;
  COMMIT;
  ```
