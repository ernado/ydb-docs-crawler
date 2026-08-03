---
title: "Query Execution"
url: "https://ydb.tech/docs/en/concepts/analytics/concepts/execution?version=v26.1"
doc_path: "en/concepts/analytics/concepts/execution"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/analytics/concepts/execution.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/analytics/concepts/execution.md"
description: "YDB is a distributed Massively Parallel Processing (MPP) database designed for executing complex analytical queries on large volumes of data. Each query is auto"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Query Execution

YDB is a distributed Massively Parallel Processing (MPP) database designed for executing complex analytical queries on large volumes of data. Each query is automatically parallelized across all available compute nodes in the cluster, enabling efficient use of compute resources.

YDB supports several key technologies that ensure high performance and stability:

- [Decentralized MPP architecture](execution.md#mpp)
- [Cost-Based Query Optimizer](execution.md#cbo)
- [Handling data that exceeds RAM](execution.md#spilling)
- [Workload Isolation and Resource Management](execution.md#resource_management)

## Decentralized MPP architecture {#mpp}

Unlike MPP systems with a dedicated master node, YDB's architecture is completely decentralized. This provides two main advantages:

- High fault tolerance: any node in the cluster can accept and coordinate query execution. There is no single point of failure (SPOF). The failure of some nodes does not halt the cluster—the load is automatically redistributed among the remaining nodes.
- Compute scalability: you can add or remove compute nodes without downtime, and the system automatically adapts, distributing the load to account for the new cluster composition.

## Cost-Based Query Optimizer {#cbo}

Before executing a query, YDB uses a [Cost-Based Optimizer (CBO)](../../query_execution/optimizer.md). It analyzes the query text, metadata, and statistics on data distribution in tables to build a physical execution plan with the lowest estimated cost.

The optimizer can:

- choose the join order for queries with dozens of `JOIN`s;
- select distributed `JOIN` algorithms (e.g., Grace Join, Broadcast Join) depending on table sizes;
- push down filters (`WHERE` clauses) as close as possible to the data sources to reduce the amount of data processed in subsequent stages.

## Handling data that exceeds RAM {#spilling}

Analytical queries can require large amounts of RAM, especially for `JOIN` and `GROUP BY` operations. YDB is designed to work with data that may not fit into RAM.

- Spilling: if the intermediate results of a query exceed the memory limit, YDB [automatically spills](../../query_execution/spilling.md) them to the node's local disk. This prevents the query from failing with an "Out of Memory" error and allows queries to be executed on large volumes of data.
- Distributed JOIN algorithms: for joining tables that exceed the memory of a single node, distributed algorithms are used that process data in chunks across different nodes.

## Workload Isolation and Resource Management {#resource_management}

In a corporate DWH, different teams often run different types of workloads. To prevent these workloads from interfering with each other, YDB has a built-in resource manager.

- Workload Manager: the built-in `workload manager` allows you to create resource pools and, using [classifiers](../../glossary.md#resource-pool-classifier), assign queries from different user groups to different pools. This mechanism solves the "noisy neighbor" problem, where a single resource-intensive query can slow down the system for all other users.
