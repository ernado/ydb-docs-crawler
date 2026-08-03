---
title: "WHERE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/where?version=v26.1"
doc_path: "en/yql/reference/syntax/select/where"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/where.md"
description: "Filtering rows in the SELECT result based on a condition in row-oriented or column-oriented. Example. SELECT key FROM my_table WHERE value > 0;"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# WHERE

Filtering rows in the `SELECT` result based on a condition in [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) or [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables).

## Example

```yql
SELECT key FROM my_table
WHERE value > 0;
```
