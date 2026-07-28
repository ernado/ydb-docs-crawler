---
title: "DROP USER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-user?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-user"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-user.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-user.md"
description: "Deletes the specified user. You can list multiple users under one operator. Syntax: DROP USER [ IF EXISTS ] user_name [,...]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP USER

Deletes the specified user. You can list multiple users under one operator.

Syntax:

```yql
DROP USER [ IF EXISTS ] user_name [, ...]
```

- `IF EXISTS`: Suppress an error if the user doesn't exist.
- `user_name`: The name of the user to be deleted. It also supports the ability to set a comma-separated list of users, for example: `DROP USER user1, user2, user3;`
