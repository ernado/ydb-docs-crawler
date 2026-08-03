---
title: "INDEX"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create_table/secondary_index?version=v26.1"
doc_path: "en/yql/reference/syntax/create_table/secondary_index"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create_table/secondary_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create_table/secondary_index.md"
description: "The INDEX construct is used to define a secondary index in a row-oriented table:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# INDEX

The INDEX construct is used to define a [secondary index](../../../../concepts/secondary_indexes.md) in a [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) table:

```yql
CREATE TABLE `<table_name>` (
  ...
    INDEX `<index_name>`
    [GLOBAL|LOCAL]
    [SYNC|ASYNC]
    [USING <index_type>]
    ON ( <index_columns> )
    [COVER ( <cover_columns> )]
    [WITH ( <parameter_name> = <parameter_value>[, ...])]
  [,   ...]
)
```

where:

- `GLOBAL/LOCAL` — global or local index; depending on the index type (`<index_type>`), only one of them may be available:

  - `GLOBAL` — an index implemented as a separate table or set of tables. Synchronous updates to such an index require distributed transactions.
  - `LOCAL` — a local index within a shard of a row-oriented or column-oriented table. Does not require distributed transactions for updates, but does not provide pruning during search.

- `<index_name>` — unique index name that will be used to access data.

- `SYNC/ASYNC` — the index synchronization mode.

  - `SYNC` — a [synchronous](../../../../concepts/query_execution/secondary_indexes.md#sync) index. This is the default value.
  - `ASYNC` — an [asynchronous](../../../../concepts/query_execution/secondary_indexes.md#async) index.

- `<index_type>` — index type, currently supported:

  - `secondary` — secondary index. Only `GLOBAL` is available. This is the default value.
  - `vector_kmeans_tree` — vector index. Described in detail in [Vector index](vector_index.md).

- `<index_columns>` — comma-separated list of column names for the table being created. This list defines the composition and order of columns included in the index key. Must be specified. The index key will include both the columns listed and the columns from the table's primary key.

- `<cover_columns>` — comma-separated list of column names from the created table that will be saved in the index in addition to index key columns, providing the ability to get additional data without accessing the table. Empty by default.

- `<parameter_name>` and `<parameter_value>` — index parameters specific to a particular `<index_type>`.

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

## Example

```yql
CREATE TABLE my_table (
    a Uint64,
    b Bool,
    c Utf8,
    d Date,
    INDEX idx_d GLOBAL ON (d),
    INDEX idx_ba GLOBAL ASYNC ON (b, a) COVER (c),
    PRIMARY KEY (a)
)
```
