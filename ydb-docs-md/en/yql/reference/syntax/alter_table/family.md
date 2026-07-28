---
title: "Changing column groups"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/family?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/family"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/family.md"
description: "Warning. Supported only for row-oriented tables."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Changing column groups

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables.

The mechanism of [column groups](../../../../concepts/datamodel/table.md#column-groups) allows for improved performance of partial row read operations by dividing the storage of table columns into several groups. The most commonly used scenario is to organize the storage of infrequently used attributes into a separate column group.

## Creating column groups

`ADD FAMILY`: Creates a new group of columns in the table. The code below creates the `family_small` column group in the `series_with_families` table.

```yql
ALTER TABLE series_with_families ADD FAMILY family_small (
    DATA = "ssd",
    COMPRESSION = "off"
);
```

## Modifying column groups {#mod-column-groups}

Using the `ALTER COLUMN` command, you can change a column group for the specified column. The code below for the `release_date` column in the `series_with_families` table changes the column group to `family_small`.

```sql
ALTER TABLE series_with_families ALTER COLUMN release_date SET FAMILY family_small;
```

The two previous commands from listings 8 and 9 can be combined into one `ALTER TABLE` call. The code below creates the `family_small` column group and sets it for the `release_date` column in the `series_with_families` table.

```yql
ALTER TABLE series_with_families
    ADD FAMILY family_small (
        DATA = "ssd",
        COMPRESSION = "off"
    ),
    ALTER COLUMN release_date SET FAMILY family_small;
```

Using the `ALTER FAMILY` command, you can change the parameters of the column group.

### Changing storage type

The code below changes the storage type to `rot` for the `default` column group in the `series_with_families` table:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET DATA "rot";
```

> [!NOTE]
> Available types of storage devices depend on the YDB cluster configuration.

### Changing compression codec

The code below changes the compression codec to `lz4` for the `default` column group in the `series_with_families` table:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET COMPRESSION "lz4";
```

### Changing cache mode

When switching the cache mode to `in_memory` for an existing table with `ALTER TABLE`, the pages that are not yet in memory are loaded automatically.

If the table was previously in `in_memory` mode and `ALTER TABLE` then sets the cache mode to `regular`, the pages that are already in memory stay there, but they may later be evicted according to the general caching policy.

The code below changes the [cache mode](../../../../concepts/datamodel/table.md#cache-modes) to `in_memory` for the `default` column group in the `series_with_families` table:

```yql
ALTER TABLE series_with_families ALTER FAMILY default SET CACHE_MODE "in_memory";
```

You can specify any column group parameters described in the [`CREATE TABLE`](../create_table/index.md) command.
