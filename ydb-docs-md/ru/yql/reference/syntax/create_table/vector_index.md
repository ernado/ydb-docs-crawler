---
title: "Векторный индекс"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/vector_index?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/vector_index"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/vector_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/vector_index.md"
description: "Векторный индекс в строковых таблицах создаётся с помощью того же синтаксиса, что и вторичные индексы, при указании vector_kmeans_tree в качестве типа индекса."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Векторный индекс

[Векторный индекс](../../../../concepts/glossary.md#vector-index) в [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблицах создаётся с помощью того же синтаксиса, что и [вторичные индексы](secondary_index.md), при указании `vector_kmeans_tree` в качестве типа индекса. Подмножество доступного для векторных индексов синтаксиса:

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

Где:

- `<index_name>` - уникальное имя индекса для доступа к данным
- `SYNC` - указывает на синхронную запись данных в индекс. Это единственная доступная на данный момент опция, явно указывать не обязательно.
- `<index_columns>` - список колонок таблицы через запятую, используемых для поиска по индексу (последняя колонка используется как эмбеддинг, остальные - как фильтрующие колонки)
- `<cover_columns>` - список дополнительных колонок создаваемой таблицы, которые будут сохранены в индексе для возможности их извлечения без обращения к основной таблице
- `<parameter_name>` и `<parameter_value>` - список параметров в формате ключ-значение:

- общие параметры для всех векторных индексов:

  - `vector_dimension` - размерность вектора эмбеддинга (значение от 1 до 16384);
  - `vector_type` - тип значений вектора (`float`, `uint8` или `int8`);
  - `distance` - [функция расстояния](../../udf/list/knn.md#functions-distance) (`cosine`, `manhattan` или `euclidean`), взаимосключающий с `similarity`;
  - `similarity` - [функция схожести](../../udf/list/knn.md#functions-distance) (`inner_product` или `cosine`), взаимосключающий с `distance`;

- специфичные параметры для `vector_kmeans_tree` (см. [документацию](../../../../dev/vector-indexes.md#kmeans-tree-type)):

  - `clusters` - количество центроидов для алгоритма k-means (значение от 2 до 2048);
  - `levels` - количество уровней в дереве (значение от 1 до 16);
  - `overlap_clusters` - число ближайших кластеров, в которые будет добавлен каждый вектор (по умолчанию 1).
  - общее количество узлов в дереве, рассчитываемое как `clusters` в степени `levels`, должно быть не более чем 1073741824;
  - произведение `vector_dimension` на `clusters` должно быть не более чем 4194304.

> [!WARNING]
> При накоплении значительного объёма изменений в таблицах с векторным индексом полнота или производительность поиска может ухудшиться. Подробности смотрите в разделе [Обновление векторных индексов](../../../../dev/vector-indexes.md#update).

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

## Пример {#primer}

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
