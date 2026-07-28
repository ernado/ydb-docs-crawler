---
title: "DROP EXTERNAL TABLE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-external-table?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-external-table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-external-table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-external-table.md"
description: "Удаляет указанную внешнюю таблицу. Если внешней таблицы с таким именем не существует, возвращается ошибка. Пример. DROP EXTERNAL TABLE my_table;"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP EXTERNAL TABLE

Удаляет указанную [внешнюю таблицу](../../../concepts/datamodel/external_table.md).

Если внешней таблицы с таким именем не существует, возвращается ошибка.

## Пример {#primer}

```yql
DROP EXTERNAL TABLE my_table;
```
