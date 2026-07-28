---
title: "Importing and exporting data with federated queries"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/import_and_export?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/import_and_export"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/import_and_export.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/import_and_export.md"
description: "Note. When importing or exporting data to or from S3 in Parquet format, take into account the YQL and Apache Arrow type mapping. Importing data."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Importing and exporting data with federated queries

> [!NOTE]
> When importing or exporting data to or from S3 in Parquet format, take into account the [YQL and Apache Arrow type mapping](s3/arrow_types_mapping.md).

## Importing data {#import}

Federated queries let you import data from connected external sources into YDB tables. To import data, use a read query from an [external data source](../../datamodel/external_data_source.md) or [external table](../../datamodel/external_table.md) and write into a YDB table.

For column-oriented tables, massively parallel import from an external source is supported when using `UPSERT` and `INSERT`: several worker threads read data from the external source in parallel and write into the table. For row-oriented tables, this functionality is under development.

| Operation | Writes to [row-oriented tables](../../datamodel/table.md#row-oriented-tables) | Writes to [column-oriented tables](../../datamodel/table.md#column-oriented-tables) |
| --- | --- | --- |
| [UPSERT](../../../yql/reference/syntax/upsert_into.md) | single-threaded | parallel |
| [REPLACE](../../../yql/reference/syntax/replace_into.md) | single-threaded | parallel |
| [INSERT](../../../yql/reference/syntax/insert_into.md) | single-threaded | parallel |

> [!TIP]
> The recommended import options using federated queries are `UPSERT` and `REPLACE` — the import path is heavily optimized for them.

Example: import data from a PostgreSQL table into a YDB table:

```yql
UPSERT INTO target_table
SELECT * FROM postgresql_datasource.source_table
```

For more on creating external data sources and external tables, and on read queries, see:

- [ClickHouse](clickhouse.md#query)
- [Greenplum](greenplum.md#query)
- [Microsoft SQL Server](ms_sql_server.md#query)
- [MySQL](mysql.md#query)
- [PostgreSQL](postgresql.md#query)
- [S3](s3/external_table.md)
- [YDB](ydb.md#query)

## Exporting data {#export}

Currently, exporting data with federated queries is supported only for S3-compatible storage; see [Exporting data to S3 object storage](s3/write_data.md#export-to-s3).
