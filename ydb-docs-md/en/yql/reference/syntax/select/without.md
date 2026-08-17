---
title: "WITHOUT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/without?version=v26.1"
doc_path: "en/yql/reference/syntax/select/without"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/without.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/without.md"
description: "Excluding columns from the result of SELECT *. Examples. SELECT * WITHOUT foo, bar FROM my_table;"
revision: "6cf79b202d43efced4776d730126c3952ec44c6d"
---

# WITHOUT

Excluding columns from the result of `SELECT *`.

## Examples

```yql
SELECT * WITHOUT foo, bar FROM my_table;
```

```yql
PRAGMA simplecolumns;
SELECT * WITHOUT t.foo FROM my_table AS t
CROSS JOIN (SELECT 1 AS foo) AS v;
```
