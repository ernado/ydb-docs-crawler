---
title: "Сортировка и фильтрация"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/basic_filter_and_sort?version=v26.1"
doc_path: "ru/dev/yql-tutorial/basic_filter_and_sort"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/basic_filter_and_sort.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/basic_filter_and_sort.md"
description: "Выберите первые три эпизода из всех сезонов IT Crowd за исключением первого. Примечание."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Сортировка и фильтрация

Выберите первые три эпизода из всех сезонов IT Crowd за исключением первого.

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
SELECT
   series_id,
   season_id,
   episode_id,
   CAST(air_date AS Date) AS air_date,
   title

FROM episodes
WHERE
   series_id = 1      -- Список условий для формирования результата.
   AND season_id > 1  -- Логическое И (AND) используется для написания сложных условий.

ORDER BY              -- Сортировка результатов.
   series_id,         -- ORDER BY сортирует значения по одному или нескольким
   season_id,         -- столбцам. Столбцы перечисляются через запятую.
   episode_id

LIMIT 3               -- LIMIT N после ORDER BY означает
                      -- «получить первые N» или «последние N» результатов
;                     -- в зависимости от порядка сортировки.
```
