---
title: "GRANT"
url: "https://ydb.tech/docs/en/yql/reference/syntax/grant?version=v26.1"
doc_path: "en/yql/reference/syntax/grant"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/grant.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/grant.md"
description: "The GRANT command allows setting access rights to schema objects for a user or group of users. Syntax:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# GRANT

The `GRANT` command allows setting access rights to schema objects for a user or group of users.

Syntax:

```yql
GRANT {{permission_name} [, ...] | ALL [PRIVILEGES]} ON {path_to_scheme_object [, ...]} TO {role_name [, ...]} [WITH GRANT OPTION]
```

- `permission_name` - the name of the access right to schema objects that needs to be assigned.
- `path_to_scheme_object` - the path to the schema object to which rights are granted.
- `role_name` - the name of the user or group for which rights to the schema object are granted.

`WITH GRANT OPTION` - using this clause gives the user or group the right to manage access rights - to grant or revoke specific rights. The clause functions similarly to granting the `"ydb.access.grant"` right or `GRANT`.  
 A subject with the `ydb.access.grant` right cannot grant rights broader than they themselves have on the access object `path_to_scheme_object`.

## Access rights {#permissions-list}

As names of access rights, you can use either the names of YDB rights or the corresponding YQL keywords.  
 The possible names of rights are listed in the table below.

| YDB right | YQL keyword | Description |
| --- | --- | --- |
| **Database-level rights** |  |  |
| `ydb.database.connect` | `CONNECT` | The right to connect to a database |
| `ydb.database.create` | `CREATE` | The right to create new databases in the cluster |
| `ydb.database.drop` | `DROP` | The right to delete databases in the cluster |
| **Elementary rights for database objects** |  |  |
| `ydb.granular.select_row` | `SELECT ROW` | The right to read rows from a table (select), read messages from topics, use secret values |
| `ydb.granular.update_row` | `UPDATE ROW` | The right to update rows in a table (insert, update, upsert, replace), write messages to topics |
| `ydb.granular.erase_row` | `ERASE ROW` | The right to delete rows from a table (delete) |
| `ydb.granular.create_directory` | `CREATE DIRECTORY` | The right to create and delete directories, including existing and nested ones |
| `ydb.granular.create_table` | `CREATE TABLE` | The right to create tables (including index, external, columnar), views, sequences |
| `ydb.granular.create_queue` | `CREATE QUEUE` | The right to create topics |
| `ydb.granular.remove_schema` | `REMOVE SCHEMA` | The right to delete objects (directories, tables, topics) that were created using rights |
| `ydb.granular.describe_schema` | `DESCRIBE SCHEMA` | The right to view existing access rights (ACL) on an access object, view descriptions of access objects (directories, tables, topics) |
| `ydb.granular.alter_schema` | `ALTER SCHEMA` | The right to modify access objects (directories, tables, topics), including users' rights to access objects |
| **Additional flags** |  |  |
| `ydb.access.grant` | `GRANT` | The right to grant or revoke rights from other users to the extent not exceeding the current scope of the user's rights on the access object |
| `ydb.tables.modify` | `MODIFY TABLES` | `ydb.granular.update_row` + `ydb.granular.erase_row` |
| `ydb.tables.read` | `SELECT TABLES` | Alias for `ydb.granular.select_row` |
| `ydb.generic.list` | `LIST` | Alias for `ydb.granular.describe_schema` |
| `ydb.generic.read` | `SELECT` | `ydb.granular.select_row` + `ydb.generic.list` |
| `ydb.generic.write` | `INSERT` | `ydb.granular.update_row` + `ydb.granular.erase_row` + `ydb.granular.create_directory` + `ydb.granular.create_table` + `ydb.granular.create_queue` + `ydb.granular.remove_schema` + `ydb.granular.alter_schema` |
| `ydb.generic.use_legacy` | `USE LEGACY` | `ydb.generic.read` + `ydb.generic.write` + `ydb.access.grant` |
| `ydb.generic.use` | `USE` | `ydb.generic.use_legacy` + `ydb.database.connect` |
| `ydb.generic.manage` | `MANAGE` | `ydb.database.create` + `ydb.database.drop` |
| `ydb.generic.full_legacy` | `FULL LEGACY` | `ydb.generic.use_legacy` + `ydb.generic.manage` |
| `ydb.generic.full` | `FULL` | `ydb.generic.use` + `ydb.generic.manage` |

- `ALL [PRIVILEGES]` is used to specify all possible rights on schema objects for users or groups. `PRIVILEGES` is an optional keyword needed for compatibility with the SQL standard.

> [!NOTE]
> Rights `ydb.database.connect`, `ydb.granular.describe_schema`, `ydb.granular.select_row`, and `ydb.granular.update_row` should be considered as layers of rights.
>
> For example, to update rows, you need not only the right `ydb.granular.update_row`, but also all the overlying rights.

## Examples

- Assign the `ydb.generic.read` right to the table `/shop_db/orders` for the user `user1`:

  ```yql
  GRANT 'ydb.generic.read' ON `/shop_db/orders` TO user1;
  ```

  The same command, using the keyword:

  ```yql
  GRANT SELECT ON `/shop_db/orders` TO user1;
  ```

- Assign the rights `ydb.database.connect` and `ydb.generic.list` to the root of the database `/shop_db` for user `user2` and group `group1`:

  ```yql
  GRANT LIST, CONNECT ON `/shop_db` TO user2, group1;
  ```

- Assign the `ydb.generic.use` right to the tables `/shop_db/orders` and `/shop_db/sellers` for users `user1@domain` and `user2@domain`:

  ```yql
  GRANT 'ydb.generic.use' ON `/shop_db/orders`, `/shop_db/sellers` TO `user1@domain`, `user2@domain`;
  ```

- Grant all rights to the table `/shop_db/sellers` for the user `admin_user`:

  ```yql
  GRANT ALL ON `/shop_db/sellers` TO admin_user;
  ```
