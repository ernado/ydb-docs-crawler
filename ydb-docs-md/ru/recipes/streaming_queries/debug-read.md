---
title: "Отладочное чтение из топика"
url: "https://ydb.tech/docs/ru/recipes/streaming_queries/debug-read?version=v26.1"
doc_path: "ru/recipes/streaming_queries/debug-read"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/streaming_queries/debug-read.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/streaming_queries/debug-read.md"
description: "При разработке потоковых запросов бывает полезно быстро посмотреть, какие данные поступают в топик, без создания полноценного потокового запроса. Для этого можн"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Отладочное чтение из топика

При разработке [потоковых запросов](../../concepts/streaming-query/streaming-query.md) бывает полезно быстро посмотреть, какие данные поступают в [топик](../../concepts/datamodel/topic.md), без создания полноценного потокового запроса. Для этого можно выполнить обычный `SELECT` с параметром `STREAMING = TRUE`.

> [!WARNING]
> Этот способ предназначен только для отладки и проверки данных в топике. Для промышленного использования создавайте потоковые запросы через [CREATE STREAMING QUERY](../../yql/reference/syntax/create-streaming-query.md).

> [!NOTE]
> В примерах `ydb_source` — это заранее созданный [внешний источник данных](../../concepts/datamodel/external_data_source.md), а `topic_name` / `input_topic` — топики, доступные через него.

## Чтение сырых данных {#chtenie-syryh-dannyh}

Простейший способ — прочитать сообщения в формате `raw`, без разбора схемы:

```sql
SELECT
    Data
FROM
    ydb_source.topic_name
WITH (
    FORMAT = raw,
    SCHEMA = (
        Data String
    ),
    STREAMING = TRUE
)
LIMIT 1
```

Параметр `LIMIT` обязателен — без него запрос не завершится, так как будет ожидать новые сообщения бесконечно.

## Чтение с разбором JSON {#chtenie-s-razborom-json}

Если данные в топике хранятся в формате JSON, можно сразу разобрать их по полям:

```sql
SELECT
    *
FROM
    ydb_source.topic_name
WITH (
    FORMAT = json_each_row,
    SCHEMA = (
        Time String NOT NULL,
        Level String NOT NULL,
        Host String NOT NULL
    ),
    STREAMING = TRUE
)
LIMIT 5
```

## См. также {#sm-takzhe}

- [Потоковые запросы](../../concepts/streaming-query/streaming-query.md)
- [Форматы данных при чтении/записи из топиков](../../dev/streaming-query/streaming-query-formats.md) — поддерживаемые форматы данных
- [Потоковое чтение данных из топика](../../yql/reference/syntax/select/streaming.md) — описание `STREAMING = TRUE` в справочнике YQL
