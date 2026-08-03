---
title: "ALTER STREAMING QUERY"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-streaming-query?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-streaming-query"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-streaming-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-streaming-query.md"
description: "ALTER STREAMING QUERY changes settings of streaming queries and controls their lifecycle (start and stop). Syntax."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER STREAMING QUERY

`ALTER STREAMING QUERY` changes settings of [streaming queries](../../../concepts/streaming-query/streaming-query.md) and controls their lifecycle (start and stop).

## Syntax

```sql
ALTER STREAMING QUERY [IF EXISTS] <query_name> SET (
    <key1> = <value1>,
    <key2> = <value2>,
    ...
)
```

### Parameters

- `IF EXISTS` — do not fail if the streaming query does not exist.
- `query_name` — name of the streaming query to change.
- `SET (<key> = <value>)` — optional list of settings to update.

### Changing query settings

Syntax:

```sql
ALTER STREAMING QUERY [IF EXISTS] <query_name> SET (<key> = <value>)
```

Available parameters:

- `RUN = (TRUE|FALSE)` — start or stop the query.
- `RESOURCE_POOL = <resource_pool_name>` — name of the [resource pool](../../../concepts/glossary.md#resource-pool) where the query runs.

When you run `SET (RUN = TRUE)`, read offsets from topics and aggregation state are restored from a [checkpoint](../../../dev/streaming-query/checkpoints.md). If there is no checkpoint, reading starts from the latest data.

Examples of changing settings are [below](alter-streaming-query.md#parameters-changing-examples).

## Permissions

Streaming queries require [permission](grant.md#permissions-list) `ALTER SCHEMA`. Example grant for `my_streaming_query`:

```sql
GRANT ALTER SCHEMA ON my_streaming_query TO `user@domain`
```

## Examples

### Changing settings {#parameters-changing-examples}

Stop `my_streaming_query`:

```sql
ALTER STREAMING QUERY my_streaming_query SET (
    RUN = FALSE
)
```

Start `my_streaming_query` in [resource pool](../../../concepts/glossary.md#resource-pool) `my_resource_pool`:

```sql
ALTER STREAMING QUERY my_streaming_query SET (
    RUN = TRUE,
    RESOURCE_POOL = my_resource_pool
)
```

### Query status {#status-of-query}

Current status is available in the `Status` column of the ⟦C2⟧ system view [System database views](../../../dev/system-views.md):

```sql
SELECT
    Path,
    Status,
    Text,
    Run
FROM
    `.sys/streaming_queries`
```

Possible status values:

1. `CREATING` — query is being created after `CREATE STREAMING QUERY`.
2. `CREATED` — query exists but is not running (for example, `RUN = FALSE`).
3. `STARTING` — query is starting.
4. `RUNNING` — query is executing.
5. `SUSPENDED` — query paused due to internal errors; the system will retry.
6. `STOPPING` — query is stopping after `ALTER STREAMING QUERY ... SET (RUN = FALSE)`.
7. `STOPPED` — query is stopped.

After successful DDL for create or alter, status is guaranteed to be `CREATED`, `STARTING`, `RUNNING`, `STOPPED`, or `SUSPENDED` depending on `RUN = (TRUE|FALSE)` and whether startup succeeded.

More examples for other data formats: [Topic read and write formats](../../../dev/streaming-query/streaming-query-formats.md). For capabilities and limitations of streaming queries, see [Streaming queries](../../../concepts/streaming-query/streaming-query.md).

## See also

- [Streaming queries](../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](create-streaming-query.md)
- [DROP STREAMING QUERY](drop-streaming-query.md)
