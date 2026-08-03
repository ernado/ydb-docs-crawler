---
title: "Paginated output"
url: "https://ydb.tech/docs/en/dev/paging?version=v26.1"
doc_path: "en/dev/paging"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/paging.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/paging.md"
description: "This section provides recommendations for organizing paginated data output."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Paginated output

This section provides recommendations for organizing paginated data output.

To organize paginated output, we recommend selecting data sorted by primary key sequentially, limiting the number of rows with the LIMIT keyword.

> [!NOTE]
> `$lastCity, $lastNumber`: Primary key values obtained from the previous query.

A query demonstrating the recommended way to organize paginated output:

```yql
--  Table `schools`:
-- ┌─────────┬─────────┬─────┐
-- | Name    | Type    | Key |
-- ├─────────┼─────────┼─────┤
-- | city    | Utf8?   | K0  |
-- | number  | Uint32? | K1  |
-- | address | Utf8?   |     |
-- └─────────┴─────────┴─────┘

DECLARE $limit AS Uint64;
DECLARE $lastCity AS Utf8;
DECLARE $lastNumber AS Uint32;

SELECT * FROM schools
WHERE (city, number) > ($lastCity, $lastNumber)
ORDER BY city, number
LIMIT $limit;
```

In the query example shown above, the `WHERE` clause uses a tuple comparison to select the next set of rows. Tuples are compared element by element from left to right, so the order of the fields in the tuple must match the order of the fields in the primary key to avoid table full scan.

> [!WARNING]
> **NULL value in key column**
>
> In YDB, all columns, including key ones, may have a NULL value. Despite this, using `NULL` as key column values is highly discouraged, since the SQL standard doesn't allow `NULL` to be compared. As a result, concise SQL statements with simple comparison operators won't work correctly. Instead, you'll have to use cumbersome statements with `IS NULL`/`IS NOT NULL` expressions.

## Examples of paginated output implementation

- [C++](https://github.com/ydb-platform/ydb/tree/main/ydb/public/sdk/cpp/examples/pagination)
- [Java](https://github.com/ydb-platform/ydb-java-examples/tree/master/ydb-cookbook/src/main/java/tech/ydb/examples/pagination)
- [Python](https://github.com/ydb-platform/ydb-python-sdk/tree/main/examples/pagination)
- [Go](https://github.com/ydb-platform/ydb-go-examples/tree/master/pagination)
