---
title: "Выборка данных из определенных колонок"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/select_specific_columns?version=v26.1"
doc_path: "ru/dev/yql-tutorial/select_specific_columns"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/select_specific_columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/select_specific_columns.md"
description: "Выберите данные из колонок series_id, release_date и title. При этом переименуйте title в series_title и преобразуйте тип release_date из Uint32 в Date."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Выборка данных из определенных колонок

Выберите данные из колонок `series_id`, `release_date` и `title`. При этом переименуйте `title` в `series_title` и преобразуйте тип `release_date` из `Uint32` в `Date`.

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
SELECT
    series_id,             -- Имена колонок (series_id, release_date, title)
                           -- перечисляются через запятую.

    title AS series_title, -- С помощью AS можно переименовать столбцы
                           -- или дать имя произвольному выражению

    CAST(release_date AS Date) AS release_date

FROM series;
```
