---
title: "Joining tables with JOIN"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/join_tables?version=v26.1"
doc_path: "en/dev/yql-tutorial/join_tables"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/join_tables.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/join_tables.md"
description: "Merge the columns of the source tables seasons and series, then output all the seasons of the IT Crowd series to the resulting table using the JOIN operator."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Joining tables with JOIN

Merge the columns of the source tables `seasons` and `series`, then output all the seasons of the IT Crowd series to the resulting table using the [JOIN](../../yql/reference/syntax/select/join.md) operator.

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
SELECT
    sa.title AS season_title,    -- sa and sr are "join names",
    sr.title AS series_title,    -- table aliases declared below using AS.
    sr.series_id,                -- They are used to avoid
    sa.season_id                 -- ambiguity in the column names used.

FROM
    seasons AS sa
INNER JOIN
    series AS sr
ON sa.series_id = sr.series_id
WHERE sa.series_id = 1
ORDER BY                         -- Sorting of the results.
    sr.series_id,
    sa.season_id                 -- ORDER BY sorts the values by one column
;                                -- or multiple columns.
                                 -- Columns are separated by commas.

COMMIT;
```
