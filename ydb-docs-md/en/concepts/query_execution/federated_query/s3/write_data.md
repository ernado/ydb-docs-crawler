---
title: "Writing Data to S3 Buckets (Yandex Object Storage)"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/s3/write_data?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/s3/write_data"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/s3/write_data.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/s3/write_data.md"
description: "In YDB, you can use external connections or external tables to write data to the Yandex Object Storage bucket. Writing Data via External Connection."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Writing Data to S3 Buckets (Yandex Object Storage)

In YDB, you can use [external connections](write_data.md#connection-write) or [external tables](write_data.md#external-table-write) to write data to the Yandex Object Storage bucket.

## Writing Data via External Connection {#connection-write}

Using connections for data writing is convenient for prototyping and initial setup. The SQL expression demonstrates writing data directly to an external data source.

```yql
INSERT INTO `connection`.`test/`
WITH
(
  FORMAT = "csv_with_names"
)
SELECT
    "value" AS value, "name" AS name
```

The data will be written to the specified path. In this mode, the resulting files will not be partitioned. If you need to partition the resulting files, use writing via [external tables](write_data.md#external-table-write). The files created during the writing process are assigned random names.

When working with external connections, only read (`SELECT`) and insert (`INSERT`) operations are possible; other types of operations are not supported.

## Writing Data via External Tables {#external-table-write}

If you need to write data regularly, doing this using external tables is convenient. In this case, there is no need to specify all the details of working with this data in each query. To write data to the bucket, create an [external table](external_table.md) in S3 (Yandex Object Storage) and use the usual SQL `INSERT INTO` statement:

```yql
INSERT INTO `test`
SELECT
    "value" AS value, "name" AS name
```

## Exporting data to S3 object storage {#export-to-s3}

YDB supports exporting table data to S3 using an [external data source](../../../datamodel/external_data_source.md).

To export, use a [write query via external data source](write_data.md#connection-write) and specify the [format of the exported files](formats.md#formats):

```yql
INSERT INTO external_source.`test/`
WITH
(
    FORMAT = "parquet"
)
SELECT
    *
FROM table
```

You can export both regular YDB [tables](../../../datamodel/table.md) and any [external tables](../../../datamodel/external_table.md).

> [!TIP]
> The recommended export format is `parquet`; import and export paths are optimized for it.

To export all tables under a given directory in the data schema, plus metadata about tables, directories, and table indexes, to S3-compatible storage, use the YDB CLI. For details, see [Exporting data to S3-compatible storage](../../../../reference/ydb-cli/export-import/export-s3.md).
