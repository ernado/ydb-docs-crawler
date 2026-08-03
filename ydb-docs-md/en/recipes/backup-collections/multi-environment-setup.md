---
title: "Setting Up Backups for Multiple Environments"
url: "https://ydb.tech/docs/en/recipes/backup-collections/multi-environment-setup?version=v26.1"
doc_path: "en/recipes/backup-collections/multi-environment-setup"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/backup-collections/multi-environment-setup.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/backup-collections/multi-environment-setup.md"
description: "Configure different backup strategies for development and production environments. Development environment."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Setting Up Backups for Multiple Environments

Configure different backup strategies for development and production environments.

## Development environment

Use simpler configurations with fewer tables for testing:

```sql
-- Create collection with fewer tables for testing
CREATE BACKUP COLLECTION dev_test_backups
    ( TABLE users
    , TABLE test_data
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );

-- Take daily full backups in development
BACKUP dev_test_backups;
```

## Production environment

Create comprehensive collections with more frequent incremental backups:

```sql
-- Create comprehensive collection for production
CREATE BACKUP COLLECTION prod_daily_backups
    ( TABLE orders
    , TABLE products
    , TABLE customers
    , TABLE inventory
    , TABLE transactions
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );

-- Weekly full backup
BACKUP prod_daily_backups;

-- Daily incremental backups
BACKUP prod_daily_backups INCREMENTAL;
```

## Recommended backup schedules

| Environment | Full Backup | Incremental Backup |
| --- | --- | --- |
| Development | Daily | None |
| Staging | Weekly | Daily |
| Production | Weekly | Daily or hourly |

## Next steps

- [Backup Strategy for Microservices](microservices-backup-strategy.md)
- [Exporting Backups to External Storage](exporting-to-external-storage.md)
