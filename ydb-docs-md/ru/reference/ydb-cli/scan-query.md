---
title: "Выполнение скан запросов"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/scan-query?version=v26.1"
doc_path: "ru/reference/ydb-cli/scan-query"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/scan-query.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/scan-query.md"
description: "Важно. Использование ScanQuery не рекомендуется для новых сценариев. Для выполнения запросов используйте стандартные механизмы."
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# Выполнение скан запросов

> [!WARNING]
> Использование `ScanQuery` не рекомендуется для новых сценариев. Для выполнения запросов используйте стандартные механизмы.
>
> Подробнее см. в разделе [Выполнение запросов](yql.md).
>
> Исключение — выполнение длительных (более 5 минут) запросов к строчным таблицам. В этом случае мы по-прежнему рекомендуем использовать `ScanQuery`, так как стандартные механизмы выполнения запросов пока не полностью поддерживают этот сценарий.

Запуск запроса через [Scan Queries](../../concepts/query_execution/scan_query.md) посредством YDB CLI осуществляется добавлением флага `-t scan` в команду `ydb table query execute`.

Выполните запрос к данным:

```bash
ydb table query execute -t scan \
 --query "SELECT season_id, episode_id, title \
 FROM episodes \
 WHERE series_id = 1 AND season_id > 1 \
 ORDER BY season_id, episode_id \
 LIMIT 3"
```

Где:

- `--query` — текст запроса.

Результат:

```text
┌───────────┬────────────┬──────────────────────────────┐
| season_id | episode_id | title |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 1 | "The Work Outing" |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 2 | "Return of the Golden Child" |
├───────────┼────────────┼──────────────────────────────┤
| 2 | 3 | "Moss and the German" |
└───────────┴────────────┴──────────────────────────────┘
```
