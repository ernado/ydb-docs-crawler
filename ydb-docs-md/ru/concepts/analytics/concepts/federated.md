---
title: "Федеративные запросы"
url: "https://ydb.tech/docs/ru/concepts/analytics/concepts/federated?version=v26.1"
doc_path: "ru/concepts/analytics/concepts/federated"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/analytics/concepts/federated.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/analytics/concepts/federated.md"
description: "Федеративные запросы — это возможность выполнять запросы к данным, хранящимся во внешних системах, без их предварительной загрузки (ETL) в YDB. Наиболее популяр"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Федеративные запросы

[Федеративные запросы](../../query_execution/federated_query/index.md) — это возможность выполнять запросы к данным, хранящимся во внешних системах, без их предварительной загрузки (ETL) в YDB. Наиболее популярный сценарий — работа с данными в объектных хранилищах, совместимых с S3.

## Как это работает {#kak-eto-rabotaet}

Вы можете создать во YDB [внешнюю таблицу](../../datamodel/external_table.md), которая ссылается на данные в S3. При выполнении запроса `SELECT` к такой таблице YDB инициирует параллельное чтение данных со всех вычислительных узлов. Каждый узел считывает и обрабатывает только ту часть данных, которая ему необходима.

- Поддерживаемые форматы: [Parquet, CSV, JSON](../../query_execution/federated_query/s3/formats.md) с [различными алгоритмами сжатия](../../query_execution/federated_query/s3/formats.md#compression).
- Оптимизация чтения: YDB использует механизмы оптимизации чтения данных из S3 (partition pruning) для [Hive-размещения данных](../../query_execution/federated_query/s3/partitioning.md#podderzhivaemye-formaty-putej-hraneniya) и для [более сложных алгоритмов размещения](../../query_execution/federated_query/s3/partition_projection.md).

![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/concepts/analytics/concepts/_includes/s3_read.png)
