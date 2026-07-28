---
title: "Импорт и восстановление резервных копий"
url: "https://ydb.tech/docs/ru/recipes/backup-collections/importing-and-restoring?version=v26.1"
doc_path: "ru/recipes/backup-collections/importing-and-restoring"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/backup-collections/importing-and-restoring.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/backup-collections/importing-and-restoring.md"
description: "Импорт резервных копий из внешнего хранилища и восстановление данных в базе данных. Импорт из файловой системы. Импорт ранее экспортированных резервных копий:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Импорт и восстановление резервных копий

Импорт резервных копий из внешнего хранилища и восстановление данных в базе данных.

## Импорт из файловой системы {#import-iz-fajlovoj-sistemy}

Импорт ранее экспортированных резервных копий:

```bash
# Импорт резервной копии в целевую базу данных
ydb tools restore -p .backups/collections/production_backups_restored -i /backup/exports/production_backups_export

# Импорт конкретной резервной копии в коллекцию
ydb tools restore -p .backups/collections/emergency_restore -i /backup/exports/backup_20250601
```

## Импорт из S3 {#import-iz-s3}

```bash
ydb import s3 \
  --s3-endpoint storage.yandexcloud.net \
  --bucket my-backup-bucket \
  --item src=backups/production_backups,dst=.backups/collections/production_backups
```

## Восстановление данных {#vosstanovlenie-dannyh}

После импорта резервных копий в кластер восстановите данные:

```sql
RESTORE production_backups;
```

## Процесс аварийного восстановления {#process-avarijnogo-vosstanovleniya}

1. **Импорт полной резервной копии**: сначала импортируйте базовую полную резервную копию
2. **Импорт инкрементальных копий**: импортируйте каждую инкрементальную резервную копию по порядку
3. **Выполнение RESTORE**: запустите команду RESTORE для применения цепочки резервных копий

```bash
# Шаг 1: Импорт полной резервной копии
ydb tools restore -p .backups/collections/recovery/20250821141425Z_full -i /backup/full_20250821

# Шаг 2: Импорт инкрементальных копий по порядку
ydb tools restore -p .backups/collections/recovery/20250822070000Z_incremental -i /backup/inc_20250822

# Шаг 3: Восстановление
ydb yql -s "RESTORE recovery;"
```

## Следующие шаги {#sleduyushie-shagi}

- [Обслуживание и очистка резервных копий](maintenance-and-cleanup.md)
- [Проверка и тестирование резервных копий](validation-and-testing.md)
