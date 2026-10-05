---
title: "LIMIT and OFFSET"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/limit_offset?version=v26.1"
doc_path: "en/yql/reference/syntax/select/limit_offset"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/limit_offset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/limit_offset.md"
description: "LIMIT: limits the output to the specified number of rows. By default, the output is not restricted."
revision: "259414a47522df8faa233e3f6fd5c97bc5325d93"
---

# LIMIT and OFFSET

`LIMIT`: limits the output to the specified number of rows. By default, the output is not restricted.

`OFFSET`: specifies the offset from the beginning (in rows). By default, it's zero.

## Examples

```yql
SELECT key FROM my_table
LIMIT 7;
```

```yql
SELECT key FROM my_table
LIMIT 7 OFFSET 3;
```

```yql
SELECT key FROM my_table
LIMIT 3, 7; -- equivalent to the previous example
```
