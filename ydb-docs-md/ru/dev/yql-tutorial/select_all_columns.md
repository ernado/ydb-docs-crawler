---
title: "Выборка данных из всех колонок"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/select_all_columns?version=v26.1"
doc_path: "ru/dev/yql-tutorial/select_all_columns"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/select_all_columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/select_all_columns.md"
description: "Выберите все колонки из таблиц с помощью оператора SELECT. Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Выборка данных из всех колонок

Выберите все колонки из таблиц с помощью оператора [SELECT](../../yql/reference/syntax/select/index.md).

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

```yql
SELECT         -- Оператор выбора данных.

    *          -- Выбор всех колонок из таблицы.

FROM `<table_name>`; -- Таблица, из которой нужно выбрать данные. 
                   -- Можно выбрать данные из таблиц: series, seasons, episodes.
```
