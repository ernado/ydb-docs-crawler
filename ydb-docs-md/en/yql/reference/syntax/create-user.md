---
title: "CREATE USER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-user?version=v26.1"
doc_path: "en/yql/reference/syntax/create-user"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-user.md"
description: "Creates a user with the specified name and password. Syntax: CREATE USER user_name [ option ]."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE USER

Creates a user with the specified name and password.

Syntax:

```yql
CREATE USER user_name [option]
```

- `user_name`: The name of the user. It may contain lowercase Latin letters and digits.

- `option` — command option:

  - `PASSWORD 'password'` — creates a user with the password `password`.
  - `PASSWORD NULL` — creates a user with an empty password (default).
  - `NOLOGIN` - disallows user login (user lockout).
  - `LOGIN` - allows user login (default).

> [!NOTE]
> The scope of the commands `CREATE USER`, `ALTER USER`, and `DROP USER` does not extend to external user directories. Keep this in mind if users with third-party authentication (e.g., LDAP) are connecting to YDB. For example, the `CREATE USER` command does not create a user in the LDAP directory. Learn more about [YDB's interaction with the LDAP directory](../../../security/authentication.md#ldap-auth-provider).
