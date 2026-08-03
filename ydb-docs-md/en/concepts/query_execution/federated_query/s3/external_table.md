---
title: "Reading Data from an External Table Pointing to S3 (Object Storage)"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/s3/external_table?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/s3/external_table"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/s3/external_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/s3/external_table.md"
description: "Sometimes, the same data queries need to be executed regularly. To avoid specifying all the details of working with this data every time a query is called, use"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Reading Data from an External Table Pointing to S3 (Object Storage)

Sometimes, the same data queries need to be executed regularly. To avoid specifying all the details of working with this data every time a query is called, use the mode with [external tables](../../../datamodel/external_table.md). In this case, the query looks like a regular query to YDB tables.

Example query for reading data:

```yql
SELECT
    *
FROM
    `s3_test_data`
WHERE
    version > 1
```

## Creating an External Table Pointing to an S3 Bucket (Object Storage) {#external-table-settings}

To create an external table describing the S3 bucket (Object Storage), execute the following SQL query. The query creates an external table named `s3_test_data`, containing files in the `CSV` format with string fields `key` and `value`, located inside the bucket at the path `test_folder`, using the connection credentials specified by the [external data source](../../../datamodel/external_data_source.md) object `bucket`:

```yql
CREATE EXTERNAL TABLE `s3_test_data` (
  key Utf8 NOT NULL,
  value Utf8 NOT NULL
) WITH (
  DATA_SOURCE="bucket",
  LOCATION="folder",
  FORMAT="csv_with_names",
  COMPRESSION="gzip"
);
```

Where:

- `key, value` - list of data columns and their types;
- `bucket` - name of the [external data source](../../../datamodel/external_data_source.md) to S3 (Object Storage);
- `folder` - path within the bucket containing the data;
- `csv_with_names` - one of the [permitted data storage formats](formats.md);
- `gzip` - one of the [permitted compression algorithms](formats.md#compression).

You can also specify [format settings](external_data_source.md#format_settings).

## Data Model

Reading data using external tables from S3 (Object Storage) is done with regular SQL queries as if querying a normal table.

```yql
SELECT
  <expression>
FROM
  `s3_test_data`
WHERE
  <filter>;
```

## Limitations

There are a number of limitations when working with S3 buckets (Object Storage).

Limitations:

1. Only data read requests - `SELECT` and `INSERT` are supported; other requests are not.
2. If the date value stored in the external data source is outside the allowed range for YDB (all dates used must be later than 1970-01-01 but earlier than 2105-12-31), such a value in YDB will be converted to `NULL`.
