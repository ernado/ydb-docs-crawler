---
title: "en/yql/reference/syntax/select/from_select"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/from_select?version=v26.1"
doc_path: "en/yql/reference/syntax/select/from_select"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/from_select.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/from_select.md"
description: "FROM... SELECT... An inverted format, first specifying the data source and then the operation. Examples. FROM my_table SELECT key, value;"
revision: "0b31976d929e6dd165473a40bb0855b365abe8f7"
---

# en/yql/reference/syntax/select/from_select

## FROM ... SELECT ...

An inverted format, first specifying the data source and then the operation.

### Examples

```yql
FROM my_table SELECT key, value;
```

```yql
FROM a_table AS a
JOIN b_table AS b
USING (key)
SELECT *;
```
