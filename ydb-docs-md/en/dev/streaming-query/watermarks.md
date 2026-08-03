---
title: "Watermarks"
url: "https://ydb.tech/docs/en/dev/streaming-query/watermarks?version=v26.1"
doc_path: "en/dev/streaming-query/watermarks"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/watermarks.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/watermarks.md"
description: "Watermark — a monotonically increasing lower bound on event times in the stream (more about the concept: Watermarks ). This section describes the configuration"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Watermarks

Watermark — a monotonically increasing lower bound on event times in the stream (more about the concept: [Watermarks](../../concepts/streaming-query/watermarks.md)). This section describes the configuration of watermarks in streaming queries YDB.

## Event time

In stream processing, each event has a timestamp that the system uses to track the progress of time in the stream. In the current implementation, the only source of event time is the write time of the event to the [topic](../../concepts/datamodel/topic.md), available via the system column `__ydb_write_time`.

> [!NOTE]
> Support for arbitrary expressions to extract time from event data (for example, the `event.created_at` field) is planned in future versions.

## Usage

Watermark is used by operations that depend on the progress of event time in the stream. In YDB, such operations include window aggregation [HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — it defines sliding time windows that group events. When a watermark is received, `HoppingWindow` closes all windows that are fully covered by this value.

## Watermark computation

When the system receives an event, it updates the watermark — **advancing** it forward along the time axis. The watermark is calculated as `maximum observed event time − delay`, where `delay` is the lag value specified in the [`WATERMARK`](watermarks.md#configuration) expression (for example, `Interval("PT5S")` in `WATERMARK = __ydb_write_time - Interval("PT5S")`).

Events in a stream may arrive out of chronological order: an event with timestamp 10:00:03 may be processed after an event with timestamp 10:00:05. Reasons: clock skew in a distributed system, network delays, uneven load on topic [partitions](../../concepts/datamodel/topic.md#partitioning).

The `delay` parameter sets the allowable time margin for events arriving with a delay. For example, with `delay` of 5 seconds, an event with time 00:00:48 will be accepted even if events with time 00:00:50 have already arrived: the watermark has not yet reached 00:00:48. If the same event arrives later, when the watermark has already advanced past 00:00:48, it will be considered late and discarded.

On the trade-off between accuracy and result delivery latency: [Accuracy vs. Latency Trade-off](../../concepts/streaming-query/watermarks.md#tradeoff).

## Idle partitions

If the input topic contains multiple [partitions](../../concepts/datamodel/topic.md#partitioning), each of them advances the watermark independently. The overall query watermark does not advance ahead of the slowest partition: windows are not closed until at least one partition has reached the corresponding point in time.

If one of the partitions stops receiving data, its watermark stops advancing. Such a partition is called idle. As long as the idle partition is taken into account when computing the overall watermark, it also stops advancing, and results are not emitted despite data arriving from other partitions.

To avoid this blocking, an idle partition is excluded from the common watermark calculation after a configurable timeout period (the `WATERMARK_IDLE_TIMEOUT` parameter; for details, see the [Configuration](watermarks.md#configuration) section).

## Configuration

Watermarks are enabled and configured in the [WITH](../../yql/reference/syntax/select/with.md) section when reading from a topic.

Configuration parameters:

- `WATERMARK` — expression for calculating the [watermark](watermarks.md). Currently, only the write time to a [topic](../../concepts/datamodel/topic.md) with a constant delay is supported. Format: `__ydb_write_time - Interval("<delay>")`, where `<delay>` is specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format.
- `WATERMARK_GRANULARITY` — watermark generation frequency. The smaller it is, the higher the CPU consumption by the query and the lower the response latency. Only relevant for [streaming queries](index.md). Specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format. Default value — 1 second.
- `WATERMARK_IDLE_TIMEOUT` — period after which an [idle partition](watermarks.md#idle-partitions) will be excluded from the combined watermark calculation. Only relevant for [streaming queries](index.md). Specified in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format. Default value — 5 seconds.

> [!WARNING]
> When using [HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window), the first parameter (time extractor) and the time source in the WATERMARK expression must match. In the current implementation, both must use `__ydb_write_time`.

## Example

Below is an example of a streaming query with watermark and window aggregation. The query reads events from a topic, filters them by the `pass` field, and aggregates the `payload` values in windows of 10 seconds with a 5-second step. The watermark is configured with a 5-second lag.

### Input data

```json
{"pass": 1, "payload": "a"} // record time: 1970-01-01T00:00:40Z
{"pass": 1, "payload": "b"} // record time: 1970-01-01T00:00:42Z
{"pass": 0, "payload": "c"} // record time: 1970-01-01T00:00:50Z
{"pass": 1, "payload": "d"} // record time: 1970-01-01T00:00:40Z
```

### Query

```yql
CREATE STREAMING QUERY example AS
DO BEGIN
    $input = (
        SELECT
            t.*,
            __ydb_write_time AS ts
        FROM
            Input
        WITH (
            FORMAT = json_each_row,
            SCHEMA = (
                pass Int64,
                payload String
            ),
            WATERMARK = __ydb_write_time - Interval("PT5S")
        ) AS t
    );

    $output = (
        SELECT
            AGGREGATE_LIST(payload) AS result,
            CAST(HOP_END() AS String) AS ts
        FROM
            $input
        WHERE pass > 0
        GROUP BY
            HoppingWindow(ts, "PT5S", "PT10S")
    );

    INSERT INTO Output
    SELECT
        ToBytes(Unwrap(Yson2::SerializeJson(Yson::From(TableRow()))))
    FROM $output;
END DO;
```

Where:

- [`CREATE STREAMING QUERY`](../../yql/reference/syntax/create-streaming-query.md) — creates a named streaming query.
- `__ydb_write_time` is a system column containing the time the event was written to the [topic](../../concepts/datamodel/topic.md).
- `FORMAT = json_each_row` — [data format](streaming-query-formats.md) in a topic, each line contains a separate JSON object.
- `WATERMARK = __ydb_write_time - Interval("PT5S")` is a watermark with a 5-second lag. `Interval("PT5S")` sets the interval in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) format.
- [`AGGREGATE_LIST`](../../yql/reference/builtins/aggregation.md#agg-list) — aggregate function that collects values into a list.
- [`HOP_END()`](../../yql/reference/syntax/select/group-by.md#group-by-hop) returns the timestamp of the end of the current window.
- [`HoppingWindow(ts, "PT5S", "PT10S")`](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — window function with a step of 5 seconds and a window size of 10 seconds.

### Result

```json
{"result": ["a", "b"], "ts": "1970-01-01T00:00:45.000000Z"}
```

### Explanation

1. The first event (`"a"`, record time 40s) passes the filter (`pass > 0`) and enters windows `[35; 45)` and `[40; 50)`. Watermark advances to 35s and does not close any window.
2. The second event (`"b"`, record time 42s) similarly falls into windows `[35; 45)` and `[40; 50)`. The watermark advances to 37s.
3. The third event (`"c"`, record time 50s) is discarded by the filter (`pass = 0`). Despite this, the event still advances the watermark to 45s. The watermark closes window `[35; 45)` — result `["a", "b"]` is output.
4. The fourth event (`"d"`, record time 40s) does not advance the watermark: it is already at the 45s mark. The event passes the filter but is discarded as late — its record time (40s) is less than the current watermark (45s). Although window `[40; 50)` is still open, the watermark has already promised that no events with time < 45s will arrive, so `d` is not counted in any of its windows.

## See also

- [GROUP BY ... HoppingWindow](../../yql/reference/syntax/select/group-by.md#group-by-hopping_window) — a window function that uses watermarks.
- [WITH](../../yql/reference/syntax/select/with.md) — the WITH clause for configuring topic read parameters.
- [Data delivery guarantees](guarantees.md) — data delivery guarantees.
- [Checkpoints](checkpoints.md) — checkpoint mechanism.
