---
title: "Добавление и удаление колонок"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/alter_table?version=v26.1"
doc_path: "ru/dev/yql-tutorial/alter_table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/alter_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/alter_table.md"
description: "Добавьте новую колонку в таблицу, а затем удалите ее. Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Добавление и удаление колонок

Добавьте новую колонку в таблицу, а затем удалите ее.

> [!NOTE]
> Предполагается, что вы уже создали таблицы ранее на шаге [Создание таблиц](create_demo_tables.md) и заполнили их данными на шаге [Добавление данных в таблицы](fill_tables_with_data.md).

## Добавить колонку {#add-column}

Добавьте неключевую колонку в существующую таблицу:

```yql
ALTER TABLE episodes ADD COLUMN viewers Uint64;
```

## Удалить колонку {#delete-column}

Удалите добавленную колонку из таблицы:

```yql
ALTER TABLE episodes DROP COLUMN viewers;
```
