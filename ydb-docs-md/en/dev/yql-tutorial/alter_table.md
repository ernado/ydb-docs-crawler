---
title: "Adding and deleting columns"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/alter_table?version=v26.1"
doc_path: "en/dev/yql-tutorial/alter_table"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/alter_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/alter_table.md"
description: "Add a new column to the table and then delete it. Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Adding and deleting columns

Add a new column to the table and then delete it.

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

## Adding a column {#add-column}

Add a non-key column to the existing table:

```yql
ALTER TABLE episodes ADD COLUMN viewers Uint64;
```

## Deleting a column {#delete-column}

Delete the column you added from the table:

```yql
ALTER TABLE episodes DROP COLUMN viewers;
```
