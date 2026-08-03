---
title: "Обновление данных с помощью UPDATE"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/update?version=v26.1"
doc_path: "ru/dev/yql-tutorial/update"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/update.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/update.md"
description: "Обновите данные в таблице с помощью оператора UPDATE. Примечание."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обновление данных с помощью UPDATE

Обновите данные в таблице с помощью оператора [UPDATE](../../yql/reference/syntax/update.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
UPDATE episodes
SET title="test Episode 2"
WHERE
    series_id = 2
    AND season_id = 5
    AND episode_id = 12
;

COMMIT;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;

-- YDB не знает об изменениях, имевших место в начале транзакции,
-- поэтому сначала выполняет чтение. Невозможно обновить или удалить таблицу,
-- которая уже была изменена в рамках текущей транзакции. UPDATE ON и
-- DELETE ON позволяют читать, обновлять и удалять несколько строк в таблице
-- в рамках одной транзакции.

$to_update = (
    SELECT series_id,
           season_id,
           episode_id,
           Utf8("Yesterday's Jam UPDATED") AS title
    FROM episodes
    WHERE series_id = 1 AND season_id = 1 AND episode_id = 1
);

SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;

UPDATE episodes ON
SELECT * FROM $to_update;

COMMIT;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;
```
