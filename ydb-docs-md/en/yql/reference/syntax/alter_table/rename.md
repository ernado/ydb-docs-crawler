---
title: "Renaming a table"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/rename?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/rename"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/rename.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/rename.md"
description: "ALTER TABLE old_table_name RENAME TO new_table_name; Note. When choosing a name for the table, consider the common schema object naming rules."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Renaming a table

```yql
ALTER TABLE old_table_name RENAME TO new_table_name;
```

> [!NOTE]
> When choosing a name for the table, consider the common [schema object naming rules](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

If a table with the new name already exists, an error will be returned. The ability to transactionally replace a table under load is supported by specialized methods in CLI and SDK.

> [!WARNING]
> If a YQL query contains multiple `ALTER TABLE ... RENAME TO ...` commands, each will be executed in auto-commit mode in a separate transaction. From the perspective of an external process, the tables will be renamed sequentially, one after another. To rename multiple tables in a single transaction, use specialized methods available in CLI and SDK.

Renaming can be used to move a table from one directory within the database to another, for example:

```yql
ALTER TABLE `table1` RENAME TO `/backup/table1`;
```
