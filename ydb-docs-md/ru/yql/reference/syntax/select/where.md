---
title: "WHERE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/where?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/where"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/where.md"
description: "Фильтрация строк в результате выполнения SELECT по условию в колоночной или строковой таблице. Пример. SELECT key FROM my_table WHERE value > 0;"
revision: "8c7501e02fd7c6de0c7110aafa90f78948400f1e"
---

# WHERE

Фильтрация строк в результате выполнения `SELECT` по условию в колоночной или строковой таблице.

## Пример {#primer}

```yql
SELECT key FROM my_table
WHERE value > 0;
```
