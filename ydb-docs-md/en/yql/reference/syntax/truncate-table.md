---
title: "TRUNCATE TABLE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/truncate-table?version=v26.1"
doc_path: "en/yql/reference/syntax/truncate-table"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/truncate-table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/truncate-table.md"
description: "TRUNCATE TABLE removes all user data from the specified table and its indexes. Syntax. TRUNCATE TABLE <table_name>; Limitations."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# TRUNCATE TABLE

`TRUNCATE TABLE` removes all user data from the specified table and its indexes.

## Syntax

```yql
TRUNCATE TABLE <table_name>;
```

## Limitations

- Supported only for [row-oriented tables](../../../concepts/glossary.md#row-oriented-table).

- While the operation runs, the table is locked for reads and writes.

- The operation cannot be interrupted or canceled after it has started.

- The operation cannot be performed if the table has:

  - an [asynchronous secondary index](../../../concepts/query_execution/secondary_indexes.md#async),
  - a [changefeed](alter_table/changefeed.md),
  - [asynchronous replication](../../../concepts/async-replication.md).

## Examples

Removes all data from the table with the full path `/Root/test/my_table`.

```yql
TRUNCATE TABLE `/Root/test/my_table`;
```

Removes all data from table `my_table` in the current database.

```yql
TRUNCATE TABLE `my_table`;
```

## See also

- [CREATE TABLE](create_table/index.md)
- [ALTER TABLE](alter_table/index.md)
- [DROP TABLE](drop_table.md)
