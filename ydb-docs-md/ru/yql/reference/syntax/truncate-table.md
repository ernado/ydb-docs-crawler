---
title: "TRUNCATE TABLE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/truncate-table?version=v26.1"
doc_path: "ru/yql/reference/syntax/truncate-table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/truncate-table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/truncate-table.md"
description: "TRUNCATE TABLE удаляет все пользовательские данные из указанной таблицы и ее индексов. Синтаксис. TRUNCATE TABLE <table_name>; Ограничения."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# TRUNCATE TABLE

`TRUNCATE TABLE` удаляет все пользовательские данные из указанной таблицы и ее индексов.

## Синтаксис {#sintaksis}

```yql
TRUNCATE TABLE <table_name>;
```

## Ограничения {#ogranicheniya}

- Поддерживается только для [строковых таблиц](../../../concepts/glossary.md#row-oriented-table).

- Во время выполнения операции таблица блокируется на чтение и запись.

- Операцию нельзя прервать или отменить после начала выполнения.

- Операцию нельзя выполнить, если у таблицы есть:

  - [асинхронный вторичный индекс](../../../concepts/query_execution/secondary_indexes.md#async),
  - [поток изменений](alter_table/changefeed.md),
  - [асинхронная репликация](../../../concepts/async-replication.md).

## Примеры {#primery}

Удаляет все данные из таблицы с полным путем `/Root/test/my_table`.

```yql
TRUNCATE TABLE `/Root/test/my_table`;
```

Удаляет все данные из таблицы `my_table` в текущей базе данных.

```yql
TRUNCATE TABLE `my_table`;
```

## См. также {#sm-takzhe}

- [CREATE TABLE](create_table/index.md)
- [ALTER TABLE](alter_table/index.md)
- [DROP TABLE](drop_table.md)
