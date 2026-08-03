---
title: "Selecting data from all columns"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/select_all_columns?version=v26.1"
doc_path: "en/dev/yql-tutorial/select_all_columns"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/select_all_columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/select_all_columns.md"
description: "Select all columns from the table using SELECT: Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Selecting data from all columns

Select all columns from the table using [SELECT](../../yql/reference/syntax/select/index.md):

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
SELECT         -- Data selection operator.

    *          -- Select all columns from the table.

FROM episodes; -- The table to select the data from.

COMMIT;
```
