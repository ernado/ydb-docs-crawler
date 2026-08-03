---
title: "Backup Collection Recipes"
url: "https://ydb.tech/docs/en/recipes/backup-collections/?version=v26.1"
doc_path: "en/recipes/backup-collections/"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/backup-collections/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/backup-collections/index.md"
description: "Step-by-step guides for common backup collection scenarios. Getting Started."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Backup Collection Recipes

Step-by-step guides for common backup collection scenarios.

## Getting Started

- [Creating Your First Backup Collection](getting-started.md) - Create a collection, take backups, and monitor operations

## Environment Configuration

- [Setting Up Backups for Multiple Environments](multi-environment-setup.md) - Configure backups for development and production
- [Backup Strategy for Microservices](microservices-backup-strategy.md) - Organize backups by service boundaries

## External Storage

- [Exporting Backups to External Storage](exporting-to-external-storage.md) - Export to S3 or filesystem for disaster recovery
- [Importing and Restoring Backups](importing-and-restoring.md) - Restore from external storage

## Maintenance

- [Backup Maintenance and Cleanup](maintenance-and-cleanup.md) - Manage backup lifecycle and storage
- [Validating and Testing Backups](validation-and-testing.md) - Verify backup integrity

## See also

- [Backup collections](../../concepts/datamodel/backup-collection.md)
- [Backup and recovery guide](../../devops/backup-and-recovery.md)
- [CREATE BACKUP COLLECTION](../../yql/reference/syntax/create-backup-collection.md)
- [BACKUP](../../yql/reference/syntax/backup.md)
- [RESTORE](../../yql/reference/syntax/restore-backup-collection.md)
- [DROP BACKUP COLLECTION](../../yql/reference/syntax/drop-backup-collection.md)
