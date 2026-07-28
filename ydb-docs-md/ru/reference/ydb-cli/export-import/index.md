---
title: "Выгрузка и загрузка данных"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/export-import/?version=v26.1"
doc_path: "ru/reference/ydb-cli/export-import/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/export-import/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/export-import/index.md"
description: "Выгрузка и загрузка данных."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Выгрузка и загрузка данных

YDB CLI содержит набор команд, предназначенных для выгрузки (экспорта) и загрузки (импорта) данных и описаний объектов схемы данных. Выгрузка данных может применяться как для создания резервных копий в целях последующего восстановления, так и в других целях.

- [Файловая структура выгрузки](file-structure.md), применяемая как при выгрузке в файловую систему, так и при выгрузке в S3-совместимое объектное хранилище.
- [Выгрузка метаданных кластера в файловую систему с помощью `admin cluster dump`](tools-dump.md#cluster)
- [Загрузка метаданных кластера из файловой системы с помощью `admin cluster restore`](tools-restore.md#cluster)
- [Выгрузка данных и метаданных базы данных в файловую систему с помощью `admin database dump`](tools-dump.md#db)
- [Загрузка данных и метаданных базы данных из файловой системы с помощью `admin database restore`](tools-restore.md#db)
- [Выгрузка отдельных схемных объектов в файловую систему с помощью `tools dump`](tools-dump.md#schema-objects)
- [Загрузка отдельных схемных объектов из файловой системы с помощью `tools restore`](tools-restore.md#schema-objects)
- [Соединение и аутентификация при работе с S3-совместимым объектным хранилищем](auth-s3.md)
- [Выгрузка в S3-совместимое объектное хранилище `export s3`](export-s3.md)
- [Загрузка из S3-совместимого объектного хранилища `import s3`](import-s3.md)
