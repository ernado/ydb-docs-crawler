---
title: "Настройка резервного копирования для разных сред"
url: "https://ydb.tech/docs/ru/recipes/backup-collections/multi-environment-setup?version=v26.1"
doc_path: "ru/recipes/backup-collections/multi-environment-setup"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/backup-collections/multi-environment-setup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/backup-collections/multi-environment-setup.md"
description: "Настройка различных стратегий резервного копирования для сред разработки и продуктовых сред. Среда разработки."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Настройка резервного копирования для разных сред

Настройка различных стратегий резервного копирования для сред разработки и продуктовых сред.

## Среда разработки {#sreda-razrabotki}

Используйте упрощённые конфигурации с меньшим количеством таблиц для тестирования:

```sql
-- Создание коллекции с меньшим количеством таблиц для тестирования
CREATE BACKUP COLLECTION dev_test_backups
    ( TABLE users
    , TABLE test_data
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );

-- Ежедневные полные резервные копии в среде разработки
BACKUP dev_test_backups;
```

## Производственная среда {#proizvodstvennaya-sreda}

Создавайте коллекции с более частыми инкрементальными резервными копиями:

```sql
-- Создание коллекции для продуктовой среды
CREATE BACKUP COLLECTION prod_daily_backups
    ( TABLE orders
    , TABLE products
    , TABLE customers
    , TABLE inventory
    , TABLE transactions
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );

-- Еженедельная полная резервная копия
BACKUP prod_daily_backups;

-- Ежедневные инкрементальные резервные копии
BACKUP prod_daily_backups INCREMENTAL;
```

## Рекомендуемое расписание резервного копирования {#rekomenduemoe-raspisanie-rezervnogo-kopirovaniya}

| Среда | Полная копия | Инкрементальная копия |
| --- | --- | --- |
| Разработка | Ежедневно | Нет |
| Staging | Еженедельно | Ежедневно |
| Продуктовая среда | Еженедельно | Ежедневно или ежечасно |

## Следующие шаги {#sleduyushie-shagi}

- [Стратегия резервного копирования для микросервисов](microservices-backup-strategy.md)
- [Экспорт резервных копий во внешнее хранилище](exporting-to-external-storage.md)
