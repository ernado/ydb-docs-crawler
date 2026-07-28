---
title: "Внешние таблицы"
url: "https://ydb.tech/docs/ru/concepts/datamodel/external_table?version=v26.1"
doc_path: "ru/concepts/datamodel/external_table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/datamodel/external_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/datamodel/external_table.md"
description: "Часть внешних источников, например, системы управления базами данных, хранят данные в схематизированном виде, а часть, как S3 (Yandex Object Storage), в виде от"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Внешние таблицы

Часть [внешних источников](external_data_source.md), например, системы управления базами данных, хранят данные в схематизированном виде, а часть, как S3 (Yandex Object Storage), в виде отдельных файлов. Для работы с файловыми источниками данных необходимо знать как правила расположения файлов, так и форматы самих хранимых данных.

Для описания хранимых данных в таких источниках используется специальная сущность - внешние таблицы, `EXTERNAL TABLE`. Внешние таблицы позволяют задать схему данных у хранимых файлов, а также описать схему расположения файлов внутри источника.

Запись в YQL может выглядеть так:

```yql
CREATE EXTERNAL TABLE s3_test_data (
  key Utf8 NOT NULL,
  value Utf8 NOT NULL
) WITH (
  DATA_SOURCE="bucket",
  LOCATION="folder",
  FORMAT="csv_with_names",
  COMPRESSION="gzip"
);
```

Во внешние таблицы можно вставлять данные, так же, как и в обычные. Например, для записи данных во внешнюю таблицу достаточно выполнить следующий запрос:

```yql
INSERT INTO s3_test_data
SELECT * FROM Table
```

Подробнее про работу с внешними таблицами, описывающими бакеты S3 (Object Storage) описано в разделе [Чтение из бакетов S3 через внешние таблицы](../query_execution/federated_query/s3/external_table.md).
