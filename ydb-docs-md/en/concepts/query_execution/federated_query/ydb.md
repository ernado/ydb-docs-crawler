---
title: "Working with YDB Databases"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/ydb?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/ydb"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/ydb.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/ydb.md"
description: "YDB can act as an external data source for another YDB database. This section discusses the organization of collaboration between two independent YDB databases"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Working with YDB Databases

YDB can act as an external data source for another YDB database. This section discusses the organization of collaboration between two independent YDB databases in federated query processing mode.

To connect to an external YDB database from another YDB database acting as the federated query engine, the following steps need to be performed on the latter:

1. Prepare authentication data to access the remote YDB database. Currently, in federated queries to YDB, the only available authentication method is [login and password](../../../security/authentication.md#static-credentials) (other methods are not supported). The password to the external database is stored as a [secret](../../datamodel/secrets.md):

   ```yql
   CREATE SECRET ydb_datasource_user_password WITH (value = "<password>");
   ```

2. Create an [external data source](../../datamodel/external_data_source.md) describing the external YDB database. The `LOCATION` parameter contains the network address of the YDB instance to which the network connection is made. The `DATABASE_NAME` specifies the name of the database (e.g., `local`). For authentication to the external database, the `LOGIN` and `PASSWORD_SECRET_PATH` parameters are used. Encryption of connections to the external database can be enabled using the `USE_TLS="TRUE"` parameter. If encryption is enabled, the `<port>` field in the `LOCATION` parameter should specify the gRPCs port of the external YDB; otherwise, the gRPC port should be specified.

   ```yql
   CREATE EXTERNAL DATA SOURCE ydb_datasource WITH (
       SOURCE_TYPE="Ydb",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="ydb_datasource_user_password",
       USE_TLS="TRUE"
   );
   ```

3. Deploy the [connector](architecture.md#connectors) and [configure](../../../devops/deployment-options/manual/federated-queries/index.md) the YDB dynamic nodes to interact with it. Additionally, ensure network access from the YDB dynamic nodes to the external data source (at the address specified in the `LOCATION` parameter of the `CREATE EXTERNAL DATA SOURCE` request). If network connection encryption to the external source was enabled in the previous step, the connector will use the system's root certificates. More details on TLS configuration can be found in the [guide](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) on deploying the connector.

4. [Execute a query](ydb.md#query) to the external data source.

## Query Syntax {#query}

To retrieve data from tables of the external YDB database, the following form of SQL query is used:

```yql
SELECT * FROM ydb_datasource.`<table_name>`
```

Where:

- `ydb_datasource` - identifier of the external data source;
- `<table_name>` - full name of the table within the [hierarchy](../../concepts/index.md#ydb-hierarchy) of directories in the YDB database, e.g., `table`, `dir1/table1`, or `dir1/dir2/table3`.

If the table is at the top level of the hierarchy (not belonging to any directories), it is permissible not to enclose the table name in backticks "\`":

```yql
SELECT * FROM ydb_datasource.<table_name>
```

## Limitations

There are several limitations when working with external YDB data sources:

1. External sources are available only for reading data through `SELECT` queries. The federated query processing engine currently does not support queries that modify tables in external sources.

2. The YDB federated query processing system is capable of delegating the execution of certain parts of a query to the system acting as the data source. Query fragments are passed through YDB directly to the external system and processed by them. This optimization, known as "predicate pushdown", significantly reduces the amount of data transferred from the source to the federated query processing engine. This reduces network load and saves computational resources for the federated YDB.

   A specific case of predicate pushdown, when the filtering expressions are specified after the `WHERE` keyword, are passed to the data source, is called "filter pushdown". Filter pushdown is possible when using:

   | Description | Example | Limitation |
   | --- | --- | --- |
   | `NULL` checks | `WHERE column1 IS NULL` or `WHERE column1 IS NOT NULL` |  |
   | Logical conditions `OR`, `NOT`, `AND` and parentheses for controlling calculation priority. | `WHERE column1 IS NULL OR (column2 IS NOT NULL AND column3 > 10)`. |  |
   | [Comparison operators](../../../yql/reference/syntax/expressions.md#comparison-operators) with other columns or constants. | `WHERE column1 > column2 OR column3 <= 10`. |  |
   | String pattern matching operator `LIKE`. | `WHERE column1 LIKE '_abc%'` | Currently only supports pushdown of simple patterns based on prefixes (`'abc_'`, `'abc%'`), suffixes (`'_abc'`, `'%abc'`) or substring search (`'_abc_'`, `'%abc%'`, `'_abc%'`, `'%abc_'`). For more complex pattern pushdown, it is recommended to use `REGEXP`. |
   | String pattern matching operator `REGEXP`. | `WHERE column1 REGEXP '.*abc.*'` |  |

   When using other types of filters, pushdown to the data source is not performed: filtering of the external table rows will be executed by the federated YDB, which means that YDB will perform a full scan of the external table when processing the query.

   Supported data types for the filter pushdown:

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
   | `Utf8` |

## Supported Data Types

When working with tables located in the external YDB database, users have access to a limited set of data types. All other types, except for those listed below, are not supported. In some cases the type conversion is performed, meaning that the columns of the table from the external YDB database may change their type after being read by the YDB database processing the federated query.

| External YDB data type | Federated YDB data type |
| --- | --- |
| `Bool` | `Bool` |
| `Int8` | `Int8` |
| `Int16` | `Int16` |
| `Int32` | `Int32` |
| `Int64` | `Int64` |
| `Uint8` | `Uint8` |
| `Uint16` | `Uint16` |
| `Uint32` | `Uint32` |
| `Uint64` | `Uint64` |
| `Float` | `Float` |
| `Double` | `Double` |
| `String` | `String` |
| `Utf8` | `Utf8` |
| `Date` | `Date` |
| `Datetime` | `Datetime` |
| `Timestamp` | `Timestamp` |
| `Json` | `Json` |
| `JsonDocument` | `Json` |
