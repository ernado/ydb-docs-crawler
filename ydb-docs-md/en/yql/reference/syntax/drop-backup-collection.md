---
title: "DROP BACKUP COLLECTION"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-backup-collection?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-backup-collection"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-backup-collection.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-backup-collection.md"
description: "The DROP BACKUP COLLECTION statement deletes a backup collection and all its backups. DROP BACKUP COLLECTION collection_name; Parameters."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP BACKUP COLLECTION

The `DROP BACKUP COLLECTION` statement deletes a [backup collection](../../../concepts/datamodel/backup-collection.md) and all its backups.

```yql
DROP BACKUP COLLECTION collection_name;
```

## Parameters

- `collection_name` — name of the backup collection to drop.

> [!WARNING]
> This operation permanently deletes the backup collection and all backups it contains from the cluster. This action cannot be undone.

> [!NOTE]
> Dropping a backup collection only affects cluster-stored data. Any backups previously exported to external storage (S3 or filesystem) are not affected and remain available for import.

## Examples

Dropping a backup collection:

```yql
DROP BACKUP COLLECTION old_backups;
```

## See also

- [Backup collections](../../../concepts/datamodel/backup-collection.md).
- [CREATE BACKUP COLLECTION](create-backup-collection.md).
- [BACKUP](backup.md).
- [RESTORE](restore-backup-collection.md).
