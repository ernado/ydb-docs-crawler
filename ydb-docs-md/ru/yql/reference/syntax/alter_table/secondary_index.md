---
title: "Добавление, удаление и переименование индекса"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/secondary_index?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/secondary_index"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/indexes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/indexes.md"
description: "Добавление индекса. ADD INDEX — добавляет индекс с указанным именем и типом для заданного набора колонок в строковых таблицах. Грамматика:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Добавление, удаление и переименование индекса

## Добавление индекса {#add-index}

`ADD INDEX` — добавляет индекс с указанным именем и типом для заданного набора колонок в строковых таблицах. Грамматика:

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

- `GLOBAL/LOCAL` — глобальный или локальный индекс, в зависимости от типа индекса (`<index_type>`) может быть доступен только один из них:

  - `GLOBAL` — индекс, реализованный в виде отдельной таблицы или набора таблиц. Синхронное обновление такого индекса требует распределённых транзакций.
  - `LOCAL` — локальный индекс в рамках шарда колоночной или строковой таблицы, не требует распределённых транзакций при обновлении, однако не обеспечивает прюнинг при поиске.

- `<index_name>` — уникальное имя индекса, по которому будет возможно обращение к данным.

- `SYNC/ASYNC` — признак синхронности индекса.

  - `SYNC` - [синхронный](../../../../concepts/query_execution/secondary_indexes.md#sync) индекс. Значение по умолчанию.
  - `ASYNC` - [асинхронный](../../../../concepts/query_execution/secondary_indexes.md#async) индекс.

- `<index_type>` - тип индекса, в настоящее время поддерживаются:

  - `secondary` — вторичный индекс. Доступен только `GLOBAL`. Является значением по умолчанию.
  - `vector_kmeans_tree` — векторный индекс. Подробнее описан в [Векторный индекс](../create_table/vector_index.md).

- `<index_columns>` — список имён колонок создаваемой таблицы через запятую, по которому определяется состав и порядок включения колонок в ключ индекса. Обязательно должен быть указан. Ключ индекса будет состоять из этих колонок с добавлением колонок первичного ключа таблицы.

- `<cover_columns>` — список имён колонок создаваемой таблицы через запятую, которые будут сохранены в индексе дополнительно к колонкам ключа индекса, давая возможность получить дополнительные данные без обращения за ними в таблицу. По умолчанию пуст.

- `<parameter_name>` и `<parameter_value>` — параметры индекса, специфичные для конкретного `<index_type>`.

Параметры, специфичные для векторных индексов:

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

Также добавить вторичный индекс можно с помощью команды [table index](../../../../reference/ydb-cli/commands/secondary_index.md#add) YDB CLI.

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

### Примеры {#primery}

Вторичный индекс:

```yql
ALTER TABLE `series`
  ADD INDEX `title_index`
  GLOBAL ON (`title`);
```

Векторный индекс:

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

## Изменение параметров индекса {#alter-index}

Индексы имеют параметры, зависящие от типа, которые можно настраивать. Глобальные индексы, [синхронные](../../../../concepts/secondary_indexes.md#sync) или [асинхронные](../../../../concepts/secondary_indexes.md#async), реализованы в виде скрытых таблиц, и их параметры автоматического партиционирования и реплик можно регулировать так же, как и настройки обычных таблиц.

> [!NOTE]
> В настоящее время задание настроек партиционирования вторичных индексов при создании индекса не поддерживается ни в операторе [`ALTER TABLE ADD INDEX`](indexes.md#add-index), ни в операторе [`CREATE TABLE INDEX`](../create_table/secondary_index.md).

```yql
ALTER TABLE <table_name> ALTER INDEX <index_name> SET <setting_name> <value>;
ALTER TABLE <table_name> ALTER INDEX <index_name> SET (<setting_name_1> = <value_1>, ...);
```

- `<table_name>` - имя таблицы, индекс которой нужно изменить.

- `<index_name>` - имя индекса, который нужно изменить.

- `<setting_name>` - имя изменяемого параметра, который должен быть одним из следующих:

  - [AUTO_PARTITIONING_BY_SIZE](../../../../concepts/datamodel/table.md#auto_partitioning_by_size)
  - [AUTO_PARTITIONING_BY_LOAD](../../../../concepts/datamodel/table.md#auto_partitioning_by_load)
  - [AUTO_PARTITIONING_PARTITION_SIZE_MB](../../../../concepts/datamodel/table.md#auto_partitioning_partition_size_mb)
  - [AUTO_PARTITIONING_MIN_PARTITIONS_COUNT](../../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count)
  - [AUTO_PARTITIONING_MAX_PARTITIONS_COUNT](../../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count)
  - [READ_REPLICAS_SETTINGS](../../../../concepts/datamodel/table.md#read_only_replicas)

> [!NOTE]
> Эти настройки нельзя вернуть к исходным.

- `<value>` - новое значение параметра. Возможные значения включают:

  - `ENABLED` или `DISABLED` для параметров `AUTO_PARTITIONING_BY_SIZE` и `AUTO_PARTITIONING_BY_LOAD`
  - `"PER_AZ:<count>"` или `"ANY_AZ:<count>"` где `<count>` — число реплик для `READ_REPLICAS_SETTINGS`
  - для остальных параметров — целое число типа `Uint64`

### Пример {#primer}

Код из следующего примера включает автоматическое партиционирование по нагрузке для индекса с именем `title_index` в таблице `series`, устанавливает минимальное количество партиций равным 5 и запускает по одной реплике в каждой зоне доступности (AZ) для каждой партиции:

```yql
ALTER TABLE `series` ALTER INDEX `title_index` SET (
    AUTO_PARTITIONING_BY_LOAD = ENABLED,
    AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 5,
    READ_REPLICAS_SETTINGS = "PER_AZ:1"
);
```

## Удаление индекса {#drop-index}

`DROP INDEX` — удаляет индекс с указанным именем. Приведенный ниже код удалит индекс с именем `title_index`.

```yql
ALTER TABLE `series` DROP INDEX `title_index`;
```

Также удалить индекс можно с помощью команды [table index](../../../../reference/ydb-cli/commands/secondary_index.md#drop) YDB CLI.

## Переименование вторичного индекса {#rename-secondary-index}

`RENAME INDEX` — переименовывает индекс с указанным именем. Если индекс с новым именем существует, будет возвращена ошибка.

Возможность атомарной замены индекса под нагрузкой поддерживается командой [ydb table index rename](../../../../reference/ydb-cli/commands/secondary_index.md#rename) YDB CLI и специализированными методами YDB SDK.

Пример переименования индекса:

```yql
ALTER TABLE `series` RENAME INDEX `title_index` TO `title_index_new`;
```
