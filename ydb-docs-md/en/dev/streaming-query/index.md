---
title: "Streaming queries"
url: "https://ydb.tech/docs/en/dev/streaming-query/?version=v26.1"
doc_path: "en/dev/streaming-query/"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/index.md"
description: "Practical guidance for working with streaming queries: Common patterns — minimal examples to get started quickly."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Streaming queries

Practical guidance for working with [streaming queries](../../concepts/glossary.md#streaming-query):

- [Common patterns](patterns.md) — minimal examples to get started quickly
- [Writing to tables](table-writing.md) — how streaming queries write into YDB tables in near real time
- [Data enrichment](enrichment.md) — enriching the stream using external sources
- [Topic read/write formats](streaming-query-formats.md) — supported formats when working with topics and usage examples
- [Delivery guarantees](guarantees.md) — guarantee levels, windowing anomalies, and recommendations
- [Checkpoints](checkpoints.md) — persisting processing state for fault tolerance and recovery
- [Watermarks](watermarks.md) — tracking event-time progress in a stream

## See also

- [Recipes for streaming queries](../../recipes/streaming_queries/index.md)
- [Streaming queries overview](../../concepts/streaming-query/streaming-query.md)
