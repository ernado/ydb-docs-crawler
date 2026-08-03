---
title: "Creating Your First Backup Collection"
url: "https://ydb.tech/docs/en/recipes/backup-collections/getting-started?version=v26.1"
doc_path: "en/recipes/backup-collections/getting-started"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/backup-collections/getting-started.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/backup-collections/getting-started.md"
description: "This guide walks you through creating a backup collection, taking your first backups, and monitoring backup operations. Creating a backup collection."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Creating Your First Backup Collection

This guide walks you through creating a backup collection, taking your first backups, and monitoring backup operations.

## Creating a backup collection

A backup collection is a [schema object](../../concepts/datamodel/index.md) stored in the database schema. You create and manage collections using SQL statements, and browse them using schema navigation commands (like `ydb scheme ls`) since they appear as directories in the database structure.

Create a collection that includes the tables you want to back up together:

```sql
-- Create a collection for related tables
CREATE BACKUP COLLECTION production_backups
    ( TABLE orders
    , TABLE products
    , TABLE customers
    )
WITH ( STORAGE = 'cluster', INCREMENTAL_BACKUP_ENABLED = 'true' );
```

## Taking backups

After creating the collection, take an initial full backup, then use incremental backups for subsequent operations:

```sql
-- Take initial full backup
BACKUP production_backups;

-- Make changes to your data...
-- INSERT, UPDATE, or DELETE operations on backed-up tables

-- Later, take incremental backups to capture the changes
BACKUP production_backups INCREMENTAL;
```

> [!NOTE]
> Backup operations run asynchronously and are not idempotent — each `BACKUP` command creates a new backup. Before retrying after a timeout, check operation status with `ydb operation list incbackup`.

## Monitoring backup operations

Track backup progress and browse your backup structure:

```bash
# Check backup operation status
ydb operation list incbackup

# Get details for specific operation
ydb operation get <operation-id>

# Browse backup collections
ydb scheme ls .backups/collections/

# List backups in a collection
ydb scheme ls .backups/collections/production_backups/
```

## Next steps

- [Setting Up Backups for Multiple Environments](multi-environment-setup.md)
- [Exporting Backups to External Storage](exporting-to-external-storage.md)
- [Validating and Testing Backups](validation-and-testing.md)
