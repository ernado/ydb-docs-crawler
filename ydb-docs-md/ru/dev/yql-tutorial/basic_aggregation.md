---
title: "Агрегирование данных"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/basic_aggregation?version=v26.1"
doc_path: "ru/dev/yql-tutorial/basic_aggregation"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/basic_aggregation.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/basic_aggregation.md"
description: "Узнайте количество эпизодов с уникальными названиями для каждого сезона каждого сериала. Примечание."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Агрегирование данных

Узнайте количество эпизодов с уникальными названиями для каждого сезона каждого сериала.

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
SELECT
    series_id,
    season_id,
    COUNT (*) AS cnt -- Агрегатная функция COUNT возвращает количество строк,
                     -- полученных в результате выполнения запроса.
                     -- Звездочка (*) указывает, что функция COUNT
                     -- посчитает количество всех строк в таблице.
                     -- COUNT(*) возвращает количество строк в
                     -- указанной таблице с учетом повторяющихся строк.
                     -- Функция считает каждую строку отдельно.
                     -- В результат также входят строки, содержащие значения null.
FROM episodes

GROUP BY
    series_id,       -- Результат выполнения запроса будет выведен в порядке указанных колонок.
    season_id        -- Несколько колонок разделяются запятой.
                     -- Другие колонки можно указать после выполнения SELECT, только если
                     -- они передаются в функцию агрегации.
ORDER BY
    series_id,
    season_id
;
```
