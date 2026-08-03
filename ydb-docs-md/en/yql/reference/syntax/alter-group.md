---
title: "ALTER GROUP"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-group?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-group"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-group.md"
description: "Adds/removes the group to/from a specific user. You can list multiple users under one operator. Syntax:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER GROUP

Adds/removes the group to/from a specific user. You can list multiple users under one operator.

Syntax:

```yql
ALTER GROUP role_name ADD USER user_name [, ... ]
ALTER GROUP role_name DROP USER user_name [, ... ]
```

- `role_name`: The name of the group.
- `user_name`: The name of the user.

## Built-in groups {#builtin}

The YDB cluster has built-in groups providing predefined role sets:

| Group | Description |
| --- | --- |
| `ADMINS` | Unlimited rights over the entire cluster schema |
| `DATABASE-ADMINS` | Rights to create and delete databases (`CreateDatabase`, `DropDatabase`) |
| `ACCESS-ADMINS` | Rights to manage other users' permissions (`GrantAccessRights`) |
| `DDL-ADMINS` | Rights to alter database schemas (`CreateDirectory`, `CreateTable`, `WriteAttributes`, `AlterSchema`, `RemoveSchema`) |
| `DATA-WRITERS` | Rights to modify data (`UpdateRow`, `EraseRow`) |
| `DATA-READERS` | Rights to read data (`SelectRow`) |
| `METADATA-READERS` | Rights to read metadata, without access to data (`DescribeSchema` and `ReadAttributes`) |
| `USERS` | Rights to connect to databases (`ConnectDatabase`) |

By default, all users are included in the `USERS` group, and the `root` user is included in the `ADMINS` group.

Below is a diagram demonstrating how groups inherit permissions from each other. For example, `DATA-WRITERS` includes all permissions of `DATA-READERS`:
