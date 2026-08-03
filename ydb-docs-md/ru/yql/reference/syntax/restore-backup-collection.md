---
title: "RESTORE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/restore-backup-collection?version=v26.1"
doc_path: "ru/yql/reference/syntax/restore-backup-collection"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/restore-backup-collection.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/restore-backup-collection.md"
description: "Выражение RESTORE восстанавливает таблицы из коллекции резервных копий. RESTORE collection_name; Параметры."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# RESTORE

Выражение `RESTORE` восстанавливает таблицы из [коллекции резервных копий](../../../concepts/datamodel/backup-collection.md).

```yql
RESTORE collection_name;
```

## Параметры {#parametry}

- `collection_name` — имя коллекции резервных копий для восстановления.

## Поведение восстановления {#povedenie-vosstanovleniya}

Операция восстановления:

- Находит в коллекции **актуальную цепочку** резервных копий (полная копия и следующие за ней инкрементальные).
- Восстанавливает таблицы в состояние на момент **самой поздней** резервной копии в этой цепочке: последовательно применяет полную копию и все последующие инкрементальные.
- Завершается с ошибкой, если хотя бы одна из восстанавливаемых таблиц уже существует по тому же пути.

Произвольная точка восстановления «между» двумя сохранёнными копиями не задаётся: восстанавливается состояние, зафиксированное одной из копий в цепочке.

> [!WARNING]
> Операция восстановления завершится с ошибкой, если хотя бы одна из восстанавливаемых таблиц уже существует по тому же пути. Переименуйте или удалите конфликтующие таблицы перед восстановлением.

## Примеры {#primery}

Восстановление из коллекции резервных копий:

```yql
-- Восстановить все таблицы из коллекции
RESTORE production_backups;
```

## Мониторинг операций восстановления {#monitoring-operacij-vosstanovleniya}

Операции восстановления выполняются асинхронно в фоновом режиме. Вы можете отслеживать их прогресс с помощью YDB CLI:

```bash
# Список операций восстановления
ydb operation list incbackup

# Получить детали операции
ydb operation get <operation-id>
```

## См. также {#sm-takzhe}

- [Коллекции резервных копий](../../../concepts/datamodel/backup-collection.md)
- [CREATE BACKUP COLLECTION](create-backup-collection.md)
- [BACKUP](backup.md)
- [DROP BACKUP COLLECTION](drop-backup-collection.md)
- [Резервное копирование и восстановление](../../../devops/backup-and-recovery/index.md)
