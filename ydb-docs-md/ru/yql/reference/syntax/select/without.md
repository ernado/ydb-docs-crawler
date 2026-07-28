---
title: "WITHOUT"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/without?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/without"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/without.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/without.md"
description: "Исключение столбцов из результата запроса SELECT *. Примеры. SELECT * WITHOUT foo, bar FROM my_table;"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# WITHOUT

Исключение столбцов из результата запроса `SELECT *`.

## Примеры {#primery}

```yql
SELECT * WITHOUT foo, bar FROM my_table;
```

```yql
PRAGMA simplecolumns;
SELECT * WITHOUT t.foo FROM my_table AS t
CROSS JOIN (SELECT 1 AS foo) AS v;
```
