---
title: "Exporting Backups to External Storage"
url: "https://ydb.tech/docs/en/recipes/backup-collections/exporting-to-external-storage?version=v26.1"
doc_path: "en/recipes/backup-collections/exporting-to-external-storage"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/backup-collections/exporting-to-external-storage.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/backup-collections/exporting-to-external-storage.md"
description: "Export backup collections to S3-compatible storage or filesystem for disaster recovery. Export to S3."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Exporting Backups to External Storage

Export backup collections to S3-compatible storage or filesystem for disaster recovery.

## Export to S3

For large backups or disaster recovery, export directly to S3-compatible storage:

```bash
# Export a backup collection to S3
ydb export s3 \
  --s3-endpoint storage.yandexcloud.net \
  --bucket my-backup-bucket \
  --item src=.backups/collections/production_backups,dst=backups/production_backups

# Export specific backup to S3
ydb export s3 \
  --s3-endpoint storage.yandexcloud.net \
  --bucket my-backup-bucket \
  --item src=.backups/collections/production_backups/20250821141425Z_full,dst=backups/20250821141425Z_full
```

## Export to filesystem

For smaller backups or local testing, export to local filesystem:

```bash
# Export a backup collection
ydb tools dump -p .backups/collections/production_backups -o /backup/exports/production_backups_export

# Export specific backup from a collection
ydb tools dump -p .backups/collections/production_backups/20250601120000Z_full -o /backup/exports/backup_20250601
```

## Export best practices

- **Export each backup separately**: Export full backups and incrementals individually to maintain chain integrity
- **Preserve chain order**: When exporting a chain, export the full backup first, then incrementals in order
- **Verify exports**: Check that exported data is complete before deleting cluster-stored backups
- **Schedule regular exports**: Automate exports to external storage for disaster recovery

## Next steps

- [Importing and Restoring Backups](importing-and-restoring.md)
- [Backup Maintenance and Cleanup](maintenance-and-cleanup.md)
