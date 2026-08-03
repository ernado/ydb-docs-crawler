---
title: "Data aggregation"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/basic_aggregation?version=v26.1"
doc_path: "en/dev/yql-tutorial/basic_aggregation"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/basic_aggregation.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/basic_aggregation.md"
description: "Find out the number of unique episodes within every season of every series. Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Data aggregation

Find out the number of unique episodes within every season of every series.

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
SELECT
    series_id,
    season_id,
    COUNT(*) AS cnt  -- Aggregation function COUNT returns the number of rows
                     -- output by the query.
                     -- Asterisk (*) specifies that COUNT
                     -- counts the total number of rows in the table.
                     -- COUNT(*) returns the number of rows in
                     -- the specified table, preserving the duplicate rows.
                     -- It counts each row separately.
                     -- The result includes rows that contain null values.
FROM episodes

GROUP BY
    series_id,       -- The query result will follow the listed order of columns.
    season_id        -- Multiple columns are separated by a comma.
                     -- Other columns can be listed after a SELECT only if
                     -- they are passed to an aggregate function.
ORDER BY
    series_id,
    season_id
;

COMMIT;
```
