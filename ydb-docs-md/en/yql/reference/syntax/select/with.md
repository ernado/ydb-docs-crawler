---
title: "WITH"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/with?version=v26.1"
doc_path: "en/yql/reference/syntax/select/with"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/with.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/with.md"
description: "Specified after the data source in FROM and used to provide additional hints for table usage. Hints cannot be specified for subqueries and named expressions."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# WITH

Specified after the data source in `FROM` and used to provide additional hints for table usage. Hints cannot be specified for subqueries and [named expressions](../expressions.md#named-nodes).

The following values are supported:

- `INFER_SCHEMA` — sets the flag for inferring the table schema. The behavior is similar to setting the [yt.InferSchema pragma](../pragma.md#inferschema), but only for a specific data source. You can specify the number of rows to infer (a number from 1 to 1000).
- `FORCE_INFER_SCHEMA` — sets the flag for forcing schema inference of the table. The behavior is similar to setting the [yt.ForceInferSchema pragma](../pragma.md#inferschema), but only for a specific data source. You can specify the number of rows to infer (a number from 1 to 1000).
- `DIRECT_READ` — suppresses the operation of some optimizers and forces the table contents to be used as is. The behavior is similar to setting the debug [DirectRead pragma](../pragma.md#debug), but only for a specific data source.
- `INLINE` — indicates that the table contents are small and should be processed using an in-memory representation. The actual table size is not checked, and if it is large, the query may fail due to memory exhaustion.
- `UNORDERED` — suppresses the use of the table's original sorting.
- `XLOCK` — indicates that an exclusive lock should be taken on the table. Useful when the table is read during the [query metaprogram](../action.md) processing stage and then its contents are updated in the main query. It helps avoid data loss if an external process modifies the table between the execution of the metaprogram phase and the main part of the query.
- `SCHEMA` type — indicates that the specified table schema should be used entirely, ignoring the schema in the metadata.
- `COLUMNS` type — indicates that the specified types should be used for columns whose names match the column names in the table metadata, as well as which additional columns are present in the table.
- `IGNORETYPEV3`, `IGNORE_TYPE_V3` — sets the flag to ignore type_v3 types in the table. The behavior is similar to setting the [yt.IgnoreTypeV3 pragma](../pragma.md#ignoretypev3), but only for a specific data source.

When working with [external file data sources](../../../../concepts/datamodel/external_data_source.md), you can additionally specify a number of parameters:

- `FORMAT`: data storage format in file storages in [federated queries](../../../../concepts/query_execution/federated_query/s3/formats.md). Allowed values: `csv_with_names`, `tsv_with_names`, `json_list`, `json_each_row`, `json_as_string`, `parquet`, `raw`.
- `COMPRESSION`: file compression format in file storages in [federated queries](../../../../concepts/query_execution/federated_query/s3/partition_projection.md). Valid values: [gzip](https://en.wikipedia.org/wiki/Gzip), [zstd](https://en.wikipedia.org/wiki/Zstd), [lz4](<https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)>), [brotli](https://en.wikipedia.org/wiki/Brotli), [bzip2](https://en.wikipedia.org/wiki/Bzip2), [xz](https://en.wikipedia.org/wiki/XZ_Utils).
- `PARTITIONED_BY` - a list of [partitioning columns](../../../../concepts/query_execution/federated_query/s3/partitioning.md) of data in file storages in federated queries. Contains a list of columns in the order they are placed in the file storage.
- `projection.enabled` - a flag for enabling [extended data partitioning](../../../../concepts/query_execution/federated_query/s3/partition_projection.md). Valid values: `true`, `false`.
- `projection.<field_name>.type` - field type of [extended data partitioning](../../../../concepts/query_execution/federated_query/s3/partition_projection.md). Valid values: `integer`, `enum`, `date`.
- `projection.<field_name>.<options>` - extended properties of the field of [extended data partitioning](../../../../concepts/query_execution/federated_query/s3/partition_projection.md).

When reading from a [topic](../../../../concepts/datamodel/topic.md) in [streaming queries](../../../../dev/streaming-query/index.md), you can specify watermarks parameters:

- `WATERMARK` — expression for calculating the [watermark](../../../../dev/streaming-query/watermarks.md). Currently, only the write time to a [topic](../../../../concepts/datamodel/topic.md) with a constant delay is supported. Format: `__ydb_write_time - Interval("<delay>")`, where `<delay>` is specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format.
- `WATERMARK_GRANULARITY` — watermark generation frequency. The smaller it is, the higher the CPU consumption by the query and the lower the response latency. Only relevant for [streaming queries](../../../../dev/streaming-query/index.md). Specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format. Default value — 1 second.
- `WATERMARK_IDLE_TIMEOUT` — period after which an [idle partition](../../../../dev/streaming-query/watermarks.md#idle-partitions) will be excluded from the combined watermark calculation. Only relevant for [streaming queries](../../../../dev/streaming-query/index.md). Specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format. Default value — 5 seconds.

When specifying hints `SCHEMA` and `COLUMNS`, the type value must be a [structure](../../types/containers.md) type.

## Examples

```yql
SELECT key FROM my_table WITH INFER_SCHEMA;
SELECT key FROM my_table WITH FORCE_INFER_SCHEMA="42";
```

```yql
$s = (SELECT COUNT(*) FROM my_table WITH XLOCK);

INSERT INTO my_table WITH TRUNCATE
SELECT EvaluateExpr($s) AS a;
```

```yql
SELECT key, value FROM my_table WITH SCHEMA Struct<key:String, value:Int32>;
```

```yql
SELECT key, value FROM my_table WITH COLUMNS Struct<value:Int32?>;
```

```yql
SELECT key, value FROM EACH($my_tables) WITH SCHEMA Struct<key:String, value:List<Int32>>;
```

```yql
SELECT
    *
FROM
    my_topic
WITH (
    FORMAT = json_each_row,
    SCHEMA = (
        ts String
    ),
    WATERMARK = __ydb_write_time - Interval("PT5S"),
    WATERMARK_GRANULARITY = "PT1S",
    WATERMARK_IDLE_TIMEOUT = "PT5S"
);
```
