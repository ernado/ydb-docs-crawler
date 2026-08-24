---
title: "Вставка и модификация данных с помощью UPSERT"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/upsert_into?version=v26.1"
doc_path: "ru/dev/yql-tutorial/upsert_into"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/upsert_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/upsert_into.md"
description: "Добавьте данные в таблицу с помощью конструкции UPSERT INTO. Примечание."
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# Вставка и модификация данных с помощью UPSERT

Добавьте данные в таблицу с помощью конструкции [UPSERT INTO](../../yql/reference/syntax/upsert_into.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
UPSERT INTO episodes
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
    13,
    "Test Episode",
    CAST(Date("2018-08-27") AS Uint64)
)
;

COMMIT;

-- Посмотреть результат:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;
```
