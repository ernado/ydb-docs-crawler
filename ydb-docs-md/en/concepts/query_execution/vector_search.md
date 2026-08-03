---
title: "Vector search"
url: "https://ydb.tech/docs/en/concepts/query_execution/vector_search?version=v26.1"
doc_path: "en/concepts/query_execution/vector_search"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/vector_search.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/vector_search.md"
description: "Vector search concept."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Vector search

## Vector search concept

**Vector search**, also known as [nearest neighbor search](https://en.wikipedia.org/wiki/Nearest_neighbor_search) (NN), is an optimization problem of finding the nearest vector (or set of vectors) in a given dataset relative to a query vector. Proximity between vectors is determined using distance or similarity metrics.

A common approach, especially with large datasets, is approximate nearest neighbor (ANN) search, which yields faster results at the possible cost of some accuracy.

Vector search is widely used in:

- recommendation systems;
- semantic search;
- image similarity search;
- anomaly detection;
- classification systems.

In addition, **vector search** in YDB is widely applied in machine learning (ML) and artificial intelligence (AI) tasks. It is particularly useful in Retrieval-Augmented Generation (RAG) approaches, which utilize vector search to retrieve relevant information from large volumes of data, significantly enhancing the quality of generative models.

Vector search methods can be divided into three main categories:

- [exact methods](vector_search.md#vector-search-exact);
- [approximate methods without index](vector_search.md#vector-search-approximate);
- [approximate methods with index](vector_search.md#vector-search-index).

The choice of method depends on the number of vectors and the workload. Exact methods are slower to search and faster to update; indexes are the opposite.

## Exact vector search {#vector-search-exact}

The foundation of the exact method is the calculation of the distance from the query vector to all the vectors in the dataset. This algorithm, also known as the naive approach or brute force method, has a runtime of `O(dn)`, where `n` is the number of vectors in the dataset, and `d` is their dimensionality.

[Exact vector search](../../yql/reference/udf/list/knn.md#exact-vector-search-examples) is best utilized if the complete enumeration of the vectors occurs within acceptable time limits. This includes cases where they can be pre-filtered based on some condition, such as a user identifier. In such instances, the exact method may perform faster than the current implementation of [vector indexes](../../dev/vector-indexes.md).

Main advantages:

- No need for additional data structures, such as specialized [vector indexes](../glossary.md#vector-index).
- Full support for [transactions](../glossary.md#transactions), including in strict consistency mode.
- Instant execution of data modification operations: insertion, update, deletion.

For more information, see [exact vector search examples](../../yql/reference/udf/list/knn.md#exact-vector-search-examples).

## Approximate vector search without index {#vector-search-approximate}

Approximate methods do not perform a complete enumeration of the initial data. This allows significantly speeding up the search process, although it might lead to some reduction in the quality of the results.

[Scalar Quantization](../../yql/reference/udf/list/knn.md#approximate-vector-search-scalar-quantization) is a method of reducing vector dimensionality, where a set of coordinates is mapped into a space of smaller dimensions.

YDB supports vector searching for vector types `Float`, `Int8`, `Uint8`, and `Bit`. Consequently, it is possible to apply scalar quantization to transform data from `Float` to any of these types.

Scalar quantization reduces the time required for reading and writing data by decreasing the number of bytes. For example, when quantizing from `Float` to `Bit`, each vector is reduced by 32 times.

[Approximate vector search without an index](../../yql/reference/udf/list/knn.md#approximate-vector-search-examples) uses a very simple additional data structure - a set of vectors with other quantization. This allows the use of a simple search algorithm: first, a rough preliminary search is performed on the compressed vectors, followed by refining the results on the original vectors.

Main advantages:

- Full support for [transactions](../glossary.md#transactions), including in strict consistency mode.
- Instant application of data modification operations: insertion, update, deletion.

Learn more about [approximate vector search without index](../../yql/reference/udf/list/knn.md#approximate-vector-search-examples).

## Approximate vector search with index {#vector-search-index}

When the data volume significantly increases, non-index approaches cease to work within acceptable time limits. In such cases, additional data structures are necessary such as [vector indexes](../../dev/vector-indexes.md), which accelerate the search process.

Main advantage:

- ability to work with a large number of vectors.

Disadvantages:

- index build can take considerable time;
- the current version does not support data modification operations: insert, update, delete.
