---
title: "WHERE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/where?version=v26.1"
doc_path: "en/yql/reference/syntax/select/where"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/where.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/where.md"
description: "Filtering rows in the SELECT result based on a condition in row-oriented or column-oriented. Example. SELECT key FROM my_table WHERE value > 0;"
revision: "8c7501e02fd7c6de0c7110aafa90f78948400f1e"
---

# WHERE

Filtering rows in the `SELECT` result based on a condition in [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) or [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables).

## Example

```yql
SELECT key FROM my_table
WHERE value > 0;
```
