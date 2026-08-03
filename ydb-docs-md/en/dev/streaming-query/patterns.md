---
title: "Common streaming query patterns"
url: "https://ydb.tech/docs/en/dev/streaming-query/patterns?version=v26.1"
doc_path: "en/dev/streaming-query/patterns"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/patterns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/patterns.md"
description: "This section collects minimal examples of streaming queries for typical scenarios. It starts with a basic topic read, then shows end-to-end processing: handling"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Common streaming query patterns

This section collects minimal examples of [streaming queries](../../concepts/streaming-query/streaming-query.md) for typical scenarios. It starts with a basic topic read, then shows end-to-end processing: handling data and writing results to a topic as JSON, to a topic as a plain string, and to a table. Each example can be used as a starting point for your own workloads.

## Reading from a topic {#topic-read}

Read from a topic using `SELECT ... FROM ... WITH (FORMAT, SCHEMA)`. The `WITH` block specifies the input format and schema—the fields expected in each message and their types. This pattern appears in all examples below.

> [!NOTE]
> Topics are accessed through an [external data source](../../concepts/datamodel/external_data_source.md).
>
> In the examples:
>
> - `ydb_source` — a pre-created external data source;
> - `input_topic` — topic to read from;
> - `output_topic` — topic to write results to;
> - `output_table` — YDB table to write results to.

The following snippet reads JSON events from a topic. Use it inside [CREATE STREAMING QUERY](../../yql/reference/syntax/create-streaming-query.md) in a `DO BEGIN ... END DO` block:

```yql
SELECT
    *
FROM
    ydb_source.input_topic
WITH (
    FORMAT = json_each_row,
    SCHEMA = (
        Id Uint64 NOT NULL,
        Name Utf8 NOT NULL
    )
);
```

For more on formats, see [Topic read and write formats](streaming-query-formats.md).

## Writing to a topic (JSON) {#topic-json}

The query reads events from the input topic, builds a JSON object from fields, and writes to the output topic. `AsStruct` builds a structure from the fields, `Yson::From` converts it to Yson, `Yson::SerializeJson` serializes to a JSON string, and `ToBytes` converts to `String`, which is required for topic writes.

```yql
CREATE STREAMING QUERY write_json_example AS
DO BEGIN

-- ydb_source — external data source for topics
INSERT INTO ydb_source.output_topic
SELECT
    -- Build JSON from fields
    ToBytes(Unwrap(Yson::SerializeJson(Yson::From(
        AsStruct(Id AS id, Name AS name)
    ))))
FROM
    ydb_source.input_topic
WITH (
    FORMAT = json_each_row,  -- Input data format
    SCHEMA = (               -- Input schema
        Id Uint64 NOT NULL,
        Name Utf8 NOT NULL
    )
);

END DO
```

More on the functions:

- [AsStruct](../../yql/reference/builtins/basic.md#as-container)
- [Yson::From](../../yql/reference/udf/list/yson.md#ysonfrom)
- [Yson::SerializeJson](../../yql/reference/udf/list/yson.md#ysonserializejson)
- [Unwrap](../../yql/reference/builtins/basic.md#unwrap)
- [ToBytes](../../yql/reference/builtins/basic.md#to-from-bytes).

## Writing to a topic (string) {#topic-utf8}

The query reads events from the input topic and writes a single field as a string to the output topic. Topic writes require `SELECT` to return a single column of type `String` or `Utf8`.

```yql
CREATE STREAMING QUERY write_utf8_example AS
DO BEGIN

-- ydb_source — external data source for topics
INSERT INTO ydb_source.output_topic
SELECT
    Name
FROM
    ydb_source.input_topic
WITH (
    FORMAT = json_each_row,  -- Input data format
    SCHEMA = (               -- Input schema
        Id Uint64 NOT NULL,
        Name Utf8 NOT NULL
    )
);

END DO
```

More on write formats: [Write formats](streaming-query-formats.md#write_formats).

## Writing to a table {#table-write}

The query reads events from a topic and writes them to `output_table`. Create the table beforehand with a schema that matches the selected columns.

> [!WARNING]
> Table writes in streaming queries support **UPSERT only**. `INSERT INTO` is not supported: with [at-least-once](../../concepts/streaming-query/streaming-query.md#guarantees) delivery, retries would duplicate rows. With `UPSERT`, an existing row with the same primary key is updated; otherwise a new row is inserted, while `INSERT INTO` fails.

```yql
CREATE STREAMING QUERY write_table_example AS
DO BEGIN

-- Write to table (UPSERT only; INSERT is not supported)
UPSERT INTO output_table
SELECT
    Id,
    Name
FROM
    -- ydb_source — external data source for topics
    ydb_source.input_topic
WITH (
    FORMAT = json_each_row,  -- Input data format
    SCHEMA = (               -- Input schema
        Id Uint64 NOT NULL,
        Name Utf8 NOT NULL
    )
);

END DO
```

More details: [Writing to tables](table-writing.md).

## See also

- [CREATE STREAMING QUERY](../../yql/reference/syntax/create-streaming-query.md)
- [Quickstart: reading and writing topics](../../recipes/streaming_queries/topics.md)
