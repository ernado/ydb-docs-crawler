---
title: "ALTER TABLE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/index.md"
description: "При помощи команды ALTER TABLE можно изменить состав колонок и дополнительные параметры строковых и колоночных таблиц. В одной команде можно указать несколько д"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER TABLE

При помощи команды `ALTER TABLE` можно изменить состав колонок и дополнительные параметры [строковых](../../../concepts/datamodel/table.md#row-tables) и [колоночных](../../../concepts/datamodel/table.md#colums-tables) таблиц. В одной команде можно указать несколько действий. В общем случае команда `ALTER TABLE` выглядит так:

```yql
ALTER TABLE table_name action1, action2, ..., actionN;
```

`action` — это любое действие по изменению таблицы, из описанных ниже:

- [Переименование таблицы](alter_table/rename.md).
- Работа с [колонками](alter_table/columns.md) строковой и колоночной таблиц.
- Добавление или удаление [потока изменений](alter_table/changefeed.md).
- Работа с [индексами](alter_table/indexes.md).
- Работа с [группами колонок](alter_table/family.md) строковой таблицы.
- Изменение [дополнительных параметров таблиц](alter_table/set.md).
