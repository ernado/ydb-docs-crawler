---
title: "Sorting and filtering"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/basic_filter_and_sort?version=v26.1"
doc_path: "en/dev/yql-tutorial/basic_filter_and_sort"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/basic_filter_and_sort.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/basic_filter_and_sort.md"
description: "Select the first three episodes from every season of \"IT Crowd\", except the first season. Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Sorting and filtering

Select the first three episodes from every season of "IT Crowd", except the first season.

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
SELECT
   series_id,
   season_id,
   episode_id,
   CAST(air_date AS Date) AS air_date,
   title

FROM episodes
WHERE
   series_id = 1      -- List of conditions to build the result
   AND season_id > 1  -- Logical AND is used for complex conditions

ORDER BY              -- Sorting the results.
   series_id,         -- ORDER BY sorts the values by one or multiple
   season_id,         -- columns. Columns are separated by commas.
   episode_id

LIMIT 3               -- LIMIT N after ORDER BY means
                      -- "get top N" or "get bottom N" results,
;                     -- depending on sort order.

COMMIT;
```
