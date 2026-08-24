---
title: "Writing to tables"
url: "https://ydb.tech/docs/en/dev/streaming-query/table-writing?version=v26.1"
doc_path: "en/dev/streaming-query/table-writing"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/table-writing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/table-writing.md"
description: "Writing to tables lets you save the results of a streaming query for later analysis with regular SQL queries. For example, you can aggregate events from a strea"
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# Writing to tables

Writing to tables lets you save the results of a streaming query for later analysis with regular SQL queries. For example, you can aggregate events from a stream and save the results to a table.

For writing, [UPSERT INTO](../../yql/reference/syntax/upsert_into.md) is used — inserting a new row or updating an existing one by primary key. The UPSERT operation is idempotent by primary key: rewriting the same row results in an update, not duplication. This is important because streaming queries provide the [at-least-once](../../concepts/streaming-query/streaming-query.md#guarantees) guarantee — when recovering from a [checkpoint](checkpoints.md), some events may be processed again.

> [!CAUTION]
> Not supported:
>
> - [INSERT INTO](../../yql/reference/syntax/insert_into.md) — use UPSERT INTO instead. `INSERT INTO` would duplicate rows on retries under at-least-once delivery.
> - Writing to YDB tables in **external** databases. Currently only local tables can be written to.

## Example

The query reads events from a topic and writes them to `output_table`. `Ts` is cast from string to `Timestamp`, and [Unwrap](../../yql/reference/builtins/basic.md#unwrap) removes optionality.

```sql
CREATE STREAMING QUERY query_with_table_write AS
DO BEGIN

-- Reading from a topic and writing to a table
UPSERT INTO
    output_table
SELECT
    -- Converting a string to Timestamp
    Unwrap(CAST(Ts AS Timestamp)) AS Ts,
    Country,
    Count
FROM
    -- Read events from topic
    ydb_source.input_topic
WITH (
    -- Data format in a topic
    FORMAT = json_each_row,
    -- Data schema
    SCHEMA = (
        Ts String NOT NULL,
        Count Uint64 NOT NULL,
        Country Utf8 NOT NULL
    )
);

END DO
```

## Limitations

In a single streaming query:

- You cannot use the same table for [stream enrichment](enrichment.md) using `JOIN` and for writing the query result.
- You cannot write to the same table multiple times.
