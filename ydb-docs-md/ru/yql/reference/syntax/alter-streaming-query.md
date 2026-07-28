---
title: "ALTER STREAMING QUERY"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-streaming-query?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-streaming-query"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-streaming-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-streaming-query.md"
description: "ALTER STREAMING QUERY изменяет настройки потоковых запросов, а также управляет их состоянием: запуском и остановкой. Синтаксис."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER STREAMING QUERY

`ALTER STREAMING QUERY` изменяет настройки [потоковых запросов](../../../concepts/streaming-query/streaming-query.md), а также управляет их состоянием: запуском и остановкой.

## Синтаксис {#sintaksis}

```sql
ALTER STREAMING QUERY [IF EXISTS] <query_name> SET (
    <key1> = <value1>,
    <key2> = <value2>,
    ...
)
```

### Параметры {#parametry}

- `IF EXISTS` — не выводить ошибку, если потокового запроса не существует.
- `query_name` — имя потокового запроса, подлежащего изменению.
- `SET (<key> = <value>)` — список настроек потокового запроса, которые нужно обновить, опционально.

### Изменение параметров запроса {#izmenenie-parametrov-zaprosa}

Синтаксис:

```sql
ALTER STREAMING QUERY [IF EXISTS] <query_name> SET (<key> = <value>)
```

Доступные параметры:

- `RUN = (TRUE|FALSE)` — запустить или остановить запрос.
- `RESOURCE_POOL = <resource_pool_name>` — имя [пула ресурсов](../../../concepts/glossary.md#resource-pool), в котором будет выполняться запрос.

При выполнении `SET (RUN = TRUE)` смещения чтения из топика и состояния агрегационных функций восстанавливаются из [чекпоинта](../../../dev/streaming-query/checkpoints.md). При отсутствии чекпоинта чтение начинается с самых свежих данных.

Примеры изменения параметров запроса [см. ниже](alter-streaming-query.md#parameters-changing-examples).

## Разрешения {#razresheniya}

Для работы с потоковыми запросами требуется [разрешение](grant.md#permissions-list) `ALTER SCHEMA`, пример выдачи такого разрешения для запроса `my_streaming_query`:

```sql
GRANT ALTER SCHEMA ON my_streaming_query TO `user@domain`
```

## Примеры {#primery}

### Изменение параметров {#parameters-changing-examples}

Остановка запроса `my_streaming_query`:

```sql
ALTER STREAMING QUERY my_streaming_query SET (
    RUN = FALSE
)
```

Запуск запроса `my_streaming_query` в [пуле ресурсов](../../../concepts/glossary.md#resource-pool) `my_resource_pool`:

```sql
ALTER STREAMING QUERY my_streaming_query SET (
    RUN = TRUE,
    RESOURCE_POOL = my_resource_pool
)
```

### Статус запроса {#status-of-query}

Текущий статус запроса доступен в колонке `Status` системной таблицы [.sys/streaming_queries](../../../dev/system-views.md):

```sql
SELECT
    Path,
    Status,
    Text,
    Run
FROM
    `.sys/streaming_queries`
```

Возможные значения статуса:

1. `CREATING` — запрос создаётся после выполнения команды `CREATE STREAMING QUERY`.
2. `CREATED` — запрос создан, но не запущен (например, при указании `RUN = FALSE`).
3. `STARTING` — запрос запускается.
4. `RUNNING` — запрос выполняется.
5. `SUSPENDED` — запрос приостановлен из-за внутренних ошибок. Система автоматически повторит запуск.
6. `STOPPING` — запрос останавливается по команде `ALTER STREAMING QUERY ... SET (RUN = FALSE)`.
7. `STOPPED` — запрос остановлен.

Гарантируется, что на момент успешного завершения DDL для создания или изменения потокового запроса, статус будет `CREATED`, `STARTING`, `RUNNING`, `STOPPED` или `SUSPENDED` в зависимости от настройки `RUN = (TRUE|FALSE)` и успешности запуска запроса.

Примеры обработки данных в других форматах приведены в статье [Форматы данных при чтении/записи из топиков](../../../dev/streaming-query/streaming-query-formats.md). Подробнее о возможностях и ограничениях потоковых запросов [см. в документации](../../../concepts/streaming-query/streaming-query.md).

## См. также {#sm-takzhe}

- [Потоковые запросы](../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](create-streaming-query.md)
- [DROP STREAMING QUERY](drop-streaming-query.md)
