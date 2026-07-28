---
title: "en/yql/reference/syntax/select/from"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/from?version=v26.1"
doc_path: "en/yql/reference/syntax/select/from"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/from.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/from.md"
description: "FROM."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# en/yql/reference/syntax/select/from

## FROM

Data source for `SELECT`. The argument can accept the table name, the result of another `SELECT`, or a [named expression](../expressions.md#named-nodes). Between `SELECT` and `FROM`, list the comma-separated column names from the source (or `*` to select all columns).

### Examples

```yql
SELECT key FROM my_table;
```

```yql
SELECT * FROM
  (SELECT value FROM my_table);
```

```yql
$table_name = "my_table";
SELECT * FROM $table_name;
```
