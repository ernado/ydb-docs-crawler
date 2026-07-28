---
title: "COMMIT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/commit?version=v26.1"
doc_path: "en/yql/reference/syntax/commit"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/commit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/commit.md"
description: "By default, the entire YQL query is executed within a single transaction, and independent parts inside it are executed in parallel, if possible."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# COMMIT

By default, the entire YQL query is executed within a single transaction, and independent parts inside it are executed in parallel, if possible.  
 Using the `COMMIT;` keyword you can add a barrier to the execution process to delay execution of expressions that follow until all the preceding expressions have completed.

To commit in the same way automatically after each expression in the query, you can use `PRAGMA autocommit;`.

## Examples

```yql
INSERT INTO result1 SELECT * FROM my_table;
INSERT INTO result2 SELECT * FROM my_table;
COMMIT;
-- result2 will already include the SELECT contents from the second line:
INSERT INTO result3 SELECT * FROM result2;
```
