---
title: "UPSERT INTO"
url: "https://ydb.tech/docs/en/yql/reference/syntax/upsert_into?version=v26.1"
doc_path: "en/yql/reference/syntax/upsert_into"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/upsert_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/upsert_into.md"
description: "Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# UPSERT INTO

> [!WARNING]
> Currently, mixing [column-oriented tables](../../../concepts/glossary.md#column-oriented-table) and [row-oriented tables](../../../concepts/glossary.md#row-oriented-table) in a single transaction is supported only if the transaction performs read operations; no writes are allowed. Support for read-write transactions involving both table types is under development.
>
> If a write transaction includes both types of tables, it fails with the following error: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

UPSERT (which stands for UPDATE or INSERT) updates or inserts multiple rows to a table based on a comparison by the primary key. Missing rows are added. For the existing rows, the values of the specified columns are updated, but the values of the other columns are preserved.

`UPSERT` and [`REPLACE`](replace_into.md) are data modification operations that don't require a prefetch and run faster and cheaper than other operations because of that.

Column mapping when using `UPSERT INTO ... SELECT` is done by names. Use `AS` to fetch a column with the desired name in `SELECT`.

## Examples

```yql
UPSERT INTO my_table
SELECT pk_column, data_column1, col24 as data_column3 FROM other_table
```

```yql
UPSERT INTO my_table ( pk_column1, pk_column2, data_column2, data_column5 )
VALUES ( 1, 10, 'Some text', Date('2021-10-07')),
       ( 2, 10, 'Some text', Date('2021-10-08'))
```

## UPSERT INTO ... RETURNING {#upsert-into-returning-{upsert-into-returning}}

Inserts or updates a row and returns their values in a single operation. It allows to retrieve information about the affected row in one query, eliminating the need for an additional SELECT statement.

### Examples {#examples1}

- Return all values of modified row

```yql
UPSERT INTO orders (order_id, status, amount)
VALUES (1001, 'shipped', 500)
RETURNING *;
```

- Return specific columns

```yql
UPSERT INTO users (user_id, name, email)
VALUES (42, 'John Doe', 'john@example.com')
RETURNING user_id, email;
```
