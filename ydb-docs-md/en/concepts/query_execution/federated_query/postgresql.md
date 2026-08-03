---
title: "Working with PostgreSQL Databases"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/postgresql?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/postgresql"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/postgresql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/postgresql.md"
description: "This section provides basic information on working with external PostgreSQL databases."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Working with PostgreSQL Databases

This section provides basic information on working with external [PostgreSQL](http://postgresql.org) databases.

To work with an external PostgreSQL database, you need to follow these steps:

1. Create a [secret](../../datamodel/secrets.md) containing the password for connecting to the database.

   ```yql
   CREATE SECRET postgresql_datasource_user_password WITH (value = "<password>");
   ```

2. Create an [external data source](../../datamodel/external_data_source.md) that describes a specific database within the PostgreSQL cluster. By default, the [namespace](https://www.postgresql.org/docs/current/catalog-pg-namespace.html) `public` is used for reading, but this value can be changed using the optional `SCHEMA` parameter. The network connection is made using the standard ([Frontend/Backend Protocol](https://www.postgresql.org/docs/current/protocol.html)) over TCP transport (`PROTOCOL="NATIVE"`). You can enable encryption of connections to the external database using the `USE_TLS="TRUE"` parameter.

   ```yql
   CREATE EXTERNAL DATA SOURCE postgresql_datasource WITH (
       SOURCE_TYPE="PostgreSQL",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="postgresql_datasource_user_password",
       PROTOCOL="NATIVE",
       USE_TLS="TRUE",
       SCHEMA="<schema>"
   );
   ```

3. Deploy the [connector](architecture.md#connectors) and [configure](../../../devops/deployment-options/manual/federated-queries/index.md) the YDB dynamic nodes to interact with it. Additionally, ensure network access from the YDB dynamic nodes to the external data source (at the address specified in the `LOCATION` parameter of the `CREATE EXTERNAL DATA SOURCE` request). If network connection encryption to the external source was enabled in the previous step, the connector will use the system's root certificates. More details on TLS configuration can be found in the [guide](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) on deploying the connector.

4. [Execute a query](postgresql.md#query) to the database.

## Query Syntax {#query}

The following SQL query format is used to work with PostgreSQL:

```yql
SELECT * FROM postgresql_datasource.<table_name>
```

where:

- `postgresql_datasource` - identifier of the external data source;
- `<table_name>` - table name within the external data source.

## Limitations

When working with PostgreSQL clusters, there are a number of limitations:

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
   | `Decimal` |

## Supported Data Types

In the PostgreSQL database, the optionality of column values (whether a column can contain `NULL` values) is not part of the data type system. The `NOT NULL` constraint for each column is implemented as the `attnotnull` attribute in the system catalog [pg_attribute](https://www.postgresql.org/docs/current/catalog-pg-attribute.html), i.e., at the metadata level of the table. Therefore, all basic PostgreSQL types can contain `NULL` values by default, and in the YDB type system, they should be mapped to [optional](../../../yql/reference/types/optional.md) types.

Below is a correspondence table between PostgreSQL and YDB types. All other data types, except those listed, are not supported.

| PostgreSQL Data Type | YDB Data Type | Notes |
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
| `date` | `Optional<Date>` | Valid date range from 1970-01-01 to 2105-12-31. Values outside this range return `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `bytea` | `Optional<String>` |  |
| `character` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html), string padded with spaces to the required length. |
| `character varying` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html). |
| `text` | `Optional<Utf8>` | [Default collation rules](https://www.postgresql.org/docs/current/collation.html). |
| `json` | `Optional<Json>` |  |
| `numeric(p,s)` | `Optional<Decimal(p,s)>` | `p` - total number of digits in the number, `s` - number of digits after the decimal point. Unconstrained numbers (`numeric` without parameters) are mapped into `<Optional<Decimal(35,0)>>`. `numeric` types with `p > 35` or `s < 0` are not supported. |
