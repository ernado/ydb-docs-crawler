---
title: "Data delivery guarantees"
url: "https://ydb.tech/docs/en/dev/streaming-query/guarantees?version=v26.1"
doc_path: "en/dev/streaming-query/guarantees"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/guarantees.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/guarantees.md"
description: "Delivery guarantees determine how many times each event from the input topic will be processed by a streaming query. Understanding the system's guarantees is cr"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Data delivery guarantees

Delivery guarantees determine how many times each event from the input topic will be processed by a streaming query. Understanding the system's guarantees is critical when designing data processing pipelines.

> [!NOTE]
> We are constantly working on developing streaming processing mechanisms. In future versions, the guarantees provided will be improved.

**Data processing guarantees (dataplane)**:

- [at-least-once](guarantees.md#at-least-once) — for all query types, each event is processed at least once.

**Anomalies when modifying queries (control plane)**:

- [Event loss when recreating a query](guarantees.md#incomplete-windows-restart) — when recreating a query via DROP + CREATE, some events that arrived between deletion and creation will be skipped.
- [Partial first aggregation window](guarantees.md#partial-first-window) — when a query starts, the first aggregation window contains incomplete data.

## Checkpoints and recovery {#checkpoints}

YDB periodically saves a [checkpoint](checkpoints.md) — a snapshot of the query state containing:

- [offsets](../../concepts/datamodel/topic.md#consumer-offset) in input topics — positions up to which events have been read and processed;
- aggregation states — intermediate results of operations, for example accumulated values in [GROUP BY HOP](../../yql/reference/syntax/select/group-by.md#group-by-hop).

YDB stores read offsets in its own checkpoints, rather than relying on the offsets of a [consumer](../../concepts/datamodel/topic.md#consumer) in an external system.

During recovery, the query rolls back to the last checkpoint: it resumes reading from the saved offsets and restores the aggregation states. Events that arrived between the checkpoint and the failure will be reprocessed. For more details on the checkpoint mechanism, see the [Checkpoints](checkpoints.md) section.

## Data processing guarantees (dataplane) — at-least-once {#at-least-once}

If a failure occurs during stream processing (compute node restart, network outage, timeout), YDB automatically restores the query from the last checkpoint. The [at-least-once](https://en.wikipedia.org/wiki/Reliable_messaging#At-least-once_delivery) guarantee is provided for all types of streaming queries — each event will be processed at least once. The query resumes reading from the saved offset and resends the processing results. This applies to all types of queries: queries without aggregation (filtering, enrichment, transformation) and queries with [window aggregation](../../yql/reference/syntax/select/group-by.md#group-by-hop).

When writing the result to a table via [UPSERT](../../yql/reference/syntax/upsert_into.md), reprocessing does not lead to duplication: UPSERT updates the existing row by primary key. Data is not lost, and duplicates do not accumulate.

When writing the result to an output topic, reprocessing leads to duplicates: the same events will be written to the topic more than once. The consumer of the output topic must account for this and, if necessary, perform deduplication on its own.

## Guarantees when modifying a query (control plane) {#modification-anomalies}

Currently, changing the query text without stopping it is not supported. To update a query, a combination of [DROP](../../yql/reference/syntax/drop-streaming-query.md) and [CREATE](../../yql/reference/syntax/create-streaming-query.md) commands is used; in this case, the `at-least-once` guarantee is not met: some events may be skipped. The scenarios where this occurs are described below.

### Partial results of the first window when starting a query {#partial-first-window}

Time windows ( [GROUP BY HOP](../../yql/reference/syntax/select/group-by.md#group-by-hop)) calculate their boundaries based on absolute (wall-clock) time. Window boundaries are aligned to multiples of intervals from the start of the epoch: for example, with a 1-minute window, boundaries always occur at 12:00:00, 12:01:00, 12:02:00, etc., regardless of when the query was started. If the query starts at 12:00:30, it falls into the already running window \[12:00:00 .. 12:01:00\], but data only starts arriving at 12:00:30. As a result, the aggregate of the first window is computed from 30 seconds of data instead of a full minute.

This is expected behavior on the first start — all subsequent windows will receive data for the full interval, which is important to consider when recreating a query.

### Event loss when recreating a query {#incomplete-windows-restart}

To change the query text, the combination of commands [DROP](../../yql/reference/syntax/drop-streaming-query.md) + [CREATE](../../yql/reference/syntax/create-streaming-query.md) is used. When `DROP`, the checkpoint is deleted along with the query, since YDB uses internal storage of read offsets from the source, these offsets are deleted along with the query. The new query does not have a saved position and starts reading from the end of the topic. All events that arrived in the topic between the deletion of the old query and the start of the new one will not be read.

A similar situation occurs if the data pointed to by the offset in the checkpoint has already been deleted from the topic by [TTL](../../concepts/datamodel/topic.md#retention-time).

For queries with window aggregation, the first windows after recreation will contain data gaps and understated aggregates.

## See also

- [Streaming queries](../../concepts/streaming-query/streaming-query.md) — general description of streaming queries.
- [Checkpoints](checkpoints.md) — checkpoint mechanism that ensures recovery after failures.
- [Writing to tables](table-writing.md) — writing to tables and UPSERT idempotence.
