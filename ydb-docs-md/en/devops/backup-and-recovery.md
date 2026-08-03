---
title: "Backup and Recovery"
url: "https://ydb.tech/docs/en/devops/backup-and-recovery?version=v26.1"
doc_path: "en/devops/backup-and-recovery"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/backup-and-recovery.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/backup-and-recovery.md"
description: "YDB is designed to preserve data against hardware failures: redundancy options are available for various numbers of availability zones, racks, hosts, disks, and"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Backup and Recovery

YDB is designed to preserve data against hardware failures: redundancy options are available for various numbers of availability zones, racks, hosts, disks, and other components (see [cluster operating modes](../concepts/topology.md#cluster-config)). This reduces the risk of data loss due to hardware failures.

However, data can be lost or corrupted **logically**: errors or malicious actions can cause mass deletion or distortion of data through operations that are legitimate from the DBMS perspective. In such cases, cluster fault tolerance does not replace a **separate copy** of data outside the cluster.

Backup is used to protect against such scenarios and allows you to restore data from a backup copy. It is recommended to keep copies on separate storage media or in cloud object storage (for example, via [dumping to files](backup-and-recovery.md#files) or [export to S3](backup-and-recovery.md#s3)).

YDB provides several solutions for performing backup and recovery. For conceptual information and comparison of backup methods, see [Backup concepts](../concepts/backup.md).

- Backup to files and recovery using YDB CLI.
- Backup to S3-compatible storage and recovery using YDB CLI.

## YDB CLI {#cli}

### Files

The following commands are used to back up files:

- `ydb admin cluster dump` — for backing up cluster metadata
- `ydb admin database dump` — for backing up a database
- `ydb tools dump` — for backing up individual schema objects or directories

You can learn more about these commands in [Exporting data to the file system](../reference/ydb-cli/export-import/tools-dump.md).

The following commands are used to perform recovery from a file backup:

- `ydb admin cluster restore` — for restoring cluster metadata from a backup
- `ydb admin database restore` — for restoring a database from a backup
- `ydb tools restore` — for restoring individual schema objects or directories from a backup

You can learn more about these commands in [Importing data from the file system](../reference/ydb-cli/export-import/tools-restore.md).

### S3-Compatible Storage {#s3}

The `ydb export s3` command is used to back up data to S3-compatible storage (for example, [AWS S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.html)). Follow [this link](../reference/ydb-cli/export-import/export-s3.md) to the YDB CLI reference for information about this command.

The `ydb import s3` command is used to recover data from a backup created in S3-compatible storage. Follow [this link](../reference/ydb-cli/export-import/import-s3.md) to the YDB CLI reference for information about this command.

> [!NOTE]
> The speed of backup and recovery operations to/from S3-compatible storage is configured to minimize impact on user workload. To control the speed of operations, configure limits for the corresponding queue in the [resource broker](../reference/configuration/resource_broker_config.md#resource-broker-config).

> [!NOTE]
> When running the export operation, a directory named `export_*` is created in the root directory, where `*` is the numeric part of the export ID. This directory stores tables with a consistent snapshot of exported data as of the export start time. After a successful backup, the `export_*` directory and its contents are removed.

## Backup Collections

Backup collections enable incremental backups and recovery to any saved backup point in the chain for production workloads. For conceptual information and architecture details, see [Backup collections](../concepts/datamodel/backup-collection.md).

Backup collections are recommended for production environments with regular backup schedules and large datasets where incremental changes are much smaller than total data size. For simpler scenarios (one-time migrations, development environments, small databases), consider using [export/import](backup-and-recovery.md#s3) or [dump/restore](backup-and-recovery.md#files) instead.

For step-by-step instructions on configuring and using backup collections, see:

- [Backup collections](../concepts/datamodel/backup-collection.md) — architecture, concepts, and limitations
- [Backup collection recipes](../recipes/backup-collections/index.md) — common scenarios and examples
