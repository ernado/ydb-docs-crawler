---
title: "FROM"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/from?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/from"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/from.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/from.md"
description: "Источник данных для SELECT. В качестве аргумента может принимать имя таблицы, результат другого SELECT или именованное выражение. К именованным выражениям можно"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# FROM

Источник данных для `SELECT`. В качестве аргумента может принимать имя таблицы, результат другого `SELECT` или [именованное выражение](../expressions.md#named-nodes). К именованным выражениям можно обращаться [как к таблицам](from_as_table.md)(`FROM AS_TABLE`).

Ещё в YQL можно выполнить запрос по нескольким таблицам. Для этого в `SELECT` после `FROM` можно указывать не только одну таблицу или подзапрос, но и вызывать встроенные функции, позволяющие объединять данные нескольких таблиц.

Также вы можете обходить не таблицы, а итерироваться по дереву целевого кластера, с возможностью накопить состояние, обычно список путей к таблицам.

Между `SELECT` и `FROM` через запятую указываются имена столбцов из источника или `*` для выбора всех столбцов.

## Примеры {#primery}

```yql
SELECT key FROM my_table;
```

```yql
SELECT * FROM
  (SELECT value FROM my_table);
```

```yql
$table_name = "my_table";
SELECT * FROM $table_name;
```
