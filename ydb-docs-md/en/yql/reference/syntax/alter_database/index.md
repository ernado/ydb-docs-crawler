---
title: "ALTER DATABASE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_database/?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_database/"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_database/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_database/index.md"
description: "Changes database settings. Syntax. ALTER DATABASE path action; Parameters. path — path to the database;"
revision: "610144200e326713a5926ef40527cb973f94a519"
---

# ALTER DATABASE

Changes database settings.

## Syntax

```yql
ALTER DATABASE path action;
```

### Parameters

- `path` — path to the database;

- `action` — any of the database modification actions described below:

  - [Change database owner](owner.md).
  - [Change database settings](settings.md).
