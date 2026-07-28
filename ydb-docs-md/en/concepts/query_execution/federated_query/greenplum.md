---
title: "Working with Greenplum Databases"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/greenplum?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/greenplum"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/greenplum.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/greenplum.md"
description: "This section provides basic information on working with external Greenplum databases. Since Greenplum is based on PostgreSQL, integrations with them are similar"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Working with Greenplum Databases

This section provides basic information on working with external [Greenplum](https://greenplum.org) databases. Since Greenplum is based on [PostgreSQL](postgresql.md), integrations with them are similar, and some links below may lead to PostgreSQL documentation.

Follow these steps to work with an external Greenplum database:

1. Create a [secret](../../datamodel/secrets.md) containing the password for connecting to the database.

   ```yql
   CREATE SECRET greenplum_datasource_user_password WITH (value = "<password>");
   ```

2. Create an [external data source](../../datamodel/external_data_source.md) that describes a specific database within the Greenplum cluster. In the `LOCATION` parameter, pass the network address of the [master node](https://greenplum.org/introduction-to-greenplum-architecture/) of Greenplum. By default, the [namespace](https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/ref_guide-system_catalogs-pg_namespace.html) `public` is used for reading, but this value can be changed using the optional `SCHEMA` parameter. The network connection is made using the standard [Frontend/Backend Protocol](https://www.postgresql.org/docs/current/protocol.html) over TCP transport (`PROTOCOL="NATIVE"`). You can enable encryption of connections to the external database using the `USE_TLS="TRUE"` parameter.

   ```yql
   CREATE EXTERNAL DATA SOURCE greenplum_datasource WITH (
       SOURCE_TYPE="Greenplum",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="greenplum_datasource_user_password",
       PROTOCOL="NATIVE",
       USE_TLS="TRUE",
       SCHEMA="<schema>"
   );
   ```

3. Deploy the [connector](architecture.md#connectors) and [configure](../../../devops/deployment-options/manual/federated-queries/index.md) the YDB dynamic nodes to interact with it. Additionally, ensure network access from the YDB dynamic nodes to the external data source (at the address specified in the `LOCATION` parameter of the `CREATE EXTERNAL DATA SOURCE` request). If network connection encryption to the external source was enabled in the previous step, the connector will use the system's root certificates. More details on TLS configuration can be found in the [guide](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) on deploying the connector.

4. [Execute a query](greenplum.md#query) to the database.

## Query Syntax {#query}

The following SQL query format is used to work with Greenplum:

```yql
SELECT * FROM greenplum_datasource.<table_name>
```

where:

- `greenplum_datasource` - identifier of the external data source;
- `<table_name>` - table name within the external data source.

## Limitations

When working with Greenplum clusters, there are a number of limitations:

1. External sources are available only for reading data through `SELECT` queries. The federated query processing engine currently does not support queries that modify tables in external sources.

2. If the date value stored in the external data source is outside the allowed range for YDB (all dates used must be later than 1970-01-01 but earlier than 2105-12-31), such a value in YDB will be converted to `NULL`.

3. The YDB federated query processing system is capable of delegating the execution of certain parts of a query to the system acting as the data source. Query fragments are passed through YDB directly to the external system and processed by them. This optimization, known as "predicate pushdown", significantly reduces the amount of data transferred from the source to the federated query processing engine. This reduces network load and saves computational resources for the federated YDB.

   A specific case of predicate pushdown, when the filtering expressions are specified after the `WHERE` keyword, are passed to the data source, is called "filter pushdown". Filter pushdown is possible when using:

   | Description | Example |
   | --- | --- |
   | `NULL` checks | `WHERE column1 IS NULL` or `WHERE column1 IS NOT NULL` |
   | Logical conditions `OR`, `NOT`, `AND` and parentheses for controlling calculation priority. | `WHERE column1 IS NULL OR (column2 IS NOT NULL AND column3 > 10)`. |
   | [Comparison operators](../../../yql/reference/syntax/expressions.md#comparison-operators) with other columns or constants. | `WHERE column1 > column2 OR column3 <= 10`, `WHERE column1 + column2 > 10`, `WHERE column1 = (10 + 10)` |

   When using other types of filters, pushdown to the data source is not performed: filtering of the external table rows will be executed by the federated YDB, which means that YDB will perform a full scan of the external table when processing the query.

   Supported data types for filter pushdown:

   | YDB Data Type |
   | --- |
   | `Bool` |
   | `Int8` |
   | `Int16` |
   | `Int32` |
   | `Int64` |
   | `Float` |
   | `Double` |

## Supported Data Types

In the Greenplum database, the optionality of column values (whether a column can contain `NULL` values) is not part of the data type system. The `NOT NULL` constraint for each column is implemented as the `attnotnull` attribute in the system catalog [pg_attribute](https://www.postgresql.org/docs/current/catalog-pg-attribute.html), i.e., at the metadata level of the table. Therefore, all basic Greenplum types can contain `NULL` values by default, and in the YDB type system, they should be mapped to [optional](../../../yql/reference/types/optional.md) types.

Below is a correspondence table between Greenplum and YDB types. All other data types, except those listed, are not supported.

| Greenplum Data Type | YDB Data Type | Notes |
| --- | --- | --- |
| `boolean` | `Optional<Bool>` |  |
| `smallint` | `Optional<Int16>` |  |
| `int2` | `Optional<Int16>` |  |
| `integer` | `Optional<Int32>` |  |
| `int` | `Optional<Int32>` |  |
| `int4` | `Optional<Int32>` |  |
| `serial` | `Optional<Int32>` |  |
| `serial4` | `Optional<Int32>` |  |
| `bigint` | `Optional<Int64>` |  |
| `int8` | `Optional<Int64>` |  |
| `bigserial` | `Optional<Int64>` |  |
| `serial8` | `Optional<Int64>` |  |
| `real` | `Optional<Float>` |  |
| `float4` | `Optional<Float>` |  |
| `double precision` | `Optional<Double>` |  |
| `float8` | `Optional<Double>` |  |
| `json` | `Optional<Json>` |  |
| `date` | `Optional<Date>` | Valid date range from 1970-01-01 to 2105-12-31. Values outside this range return `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `bytea` | `Optional<String>` |  |
| `character` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html), string padded with spaces to the required length. |
| `character varying` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html). |
| `text` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html). |
