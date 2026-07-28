---
title: "Changing columns"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/columns?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/columns"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/columns.md"
description: "YDB supports adding columns to row and column tables, deleting non-key columns from tables, and changing properties of existing columns. ADD COLUMN."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Changing columns

YDB supports adding columns to [row](../../../../concepts/datamodel/table.md#row-oriented-tables) and [column](../../../../concepts/datamodel/table.md#column-oriented-tables) tables, deleting non-key columns from tables, and changing properties of existing columns.

## ADD COLUMN

Builds a new column with the specified name, type, and options for the specified table.

```yql
ALTER TABLE table_name ADD COLUMN column_name column_data_type [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>] [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])];
```

## Request parameters

### table_name {#table_name}

The path of the table to be modified.

### column_name {#column_name}

The name of the column to be created. When choosing a name for the column, consider the common [column naming rules](../../../../concepts/datamodel/table.md#column-naming-rules).

### column_data_type {#column_data_type}

The data type of the column. The complete list of data types supported by YDB is available in the [YQL data types](../../types/index.md) section.

### FAMILY \<family_name> (column setting) {#family-lessfamily_namegreater-column-setting}

Specifies that this column belongs to the specified column group. For more information, see [Column groups](../create_table/family.md).

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

## Example

The code below will add a column named `views` with data type `Uint64` to the `episodes` table.

```yql
ALTER TABLE episodes ADD COLUMN views Uint64;
```

The code below will add a column named `rate` with data type `Double` and default value `5.0` to the `episodes` table.

```yql
ALTER TABLE episodes ADD COLUMN rate Double NOT NULL DEFAULT 5.0;
ALTER TABLE episodes ADD COLUMN rate Double (DEFAULT 5.0, NOT NULL); -- alternative syntax
```

## ALTER COLUMN

Modifies properties of an existing column in the specified table. Property changes are applied without recreating the column. Some properties apply only to newly written data or during compaction (see the description of each property for details).

```yql
ALTER TABLE table_name ALTER COLUMN column_name {SET | DROP} [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>] [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])];
```

### Request parameters {#request-parameters1}

#### table_name {#table_name1}

The path of the table containing the column to change.

#### column_name {#column_name1}

The name of the column to change in the specified table.

#### SET

Set a column option.

#### DROP

Remove a column option. Currently only `NOT NULL` can be removed.

### FAMILY \<family_name> (column setting) {#family-lessfamily_namegreater-column-setting1}

Specifies that this column belongs to the specified column group. For more information, see [Column groups](../create_table/family.md).

### DEFAULT \<default_value> {#default-lessdefault_valuegreater1}

> [!WARNING]
> The `DEFAULT` option is supported:
>
> - Only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is under development.
> - Only with literal values. Support for computed expressions is under development.

Allows you to set a default value for a column. If no value is specified for this column when inserting a row, the specified default value will be used. The default value must match the column's data type.

The `DEFAULT false NOT NULL` construct is invalid due to ambiguity in interpretation. In this case, use a comma-separated list or change the order of options.

### NULL {#null1}

This column can contain `NULL` values (default).

### NOT NULL {#not-null1}

This column does not accept `NULL` values.

### COMPRESSION(\[algorithm=\<algorithm_name>\[, level=\]\]) {#]]1}

> [!WARNING]
> Supported only for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.

You can set the following compression parameters for columns:

- `algorithm` — compression algorithm. Allowed values: `off` (disable compression), `lz4`, `zstd`.
- `level` — compression level; supported only for `zstd` (allowed values are 0 through 22).

If `COMPRESSION()` is specified without parameters, the column uses the default compression. Currently that is `lz4`; future versions will let you configure default compression at the cluster or table level.

### Examples

The code below will disallow `NULL` values in the `title` column of the `episodes` table.

```yql
ALTER TABLE episodes ALTER COLUMN title SET NOT NULL;
```

> [!WARNING]
> Supported only for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.

Reset column compression settings:

```yql
ALTER TABLE compressed_table ALTER COLUMN info SET COMPRESSION();
```

After the query runs, the column uses the default compression algorithm again (see the `COMPRESSION` option above).

## DROP COLUMN

Deletes a column with the specified name from the specified table.

```yql
ALTER TABLE table_name DROP COLUMN column_name;
```

### Request parameters {#request-parameters2}

#### table_name {#table_name2}

The path of the table to be modified.

#### column_name {#column_name2}

The name of the column to be deleted.

### Example {#example1}

The code below will delete the column named `views` from the `episodes` table.

```yql
ALTER TABLE episodes DROP COLUMN views;
```
