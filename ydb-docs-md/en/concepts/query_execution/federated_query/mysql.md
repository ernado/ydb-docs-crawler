---
title: "Working with MySQL Databases"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/mysql?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/mysql"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/mysql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/mysql.md"
description: "This section provides basic information about working with external MySQL databases. To work with an external MySQL database, you need to follow these steps:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Working with MySQL Databases

This section provides basic information about working with external [MySQL](https://www.mysql.com/) databases.

To work with an external MySQL database, you need to follow these steps:

1. Create a [secret](../../datamodel/secrets.md) containing the password for connecting to the database.

   ```yql
   CREATE SECRET mysql_datasource_user_password WITH (value = "<password>");
   ```

2. Create an [external data source](../../datamodel/external_data_source.md) that describes a specific MySQL database. The `LOCATION` parameter contains the network address of the MySQL instance to connect to. The `DATABASE_NAME` specifies the database name (for example, `mysql`). The `LOGIN` and `PASSWORD_SECRET_PATH` parameters are used for authentication to the external database. You can enable encryption for connections to the external database using the `USE_TLS="TRUE"` parameter.

   ```yql
   CREATE EXTERNAL DATA SOURCE mysql_datasource WITH (
       SOURCE_TYPE="MySQL",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="mysql_datasource_user_password",
       USE_TLS="TRUE"
   );
   ```

3. Deploy the [connector](architecture.md#connectors) and [configure](../../../devops/deployment-options/manual/federated-queries/index.md) the YDB dynamic nodes to interact with it. Additionally, ensure network access from the YDB dynamic nodes to the external data source (at the address specified in the `LOCATION` parameter of the `CREATE EXTERNAL DATA SOURCE` request). If network connection encryption to the external source was enabled in the previous step, the connector will use the system's root certificates. More details on TLS configuration can be found in the [guide](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) on deploying the connector.

4. [Execute a query](mysql.md#query) to the database.

## Query Syntax {#query}

The following SQL query format is used to work with MySQL:

```yql
SELECT * FROM mysql_datasource.<table_name>
```

where:

- `mysql_datasource` - the external data source identifier;
- `<table_name>` - the table name within the external data source.

## Limitations

When working with MySQL clusters, there are a number of limitations:

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

## Supported Data Types

In the MySQL database, the optionality of column values (whether the column can contain `NULL` values or not) is not a part of the data type system. The `NOT NULL` constraint for any column of any table is stored within the `IS_NULLABLE` column in the [INFORMATION_SCHEMA.COLUMNS](https://dev.mysql.com/doc/refman/8.4/en/information-schema-columns-table.html) system table, i.e., at the table metadata level. Therefore, all basic MySQL types can contain `NULL` values by default, and in the YDB type system they should be mapped to [optional](../../../yql/reference/types/optional.md).

Below is a correspondence table between MySQL types and YDB types. All other data types, except those listed, are not supported.

| MySQL Data Type | YDB Data Type | Notes |
| --- | --- | --- |
| `bool` | `Optional<Bool>` |  |
| `tinyint` | `Optional<Int8>` |  |
| `tinyint unsigned` | `Optional<Uint8>` |  |
| `smallint` | `Optional<Int16>` |  |
| `smallint unsigned` | `Optional<Uint16>` |  |
| `mediumint` | `Optional<Int32>` |  |
| `mediumint unsigned` | `Optional<Uint32>` |  |
| `int` | `Optional<Int32>` |  |
| `int unsigned` | `Optional<Uint32>` |  |
| `bigint` | `Optional<Int64>` |  |
| `bigint unsigned` | `Optional<Uint64>` |  |
| `float` | `Optional<Float>` |  |
| `real` | `Optional<Float>` |  |
| `double` | `Optional<Double>` |  |
| `date` | `Optional<Date>` | Valid date range from 1970-01-01 to 2105-12-31. Values outside this range return `NULL`. |
| `datetime` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Valid time range from 1970-01-01 00:00:00 to 2105-12-31 23:59:59. Values outside this range return `NULL`. |
| `tinyblob` | `Optional<String>` |  |
| `blob` | `Optional<String>` |  |
| `mediumblob` | `Optional<String>` |  |
| `longblob` | `Optional<String>` |  |
| `tinytext` | `Optional<String>` |  |
| `text` | `Optional<String>` |  |
| `mediumtext` | `Optional<String>` |  |
| `longtext` | `Optional<String>` |  |
| `char` | `Optional<Utf8>` |  |
| `varchar` | `Optional<Utf8>` |  |
| `binary` | `Optional<String>` |  |
| `varbinary` | `Optional<String>` |  |
| `json` | `Optional<Json>` |  |
