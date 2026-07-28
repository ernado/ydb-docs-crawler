---
title: "Streaming reads from a topic"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/streaming?version=v26.1"
doc_path: "en/yql/reference/syntax/select/streaming"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/streaming.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/streaming.md"
description: "You can read from a topic with a regular SELECT without creating a streaming query. Set STREAMING = TRUE in the WITH block and limit output rows with LIMIT; oth"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Streaming reads from a topic

You can read from a [topic](../../../../concepts/datamodel/topic.md) with a regular `SELECT` without creating a [streaming query](../../../../concepts/streaming-query.md). Set `STREAMING = TRUE` in the `WITH` block and limit output rows with `LIMIT`; otherwise the query does not complete.

> [!WARNING]
> Use this only for debugging and inspecting topic data. For production workloads, create streaming queries with [CREATE STREAMING QUERY](../create-streaming-query.md).

> [!NOTE]
> In the examples, `ydb_source` is a pre-created [external data source](../../../../concepts/datamodel/external_data_source.md), and `topic_name` is a topic available through it.

## Example

```yql
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

## See also

- [Debug reads from a topic](../../../../recipes/streaming_queries/debug-read.md) — recipe with more examples
- [Streaming queries](../../../../concepts/streaming-query.md)
- [CREATE STREAMING QUERY](../create-streaming-query.md)
