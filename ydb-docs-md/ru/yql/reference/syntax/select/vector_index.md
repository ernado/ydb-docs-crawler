---
title: "VIEW (Векторный индекс)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/vector_index?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/vector_index"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/vector_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/vector_index.md"
description: "Для выполнения запроса SELECT с использованием векторного индекса в строчно-ориентированной таблице используйте следующий синтаксис:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# VIEW (Векторный индекс)

Для выполнения запроса `SELECT` с использованием [векторного индекса](../../../../concepts/glossary.md#vector-index) в строчно-ориентированной таблице используйте следующий синтаксис:

```yql
SELECT ...
    FROM TableName VIEW IndexName
    WHERE ...
    ORDER BY Knn::DistanceFunction(...)
    LIMIT ...
```

```yql
SELECT ...
    FROM TableName VIEW IndexName
    WHERE ...
    ORDER BY Knn::SimilarityFunction(...) DESC
    LIMIT ...
```

> [!NOTE]
> Векторный индекс поддерживает функцию расстояния или сходства [расширения Knn](../../udf/list/knn.md#functions-distance), выбранную при создании индекса.
>
> Векторный индекс не будет автоматически выбран [оптимизатором](../../../../concepts/glossary.md#optimizer), поэтому его нужно указывать явно с помощью выражения `VIEW IndexName`.
>
> Если не использовать выражение `VIEW`, запрос выполнит полное сканирование таблицы с попарным сравнением векторов. Рекомендуется проверять оптимальность написанного запроса, используя [анализ плана выполнения запроса](../../../../dev/query-execution-optimization/query-plans-optimization.md). В частности, следует следить за отсутствием полного сканирования (full scan) основной таблицы.

> [!WARNING]
> При накоплении значительного объёма изменений в таблицах с векторным индексом полнота или производительность поиска может ухудшиться. Подробности смотрите в разделе [Обновление векторных индексов](../../../../dev/vector-indexes.md#update).

## KMeansTreeSearchTopSize

Векторный поиск по индексу основан на приближённом алгоритме (ANN, Approximate Nearest Neighbors). Это значит, что результат поиска по векторному индексу может отличаться от результата поиска при полном сканировании таблицы.

Полнота поиска по индексу может быть отрегулирована параметром: `PRAGMA ydb.KMeansTreeSearchTopSize`.

Данный параметр задаёт максимальное число сканируемых кластеров, ближайших к запрашиваемому вектору, на каждом уровне дерева поиска.  
 Необходимо явно задавать значение данного параметра для каждого запроса.

Значение по умолчанию - 1. То есть, по умолчанию сканируется только 1 ближайший кластер на каждом уровне дерева поиска. Такое значение оптимально с точки зрения производительности и будет достаточным для векторов, близких к центру какого-либо кластера. Однако для векторов, примерно одинаково близких к нескольким кластерам, значения 1 не достаточно. Для увеличения полноты поиска (ценой некоторого замедления) следует увеличить значение PRAGMA, например:

```yql
PRAGMA ydb.KMeansTreeSearchTopSize="10";
SELECT *
    FROM TableName VIEW IndexName
    ORDER BY Knn::CosineDistance(embedding, $target)
    LIMIT 10
```

Принципы работы и настройки векторного индекса подробно описаны в отдельной  
 статье [Векторный индекс вида vector_kmeans_tree](../../../../dev/vector-indexes-kmeans-tree-type.md).

## Примеры {#primery}

- Выбор всех полей из таблицы `series` с использованием векторного индекса `views_index`, созданного для `embedding` с мерой близости "косинусное расстояние":

  ```yql
  SELECT series_id, title, info, release_date, views, uploaded_user_id, Knn::CosineSimilarity(embedding, $target) as similarity
      FROM series VIEW views_index
      ORDER BY similarity DESC
      LIMIT 10
  ```

- Выбор всех полей из таблицы `series` с использованием векторного индекса с фильтрацией `views_filtered_index`, созданного для `embedding` с мерой близости "косинусное расстояние" и с ускорением фильтрации по колонке `release_date`:

  ```yql
  SELECT series_id, title, info, release_date, views, uploaded_user_id, Knn::CosineSimilarity(embedding, $target) as similarity
      FROM series VIEW views_filtered_index
      WHERE release_date = "2025-03-31"
      ORDER BY similarity DESC
      LIMIT 10
  ```
