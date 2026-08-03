---
title: "Change database settings"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_database/settings?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_database/settings"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_database/settings.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_database/settings.md"
description: "Changes database settings. Only a database administrator can perform this operation. Syntax. ALTER DATABASE path SET ( key = value,...). Parameters."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Change database settings

Changes database settings. Only a database administrator can perform this operation.

## Syntax

```yql
ALTER DATABASE path SET (key = value, ...)
```

### Parameters

- `path` — path to the database.

- `key` — name of the setting to change:

  - `MAX_PATHS` — [maximum number of paths](../../../../concepts/limits-ydb.md#schema-object) (schema objects) in the database.
  - `MAX_SHARDS` — [maximum number of tablets](../../../../concepts/limits-ydb.md#schema-object) in the database.
  - `MAX_CHILDREN_IN_DIR` — [maximum number of objects in a directory](../../../../concepts/limits-ydb.md#schema-object).
  - `MAX_SHARDS_IN_PATH` — [maximum number of tablets associated with a single schema object](../../../../concepts/limits-ydb.md#schema-object). For example, the maximum number of partitions of one table.

- `value` — new value for the setting.

## Examples

Change the limit on the maximum number of paths (schema objects) for database `/Root/test`:

```yql
ALTER DATABASE `/Root/test` SET (MAX_PATHS = 20000);
```
