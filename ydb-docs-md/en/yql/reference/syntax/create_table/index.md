---
title: "CREATE TABLE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create_table/?version=v26.1"
doc_path: "en/yql/reference/syntax/create_table/"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create_table/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create_table/index.md"
description: "The invocation of CREATE TABLE creates a table with the specified data schema and primary key columns ( PRIMARY KEY ). It also allows defining secondary indexes"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE TABLE

The invocation of `CREATE TABLE` creates a [table](../../../../concepts/datamodel/table.md) with the specified data schema and primary key columns (`PRIMARY KEY`). It also allows defining secondary indexes on the created table.

```yql
CREATE TABLE [IF NOT EXISTS] <table_name> (
  [<column_name> <column_data_type>] [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>]
  [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])]
  [, ...],
    INDEX <index_name>
      [GLOBAL]
      [SYNC|ASYNC]
      [USING <index_type>]
      ON ( <index_columns> )
      [COVER ( <cover_columns> )]
      [WITH ( <parameter_name> = <parameter_value>[, ...])]
    [, ...]
  PRIMARY KEY ( <column>[, ...]),
  [FAMILY <column_family> ( family_options[, ...])]
)
[PARTITION BY HASH ( <column>[, ...])]
[WITH (<setting_name> = <setting_value>[, ...])]

[AS SELECT ...]
```

## Request parameters

### table_name {#table_name}

The path of the table to be created.

When choosing a name for the table, consider the common [schema object naming rules](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

### IF NOT EXISTS

If the table with the specified name already exists, the execution of the operator is completely skipped — no checks or schema matching is performed, and no error occurs. Note that the existing table may differ in structure from the one you would like to create with this query — no comparison or equivalence check is performed.

### column_name {#column_name}

The name of the column to be created in the new table.

When choosing a name for the column, consider the common [column naming rules](../../../../concepts/datamodel/table.md#column-naming-rules).

### column_data_type {#column_data_type}

The data type of the column. The complete list of data types supported by YDB is available in the [YQL data types](../../types/index.md) section.

### FAMILY \<family_name> (column setting) {#family-lessfamily_namegreater-column-setting}

Specifies that this column belongs to the specified column group. For more information, see [Column groups](family.md).

### DEFAULT \<default_value> {#default-lessdefault_valuegreater}

> [!WARNING]
> The `DEFAULT` option is supported:
>
> - Only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is under development.
> - Only with literal values. Support for computed expressions is under development.

Allows you to set a default value for a column. If no value is specified for this column when inserting a row, the specified default value will be used. The default value must match the column's data type.

The `DEFAULT false NOT NULL` construct is invalid due to ambiguity in interpretation. In this case, use a comma-separated list or change the order of options.

### NULL

This column can contain `NULL` values (default).

### NOT NULL

This column does not accept `NULL` values.

### COMPRESSION(\[algorithm=\<algorithm_name>\[, level=\]\]) {#]]}

> [!WARNING]
> Supported only for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.

You can set the following compression parameters for columns:

- `algorithm` — compression algorithm. Allowed values: `off` (disable compression), `lz4`, `zstd`.
- `level` — compression level; supported only for `zstd` (allowed values are 0 through 22).

If `COMPRESSION()` is specified without parameters, the column uses the default compression. Currently that is `lz4`; future versions will let you configure default compression at the cluster or table level.

### INDEX

Definition of an index on the table. [Secondary indexes](secondary_index.md) and [vector indexes](vector_index.md) are supported.

### PRIMARY KEY

Definition of the primary key of the table. Specifies the columns that make up the primary key in the order of enumeration. For more information on selecting a primary key, see the [Choosing a primary key](../../../../dev/primary-key/index.md) article.

### PARTITION BY HASH

Definition of the columns on which partitioning will occur for **column-oriented** tables. Specifies the columns on which [partitioning](../../../../concepts/glossary.md#partition) will occur using the hash function. The columns must be part of the primary key. The columns do not necessarily have to be a prefix or suffix — the requirement is to be part of the primary key.

If the parameter is not specified, the table will be partitioned on the same columns as those included in the primary key. For more information on selecting and working with partition keys in column-oriented tables, see the [Choosing keys for maximum column-oriented table performance](../../../../dev/primary-key/column-oriented.md) article.

For more information on partitioning column-oriented tables, see the [Partitioning Column-Oriented Tables](../../../../concepts/datamodel/table.md#olap-tables-partitioning) section.

### FAMILY \<column_family> (column group setting) {#family-lesscolumn_familygreater-column-group-setting}

Definition of a column group with specified parameters. For more information, see the [Column groups](family.md) section.

### WITH

Additional parameters for creating a table. For more information, see the [Additional parameters (WITH)](with.md) section.

> [!NOTE]
> YDB supports two types of tables:
>
> - [Row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables.
> - [Column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.
>
> The table type is specified by the `STORE` parameter in the `WITH` clause, where `ROW` indicates a [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) table and `COLUMN` indicates a [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) table:
>
> ```yql
> CREATE <table_name> (
>   columns
>   ...
> )
> WITH (
>   STORE = COLUMN -- Default value ROW
> )
> ```
>
> By default, if the `STORE` parameter is not specified, a row-oriented table is created.

> [!NOTE]
> When choosing a name for the table, consider the common [schema object naming rules](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

### AS SELECT

Creating and filling a table with data from a `SELECT` query. For more information, see the [Creating a table filled with query results](as_select.md) section.

## Examples of table creation {#examples-tables-creation}

{% list tabs %}

- Creating a row-oriented table

  ```yql
  CREATE TABLE <table_name> (
    a Uint64,
    b Uint64,
    c Float,
    PRIMARY KEY (a, b)
  );
  ```

  Example of creating a table with a DEFAULT value:

  ```yql
  CREATE TABLE table_with_default (
    id Uint64,
    name String DEFAULT "unknown",
    score Double NOT NULL DEFAULT 0.0,
    PRIMARY KEY (id)
  );
  ```

  For both key and non-key columns, only [primitive](../../types/primitive.md) data types are allowed.

  Without additional modifiers, a column acquires an [optional](../../types/optional.md) type and allows `NULL` values. To designate a non-optional type, use the `NOT NULL` constraint.

  Specifying a `PRIMARY KEY` with a non-empty list of columns is mandatory. These columns become part of the key in the order they are listed.

  Example of creating a row-oriented table using partitioning options:

  ```yql
  CREATE TABLE <table_name> (
    a Uint64,
    b Uint64,
    c Float,
    PRIMARY KEY (a, b)
  )
  WITH (
    AUTO_PARTITIONING_BY_SIZE = ENABLED,
    AUTO_PARTITIONING_PARTITION_SIZE_MB = 512
  );
  ```

  Such code will create a row-oriented table with automatic partitioning by partition size (`AUTO_PARTITIONING_BY_SIZE`) enabled, and with the preferred size of each partition (`AUTO_PARTITIONING_PARTITION_SIZE_MB`) set to 512 megabytes. The full list of row-oriented table partitioning options can be found in the [Partitioning Row-Oriented Tables](../../../../concepts/datamodel/table.md#partitioning_row_table) section.

- Creating a column-oriented table

  ```yql
  CREATE TABLE table_name (
    a Uint64 NOT NULL,
    b Timestamp NOT NULL,
    c Float,
    PRIMARY KEY (a, b)
  )
  PARTITION BY HASH(b)
  WITH (
    STORE = COLUMN
  );
  ```

  For column-oriented tables, you can explicitly specify the columns on which partitioning will occur using the `PARTITION BY HASH` construct. Usually, these are columns of the primary key with a large number of unique values, such as `Timestamp`. If `PARTITION BY HASH` is not specified, partitioning will occur automatically on all columns included in the primary key. For more information on selecting and working with partition keys in column-oriented tables, see the [Choosing keys for maximum column-oriented table performance](../../../../dev/primary-key/column-oriented.md) article.

  It is important to specify the correct number of partitions when creating a column-oriented table with the `AUTO_PARTITIONING_MIN_PARTITIONS_COUNT` parameter:

  ```yql
  CREATE TABLE table_name (
    a Uint64 NOT NULL,
    b Timestamp NOT NULL,
    c Float,
    PRIMARY KEY (a, b)
  )
  PARTITION BY HASH(b)
  WITH (
    STORE = COLUMN,
    AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 10
  );
  ```

  This code will create a columnar table with 10 partitions. The full list of column-oriented table partitioning options can be found in the [Partitioning Column-Oriented Tables](../../../../concepts/datamodel/table.md#olap-tables-partitioning) section.

{% endlist %}

When creating row-oriented tables, it is possible to specify:

- [A secondary index](secondary_index.md).
- [A vector index](vector_index.md).
- [Column groups](family.md).
- [Additional parameters](with.md).
- [Creating a table filled with query results](as_select.md).

When creating column-oriented tables, it is possible to specify:

- [Column groups](family.md).
- [Additional parameters](with.md).
- [Creating a table filled with query results](as_select.md).
