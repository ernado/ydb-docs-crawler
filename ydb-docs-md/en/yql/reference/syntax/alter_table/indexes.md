---
title: "Adding, removing, and renaming a index"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/indexes?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/indexes"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/indexes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/indexes.md"
description: "Adding an index. ADD INDEX — adds an index with the specified name and type for a given set of columns. Grammar:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Adding, removing, and renaming a index

## Adding an index {#add-index}

`ADD INDEX` — adds an index with the specified name and type for a given set of columns. Grammar:

```yql
ALTER TABLE `<table_name>`
  ADD INDEX `<index_name>`
    [GLOBAL|LOCAL]
    [SYNC|ASYNC]
    [USING <index_type>]
    ON ( <index_columns> )
    [COVER ( <cover_columns> )]
    [WITH ( <parameter_name> = <parameter_value>[, ...])]
  [,   ...]
```

- `GLOBAL/LOCAL` — global or local index; depending on the index type (`<index_type>`), only one of them may be available:

  - `GLOBAL` — an index implemented as a separate table or set of tables. Synchronous updates to such an index require distributed transactions.
  - `LOCAL` — a local index within a shard of a row-oriented or column-oriented table. Does not require distributed transactions for updates, but does not provide pruning during search.

- `<index_name>` — unique index name that will be used to access data.

- `SYNC/ASYNC` — the index synchronization mode.

  - `SYNC` — a [synchronous](../../../../concepts/query_execution/secondary_indexes.md#sync) index. This is the default value.
  - `ASYNC` — an [asynchronous](../../../../concepts/query_execution/secondary_indexes.md#async) index.

- `<index_type>` — index type, currently supported:

  - `secondary` — secondary index. Only `GLOBAL` is available. This is the default value.
  - `vector_kmeans_tree` — vector index. Described in detail in [Vector index](../create_table/vector_index.md).

- `<index_columns>` — comma-separated list of column names for the table being created. This list defines the composition and order of columns included in the index key. Must be specified. The index key will include both the columns listed and the columns from the table's primary key.

- `<cover_columns>` — comma-separated list of column names from the created table that will be saved in the index in addition to index key columns, providing the ability to get additional data without accessing the table. Empty by default.

- `<parameter_name>` and `<parameter_value>` — index parameters specific to a particular `<index_type>`.

Parameters specific to vector indexes:

- common parameters for all vector indexes:

  - `vector_dimension` - embedding vector dimensionality (should be between 1 and 16384)

  - `vector_type` - vector value type (`float`, `uint8`, or `int8`)

  - `distance` - [distance function](../../udf/list/knn.md#functions-distance) (`cosine`, `manhattan`, or `euclidean`), mutually exclusive with `similarity`

    - `similarity` - [similarity function](../../udf/list/knn.md#functions-distance) (`inner_product` or `cosine`), mutually exclusive with `distance`

- specific parameters for `vector_kmeans_tree` (see [the reference](../../../../dev/vector-indexes.md#kmeans-tree-type)):

  - `clusters` - number of centroids for k-means algorithm (should be between 2 and 2048)
  - `levels` - number of levels in the tree (should be between 1 and 16)
  - `overlap_clusters` - the number of nearest clusters to add each vector to (default 1)
  - the total number of nodes in the tree, calculated as `clusters` raised to the power of `levels`, should be no more than 1073741824
  - the product of `vector_dimension` and `clusters` should be no more than 4194304

You can also add a secondary index using the YDB CLI [table index](../../../../reference/ydb-cli/commands/secondary_index.md#add) command.

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

### Examples

A regular secondary index:

```yql
ALTER TABLE `series`
  ADD INDEX `title_index`
  GLOBAL ON (`title`);
```

A vector index:

```yql
ALTER TABLE `series`
  ADD INDEX emb_cosine_idx GLOBAL SYNC USING vector_kmeans_tree
  ON (embedding) COVER (title)
  WITH (
    distance="cosine",
    vector_type="float",
    vector_dimension=512,
    clusters=128,
    levels=2
  );
```

## Altering an index {#alter-index}

Indexes have type-specific parameters that can be tuned. Global indexes, whether [synchronous](../../../../concepts/secondary_indexes.md#sync) or [asynchronous](../../../../concepts/secondary_indexes.md#async), are implemented as hidden tables, and their automatic partitioning and followers settings can be adjusted just like those of regular tables.

> [!NOTE]
> Currently, specifying secondary index partitioning settings during index creation is not supported in either the [`ALTER TABLE ADD INDEX`](indexes.md#add-index) or the [`CREATE TABLE INDEX`](../create_table/secondary_index.md) statements.

```sql
ALTER TABLE <table_name> ALTER INDEX <index_name> SET <setting_name> <value>;
ALTER TABLE <table_name> ALTER INDEX <index_name> SET (<setting_name_1> = <value_1>, ...);
```

- `<table_name>`: The name of the table whose index is to be modified.

- `<index_name>`: The name of the index to be modified.

- `<setting_name>`: The name of the setting to be modified, which should be one of the following:

  - [AUTO_PARTITIONING_BY_SIZE](../../../../concepts/datamodel/table.md#auto_partitioning_by_size)
  - [AUTO_PARTITIONING_BY_LOAD](../../../../concepts/datamodel/table.md#auto_partitioning_by_load)
  - [AUTO_PARTITIONING_PARTITION_SIZE_MB](../../../../concepts/datamodel/table.md#auto_partitioning_partition_size_mb)
  - [AUTO_PARTITIONING_MIN_PARTITIONS_COUNT](../../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count)
  - [AUTO_PARTITIONING_MAX_PARTITIONS_COUNT](../../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count)
  - [READ_REPLICAS_SETTINGS](../../../../concepts/datamodel/table.md#read_only_replicas)

> [!NOTE]
> These settings cannot be reset.

- `<value>`: The new value for the setting. Possible values include:

  - `ENABLED` or `DISABLED` for the `AUTO_PARTITIONING_BY_SIZE` and `AUTO_PARTITIONING_BY_LOAD` settings
  - `"PER_AZ:<count>"` or `"ANY_AZ:<count>"` where `<count>` is the number of replicas for the `READ_REPLICAS_SETTINGS`
  - An integer of `Uint64` type for the other settings

### Example

The query in the following example enables automatic partitioning by load for the index named `title_index` of the table `series`, sets its minimum partition count to 5, and enables one follower per AZ for every partition:

```yql
ALTER TABLE `series` ALTER INDEX `title_index` SET (
    AUTO_PARTITIONING_BY_LOAD = ENABLED,
    AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 5,
    READ_REPLICAS_SETTINGS = "PER_AZ:1"
);
```

## Deleting an index {#drop-index}

`DROP INDEX`: Deletes the index with the specified name. The code below deletes the index named `title_index`.

```yql
ALTER TABLE `series` DROP INDEX `title_index`;
```

You can also remove a index using the YDB CLI [table index](../../../../reference/ydb-cli/commands/secondary_index.md#drop) command.

## Renaming an index {#rename-index}

`RENAME INDEX`: Renames the index with the specified name.

If an index with the new name exists, an error is returned.

Replacement of atomic indexes under load is supported by the command [ydb table index rename](../../../../reference/ydb-cli/commands/secondary_index.md#rename) in the YDB CLI and by YDB SDK ad-hoc methods.

Example of index renaming:

```yql
ALTER TABLE `series` RENAME INDEX `title_index` TO `title_index_new`;
```
