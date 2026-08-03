---
title: "Federated Queries"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/index.md"
description: "Federated queries allow retrieving information from various data sources without needing to transfer the data from these sources into YDB storage. Currently, fe"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Federated Queries

Federated queries allow retrieving information from various data sources without needing to transfer the data from these sources into YDB storage. Currently, federated queries support interaction with ClickHouse, PostgreSQL, and S3-compatible data stores. Using YQL queries, you can access these databases without the need to duplicate data between systems.

To work with data stored in external DBMSs, it is sufficient to create an [external data source](../../datamodel/external_data_source.md). To work with unstructured data stored in S3 buckets, you additionally need to create an [external table](../../datamodel/external_table.md). In both cases, it is necessary to create [secrets](../../datamodel/secrets.md) objects first that store confidential data required for authentication in external systems.

You can learn about the internals of the federated query processing system in the [architecture](architecture.md) section. Detailed information on working with various data sources is provided in the corresponding sections:

- [ClickHouse](clickhouse.md)
- [Greenplum](greenplum.md)
- [Microsoft SQL Server](ms_sql_server.md#query)
- [MySQL](mysql.md)
- [PostgreSQL](postgresql.md)
- [S3](s3/external_table.md)
- [YDB](ydb.md)
