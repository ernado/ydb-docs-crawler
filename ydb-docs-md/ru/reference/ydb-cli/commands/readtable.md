---
title: "Потоковое чтение строковой таблицы"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/readtable?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/readtable"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/readtable.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/readtable.md"
description: "Потоковое чтение строковой таблицы. Важно. Поддерживается только для строковых таблиц. Поддержка функциональности для колоночных таблиц находится в разработке."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Потоковое чтение строковой таблицы

> [!WARNING]
> Поддерживается только для [строковых](../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

Чтобы прочитать снапшот таблицы целиком, используйте подкоманду `read`. Данные передаются в виде стрима, что позволяет прочитать таблицу произвольного размера.

Прочитайте данные:

```bash
ydb table read episodes \
  --ordered \
  --limit 5 \
  --columns series_id,season_id,episode_id,title
```

Где :

- `--ordered` — упорядочить читаемые записи по ключу.
- `--limit` — ограничить количество читаемых записей.
- `--columns` — колонки, значения которых следует читать (по умолчанию читаются все колонки) в формате CSV.

Результат:

```text
┌───────────┬───────────┬────────────┬───────────────────────────────┐
| series_id | season_id | episode_id | title                         |
├───────────┼───────────┼────────────┼───────────────────────────────┤
| 1         | 1         | 1          | "Yesterday's Jam"             |
├───────────┼───────────┼────────────┼───────────────────────────────┤
| 1         | 1         | 2          | "Calamity Jen"                |
├───────────┼───────────┼────────────┼───────────────────────────────┤
| 1         | 1         | 3          | "Fifty-Fifty"                 |
├───────────┼───────────┼────────────┼───────────────────────────────┤
| 1         | 1         | 4          | "The Red Door"                |
├───────────┼───────────┼────────────┼───────────────────────────────┤
| 1         | 1         | 5          | "The Haunting of Bill Crouse" |
└───────────┴───────────┴────────────┴───────────────────────────────┘
```

Если вам нужно получить только количество прочитанных записей, используйте параметр `--count-only`:

```bash
ydb table read episodes \
  --columns series_id \
  --count-only
```

Результат:

```text
70
```
