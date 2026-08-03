---
title: "DROP STREAMING QUERY"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-streaming-query?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-streaming-query"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-streaming-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-streaming-query.md"
description: "DROP STREAMING QUERY deletes a streaming query. Syntax. DROP STREAMING QUERY [IF EXISTS ] < query_name >. Parameters."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP STREAMING QUERY

`DROP STREAMING QUERY` deletes a [streaming query](../../../concepts/streaming-query/streaming-query.md).

## Syntax

```sql
DROP STREAMING QUERY [IF EXISTS] <query_name>
```

### Parameters

- `IF EXISTS` — do not fail if the streaming query does not exist.
- `query_name` — name of the streaming query to delete.

## Permissions

Requires [permission](grant.md#permissions-list) `REMOVE SCHEMA` on the streaming query. Example grant for `my_streaming_query`:

```sql
GRANT REMOVE SCHEMA ON my_streaming_query TO `user@domain`
```

## Examples

Delete `my_streaming_query`:

```sql
DROP STREAMING QUERY my_streaming_query
```

## See also

- [Streaming queries](../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](create-streaming-query.md)
- [ALTER STREAMING QUERY](alter-streaming-query.md)
