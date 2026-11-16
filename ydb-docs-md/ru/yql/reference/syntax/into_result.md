---
title: "INTO RESULT"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/into_result?version=v26.1"
doc_path: "ru/yql/reference/syntax/into_result"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/into_result.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/into_result.md"
description: "Позволяет задать пользовательскую метку для SELECT. Примеры. SELECT 1 INTO RESULT foo;"
revision: "7d1701f96bbb0c1cd62ff0890f67a9b86caf1d5e"
---

# INTO RESULT

Позволяет задать пользовательскую метку для [SELECT](select/index.md).

## Примеры {#primery}

```yql
SELECT 1 INTO RESULT foo;
```

```yql
SELECT * FROM
my_table
WHERE value % 2 == 0
INTO RESULT `Название результата`;
```
