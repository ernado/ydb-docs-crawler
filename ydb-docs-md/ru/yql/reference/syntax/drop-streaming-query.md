---
title: "DROP STREAMING QUERY"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-streaming-query?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-streaming-query"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-streaming-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-streaming-query.md"
description: "DROP STREAMING QUERY удаляет потоковый запрос. Синтаксис. DROP STREAMING QUERY [IF EXISTS ] < query_name >. Параметры."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP STREAMING QUERY

`DROP STREAMING QUERY` удаляет [потоковый запрос](../../../concepts/streaming-query/streaming-query.md).

## Синтаксис {#sintaksis}

```sql
DROP STREAMING QUERY [IF EXISTS] <query_name>
```

### Параметры {#parametry}

- `IF EXISTS` — не выводить ошибку, если потокового запроса не существует.
- `query_name` — имя потокового запроса, подлежащего удалению.

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `REMOVE SCHEMA` на потоковый запрос, пример выдачи такого разрешения для запроса `my_streaming_query`:

```sql
GRANT REMOVE SCHEMA ON my_streaming_query TO `user@domain`
```

## Примеры {#primery}

Удаление запроса `my_streaming_query`:

```sql
DROP STREAMING QUERY my_streaming_query
```

## См. также {#sm-takzhe}

- [Потоковые запросы](../../../concepts/streaming-query/streaming-query.md)
- [CREATE STREAMING QUERY](create-streaming-query.md)
- [ALTER STREAMING QUERY](alter-streaming-query.md)
