---
title: "Modifying additional table parameters"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/set?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/set"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/set.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/set.md"
description: "Most parameters of row and column tables in YDB, listed on the table description page, can be modified using the ALTER command."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Modifying additional table parameters

Most parameters of row and column tables in YDB, listed on the [table description](../../../../concepts/datamodel/table.md) page, can be modified using the `ALTER` command.

Generally, the command to modify any table parameter looks as follows:

```sql
ALTER TABLE table_name SET (key = value);
```

`key` — the name of the parameter, `value` — its new value.

Example of modifying the `TTL` parameter, which controls the time-to-live of records in a table:

```sql
ALTER TABLE series SET (TTL = Interval("PT0S") ON expire_at);
```

## Resetting Additional Table Parameters {#additional-reset}

Some table parameters in YDB, listed on the [table description](../../../../concepts/datamodel/table.md) page, can be reset using the `ALTER` command. The command to reset a table parameter looks as follows:

```sql
ALTER TABLE table_name RESET (key);
```

`key` — the name of the parameter.

For example, such a command will reset (remove) the `TTL` settings for row or column tables:

```sql
ALTER TABLE series RESET (TTL);
```
