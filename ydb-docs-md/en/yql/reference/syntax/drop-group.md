---
title: "DROP GROUP"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-group?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-group"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-group.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-group.md"
description: "Deletes the specified group. You can list multiple groups under one operator. Syntax: DROP GROUP [ IF EXISTS ] group_name [,...]."
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# DROP GROUP

Deletes the specified group. You can list multiple groups under one operator.

Syntax:

```yql
DROP GROUP [ IF EXISTS ] group_name [, ...]
```

- `IF EXISTS`: Suppress an error if the group doesn't exist.
- `group_name`: The name of the group to be deleted.
