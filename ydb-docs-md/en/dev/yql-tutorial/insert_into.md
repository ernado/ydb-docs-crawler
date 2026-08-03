---
title: "Inserting data with INSERT"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/insert_into?version=v26.1"
doc_path: "en/dev/yql-tutorial/insert_into"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/insert_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/insert_into.md"
description: "Add data to the table using INSERT INTO: Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Inserting data with INSERT

Add data to the table using [INSERT INTO](../../yql/reference/syntax/insert_into.md):

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
INSERT INTO episodes
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
    21,
    "Test 21",
    CAST(Date("2018-08-27") AS Uint64)
),                                        -- Rows are separated by commas.
(
    2,
    5,
    22,
    "Test 22",
    CAST(Date("2018-08-27") AS Uint64)
)
;

COMMIT;

-- View result:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;

COMMIT;
```
