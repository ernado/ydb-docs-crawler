---
title: "Объединение таблиц с помощью JOIN"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/join_tables?version=v26.1"
doc_path: "ru/dev/yql-tutorial/join_tables"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/join_tables.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/join_tables.md"
description: "Объедините колонки исходных таблиц seasons и series и выведите все сезоны сериала IT Crowd в результирующей таблице с помощью оператора JOIN. Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Объединение таблиц с помощью JOIN

Объедините колонки исходных таблиц `seasons` и `series` и выведите все сезоны сериала IT Crowd в результирующей таблице с помощью оператора [JOIN](../../yql/reference/syntax/select/join.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
SELECT
    sa.title AS season_title,    -- sa и sr — это «связующие названия»,
    sr.title AS series_title,    -- алиасы таблиц, объявленные ниже с помощью AS.
    sr.series_id,                -- Они используются, чтобы избежать
    sa.season_id                 -- неоднозначности в именах указанных колонок.

FROM
    seasons AS sa
INNER JOIN
    series AS sr
ON sa.series_id = sr.series_id
WHERE sa.series_id = 1
ORDER BY                         -- Cортировка результатов.
    sr.series_id,
    sa.season_id                 -- ORDER BY сортирует значения по одному
;                                -- или нескольким столбцам.
                                 -- Столбцы перечисляются через запятую.
```
