---
title: "WHERE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/where?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/where"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/where.md"
description: "Фильтрация строк в результате выполнения SELECT по условию в колоночной или строковой таблице. Пример. SELECT key FROM my_table WHERE value > 0;"
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# WHERE

Фильтрация строк в результате выполнения `SELECT` по условию в колоночной или строковой таблице.

## Пример {#primer}

```yql
SELECT key FROM my_table
WHERE value > 0;
```
