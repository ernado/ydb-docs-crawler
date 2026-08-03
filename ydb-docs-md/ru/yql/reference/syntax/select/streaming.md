---
title: "Потоковое чтение данных из топика"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/streaming?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/streaming"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/streaming.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/streaming.md"
description: "Можно выполнять чтение данных из топика обычным SELECT без создания потокового запроса. Для этого необходимо указать STREAMING = TRUE в блоке WITH и задать огра"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Потоковое чтение данных из топика

Можно выполнять чтение данных из [топика](../../../../concepts/datamodel/topic.md) обычным `SELECT` без создания [потокового запроса](../../../../concepts/streaming-query/streaming-query.md). Для этого необходимо указать `STREAMING = TRUE` в блоке `WITH` и задать ограничение на количество выходных строк через `LIMIT`, иначе запрос не завершится.

> [!WARNING]
> Этот способ предназначен только для отладки и проверки данных в топике. Для production процессов создавайте потоковые запросы через [CREATE STREAMING QUERY](../create-streaming-query.md).

> [!NOTE]
> В примерах `ydb_source` — это заранее созданный [внешний источник данных](../../../../concepts/datamodel/external_data_source.md), а `topic_name` — топик, доступный через него.

## Пример {#primer}

```yql
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

## См. также {#sm-takzhe}

- [Отладочное чтение из топика](../../../../recipes/streaming_queries/debug-read.md) — рецепт с дополнительными примерами
- [Потоковые запросы](../../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](../create-streaming-query.md)
