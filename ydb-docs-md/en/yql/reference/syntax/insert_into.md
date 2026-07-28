---
title: "INSERT INTO"
url: "https://ydb.tech/docs/en/yql/reference/syntax/insert_into?version=v26.1"
doc_path: "en/yql/reference/syntax/insert_into"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/insert_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/insert_into.md"
description: "Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# INSERT INTO

> [!WARNING]
> Currently, mixing [column-oriented tables](../../../concepts/glossary.md#column-oriented-table) and [row-oriented tables](../../../concepts/glossary.md#row-oriented-table) in a single transaction is supported only if the transaction performs read operations; no writes are allowed. Support for read-write transactions involving both table types is under development.
>
> If a write transaction includes both types of tables, it fails with the following error: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Adds rows to the table. If you try to insert a row into a table with an existing primary key value, the operation fails with the `PRECONDITION_FAILED` error code and the `Operation aborted due to constraint violation: insert_pk` message returned.

`INSERT INTO` lets you perform the following operations:

- Adding constant values using [`VALUES`](values.md).

  ```yql
  INSERT INTO my_table (Key1, Key2, Value1, Value2)
  VALUES (345987,'ydb', 'Pied piper', 1414);
  COMMIT;
  ```

  ```yql
  INSERT INTO my_table (key, value)
  VALUES ("foo", 1), ("bar", 2);
  ```

- Saving the `SELECT` result.

  ```yql
  INSERT INTO my_table
  SELECT Key AS Key1, "Empty" AS Key2, Value AS Value1
  FROM my_table1;
  ```

When working with [external file data sources](../../../concepts/datamodel/external_data_source.md), you can specify additional parameters:

- `FORMAT` — stored data format in file storage for [federated queries](../../../concepts/query_execution/federated_query/s3/formats.md). Allowed values: `csv_with_names`, `tsv_with_names`, `json_list`, `json_each_row`, `json_as_string`, `parquet`, `raw`.
- `COMPRESSION` — file compression in file storage for [federated queries](../../../concepts/query_execution/federated_query/s3/formats.md#compression). Allowed values: [gzip](https://en.wikipedia.org/wiki/Gzip), [zstd](https://en.wikipedia.org/wiki/Zstd), [lz4](https://en.wikipedia.org/wiki/LZ4), [brotli](https://en.wikipedia.org/wiki/Brotli), [bzip2](https://en.wikipedia.org/wiki/Bzip2), [xz](<https://en.wikipedia.org/wiki/XZ_(compression_algorithm)>).
- `PARTITIONED_BY` — list of [partition columns](../../../concepts/query_execution/federated_query/s3/partitioning.md) for data in file storage in federated queries. Lists columns in the order they appear in the file layout.
- `projection.enabled` — flag to enable [extended data partitioning](../../../concepts/query_execution/federated_query/s3/partition_projection.md). Allowed values: `true`, `false`.
- `projection.<field_name>.type` — field type for [extended data partitioning](../../../concepts/query_execution/federated_query/s3/partition_projection.md). Allowed values: `integer`, `enum`, `date`.
- `projection.<field_name>.<options>` — extended properties of a field for [extended data partitioning](../../../concepts/query_execution/federated_query/s3/partition_projection.md).

## Example

```yql
INSERT INTO `connection`.`test/`
WITH
(
  FORMAT = "csv_with_names"
)
SELECT
    "value" AS value, "name" AS name
```

Where:

- `connection` — name of the connection to S3 (Yandex Object Storage).
- `test/` — path inside the bucket where data is written. Files are created with random names.

## INSERT INTO ... RETURNING {#insert-into-returning-{insert-into-returning}}

Inserts rows and returns their values in a single operation. It allows to retrieve data from the rows being inserted without needing to perform a separate SELECT query afterwards.

### Examples

- Return all values of modified rows

```yql
INSERT INTO some_table (id, year, color, price)
VALUES (1103, 2023, 'blue', 400)
RETURNING *;
```

- Return specific columns

```yql
INSERT INTO some_table (id, color, price)
VALUES 
    (1101, 'red', 200),
    (1102, 'green', 300)
RETURNING id, price;
```
