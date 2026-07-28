---
title: "VIEW (INDEX)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/secondary_index?version=v26.1"
doc_path: "en/yql/reference/syntax/select/secondary_index"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/secondary_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/secondary_index.md"
description: "To make a SELECT by secondary index of row-oriented table statement, use the following: SELECT * FROM TableName VIEW IndexName WHERE …. Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# VIEW (INDEX)

To make a `SELECT` by secondary index of row-oriented table statement, use the following:

```yql
SELECT *
    FROM TableName VIEW IndexName
    WHERE …
```

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

## Examples

- Select all the fields from the `series` row-oriented table using the `views_index` index with the `views >=someValue` criteria:

  ```yql
  SELECT series_id, title, info, release_date, views, uploaded_user_id
      FROM series VIEW views_index
      WHERE views >= someValue
  ```

- [`JOIN`](join.md) the `series` and `users` row-oriented tables on the `userName` field using the `users_index` and `name_index` indexes, respectively:

  ```yql
  SELECT t1.series_id, t1.title
      FROM series VIEW users_index AS t1
      INNER JOIN users VIEW name_index AS t2
      ON t1.uploaded_user_id == t2.user_id
      WHERE t2.name == userName;
  ```
