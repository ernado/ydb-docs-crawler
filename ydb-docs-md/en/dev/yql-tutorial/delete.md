---
title: "Deleting data"
url: "https://ydb.tech/docs/en/dev/yql-tutorial/delete?version=v26.1"
doc_path: "en/dev/yql-tutorial/delete"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/yql-tutorial/delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/yql-tutorial/delete.md"
description: "Delete data from the table using DELETE. Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Deleting data

Delete data from the table using [DELETE](../../yql/reference/syntax/delete.md).

> [!NOTE]
> We assume that you already created tables in step [Creating a table](create_demo_tables.md) and populated them with data in step [Adding data to a table](fill_tables_with_data.md).

```yql
DELETE
FROM episodes
WHERE
    series_id = 2
    AND season_id = 5
    AND episode_id = 12
;

COMMIT;

-- View result:
SELECT * FROM episodes WHERE series_id = 2 AND season_id = 5;

-- YDB doesn't see changes that take place at the start of the transaction,
-- which is why it first performs a read. It is impossible to execute UPDATE or DELETE on
-- if the table was changed within the current transaction. UPDATE ON and
-- DELETE ON let you read, update, and delete multiple rows from one table
-- within a single transaction.

$to_delete = (
    SELECT series_id, season_id, episode_id
    FROM episodes
    WHERE series_id = 1 AND season_id = 1 AND episode_id = 2
);

SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;

DELETE FROM episodes ON
SELECT * FROM $to_delete;

COMMIT;

-- View result:
SELECT * FROM episodes WHERE series_id = 1 AND season_id = 1;

COMMIT;
```
