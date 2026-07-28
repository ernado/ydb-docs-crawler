---
title: "Selecting data from specific columns"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/select_specific_columns?version=v26.1"
doc_path: "en/dev/yql-tutorial/select_specific_columns"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/select_specific_columns.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/select_specific_columns.md"
description: "Select the data from the columns series_id, release_date, and title. At the same time, rename title to series_title and cast the type of release_date from Uint3"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Selecting data from specific columns

Select the data from the columns `series_id`, `release_date`, and `title`. At the same time, rename `title` to `series_title` and cast the type of `release_date` from `Uint32` to `Date`.

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
SELECT
    series_id,             -- The names of columns (series_id, release_date, title)
                           -- are separated by commas.

    title AS series_title, -- You can use AS to rename columns
                           -- or give a name to an arbitrary expression

    CAST(release_date AS Date) AS release_date

FROM series;

COMMIT;
```
