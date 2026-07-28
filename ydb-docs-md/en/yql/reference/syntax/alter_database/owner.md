---
title: "Change database owner"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_database/owner?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_database/owner"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_database/owner.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_database/owner.md"
description: "Changes the database owner. Only a database administrator can perform this operation. Syntax. ALTER DATABASE path OWNER TO user_name; Parameters."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Change database owner

Changes the database owner. Only a database administrator can perform this operation.

## Syntax

```yql
ALTER DATABASE path OWNER TO user_name;
```

### Parameters

- `path` — path to the database;
- `user_name` — name of the user who will become the database owner.

## Examples

Make user `user1` the owner of database `/Root/test`:

```yql
ALTER DATABASE `/Root/test` OWNER TO user1;
```
