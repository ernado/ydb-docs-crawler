---
title: "DROP BACKUP COLLECTION"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-backup-collection?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-backup-collection"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-backup-collection.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-backup-collection.md"
description: "Выражение DROP BACKUP COLLECTION удаляет коллекцию резервных копий и все содержащиеся в ней резервные копии. DROP BACKUP COLLECTION collection_name; Параметры."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP BACKUP COLLECTION

Выражение `DROP BACKUP COLLECTION` удаляет [коллекцию резервных копий](../../../concepts/datamodel/backup-collection.md) и все содержащиеся в ней резервные копии.

```yql
DROP BACKUP COLLECTION collection_name;
```

## Параметры {#parametry}

- `collection_name` — имя удаляемой коллекции резервных копий.

> [!WARNING]
> Эта операция безвозвратно удаляет коллекцию резервных копий и все содержащиеся в ней резервные копии из кластера. Это действие не может быть отменено.

> [!NOTE]
> Удаление коллекции резервных копий затрагивает только данные в кластере. Резервные копии, ранее экспортированные во внешнее хранилище (S3 или файловую систему), не затрагиваются и остаются доступными для восстановления.

## Примеры {#primery}

Удаление коллекции резервных копий:

```yql
DROP BACKUP COLLECTION old_backups;
```

## См. также {#sm-takzhe}

- [Коллекции резервных копий](../../../concepts/datamodel/backup-collection.md).
- [CREATE BACKUP COLLECTION](create-backup-collection.md).
- [BACKUP](backup.md).
- [RESTORE](restore-backup-collection.md).
