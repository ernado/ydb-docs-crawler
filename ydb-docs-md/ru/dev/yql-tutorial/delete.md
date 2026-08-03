---
title: "Удаление данных"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/delete?version=v26.1"
doc_path: "ru/dev/yql-tutorial/delete"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/delete.md"
description: "Удалите данные из таблицы с помощью оператора DELETE. Примечание."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Удаление данных

Удалите данные из таблицы с помощью оператора [DELETE](../../yql/reference/syntax/delete.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
DELETE
FROM episodes
WHERE
    series_id = 2
    AND season_id = 5
    AND episode_id = 12
;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;

-- YDB не знает об изменениях, имевших место в начале транзакции,
-- поэтому сначала выполняет чтение. Невозможно выполнить UPDATE или DELETE,
-- если таблица уже была изменена в рамках текущей транзакции. UPDATE ON и
-- DELETE ON позволяют читать, обновлять и удалять несколько строк из одной таблицы
-- в рамках одной транзакции.

$to_delete = (
    SELECT series_id, season_id, episode_id
    FROM episodes
    WHERE series_id = 1 AND season_id = 1 AND episode_id = 2
);

SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;

DELETE FROM episodes ON
SELECT * FROM $to_delete;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;
```
