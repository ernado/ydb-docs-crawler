---
title: "INTO RESULT"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/into_result?version=v26.1"
doc_path: "ru/yql/reference/syntax/into_result"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/into_result.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/into_result.md"
description: "Позволяет задать пользовательскую метку для SELECT. Примеры. SELECT 1 INTO RESULT foo;"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
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
