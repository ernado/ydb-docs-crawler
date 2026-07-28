---
title: "Настройка времени жизни строк (TTL) таблицы"
url: "https://ydb.tech/docs/ru/recipes/ydb-cli/ttl?version=v26.1"
doc_path: "ru/recipes/ydb-cli/ttl"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-cli/ttl.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-cli/ttl.md"
description: "В этом разделе приведены примеры настройки TTL строковых и колоночных таблиц при помощи YDB CLI. Включение TTL для существующих строковых и колоночных таблиц."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Настройка времени жизни строк (TTL) таблицы

В этом разделе приведены примеры настройки TTL строковых и колоночных таблиц при помощи YDB CLI.

## Включение TTL для существующих строковых и колоночных таблиц {#enable-on-existent-table}

В приведенном ниже примере строки таблицы `mytable` будут удаляться спустя час после наступления времени, записанного в колонке `created_at`:

```bash
$ ydb -e <endpoint> -d <database> table ttl set --column created_at --expire-after 3600 mytable
```

Следующий пример демонстрирует использование колонки `modified_at` с числовым типом (`Uint32`) в качестве TTL-колонки. Значение колонки интерпретируется как секунды от Unix-эпохи:

```bash
$ ydb -e <endpoint> -d <database> table ttl set --column modified_at --expire-after 3600 --unit seconds mytable
```

## Включение вытеснения данных во внешнее S3-совместимое хранилище {#vklyuchenie-vytesneniya-dannyh-vo-vneshnee-s3-sovmestimoe-hranilishe}

> [!WARNING]
> Поддерживается только для [колоночных](../../concepts/datamodel/table.md#column-oriented-tables) таблиц. Поддержка функциональности для [строковых](../../concepts/datamodel/table.md#row-oriented-tables) таблиц находится в разработке.

Для включения вытеснения требуется объект [external data source](../../concepts/datamodel/external_data_source.md), описывающий подключение к внешнему хранилищу. Пример создания объекта можно найти в [рецептах YQL](../../yql/reference/recipes/ttl.md#enable-tiering-on-existing-tables).

Следующий пример демонстрирует включение вытеснения данных через вызов YQL-запроса из YDB CLI. Строки таблицы `mytable` будут переноситься в бакет, описанный во внешнем источнике данных `/Root/s3_cold_data`, спустя час после наступления времени, записанного в колонке `created_at`, а спустя 24 часа будут удаляться.

```bash
$ ydb -e <endpoint> -d <database> sql -s '
    ALTER TABLE `mytable` SET (
        TTL =
            Interval("PT1H") TO EXTERNAL DATA SOURCE `/Root/s3_cold_data`,
            Interval("PT24H") DELETE
        ON modified_at AS SECONDS
    );
'
```

## Выключение TTL {#disable}

```bash
$ ydb -e <endpoint> -d <database> table ttl reset mytable
```

## Получение настроек TTL {#describe}

Текущие настройки TTL можно получить из описания таблицы:

```bash
$ ydb -e <endpoint> -d <database> scheme describe mytable
```
