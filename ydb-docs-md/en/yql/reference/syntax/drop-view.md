---
title: "DROP VIEW"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-view?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-view"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-view.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-view.md"
description: "DROP VIEW deletes an existing view. Syntax. DROP VIEW [ IF EXISTS ] <name>. Parameters."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP VIEW

`DROP VIEW` deletes an existing [view](../../../concepts/datamodel/view.md).

## Syntax

```yql
DROP VIEW [IF EXISTS] <name>
```

### Parameters

- `IF EXISTS` - when specified, the statement does not return an error if a view with the given name does not exist.
- `name` - the name of the view to be deleted.

## Examples

The following command will drop the view named `recent_series`:

```yql
DROP VIEW recent_series;
```

## See also

- [CREATE VIEW](create-view.md)
- [ALTER VIEW](alter-view.md)
