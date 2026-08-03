---
title: "Federated queries"
url: "https://ydb.tech/docs/en/concepts/analytics/concepts/federated?version=v26.1"
doc_path: "en/concepts/analytics/concepts/federated"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/analytics/concepts/federated.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/analytics/concepts/federated.md"
description: "Federated queries allow you to query data stored in external systems without first loading it (ETL) into YDB. The most popular use case is working with data in"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Federated queries

[Federated queries](../../query_execution/federated_query/index.md) allow you to query data stored in external systems without first loading it (ETL) into YDB. The most popular use case is working with data in S3-compatible object storage.

## How it works

You can create an [external table](../../datamodel/external_table.md) in YDB that references data in S3. When you execute a SELECT query against such a table, YDB initiates a parallel read from all compute nodes. Each node reads and processes only the portion of data it needs.

- Supported formats: [Parquet, CSV, JSON](../../query_execution/federated_query/s3/formats.md) with [various compression algorithms](../../query_execution/federated_query/s3/formats.md#compression).
- Read optimization: YDB uses S3 data read optimization mechanisms (partition pruning) for [Hive-style partitioning](../../query_execution/federated_query/s3/partitioning.md) and for [more complex partitioning schemes](../../query_execution/federated_query/s3/partition_projection.md).

![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/concepts/analytics/concepts/_includes/s3_read.png)
