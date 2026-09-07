---
title: "INTO RESULT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/into_result?version=v26.1"
doc_path: "en/yql/reference/syntax/into_result"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/into_result.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/into_result.md"
description: "Lets you set a custom label for SELECT. Examples. SELECT 1 INTO RESULT foo; SELECT * FROM my_table WHERE value % 2 == 0 INTO RESULT `Result name`;"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# INTO RESULT

Lets you set a custom label for [SELECT](select/index.md).

## Examples

```yql
SELECT 1 INTO RESULT foo;
```

```yql
SELECT * FROM
my_table
WHERE value % 2 == 0
INTO RESULT `Result name`;
```
