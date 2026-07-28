---
title: "DROP ASYNC REPLICATION"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-async-replication?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-async-replication"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-async-replication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-async-replication.md"
description: "Вызов DROP ASYNC REPLICATION удаляет экземпляр асинхронной репликации. Вместе с экземпляром асинхронной репликации удаляются:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP ASYNC REPLICATION

Вызов `DROP ASYNC REPLICATION` удаляет экземпляр [асинхронной репликации](../../../concepts/async-replication.md). Вместе с экземпляром асинхронной репликации [удаляются](../../../concepts/async-replication.md#drop):

- автоматически созданные [потоки изменений](../../../concepts/glossary.md#changefeed);
- [объекты-реплики](../../../concepts/glossary.md#replica-object) (опционально).

## Синтаксис {#syntax}

```yql
DROP ASYNC REPLICATION <name> [CASCADE]
```

где:

- `name` — имя экземпляра асинхронной репликации.
- `CASCADE` — каскадное удаление объектов-реплик, созданных в рамках данного экземпляра асинхронной репликации.

## Примеры {#examples}

Рассмотрим примеры удаления экземпляра асинхронной репликации, созданного следующим запросом:

```yql
CREATE ASYNC REPLICATION my_replication
FOR original_table AS replica_table
WITH (
    CONNECTION_STRING = 'grpcs://example.com:2135/?database=/Root/another_database',
    TOKEN_SECRET_PATH = 'my_secret'
);
```

Удаление экземпляра асинхронной репликации и автоматически созданного потока изменений в таблице `original_table`, таблица `replica_table` остается:

```yql
DROP ASYNC REPLICATION my_replication;
```

Удаление экземпляра асинхронной репликации, автоматически созданного потока изменений в таблице `original_table` и таблицы `replica_table`:

```yql
DROP ASYNC REPLICATION my_replication CASCADE;
```

## См. также {#sm-takzhe}

- [CREATE ASYNC REPLICATION](create-async-replication.md)
- [ALTER ASYNC REPLICATION](alter-async-replication.md)
