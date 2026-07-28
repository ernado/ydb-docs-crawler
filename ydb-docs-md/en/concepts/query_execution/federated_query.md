---
title: "Federated Queries"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/index.md"
description: "Federated queries allow retrieving information from various data sources without needing to transfer the data from these sources into YDB storage. Currently, fe"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Federated Queries

Federated queries allow retrieving information from various data sources without needing to transfer the data from these sources into YDB storage. Currently, federated queries support interaction with ClickHouse, PostgreSQL, and S3-compatible data stores. Using YQL queries, you can access these databases without the need to duplicate data between systems.

To work with data stored in external DBMSs, it is sufficient to create an [external data source](../datamodel/external_data_source.md). To work with unstructured data stored in S3 buckets, you additionally need to create an [external table](../datamodel/external_table.md). In both cases, it is necessary to create [secrets](../datamodel/secrets.md) objects first that store confidential data required for authentication in external systems.

You can learn about the internals of the federated query processing system in the [architecture](federated_query/architecture.md) section. Detailed information on working with various data sources is provided in the corresponding sections:

- [ClickHouse](federated_query/clickhouse.md)
- [Greenplum](federated_query/greenplum.md)
- [Microsoft SQL Server](federated_query/ms_sql_server.md#query)
- [MySQL](federated_query/mysql.md)
- [PostgreSQL](federated_query/postgresql.md)
- [S3](federated_query/s3/external_table.md)
- [YDB](federated_query/ydb.md)
