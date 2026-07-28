---
title: "ALTER VIEW"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-view?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-view"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-view.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-view.md"
description: "ALTER VIEW changes the definition of a view. Warning. This feature is not supported yet."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER VIEW

`ALTER VIEW` changes the definition of a [view](../../../concepts/datamodel/view.md).

> [!WARNING]
> This feature is not supported yet.

Instead, you can redefine a view by dropping it and recreating it with a different query or options:

```yql
DROP VIEW redefined_view;
CREATE VIEW redefined_view ...;
```

Please note that the two statements are executed separately, unlike a single `ALTER VIEW` statement. If a view is recreated in this way, it might be possible to observe the view in a deleted state for a brief moment.

## See also

- [CREATE VIEW](create-view.md)
- [DROP VIEW](drop-view.md)
