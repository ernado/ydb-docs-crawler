---
title: "Data Storage"
url: "https://ydb.tech/docs/en/concepts/analytics/concepts/store?version=v26.1"
doc_path: "en/concepts/analytics/concepts/store"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/analytics/concepts/store.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/analytics/concepts/store.md"
description: "Efficient data storage is the foundation of any analytical warehouse. YDB uses a columnar format, a storage and compute disaggregation architecture, and automat"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Data Storage

Efficient data storage is the foundation of any analytical warehouse. YDB uses a columnar format, a storage and compute disaggregation architecture, and automatic maintenance processes to ensure high performance and a low total cost of ownership.

## Columnar tables {#column_table}

Data in [columnar tables](../../datamodel/table.md#column-oriented-tables) is stored by columns instead of rows. This approach is the standard for OLAP systems and offers two key advantages:

1. Reduced read volume: when a query (e.g., `SELECT column_a, column_b FROM...`) is executed, only the data from the columns involved in the query is read from the disk.
2. Data compression: data of the same type within a column compresses better than heterogeneous data in a row. YDB uses the `LZ4` compression algorithm.

## Architecture with storage and compute disaggregation {#disaggregation}

Storage and compute disaggregation is an architectural principle of YDB. The nodes responsible for data storage (storage nodes) and the nodes that execute queries (dynamic nodes) are separate. This allows you to:

- scale resources independently: if you run out of disk space, you add storage nodes. If you lack CPU for queries, you add compute nodes. This differs from systems where storage and compute resources are tightly coupled;
- redistribute load quickly: redistributing compute load between nodes does not require physical data movement; only metadata is transferred.

## Automatic storage optimization {#zero_admin}

YDB is designed to minimize manual maintenance operations.

- Automatic data compaction: Data is stored in [LSM-like](../../query_execution/mvcc.md#how-ydb-short-name-stores-mvcc-data) structures; data merging and optimization processes run continuously in the background. You do not need to run VACUUM or similar commands.
- Automatic data deletion: To manage the data lifecycle, use the [TTL-based deletion](../../ttl.md) mechanism.

## Built-in fault tolerance {#reliability}

YDB was designed from the ground up as a fault-tolerant system and supports [various data placement modes](../../topology.md#cluster-config) to protect against hardware, rack, or even entire data center failures.

![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/concepts/analytics/concepts/_includes/olap_3dc.png)
