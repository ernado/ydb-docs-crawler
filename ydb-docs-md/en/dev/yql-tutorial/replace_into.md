---
title: "Inserting and updating data with REPLACE"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/replace_into?version=v26.1"
doc_path: "en/dev/yql-tutorial/replace_into"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/replace_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/replace_into.md"
description: "Add data to the table using REPLACE INTO: Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Inserting and updating data with REPLACE

Add data to the table using [REPLACE INTO](../../yql/reference/syntax/replace_into.md):

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
REPLACE INTO episodes
(
    series_id,
    season_id,
    episode_id,
    title,
    air_date
)
VALUES
(
    2,
    5,
    12,
    "Test Episode !!!",
    CAST(Date("2018-08-27") AS Uint64)
)
;

-- COMMIT is called so that the next SELECT operation
-- can see the changes made by the previous transaction.
COMMIT;

-- View result:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;

COMMIT;
```
