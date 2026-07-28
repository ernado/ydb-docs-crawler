---
title: "KNN"
url: "https://ydb.tech/docs/ru/yql/reference/udf/list/knn?version=v26.1"
doc_path: "ru/yql/reference/udf/list/knn"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/udf/list/knn.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/udf/list/knn.md"
description: "Введение."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# KNN

## Введение {#introduction}

Одним из частных случаев [векторного поиска](../../../../concepts/query_execution/vector_search.md) является задача [k-NN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm), где требуется найти `k` ближайших точек к точке запроса. Это может быть полезно в различных приложениях, таких как классификация изображений, рекомендательные системы и многое другое.

Решения задачи k-NN разбивается на два крупных подкласса методов: точные и приближенные.

### Точный метод {#exact-method}

В основе точного метода лежит вычисление расстояния от вектора запроса до всех векторов в наборе данных. Этот алгоритм, также известный как наивный подход или метод грубой силы, имеет время выполнения `O(dn)`, где `n` — количество векторов в наборе данных, а `d` — их размерность.

[Точный векторный поиск](knn.md#exact-vector-search-examples) лучше использовать, если полный перебор искомых векторов происходит за приемлемое время. В том числе, когда их можно предварительно отфильтровать по некоторому условию, например, по идентификатору пользователя. В таких случаях точный метод может работать быстрее, чем текущая реализация [векторных индексов](../../../../dev/vector-indexes.md).

Основные преимущества:

- отсутствие необходимости в дополнительных структурах данных, таких как специализированные [векторные индексы](../../../../concepts/glossary.md#vector-index);
- полная поддержка [транзакций](../../../../concepts/glossary.md#transactions), в том числе в режиме строгой согласованности;
- мгновенное применение операций модификации данных: вставка, обновление, удаление.

### Приближенные методы {#approximate-methods}

Приближенные методы не осуществляют полный перебор исходных данных. Это позволяет значительно ускорить процесс поиска, хотя и может привести к некоторому снижению качества результатов.

[Скалярное квантование](knn.md#approximate-vector-search-scalar-quantization) — это метод уменьшения размерности векторов, при котором множество координат отображается в пространство меньшей размерности.

YDB поддерживает векторный поиск по векторам типов `Float`, `Int8`, `Uint8`, `Bit`. Следовательно, возможно применение скалярного квантования для преобразования данных из `Float` в любой из этих типов.

Скалярное квантование сокращает время, необходимое для чтения и записи данных, за счёт уменьшения числа байт. Например, при квантовании из `Float` в `Bit` каждый вектор сокращается в 32 раза.

[Приближенный векторный поиск без индекса](knn.md#approximate-vector-search-examples) использует очень простую дополнительную структуру данных - множество векторов с другими квантованием. Это позволяет использовать простой алгоритм поиска: сначала грубый предварительный поиск по сжатым векторам, а затем уточнять результаты по исходным векторам.

Основные преимущества:

- полная поддержка [транзакций](../../../../concepts/glossary.md#transactions), в том числе в режиме строгой согласованности;
- мгновенное применение операций модификации данных: вставка, обновление, удаление.

> [!NOTE]
> Рекомендуется проводить замеры, обеспечивает ли такое преобразование достаточную точность/полноту.

## Типы данных {#data-types}

В математике для хранения точек используется вектор вещественных или целых чисел.  
 В этом модуле вектора представлены типом данных `String`, который является бинарным сериализованным представлением вектора.

## Функции {#functions}

Функции работы с векторами реализовываются в виде пользовательских функций (UDF) в модуле `Knn`.

### Функции преобразования вектора в бинарное представление {#functions-convert}

Функции преобразования нужны для сериализации векторов во внутреннее бинарное представление и обратно.

Все функции сериализации упаковывают возвращаемые данные типа `String` в [Tagged](../../types/special.md) тип.

Бинарное представление вектора можно сохранить в YDB колонку.

> [!NOTE]
> В настоящий момент YDB не поддерживает хранение `Tagged` типов и поэтому перед сохранением бинарного представления векторов нужно извлечь `String` с помощью функции [Untag](../../builtins/basic.md#as-tagged).

> [!NOTE]
> В настоящий момент YDB не поддерживает построение векторных индексов для бинарных векторов `BitVector`.

#### Сигнатуры функций {#functions-convert-signature}

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

#### Формат сериализации {#functions-convert-format}

Функции сериализации векторных данных преобразуют массив элементов в байтовую строку следующего формата:

- **Основная часть** — непрерывный массив элементов ([knn-serializer.h](https://github.com/ydb-platform/ydb/blob/0b506f56e399e0b4e6a6a4267799da68a3164bf7/ydb/library/yql/udfs/common/knn/knn-serializer.h#L19))

- **Тип** — 1 байт в конце строки, обозначающий тип данных ([knn-defines.h](https://github.com/ydb-platform/ydb/blob/24026648dd7463d58e1470aa8981b17677116e7c/ydb/library/yql/udfs/common/knn/knn-defines.h#L5)):
   `1` — `Float` (4 байта на элемент);
   `2` — `Uint8` (1 байт на элемент);
   `3` — `Int8` (1 байт на элемент);
   `10` — `Bit` (1 бит на элемент).

Например, вектор из 5 элементов типа `Float` сериализуется в строку длиной 21 байт: 4 байта × 5 элементов (основная часть) + 1 байт (тип) = 21 байт.

#### Детали имплементации {#functions-convert-details}

`ToBinaryStringBit` преобразует в `1` все координаты, которые больше `0`. Остальные координаты преобразуются в `0`.

### Функции расстояния и сходства {#functions-distance}

Функции расстояния и сходства принимают на вход два вектора и возвращают расстояние/сходство между ними.

> [!NOTE]
> Функции расстояния возвращают малое значение для близких векторов, функции сходства возвращают большие значения для близких векторов. Это следует учитывать в порядке сортировки.

Функции сходства:

- скалярное произведение `InnerProductSimilarity` (сумма произведений координат)
- косинусное сходство `CosineSimilarity` (скалярное произведение разделенное на произведение длин векторов)

Функции расстояния:

- косинусное расстояние `CosineDistance` (1 - косинусное сходство)
- манхэттенское расстояние `ManhattanDistance`, также известно как `L1 distance` (сумма модулей покоординатной разности)
- Евклидово расстояние `EuclideanDistance`, также известно как `L2 distance` (корень суммы квадратов покоординатной разности)

#### Сигнатуры функций {#functions-distance-signatures}

```yql
Knn::InnerProductSimilarity(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::CosineSimilarity(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::CosineDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::ManhattanDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
Knn::EuclideanDistance(String{Flags:AutoMap}, String{Flags:AutoMap})->Float?
```

В случае отличающихся длины или формата, эти функции возвращают `NULL`.

> [!NOTE]
> Все функции расстояния и сходства поддерживают перегрузки с аргументами одного из типов `Tagged<String, "FloatVector">`, `Tagged<String, "Uint8Vector">`, `Tagged<String, "Int8Vector">`, `Tagged<String, "BitVector">`.
>
> Если оба аргумента `Tagged`, то значение тега должно совпадать, иначе запрос завершится с ошибкой.
>
> Пример:
>
> ```text
> Error: Failed to find UDF function: Knn.CosineDistance, reason: Error: Module: Knn, function: CosineDistance, error: Arguments should have same tags, but 'FloatVector' is not equal to 'Uint8Vector'
> ```

## Примеры точного поиска {#exact-vector-search-examples}

### Создание таблицы {#exact-vector-search-examples-create}

```yql
CREATE TABLE Facts (
    id Uint64,        -- Id of fact
    user Utf8,        -- User name
    fact Utf8,        -- Human-readable description of a user fact
    embedding String, -- Binary representation of embedding vector (result of Knn::ToBinaryStringFloat)
    PRIMARY KEY (id)
);
```

### Добавление векторов {#exact-vector-search-examples-upsert}

```yql
$vector = [1.f, 2.f, 3.f, 4.f];
UPSERT INTO Facts (id, user, fact, embedding)
VALUES (123, "Williams", "Full name is John Williams", Untag(Knn::ToBinaryStringFloat($vector), "FloatVector"));
```

### Точный поиск K ближайших векторов {#exact-vector-search-k-nearest}

```yql
$K = 10;
$TargetEmbedding = Knn::ToBinaryStringFloat([1.2f, 2.3f, 3.4f, 4.5f]);

SELECT * FROM Facts
WHERE user="Williams"
ORDER BY Knn::CosineDistance(embedding, $TargetEmbedding)
LIMIT $K;
```

### Точный поиск векторов, находящихся в радиусе R {#exact-vector-search-radius}

```yql
$R = 0.1f;
$TargetEmbedding = Knn::ToBinaryStringFloat([1.2f, 2.3f, 3.4f, 4.5f]);

SELECT * FROM Facts
WHERE Knn::CosineDistance(embedding, $TargetEmbedding) < $R;
```

## Примеры приближенного поиска {#approximate-vector-search-examples}

Данный пример отличается от [примера с точным поиском](knn.md#exact-vector-search-examples) использованием битового квантования.  
 Это позволяет сначала делать грубый предварительный поиск по колонке `embedding_bit`, а затем уточнять результаты по основной колонке с векторами `embedding`.

### Создание таблицы {#approximate-vector-search-examples-create}

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

### Добавление векторов {#approximate-vector-search-examples-upsert}

```yql
$vector = [1.f, 2.f, 3.f, 4.f];
UPSERT INTO Facts (id, user, fact, embedding, embedding_bit)
VALUES (123, "Williams", "Full name is John Williams", Untag(Knn::ToBinaryStringFloat($vector), "FloatVector"), Untag(Knn::ToBinaryStringBit($vector), "BitVector"));
```

### Скалярное квантование {#approximate-vector-search-scalar-quantization}

ML модель может выполнять квантование или это можно сделать вручную с помощью YQL.

Ниже приведен пример квантования в YQL.

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

### Приближенный поиск K ближайших векторов: битовое квантование {#approximate-vector-search-scalar-quantization-example}

Алгоритм приближенного поиска:

- производится приближенный поиск с использованием битового квантования;
- получается приближенный список векторов;
- в этом списке производим поиск без использования квантования.

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
