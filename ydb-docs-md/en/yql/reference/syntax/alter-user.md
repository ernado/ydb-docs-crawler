---
title: "ALTER USER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-user?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-user"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-user.md"
description: "Changes the user password. Syntax. ALTER USER user_name [ WITH ] option [... ]. user_name: The name of the user. option — The command option:"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# ALTER USER

Changes the user password.

## Syntax

```yql
ALTER USER user_name [ WITH ] option [ ... ]
```

- `user_name`: The name of the user.

- `option` — The command option:

  - `PASSWORD 'password'` — changes the password to `password`.
  - `PASSWORD NULL` — sets an empty password.
  - `NOLOGIN` - disallows user login (user lockout).
  - `LOGIN` - allows user login (user unlocking).
