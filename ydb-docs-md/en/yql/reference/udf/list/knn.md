---
title: "KNN"
url: "https://ydb.tech/docs/en/yql/reference/udf/list/knn?version=v26.1"
doc_path: "en/yql/reference/udf/list/knn"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/udf/list/knn.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/udf/list/knn.md"
description: "Introduction."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# KNN

## Introduction

One specific case of [vector search](../../../../concepts/query_execution/vector_search.md) is the [k-NN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) problem, where it is required to find the `k` nearest points to the query point. This can be useful in various applications such as image classification, recommendation systems, etc.

The k-NN problem solution is divided into two major subclasses of methods: exact and approximate.

### Exact method

The foundation of the exact method is the calculation of the distance from the query vector to all the vectors in the dataset. This algorithm, also known as the naive approach or brute force method, has a runtime of `O(dn)`, where `n` is the number of vectors in the dataset, and `d` is their dimensionality.

[Exact vector search](knn.md#exact-vector-search-examples) is best utilized if the complete enumeration of the vectors occurs within acceptable time limits. This includes cases where they can be pre-filtered based on some condition, such as a user identifier. In such instances, the exact method may perform faster than the current implementation of [vector indexes](../../../../dev/vector-indexes.md).

Main advantages:

- No need for additional data structures, such as specialized [vector indexes](../../../../concepts/glossary.md#vector-index).
- Full support for [transactions](../../../../concepts/glossary.md#transactions), including in strict consistency mode.
- Instant execution of data modification operations: insertion, update, deletion.

### Approximate methods

Approximate methods do not perform a complete enumeration of the initial data. This allows significantly speeding up the search process, although it might lead to some reduction in the quality of the results.

[Scalar Quantization](knn.md#approximate-vector-search-scalar-quantization) is a method of reducing vector dimensionality, where a set of coordinates is mapped into a space of smaller dimensions.

YDB supports vector searching for vector types `Float`, `Int8`, `Uint8`, and `Bit`. Consequently, it is possible to apply scalar quantization to transform data from `Float` to any of these types.

Scalar quantization reduces the time required for reading and writing data by decreasing the number of bytes. For example, when quantizing from `Float` to `Bit`, each vector is reduced by 32 times.

[Approximate vector search without an index](knn.md#approximate-vector-search-examples) uses a very simple additional data structure - a set of vectors with other quantization. This allows the use of a simple search algorithm: first, a rough preliminary search is performed on the compressed vectors, followed by refining the results on the original vectors.

Main advantages:

- Full support for [transactions](../../../../concepts/glossary.md#transactions), including in strict consistency mode.
- Instant application of data modification operations: insertion, update, deletion.

> [!NOTE]
> It is recommended to measure if such quantization provides sufficient accuracy/recall.

## Data types

In mathematics, a vector of real or integer numbers is used to store points.  
 In this module, vectors are stored in the `String` data type, which is a binary serialized representation of a vector.

## Functions

Vector functions are implemented as user-defined functions (UDF) in the `Knn` module.

### Functions for converting between vector and binary representations {#functions-convert}

Conversion functions are needed to serialize vectors into an internal binary representation and vice versa.

All serialization functions wrap returned `String` data into [Tagged](../../types/special.md) types.

The binary representation of the vector can be stored in the YDB table column.

> [!NOTE]
> Currently YDB does not support storing `Tagged`, so before storing binary representation vectors you must call [Untag](../../builtins/basic.md#as-tagged).

> [!NOTE]
> Currently YDB does not support building an index for vectors with bit quantization `BitVector`.

#### Function signatures {#functions-convert-signature}

```yql
Knn::ToBinaryStringFloat(List<Float>{Flags:AutoMap})->Tagged<String, "FloatVector">
Knn::ToBinaryStringUint8(List<Uint8>{Flags:AutoMap})->Tagged<String, "Uint8Vector">
Knn::ToBinaryStringInt8(List<Int8>{Flags:AutoMap})->Tagged<String, "Int8Vector">
Knn::ToBinaryStringBit(List<Double>{Flags:AutoMap})->Tagged<String, "BitVector">
Knn::ToBinaryStringBit(List<Float>{Flags:AutoMap})->Tagged<String, "BitVector">
Knn::ToBinaryStringBit(List<Uint8>{Flags:AutoMap})->Tagged<String, "BitVector">
Knn::ToBinaryStringBit(List<Int8>{Flags:AutoMap})->Tagged<String, "BitVector">
Knn::FloatFromBinaryString(String{Flags:AutoMap})->List<Float>?
```

#### Convert format {#functions-convert-format}

Conversion functions for vector data convert an array of elements into a byte string with the following format:

- **Main part** — a contiguous array of elements ([knn-serializer.h](https://github.com/ydb-platform/ydb/blob/0b506f56e399e0b4e6a6a4267799da68a3164bf7/ydb/library/yql/udfs/common/knn/knn-serializer.h#L19))

- **Type** — 1 byte at the end of the string that specifies the data type ([knn-defines.h](https://github.com/ydb-platform/ydb/blob/24026648dd7463d58e1470aa8981b17677116e7c/ydb/library/yql/udfs/common/knn/knn-defines.h#L5)):
   `1` — `Float` (4 bytes per element)
   `2` — `Uint8` (1 byte per element)
   `3` — `Int8` (1 byte per element)
   `10` — `Bit` (1 bit per element)

For example, a vector of 5 elements of type `Float` will be serialized into a 21-byte string:  
 4 bytes × 5 elements (main part) + 1 byte (type) = 21 bytes.

#### Implementation details {#functions-convert-details}

The `ToBinaryStringBit` function maps coordinates that are greater than `0` to `1`. All other coordinates are mapped to `0`.

### Distance and similarity functions {#functions-distance}

The distance and similarity functions take two lists of real numbers as input and return the distance/similarity between them.

> [!NOTE]
> Distance functions return small values for close vectors, while similarity functions return large values for close vectors. This should be taken into account when defining the sorting order.

Similarity functions:

- inner product `InnerProductSimilarity`, it's the dot product, also known as the scalar product (sum of products of coordinates)
- cosine similarity `CosineSimilarity` (dot product divided by product of vector lengths)

Distance functions:

- cosine distance `CosineDistance` (1 - cosine similarity)
- manhattan distance `ManhattanDistance`, also known as `L1 distance` (sum of modules of coordinate differences)
- euclidean distance `EuclideanDistance`, also known as `L2 distance` (square root of the sum of squares of coordinate differences)

#### Function signatures {#functions-distance-signatures}

```yql
Knn::InnerProductSimilarity(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::CosineSimilarity(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::CosineDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::ManhattanDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::EuclideanDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
```

In case of mismatched lengths or formats, these functions return `NULL`.

> [!NOTE]
> All distance and similarity functions support overloads when first or second arguments are `Tagged<String, "FloatVector">`, `Tagged<String, "Uint8Vector">`, `Tagged<String, "Int8Vector">`, `Tagged<String, "BitVector">`.
>
> If both arguments are `Tagged`, tag values should match, or the query will raise an error.
>
> Example:
>
> ```text
> Error: Failed to find UDF function: Knn.CosineDistance, reason: Error: Module: Knn, function: CosineDistance, error: Arguments should have same tags, but 'FloatVector' is not equal to 'Uint8Vector'
> ```

## Exact search examples {#exact-vector-search-examples}

### Creating a table {#exact-vector-search-examples-create}

```yql
CREATE TABLE Facts (
    id Uint64,        -- Id of fact
    user Utf8,        -- User name
    fact Utf8,        -- Human-readable description of a user fact
    embedding String, -- Binary representation of embedding vector (result of Knn::ToBinaryStringFloat)
    PRIMARY KEY (id)
);
```

### Adding vectors {#exact-vector-search-examples-upsert}

```yql
$vector = [1.f, 2.f, 3.f, 4.f];
UPSERT INTO Facts (id, user, fact, embedding)
VALUES (123, "Williams", "Full name is John Williams", Untag(Knn::ToBinaryStringFloat($vector), "FloatVector"));
```

### Exact search of K nearest vectors {#exact-vector-search-k-nearest}

```yql
$K = 10;
$TargetEmbedding = Knn::ToBinaryStringFloat([1.2f, 2.3f, 3.4f, 4.5f]);

SELECT * FROM Facts
WHERE user="Williams"
ORDER BY Knn::CosineDistance(embedding, $TargetEmbedding)
LIMIT $K;
```

### Exact search of vectors in radius R {#exact-vector-search-radius}

```yql
$R = 0.1f;
$TargetEmbedding = Knn::ToBinaryStringFloat([1.2f, 2.3f, 3.4f, 4.5f]);

SELECT * FROM Facts
WHERE Knn::CosineDistance(embedding, $TargetEmbedding) < $R;
```

## Approximate search examples {#approximate-vector-search-examples}

This example differs from the [exact search example](knn.md#exact-vector-search-examples) by using bit quantization.

This allows to first do a approximate preliminary search by the `embedding_bit` column, and then refine the results by the original vector column `embegging`.

### Creating a table {#approximate-vector-search-examples-create}

```yql
CREATE TABLE Facts (
    id Uint64,            -- Id of fact
    user Utf8,            -- User name
    fact Utf8,            -- Human-readable description of a user fact
    embedding String,     -- Binary representation of embedding vector (result of Knn::ToBinaryStringFloat)
    embedding_bit String, -- Binary representation of embedding vector (result of Knn::ToBinaryStringBit)
    PRIMARY KEY (id)
);
```

### Adding vectors {#approximate-vector-search-examples-upsert}

```yql
$vector = [1.f, 2.f, 3.f, 4.f];
UPSERT INTO Facts (id, user, fact, embedding, embedding_bit)
VALUES (123, "Williams", "Full name is John Williams", Untag(Knn::ToBinaryStringFloat($vector), "FloatVector"), Untag(Knn::ToBinaryStringBit($vector), "BitVector"));
```

### Scalar quantization {#approximate-vector-search-scalar-quantization}

An ML model can do quantization, or it can be done manually with YQL.

Below there is a quantization example in YQL.

#### Float -> Int8 {#approximate-vector-search-scalar-quantization-map}

```yql
$MapInt8 = ($x) -> {
    $min = -5.0f;
    $max =  5.0f;
    $range = $max - $min;
  RETURN CAST(Math::Round(IF($x < $min, -127, IF($x > $max, 127, ($x / $range) * 255))) As Int8)
};

$FloatList = [-1.2f, 2.3f, 3.4f, -4.7f];
SELECT ListMap($FloatList, $MapInt8);
```

### Approximate search of K nearest vectors: bit quantization {#approximate-vector-search-scalar-quantization-example}

Approximate search algorithm:

- an approximate search is performed using bit quantization;
- an approximate list of vectors is obtained;
- we search this list without using quantization.

```yql
$K = 10;
$Target = [1.2f, 2.3f, 3.4f, 4.5f];
$TargetEmbeddingBit = Knn::ToBinaryStringBit($Target);
$TargetEmbeddingFloat = Knn::ToBinaryStringFloat($Target);

$Ids = SELECT id FROM Facts
ORDER BY Knn::CosineDistance(embedding_bit, $TargetEmbeddingBit)
LIMIT $K * 10;

SELECT * FROM Facts
WHERE id IN $Ids
ORDER BY Knn::CosineDistance(embedding, $TargetEmbeddingFloat)
LIMIT $K;
```
