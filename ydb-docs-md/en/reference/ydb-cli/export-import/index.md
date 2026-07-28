---
title: "Exporting and importing data"
url: "https://ydb.tech/docs/en/reference/ydb-cli/export-import/?version=v26.1"
doc_path: "en/reference/ydb-cli/export-import/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/export-import/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/export-import/index.md"
description: "Exporting and importing data."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Exporting and importing data

The YDB CLI contains a set of commands designed to export and import data and descriptions of data schema objects. Data can be exported to create backups for subsequent recovery and for other purposes.

- [The export file structure](file-structure.md) is used for exporting data both to the file system and S3-compatible object storage.
- [Exporting cluster' metadata to the file system using `admin cluster dump`](tools-dump.md#cluster)
- [Importing cluster' metadata from the file system using `admin cluster restore`](tools-restore.md#cluster)
- [Exporting database' metadata and data to the file system using `admin database dump`](tools-dump.md#db)
- [Importing database' metadata and data from the file system using `admin database restore`](tools-restore.md#db)
- [Exporting individual schema objects to the file system using `tools dump`](tools-dump.md#schema-objects)
- [Importing individual schema objects from the file system using `tools restore`](tools-restore.md#schema-objects)
- [Connecting to and authenticating with S3-compatible object storage](auth-s3.md)
- [Exporting data to S3-compatible object storage using `export s3`](export-s3.md)
- [Importing data from S3-compatible object storage using `import s3`](import-s3.md)
