---
title: "Streaming read from a topic"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/streaming?version=v26.1"
doc_path: "en/yql/reference/syntax/select/streaming"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/streaming.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/streaming.md"
description: "You can read from a topic with a regular SELECT without creating a streaming query. Set STREAMING = TRUE in the WITH block and limit output rows with LIMIT; oth"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Streaming read from a topic

You can read from a [topic](../../../../concepts/datamodel/topic.md) with a regular `SELECT` without creating a [streaming query](../../../../concepts/streaming-query/streaming-query.md). Set `STREAMING = TRUE` in the `WITH` block and limit output rows with `LIMIT`; otherwise the query does not complete.

> [!WARNING]
> This method is intended only for debugging and checking data in a topic. For production processes, create streaming queries using [CREATE STREAMING QUERY](../create-streaming-query.md).

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

- [Debug reads from a topic](../../../../recipes/streaming_queries/debug-read.md) — recipe with additional examples
- [Streaming queries](../../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](../create-streaming-query.md)
