---
title: "Exporting data to the file system"
url: "https://ydb.tech/docs/en/reference/ydb-cli/export-import/tools-dump?version=v26.1"
doc_path: "en/reference/ydb-cli/export-import/tools-dump"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/export-import/tools-dump.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/export-import/tools-dump.md"
description: "Exporting data to the file system Cluster."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Exporting data to the file system

## Cluster

The `admin cluster dump` command dumps the cluster' metadata to the client file system in the format described in the [File structure of an export](file-structure.md) article:

```bash
ydb [connection options] admin cluster dump [options]
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

`[options]` – command parameters:

- `-o <PATH>` or `--output <PATH>`: Path to the directory in the client file system where the data will be dumped.
   If the directory doesn't exist, it will be created. However, the entire path to the directory must already exist.

  If the specified directory exists, it must be empty.

  If the parameter is omitted, the `backup_YYYYDDMMTHHMMSS` directory will be created in the current directory, where `YYYYDDMM` is the date and `HHMMSS` is the time when the dump process began, accroding to the system clock.

A [cluster configuration](../../../maintenance/manual/config-overview.md) is dumped separately using the `ydb admin cluster config fetch` command.

## Database {#db}

The `admin database dump` command dumps the database' data and metadata to the client file system in the format described in [File structure of an export](file-structure.md):

> [!WARNING]
> Currently, this command does not process column tables. To export data from column tables, you can use [external data sources](../../../concepts/datamodel/external_data_source.md). For more information, see [Exporting data to S3 object storage](../../../concepts/query_execution/federated_query/s3/write_data.md#export-to-s3).

> [!WARNING]
> Currently, this command does not process [secrets](../../../concepts/datamodel/secrets.md). You must [create](../../../yql/reference/syntax/create-secret.md) secrets manually during restore before restoring objects that use them, such as [data transfers](../../../concepts/transfer.md).

```bash
ydb [connection options] admin database dump [options]
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

`[options]` – command parameters:

- `-o <PATH>` or `--output <PATH>`: Path to the directory in the client file system where the data will be dumped.
   If the directory doesn't exist, it will be created. However, the entire path to the directory must already exist.

  If the specified directory exists, it must be empty.

  If the parameter is omitted, the `backup_YYYYDDMMTHHMMSS` directory will be created in the current directory, where `YYYYDDMM` is the date and `HHMMSS` is the time when the dump process began, accroding to the system clock.

A [database configuration](../../../maintenance/manual/config-overview.md) is dumped separately using the `ydb admin database config fetch` command.

## Schema objects

The `tools dump` command dumps the schema objects to the client file system in the format described in [File structure of an export](file-structure.md):

> [!WARNING]
> Currently, this command does not process column tables. To export data from column tables, you can use [external data sources](../../../concepts/datamodel/external_data_source.md). For more information, see [Exporting data to S3 object storage](../../../concepts/query_execution/federated_query/s3/write_data.md#export-to-s3).

> [!WARNING]
> Currently, this command does not process [secrets](../../../concepts/datamodel/secrets.md). You must [create](../../../yql/reference/syntax/create-secret.md) secrets manually during restore before restoring objects that use them, such as [data transfers](../../../concepts/transfer.md).

```bash
ydb [connection options] tools dump [options]
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

`[options]` – command parameters:

- `-o <PATH>` or `--output <PATH>`: Path to the directory in the client file system where the data will be dumped.
   If the directory doesn't exist, it will be created. However, the entire path to the directory must already exist.

  If the specified directory exists, it must be empty.

  If the parameter is omitted, the `backup_YYYYDDMMTHHMMSS` directory will be created in the current directory, where `YYYYDDMM` is the date and `HHMMSS` is the time when the dump process began, accroding to the system clock.

- `-p <PATH>` or `--path <PATH>`: Path to the database directory with objects or a path to the table to be dumped. The root database directory is used by default. The dump includes all subdirectories whose names don't begin with a dot and the tables in them whose names don't begin with a dot. To dump such tables or the contents of such directories, you can specify their names explicitly in this parameter.

- `--exclude <STRING>`: Template ([PCRE](https://www.pcre.org/original/doc/html/pcrepattern.html)) to exclude paths from export. Specify this parameter multiple times to exclude more than one template simultaneously.

- `--scheme-only`: Dump only the details of the database schema objects without dumping their data.

- `--consistency-level <VAL>`: The consistency level. Possible options:

  - `database`: A fully consistent dump, with one snapshot taken before starting the dump. Applied by default.
  - `table`: Consistency within each dumped table, taking individual independent snapshots for each table. Might run faster and have less impact on the current workload processing in the database.

- `--avoid-copy`: Do not create a snapshot before dumping. The default consistency snapshot might be inapplicable in some cases (for example, for tables with external blobs).

- `--save-partial-result`: Retain the result of a partial dump. Without this option, dumps that terminate with an error are deleted.

- `--preserve-pool-kinds`: If enabled, the `tools dump` command saves the storage device types specified for column groups of the tables to the dump (see the `DATA` parameter in [Column groups](../../../yql/reference/syntax/create_table/family.md) for reference). To import such a dump, the same [storage pools](../../../concepts/glossary.md#storage-pool) must be present in the database. If at least one storage pool is missing, the import procedure will end with an error. By default, this option is disabled, and the import procedure uses the default storage pool specified at the time of database creation (see [Create a Database](../../../devops/deployment-options/manual/initial-deployment/deployment-configuration-v1.md#create-db) for reference).

- `--ordered`: Sorts rows in the exported tables by the primary key.

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](../profile/create.md#quickstart).

### Exporting a cluster

With automatic creation of the `backup_...` directory in the current directory:

```bash
ydb -e <endpoint> admin cluster dump
```

To a specific directory:

```bash
ydb -e <endpoint> admin cluster dump -o ~/backup_cluster
```

### Exporting a database

To an automatically created `backup_...` directory in the current directory:

```bash
ydb -e <endpoint> -d <database> admin database dump
```

To a specific directory:

```bash
ydb -e <endpoint> -d <database> admin database dump -o ~/backup_db
```

### Exporting a database schema objects

To an automatically created `backup_...` directory in the current directory:

```bash
ydb --profile quickstart tools dump
```

To a specific directory:

```bash
ydb --profile quickstart tools dump -o ~/backup_quickstart
```

### Dumping the table structure within a specified database directory (including subdirectories)

```bash
ydb --profile quickstart tools dump -p dir1 --scheme-only
```
