---
title: "Writing to tables"
url: "https://ydb.tech/docs/en/dev/streaming-query/table-writing?version=v26.1"
doc_path: "en/dev/streaming-query/table-writing"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/table-writing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/table-writing.md"
description: "Writing to tables lets you persist streaming query results for analysis with regular SQL. For example, you can aggregate events from a stream and store summarie"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Writing to tables

Writing to tables lets you persist streaming query results for analysis with regular SQL. For example, you can aggregate events from a stream and store summaries in a table.

Writes use [UPSERT INTO](../../yql/reference/syntax/upsert_into.md) — insert a new row or update an existing row by primary key. UPSERT is idempotent by primary key: writing the same row again updates it rather than duplicating. That matters because streaming queries provide [at-least-once](../../concepts/streaming-query/streaming-query.md#guarantees) delivery — after recovery from a [checkpoint](checkpoints.md), some events may be processed more than once.

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
    -- Data format in the topic
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
