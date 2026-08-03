---
title: "INTO RESULT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/into_result?version=v26.1"
doc_path: "en/yql/reference/syntax/into_result"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/into_result.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/into_result.md"
description: "Lets you set a custom label for SELECT. Examples. SELECT 1 INTO RESULT foo; SELECT * FROM my_table WHERE value % 2 == 0 INTO RESULT `Result name`;"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
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
