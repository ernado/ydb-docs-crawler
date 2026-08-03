---
title: "Создание первой коллекции резервных копий"
url: "https://ydb.tech/docs/ru/recipes/backup-collections/getting-started?version=v26.1"
doc_path: "ru/recipes/backup-collections/getting-started"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/backup-collections/getting-started.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/backup-collections/getting-started.md"
description: "Это руководство описывает создание коллекции резервных копий, выполнение первых резервных копий и мониторинг операций. Создание коллекции резервных копий."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Создание первой коллекции резервных копий

Это руководство описывает создание коллекции резервных копий, выполнение первых резервных копий и мониторинг операций.

## Создание коллекции резервных копий {#sozdanie-kollekcii-rezervnyh-kopij}

Коллекция резервных копий — это [объект схемы](../../concepts/datamodel/index.md), хранящийся в схеме базы данных. Вы создаёте и управляете коллекциями с помощью SQL-операторов, а просматриваете их с помощью команд навигации по схеме (например, `ydb scheme ls`), поскольку они отображаются как каталоги в структуре базы данных.

Создайте коллекцию, включающую таблицы, для которых нужно обеспечить согласованное резервное копирование:

```sql
-- Создание коллекции для связанных таблиц
CREATE BACKUP COLLECTION production_backups
    ( TABLE orders
    , TABLE products
    , TABLE customers
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );
```

## Создание резервных копий {#sozdanie-rezervnyh-kopij}

После создания коллекции выполните первоначальную полную резервную копию, затем используйте инкрементальные копии для последующих операций:

```sql
-- Создание первоначальной полной резервной копии
BACKUP production_backups;

-- Внесите изменения в данные...
-- Операции INSERT, UPDATE или DELETE над таблицами в коллекции

-- Позже создайте инкрементальную резервную копию, чтобы захватить изменения
BACKUP production_backups INCREMENTAL;
```

> [!NOTE]
> Операции резервного копирования выполняются асинхронно и не идемпотентны — каждая команда `BACKUP` создаёт новую резервную копию. Перед повтором после таймаута проверьте статус операции с помощью `ydb operation list incbackup`.

## Мониторинг операций резервного копирования {#monitoring-operacij-rezervnogo-kopirovaniya}

Отслеживайте прогресс резервного копирования и просматривайте структуру резервных копий:

```bash
# Проверка статуса операций резервного копирования
ydb operation list incbackup

# Получение подробностей для конкретной операции
ydb operation get <operation-id>

# Просмотр коллекций резервных копий
ydb scheme ls .backups/collections/

# Список резервных копий в коллекции
ydb scheme ls .backups/collections/production_backups/
```

## Следующие шаги {#sleduyushie-shagi}

- [Настройка резервного копирования для разных сред](multi-environment-setup.md)
- [Экспорт резервных копий во внешнее хранилище](exporting-to-external-storage.md)
- [Проверка и тестирование резервных копий](validation-and-testing.md)
