---
title: "Debug reads from a topic"
url: "https://ydb.tech/docs/en/recipes/streaming_queries/debug-read?version=v26.1"
doc_path: "en/recipes/streaming_queries/debug-read"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/streaming_queries/debug-read.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/streaming_queries/debug-read.md"
description: "When developing streaming queries, it is often useful to inspect what arrives in a topic without creating a full streaming query. Run a regular SELECT with STRE"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Debug reads from a topic

When developing [streaming queries](../../concepts/streaming-query/streaming-query.md), it is often useful to inspect what arrives in a [topic](../../concepts/datamodel/topic.md) without creating a full streaming query. Run a regular `SELECT` with `STREAMING = TRUE`.

> [!WARNING]
> For debugging and inspection only. For production, create streaming queries with [CREATE STREAMING QUERY](../../yql/reference/syntax/create-streaming-query.md).

> [!NOTE]
> In the examples, `ydb_source` is a pre-created [external data source](../../concepts/datamodel/external_data_source.md), and `topic_name` / `input_topic` are topics available through it.

## Raw reads

Simplest option — read messages in `raw` format without parsing:

```sql
SELECT
    Data
FROM
    ydb_source.topic_name
WITH (
    FORMAT = raw,
    SCHEMA = (
        Data String
    ),
    STREAMING = TRUE
)
LIMIT 1
```

`LIMIT` is required; without it the query never completes because it waits for new messages indefinitely.

## JSON parsing

If the topic stores JSON, parse fields directly:

```sql
SELECT
    *
FROM
    ydb_source.topic_name
WITH (
    FORMAT = json_each_row,
    SCHEMA = (
        Time String NOT NULL,
        Level String NOT NULL,
        Host String NOT NULL
    ),
    STREAMING = TRUE
)
LIMIT 5
```

## See also

- [Streaming queries](../../concepts/streaming-query/streaming-query.md)
- [Topic read and write formats](../../dev/streaming-query/streaming-query-formats.md) — supported data formats
- [Streaming read from a topic](../../yql/reference/syntax/select/streaming.md) — `STREAMING = TRUE` in the YQL reference
