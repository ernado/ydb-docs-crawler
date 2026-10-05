---
title: "WHERE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/where?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/where"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/where.md"
description: "Фильтрация строк в результате выполнения SELECT по условию в колоночной или строковой таблице. Пример. SELECT key FROM my_table WHERE value > 0; Важно."
revision: "259414a47522df8faa233e3f6fd5c97bc5325d93"
---

# WHERE

Фильтрация строк в результате выполнения `SELECT` по условию в колоночной или строковой таблице.

## Пример {#primer}

```yql
SELECT key FROM my_table
WHERE value > 0;
```

> [!WARNING]
> Коррелированные подзапросы в `WHERE` не поддерживаются: подзапрос не может обращаться к колонкам или псевдонимам таблиц из внешнего запроса. Для отбора строк, у которых есть совпадающие строки в другой таблице, используйте [`LEFT SEMI JOIN`](../correlated-subqueries.md#exists). Для отбора строк без совпадений используйте [`LEFT ONLY JOIN`](../correlated-subqueries.md#not-exists).
