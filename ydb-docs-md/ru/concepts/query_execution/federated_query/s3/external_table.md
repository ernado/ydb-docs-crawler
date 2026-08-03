---
title: "Чтение из бакетов S3 через внешние таблицы"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/s3/external_table?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/s3/external_table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/s3/external_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/s3/external_table.md"
description: "Иногда одни и те же запросы к данным нужно выполнять регулярно. Чтобы не указывать все детали работы с этими данными при каждом вызове запроса, используйте режи"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Чтение из бакетов S3 через внешние таблицы

Иногда одни и те же запросы к данным нужно выполнять регулярно. Чтобы не указывать все детали работы с этими данными при каждом вызове запроса, используйте режим с [внешними таблицами](../../../datamodel/external_table.md). В этом случае запрос выглядит, как обычный запрос к таблицам YDB.

Пример запроса для чтения данных:

```yql
SELECT
    *
FROM
    s3_test_data
WHERE
    version > 1
```

## Создание внешней таблицы, ведущей на бакет S3-совместимого хранилища данных {#external-table-settings}

Чтобы создать внешнюю таблицу, описывающую бакет S3, выполните следующий SQL-запрос. Запрос создает внешнюю таблицу с именем `s3_test_data`, в котором расположены файлы в формате `CSV` со строковыми полями `key` и `value`, находящиеся внутри бакета по пути `test_folder`, при этом для указания реквизитов подключения используется объект [внешний источник данных](../../../datamodel/external_data_source.md) `bucket`:

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

Где:

- `key, value` - список колонок данных и их типов, список допустимых типов описан в разделе [Поддерживаемые типы данных](formats.md#types);
- `bucket` - имя [внешнего источника данных](../../../datamodel/external_data_source.md) к S3-совместимому хранилищу данных;
- `folder` - путь внутри бакета с данными. Поддерживаются подстановочные знаки `*`, `?`, `{ ... }`; подробнее [в разделе](external_data_source.md#path_format);
- `csv_with_names` - один из [допустимых типов хранения данных](formats.md);
- `gzip` - один из [допустимых алгоритмов сжатия](formats.md#compression).

Также при создании внешних таблиц поддерживаются [параметры форматирования](external_data_source.md#format_settings).

## Модель данных {#data-model}

Чтение данных с помощью внешних таблиц из S3-совместимого хранилища данных выполняется с помощью обычных SQL-запросов, как к обычной таблице.

```yql
SELECT
    <expression>
FROM
    s3_test_data
WHERE
    <filter>;
```

## Ограничения {#ogranicheniya}

При работе с бакетами S3-совместимого хранилища данных существует ряд ограничений.

Ограничения:

1. Поддерживаются только запросы чтения данных - `SELECT` и `INSERT`, остальные виды запросов не поддерживаются.
2. Если значение даты, хранящейся во внешнем источнике данных, находится вне допустимого для YDB диапазона (все используемые даты должны быть позднее 1970-01-01, но ранее 2105-12-31), в YDB такое значение будет преобразовано в `NULL`.
