---
title: "Working with ClickHouse Databases"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/clickhouse?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/clickhouse"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/clickhouse.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/clickhouse.md"
description: "This section describes the basic information about working with the external ClickHouse database ClickHouse."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Working with ClickHouse Databases

This section describes the basic information about working with the external ClickHouse database [ClickHouse](https://clickhouse.com).

To work with the external ClickHouse database, the following steps must be completed:

1. Create a [secret](../../datamodel/secrets.md) containing the password to connect to the database.

   ```yql
   CREATE SECRET clickhouse_datasource_user_password WITH (value = "<password>");
   ```

2. Create an [external data source](../../datamodel/external_data_source.md) describing the target database inside the ClickHouse cluster. To connect to ClickHouse, you can use either the [native TCP protocol](https://clickhouse.com/docs/en/interfaces/tcp) (`PROTOCOL="NATIVE"`) or the [HTTP protocol](https://clickhouse.com/docs/en/interfaces/http) (`PROTOCOL="HTTP"`). To enable encryption for connections to the external database, use the `USE_TLS="TRUE"` parameter.

   ```yql
   CREATE EXTERNAL DATA SOURCE clickhouse_datasource WITH (
       SOURCE_TYPE="ClickHouse",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="<login>",
       PASSWORD_SECRET_PATH="clickhouse_datasource_user_password",
       PROTOCOL="NATIVE",
       USE_TLS="TRUE"
   );
   ```

3. Deploy the [connector](architecture.md#connectors) and [configure](../../../devops/deployment-options/manual/federated-queries/index.md) the YDB dynamic nodes to interact with it. Additionally, ensure network access from the YDB dynamic nodes to the external data source (at the address specified in the `LOCATION` parameter of the `CREATE EXTERNAL DATA SOURCE` request). If network connection encryption to the external source was enabled in the previous step, the connector will use the system's root certificates. More details on TLS configuration can be found in the [guide](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) on deploying the connector.

4. [Execute a query](clickhouse.md#query) to the database.

## Query Syntax {#query}

To work with ClickHouse, use the following SQL query form:

```yql
SELECT * FROM clickhouse_datasource.<table_name>
```

Where:

- `clickhouse_datasource` is the identifier of the external data source;
- `<table_name>` is the table's name within the external data source.

## Limitations

There are several limitations when working with ClickHouse clusters:

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
   | `Uint8` |
   | `Int16` |
   | `Uint16` |
   | `Int32` |
   | `Uint32` |
   | `Int64` |
   | `Uint64` |
   | `Float` |
   | `Double` |
   | `String` |

## Supported Data Types

By default, ClickHouse columns cannot physically contain `NULL` values. However, users can create tables with columns of optional or [nullable](https://clickhouse.com/docs/en/sql-reference/data-types/nullable) types. The column types displayed in YDB when extracting data from the external ClickHouse database will depend on whether primitive or optional types are used in the ClickHouse table. Due to the previously discussed limitations of YDB types used to store dates and times, all similar ClickHouse types are displayed in YDB as [optional](../../../yql/reference/types/optional.md).

Below are the mapping tables for ClickHouse and YDB types. All other data types, except those listed, are not supported.

### Primitive Data Types

| ClickHouse data type | YDB data type | Notes |
| --- | --- | --- |
| `Bool` | `Bool` |  |
| `Int8` | `Int8` |  |
| `UInt8` | `Uint8` |  |
| `Int16` | `Int16` |  |
| `UInt16` | `Uint16` |  |
| `Int32` | `Int32` |  |
| `UInt32` | `Uint32` |  |
| `Int64` | `Int64` |  |
| `UInt64` | `Uint64` |  |
| `Float32` | `Float` |  |
| `Float64` | `Double` |  |
| `Date` | `Date` |  |
| `Date32` | `Optional<Date>` | Valid date range from 1970-01-01 to 2105-12-31. Values outside this range return `NULL`. |
| `DateTime` | `Optional<DateTime>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `DateTime64` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `String` | `String` |  |
| `FixedString` | `String` | Null bytes in `FixedString` are transferred to `String` unchanged. |

### Optional Data Types

| ClickHouse data type | YDB data type | Notes |
| --- | --- | --- |
| `Nullable(Bool)` | `Optional<Bool>` |  |
| `Nullable(Int8)` | `Optional<Int8>` |  |
| `Nullable(UInt8)` | `Optional<Uint8>` |  |
| `Nullable(Int16)` | `Optional<Int16>` |  |
| `Nullable(UInt16)` | `Optional<Uint16>` |  |
| `Nullable(Int32)` | `Optional<Int32>` |  |
| `Nullable(UInt32)` | `Optional<Uint32>` |  |
| `Nullable(Int64)` | `Optional<Int64>` |  |
| `Nullable(UInt64)` | `Optional<Uint64>` |  |
| `Nullable(Float32)` | `Optional<Float>` |  |
| `Nullable(Float64)` | `Optional<Double>` |  |
| `Nullable(Date)` | `Optional<Date>` |  |
| `Nullable(Date32)` | `Optional<Date>` | Valid date range from 1970-01-01 to 2105-12-31. Values outside this range return `NULL`. |
| `Nullable(DateTime)` | `Optional<DateTime>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `Nullable(DateTime64)` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `Nullable(String)` | `Optional<String>` |  |
| `Nullable(FixedString)` | `Optional<String>` | Null bytes in `FixedString` are transferred to `String` unchanged. |
