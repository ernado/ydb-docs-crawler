---
title: "External Data Sources"
url: "https://ydb.tech/docs/en/concepts/datamodel/external_data_source?version=v26.1"
doc_path: "en/concepts/datamodel/external_data_source"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/datamodel/external_data_source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/datamodel/external_data_source.md"
description: "An external data source is an object in YDB that describes the connection parameters to an external data source. For example, in the case of ClickHouse, the ext"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# External Data Sources

An external data source is an object in YDB that describes the connection parameters to an external data source. For example, in the case of ClickHouse, the external data source describes the network address, login, and password for authentication in the ClickHouse cluster. In the case of S3 (Object Storage), it describes the access credentials and the path to the bucket.

The following example demonstrates creating an external data source pointing to a ClickHouse cluster:

```yql
CREATE EXTERNAL DATA SOURCE test_data_source WITH (
  SOURCE_TYPE="ClickHouse",
  LOCATION="192.168.1.1:8123",
  DATABASE_NAME="default",
  AUTH_METHOD="BASIC",
  USE_TLS="TRUE",
  LOGIN="login",
  PASSWORD_SECRET_PATH="test_password_path",
  PROTOCOL="NATIVE"
);
```

After creating an external data source, you can read data from the created `EXTERNAL DATA SOURCE` object. The example below illustrates reading data from the `test_table` table in the `default` database in the ClickHouse cluster:

```yql
SELECT * FROM test_data_source.test_table;
```

External data sources allow execution of [federated queries](../query_execution/federated_query/index.md) for cross-system data analytics tasks.

The following data sources can be used:

- [ClickHouse](../query_execution/federated_query/clickhouse.md)
- [PostgreSQL](../query_execution/federated_query/postgresql.md)
- [Connections to S3 (Object Storage)](../query_execution/federated_query/s3/external_data_source.md)
