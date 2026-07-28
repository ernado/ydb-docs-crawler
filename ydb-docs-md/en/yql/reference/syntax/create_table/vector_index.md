---
title: "Vector index"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create_table/vector_index?version=v26.1"
doc_path: "en/yql/reference/syntax/create_table/vector_index"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create_table/vector_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create_table/vector_index.md"
description: "Vector index in row-oriented tables is created using the same syntax as secondary indexes, by specifying vector_kmeans_tree as the index type. Subset of syntax"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Vector index

[Vector index](../../../../concepts/glossary.md#vector-index) in [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables is created using the same syntax as [secondary indexes](secondary_index.md), by specifying `vector_kmeans_tree` as the index type. Subset of syntax available for vector indexes:

```yql
CREATE TABLE `<table_name>` (
    ...
    INDEX `<index_name>`
        GLOBAL
        [SYNC]
        USING vector_kmeans_tree
        ON ( <index_columns> )
        [COVER ( <cover_columns> )]
        [WITH ( <parameter_name> = <parameter_value>[, ...])]
    [,   ...]
)
```

Where:

- `<index_name>` - unique index name for data access
- `SYNC` - indicates synchronous data writing to the index. This is the only currently available option, and it is used by default.
- `<index_columns>` - comma-separated list of table columns used for index searches (the last column is used as embedding, others as filtering columns)
- `<cover_columns>` - list of additional table columns stored in the index to enable retrieval without accessing the main table
- `<parameter_name>` and `<parameter_value>` - list of key-value parameters:

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

> [!WARNING]
> Indexed vector search completeness or performance may decrease after updating a large amount of data in a table with a vector index. For more details, see [Updating Vector Indexes](../../../../dev/vector-indexes.md#update).

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

## Example

```yql
CREATE TABLE user_articles (
    article_id Uint64,
    user String,
    title String,
    text String,
    embedding String,
    INDEX emb_cosine_idx GLOBAL SYNC USING vector_kmeans_tree
    ON (user, embedding) COVER (title, text)
    WITH (
        distance="cosine",
        vector_type="float",
        vector_dimension=512,
        clusters=128,
        levels=2
    ),
    PRIMARY KEY (article_id)
)
```
