---
title: "Экспорт резервных копий во внешнее хранилище"
url: "https://ydb.tech/docs/ru/recipes/backup-collections/exporting-to-external-storage?version=v26.1"
doc_path: "ru/recipes/backup-collections/exporting-to-external-storage"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/backup-collections/exporting-to-external-storage.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/backup-collections/exporting-to-external-storage.md"
description: "Экспорт коллекций резервных копий в S3-совместимое хранилище или файловую систему для аварийного восстановления. Экспорт в S3."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Экспорт резервных копий во внешнее хранилище

Экспорт коллекций резервных копий в S3-совместимое хранилище или файловую систему для аварийного восстановления.

## Экспорт в S3 {#eksport-v-s3}

Для больших резервных копий или аварийного восстановления экспортируйте в S3-совместимое хранилище:

```bash
# Экспорт коллекции резервных копий в S3
ydb export s3 \
  --s3-endpoint storage.yandexcloud.net \
  --bucket my-backup-bucket \
  --item src=.backups/collections/production_backups,dst=backups/production_backups

# Экспорт конкретной резервной копии в S3
ydb export s3 \
  --s3-endpoint storage.yandexcloud.net \
  --bucket my-backup-bucket \
  --item src=.backups/collections/production_backups/20250821141425Z_full,dst=backups/20250821141425Z_full
```

## Экспорт в файловую систему {#eksport-v-fajlovuyu-sistemu}

Для небольших резервных копий или локального тестирования экспортируйте в локальную файловую систему:

```bash
# Экспорт коллекции резервных копий
ydb tools dump -p .backups/collections/production_backups -o /backup/exports/production_backups_export

# Экспорт конкретной резервной копии из коллекции
ydb tools dump -p .backups/collections/production_backups/20250601120000Z_full -o /backup/exports/backup_20250601
```

## Лучшие практики экспорта {#luchshie-praktiki-eksporta}

- **Экспортируйте каждую резервную копию отдельно**: экспортируйте полные и инкрементальные копии по отдельности для сохранения целостности цепочки
- **Сохраняйте порядок цепочки**: при экспорте цепочки сначала экспортируйте полную копию, затем инкрементальные по порядку
- **Проверяйте экспорт**: убедитесь, что экспортированные данные полны, прежде чем удалять резервные копии из кластера
- **Планируйте регулярный экспорт**: автоматизируйте экспорт во внешнее хранилище для аварийного восстановления

## Следующие шаги {#sleduyushie-shagi}

- [Импорт и восстановление резервных копий](importing-and-restoring.md)
- [Обслуживание и очистка резервных копий](maintenance-and-cleanup.md)
