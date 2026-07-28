---
title: "VIEW (Vector index)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/vector_index?version=v26.1"
doc_path: "en/yql/reference/syntax/select/vector_index"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/vector_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/vector_index.md"
description: "To select data from a row-oriented table using a vector index, use the following statements:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# VIEW (Vector index)

To select data from a row-oriented table using a [vector index](../../../../concepts/glossary.md#vector-index), use the following statements:

```yql
SELECT ...
    FROM TableName VIEW IndexName
    WHERE ...
    ORDER BY Knn::SomeDistance(...)
    LIMIT ...
```

```yql
SELECT ...
    FROM TableName VIEW IndexName
    WHERE ...
    ORDER BY Knn::SomeSimilarity(...) DESC
    LIMIT ...
```

> [!NOTE]
> A vector index supports a distance or similarity function [from the Knn extension](../../udf/list/knn.md#functions-distance) specified during its construction.
>
> A vector index isn't automatically selected by the [optimizer](../../../../concepts/glossary.md#optimizer) and must be specified explicitly using the `VIEW IndexName` expression.
>
> If the `VIEW` expression is not used, the query will perform a full table scan with pairwise comparison of vectors. It is recommended to check the optimality of the written query using [query plan analysis](../../../../dev/query-execution-optimization/query-plans-optimization.md). In particular, ensure there is no full scan of the main table.

> [!WARNING]
> Indexed vector search completeness or performance may decrease after updating a large amount of data in a table with a vector index. For more details, see [Updating Vector Indexes](../../../../dev/vector-indexes.md#update).

## KMeansTreeSearchTopSize

Indexed vector search is based on an approximate algorithm (ANN, Approximate Nearest Neighbors). That means that indexed search may produce a result that differs from a similar full-scan nearest neighbor search.

Completeness of the indexed vector search is controlled by the following parameter: `PRAGMA ydb.KMeansTreeSearchTopSize`.

This parameter controls the maximum number of scanned clusters nearest to the requested search vector at every level of the search tree.  
 The parameter should be set explicitly for every search query.

The default value is 1. This means that only one nearest cluster is scanned at every level of the search tree by default. This parameter value maximizes search performance and results in good search quality for vectors near to the center of a cluster. But this value may be insufficient for vectors that are about equally close to multiple clusters. So, to increase the search quality for such vectors (at the expense of slightly reduced search performance), you should increase the PRAGMA value, for example:

```yql
PRAGMA ydb.KMeansTreeSearchTopSize="10";
SELECT *
    FROM TableName VIEW IndexName
    ORDER BY Knn::CosineDistance(embedding, $target)
    LIMIT 10
```

## Examples

- Select all the fields from the `series` row-oriented table using the `views_index` vector index created for `embedding` and cosine similarity:

  ```yql
  SELECT series_id, title, info, release_date, views, uploaded_user_id, Knn::CosineSimilarity(embedding, $target) as similarity
      FROM series VIEW views_index
      ORDER BY similarity DESC
      LIMIT 10
  ```

- Select all the fields from the `series` row-oriented table using the `views_filtered_index` filtered vector index created for `embedding` and optimized for efficient filtering by `release_date`:

  ```yql
  SELECT series_id, title, info, release_date, views, uploaded_user_id, Knn::CosineSimilarity(embedding, $target) as similarity
      FROM series VIEW views_filtered_index
      WHERE release_date = "2025-03-31"
      ORDER BY similarity DESC
      LIMIT 10
  ```
