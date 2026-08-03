---
title: "DROP EXTERNAL TABLE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-external-table?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-external-table"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-external-table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-external-table.md"
description: "Deletes the specified external table. If no external table with that name exists, an error is returned. Example. DROP EXTERNAL TABLE my_table;"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP EXTERNAL TABLE

Deletes the specified [external table](../../../concepts/datamodel/external_table.md).

If no external table with that name exists, an error is returned.

## Example

```yql
DROP EXTERNAL TABLE my_table;
```
