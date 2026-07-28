---
title: "BACKUP"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/backup?version=v26.1"
doc_path: "ru/yql/reference/syntax/backup"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/backup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/backup.md"
description: "Выражение BACKUP создает резервную копию таблиц в коллекции резервных копий. BACKUP collection_name [ INCREMENTAL ]; Параметры."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# BACKUP

Выражение `BACKUP` создает резервную копию таблиц в [коллекции резервных копий](../../../concepts/datamodel/backup-collection.md).

```yql
BACKUP collection_name [INCREMENTAL];
```

## Параметры {#parametry}

- `collection_name` — имя коллекции резервных копий.
- `INCREMENTAL` — создание инкрементальной резервной копии вместо полной.

## Типы резервных копий {#tipy-rezervnyh-kopij}

### Полная резервная копия {#polnaya-rezervnaya-kopiya}

Полная резервная копия создает снимок всех таблиц в коллекции на определенный момент времени. Это служит основой для последующих инкрементальных резервных копий.

```yql
BACKUP production_backups;
```

### Инкрементальная резервная копия {#inkrementalnaya-rezervnaya-kopiya}

Инкрементальная резервная копия захватывает только изменения (вставки, обновления, удаления) с момента предыдущей резервной копии в цепочке. Коллекция должна быть создана с `INCREMENTAL_BACKUP_ENABLED = 'true'`.

```yql
BACKUP production_backups INCREMENTAL;
```

> [!WARNING]
> Инкрементальные резервные копии требуют предыдущей полной резервной копии в той же коллекции. Всегда сначала создавайте полную резервную копию, прежде чем делать инкрементальные резервные копии.

## Примеры {#primery}

Создание начальной полной резервной копии:

```yql
-- Сначала создайте коллекцию
CREATE BACKUP COLLECTION daily_backups (
    TABLE orders
) WITH (
    STORAGE = 'cluster',
    INCREMENTAL_BACKUP_ENABLED = 'true'
);

-- Затем создайте полную резервную копию
BACKUP daily_backups;
```

Создание инкрементальных резервных копий:

```yql
-- После начальной полной резервной копии создайте инкрементальные резервные копии
BACKUP daily_backups INCREMENTAL;
```

## Мониторинг операций резервного копирования {#monitoring-operacij-rezervnogo-kopirovaniya}

Операции резервного копирования выполняются асинхронно в фоновом режиме. Вы можете отслеживать их прогресс с помощью YDB CLI:

```bash
# Список операций резервного копирования
ydb operation list incbackup

# Получить детали операции
ydb operation get <operation-id>
```

## См. также {#sm-takzhe}

- [Коллекции резервных копий](../../../concepts/datamodel/backup-collection.md).
- [CREATE BACKUP COLLECTION](create-backup-collection.md).
- [RESTORE](restore-backup-collection.md).
- [DROP BACKUP COLLECTION](drop-backup-collection.md).
- [Резервное копирование и восстановление](../../../devops/backup-and-recovery/index.md).
