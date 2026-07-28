---
title: "UPDATE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/update?version=v26.1"
doc_path: "en/yql/reference/syntax/update"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/update.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/update.md"
description: "Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# UPDATE

> [!WARNING]
> Currently, mixing [column-oriented tables](../../../concepts/glossary.md#column-oriented-table) and [row-oriented tables](../../../concepts/glossary.md#row-oriented-table) in a single transaction is supported only if the transaction performs read operations; no writes are allowed. Support for read-write transactions involving both table types is under development.
>
> If a write transaction includes both types of tables, it fails with the following error: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Updates the data in the table. After the `SET` keyword, enter the columns where you want to update values and the new values themselves. The list of rows is defined by the `WHERE` clause. If `WHERE` is omitted, the updates are applied to all the rows of the table.

`UPDATE` can't change the value of the primary key columns.

## Example

```yql
UPDATE my_table
SET Value1 = YQL::ToString(Value2 + 1), Value2 = Value2 - 1
WHERE Key1 > 1;
```

## UPDATE ON

Updates the data in the table based on the results of a subquery. The set of columns returned by the subquery must be a subset of the table's columns being updated, and all columns of the table's primary key must be present in the returned columns. The data types of the columns returned by the subquery must match the data types of the corresponding columns in the table.

The primary key value is used to search for the rows being updated. For each row found, the values of the non-key columns is replaced with the values returned in the corresponding row of the result of the subquery. The values of the table columns that are missing in the returned columns of the subquery remain unchanged.

### Example {#example1}

```yql
$to_update = (
    SELECT Key, SubKey, "Updated" AS Value FROM my_table
    WHERE Key = 1
);

UPDATE my_table ON
SELECT * FROM $to_update;
```

## UPDATE ... RETURNING {#update-returning-{update-returning}}

Updates rows and returns their new values in a single operation. It allows to retrieve information about the updated rows in one query, eliminating the need for an additional SELECT statement.

### Examples

- Return all values of modified rows

```yql
UPDATE orders
SET status = 'shipped'
WHERE order_date < '2023-01-01'
RETURNING *;
```

- Return specific columns

```yql
UPDATE products
SET price = price * 0.9 
WHERE category = 'Electronics'
RETURNING product_id, name, price AS new_price;
```

## See also

- [BATCH UPDATE](batch-update.md)
