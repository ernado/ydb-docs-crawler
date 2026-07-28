---
title: "ALTER TABLE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/index.md"
description: "Using the ALTER TABLE command, you can modify the columns and additional parameters of row and column tables. Multiple actions can be specified in a single comm"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER TABLE

Using the `ALTER TABLE` command, you can modify the columns and additional parameters of row and column tables. Multiple actions can be specified in a single command. Generally, the `ALTER TABLE` command looks like this:

```yql
ALTER TABLE table_name action1, action2, ..., actionN;
```

An action is any modification to the table, as described below:

- [Renaming the table](alter_table/rename.md).
- Managing [columns](alter_table/columns.md) of row and column tables.
- Adding or removing a [changefeed](alter_table/changefeed.md).
- Managing [indexes](alter_table/indexes.md).
- Managing [column groups](alter_table/family.md) of a row table.
- Modifying [additional table](alter_table/set.md) parameters.
