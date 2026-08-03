---
title: "INDEX"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/secondary_index?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/secondary_index"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/secondary_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/secondary_index.md"
description: "Конструкция INDEX используется для определения вторичного индекса для строковых таблиц:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# INDEX

Конструкция `INDEX` используется для определения [вторичного индекса](../../../../concepts/secondary_indexes.md) для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц:

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

где:

- `GLOBAL/LOCAL` — глобальный или локальный индекс, в зависимости от типа индекса (`<index_type>`) может быть доступен только один из них:

  - `GLOBAL` — индекс, реализованный в виде отдельной таблицы или набора таблиц. Синхронное обновление такого индекса требует распределённых транзакций.
  - `LOCAL` — локальный индекс в рамках шарда колоночной или строковой таблицы, не требует распределённых транзакций при обновлении, однако не обеспечивает прюнинг при поиске.

- `<index_name>` — уникальное имя индекса, по которому будет возможно обращение к данным.

- `SYNC/ASYNC` — признак синхронности индекса.

  - `SYNC` - [синхронный](../../../../concepts/query_execution/secondary_indexes.md#sync) индекс. Значение по умолчанию.
  - `ASYNC` - [асинхронный](../../../../concepts/query_execution/secondary_indexes.md#async) индекс.

- `<index_type>` - тип индекса, в настоящее время поддерживаются:

  - `secondary` — вторичный индекс. Доступен только `GLOBAL`. Является значением по умолчанию.
  - `vector_kmeans_tree` — векторный индекс. Подробнее описан в [Векторный индекс](vector_index.md).

- `<index_columns>` — список имён колонок создаваемой таблицы через запятую, по которому определяется состав и порядок включения колонок в ключ индекса. Обязательно должен быть указан. Ключ индекса будет состоять из этих колонок с добавлением колонок первичного ключа таблицы.

- `<cover_columns>` — список имён колонок создаваемой таблицы через запятую, которые будут сохранены в индексе дополнительно к колонкам ключа индекса, давая возможность получить дополнительные данные без обращения за ними в таблицу. По умолчанию пуст.

- `<parameter_name>` и `<parameter_value>` — параметры индекса, специфичные для конкретного `<index_type>`.

## Пример {#primer}

```yql
CREATE TABLE my_table (
    a Uint64,
    b Uint64,
    c Utf8,
    d Date,
    INDEX idx_d GLOBAL ON (d),
    INDEX idx_ba GLOBAL ASYNC ON (b, a) COVER (c),
    PRIMARY KEY (a)
)
```
