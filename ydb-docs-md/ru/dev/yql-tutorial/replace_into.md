---
title: "Вставка и модификация данных с помощью REPLACE"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/replace_into?version=v26.1"
doc_path: "ru/dev/yql-tutorial/replace_into"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/replace_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/replace_into.md"
description: "Важно."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Вставка и модификация данных с помощью REPLACE

> [!WARNING]
> В настоящее время одновременное использование [колоночных](../../concepts/glossary.md#column-oriented-table) и [строковых](../../concepts/glossary.md#row-oriented-table) таблиц поддерживается в транзакциях, в которых данные только читаются, но не изменяются. Поддержка транзакций с возможностью модификации данных при одновременном использовании строковых и колоночных таблиц находится в разработке.
>
> Если попытаться выполнить операцию записи в транзакции, в которой задействованы и колоночные, и строковые таблицы, транзакция завершится с ошибкой: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Добавьте новые данные в таблицы с одновременным обновлением уже существующих данных с помощью конструкции [REPLACE INTO](../../yql/reference/syntax/replace_into.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
REPLACE INTO episodes
(
    series_id,
    season_id,
    episode_id,
    title,
    air_date
)
VALUES
(
    2,
    5,
    12,
    "Test Episode !!!",
    CAST(Date("2018-08-27") AS Uint64)
)
;

-- Вызов COMMIT используется, чтобы следующей операции SELECT
-- были видны изменения, сделанные в рамках предыдущей транзакции.
COMMIT;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;
```
