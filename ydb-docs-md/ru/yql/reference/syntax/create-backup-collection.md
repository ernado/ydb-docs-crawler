---
title: "CREATE BACKUP COLLECTION"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-backup-collection?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-backup-collection"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-backup-collection.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-backup-collection.md"
description: "Выражение CREATE BACKUP COLLECTION создает коллекцию резервных копий."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE BACKUP COLLECTION

Выражение `CREATE BACKUP COLLECTION` создает [коллекцию резервных копий](../../../concepts/datamodel/backup-collection.md).

```yql
CREATE BACKUP COLLECTION collection_name (
    TABLE table_name [, TABLE another_table_name ...]
) WITH (option = value [, ...]);
```

## Параметры {#parametry}

- `collection_name` — имя создаваемой коллекции резервных копий.

- `table_name` — полный путь к таблице для включения в коллекцию. Можно указать несколько таблиц.

- Опции:

  - `STORAGE` — тип хранилища для резервных копий. Поддерживаемые варианты:

    - `'cluster'` — хранение в кластере YDB.

  - `INCREMENTAL_BACKUP_ENABLED` — включает или отключает поддержку инкрементальных резервных копий. Установите в `'true'` для включения инкрементальных резервных копий, `'false'` — только для полных резервных копий.

> [!NOTE]
> При выборе имени коллекции резервных копий учитывайте общие [правила именования схемных объектов](../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

## Примеры {#primery}

Создание коллекции резервных копий с одной таблицей:

```yql
CREATE BACKUP COLLECTION daily_backups (
    TABLE orders
) WITH (
    STORAGE = 'cluster',
    INCREMENTAL_BACKUP_ENABLED = 'true'
);
```

Создание коллекции резервных копий с несколькими таблицами:

```yql
CREATE BACKUP COLLECTION production_backups (
    TABLE orders,
    TABLE products,
    TABLE customers
) WITH (
    STORAGE = 'cluster',
    INCREMENTAL_BACKUP_ENABLED = 'true'
);
```

## См. также {#sm-takzhe}

- [Коллекции резервных копий](../../../concepts/datamodel/backup-collection.md).
- [BACKUP](backup.md).
- [RESTORE](restore-backup-collection.md).
- [DROP BACKUP COLLECTION](drop-backup-collection.md).
