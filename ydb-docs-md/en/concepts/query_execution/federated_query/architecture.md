---
title: "Federated Query Processing System Architecture"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/architecture?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/architecture"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/architecture.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/architecture.md"
description: "External Data Sources and External Tables."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Federated Query Processing System Architecture

## External Data Sources and External Tables

A key element of the federated query processing system in YDB is the concept of an [external data source](../../datamodel/external_data_source.md). Such sources can include relational DBMS, object storage, and other data storage systems. When processing a federated query, YDB streams data from external systems and allows performing the same range of operations on them as on local data.

To work with data located in external systems, YDB must have information about the internal structure of this data (e.g., the number, names, and types of columns in tables). Some sources provide such metadata along with the data itself, whereas for other unschematized sources, this metadata must be provided externally. This latter purpose is served by [external tables](../../datamodel/external_table.md).

Once external data sources and (if necessary) external tables are registered in YDB, the client can proceed to describe federated queries.

## Connectors

While executing federated queries, YDB needs to access external data storage systems over the network, for which it uses their client libraries. Including such dependencies negatively affects the codebase size, compilation time, and binary file size of YDB, as well as the product's overall stability.

The list of supported data sources for federated queries is constantly expanding. The most popular sources, such as S3, are natively supported by YDB. However, not all users require support for all sources simultaneously. Support can be optionally enabled using *connectors* - special microservices implementing a unified interface for accessing external data sources.

The functions of connectors include:

- Translating YQL queries into queries in the language specific to the external source (e.g., into another SQL dialect or HTTP API calls).
- Establishing network connections with data sources.
- Converting data retrieved from external sources into a columnar format in [Arrow IPC Stream](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc) format, supported by YDB.

![YDB Federated Query Architecture](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/concepts/query_execution/federated_query/_assets/architecture.png "YDB Federated Query Architecture")

Thus, connectors form an abstraction layer that hides the specifics of external data sources from YDB. The concise connector interface makes it easy to expand the list of supported sources with minimal changes to YDB's code.

Users can deploy [one of the ready-made connectors](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) or write their own implementation in any programming language according to the [gRPC specification](https://github.com/ydb-platform/ydb/tree/main/ydb/library/yql/providers/generic/connector/api/service/protos).

## List of Supported External Data Sources {#supported-datasources}

| Source | Support |
| --- | --- |
| [ClickHouse](https://clickhouse.com/) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [Greenplum](https://www.greenplum.org/) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [Microsoft SQL Server](https://learn.microsoft.com/en-us/sql/?view=sql-server-ver16) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [MySQL](https://www.mysql.com/) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [PostgreSQL](https://www.postgresql.org/) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [S3](https://aws.amazon.com/s3/) | Built into `ydbd` |
| [YDB](https://ydb.tech/) | Via connector [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
