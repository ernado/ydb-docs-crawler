---
title: "Column groups"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create_table/family?version=v26.1"
doc_path: "en/yql/reference/syntax/create_table/family"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create_table/family.md"
description: "Warning. Supported only for row-oriented tables. Columns of the same table can be grouped to set the following parameters:"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# Column groups

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables.

Columns of the same table can be grouped to set the following parameters:

- `DATA`: A storage device type for the data in this column group. Acceptable values: `"ssd"`, `"rot"`.
- `COMPRESSION`: A data compression codec. Acceptable values: `"off"`, `"lz4"`.
- `CACHE_MODE`: [Caching mode](../../../../concepts/datamodel/table.md#cache-modes). Acceptable values: `"in_memory"`, `"regular"`.

By default, all columns are in the same group named `default`. If necessary, the parameters of this group can also be redefined, if they are not redefined, then predefined values are applied.

## Example

In the example below, for the created table, the `family_large` group of columns is added and set for the `series_info` column, and the parameters for the default group, which is set by `default` for all other columns, are also redefined.

```yql
CREATE TABLE series_with_families (
    series_id Uint64,
    title Utf8,
    series_info Utf8 FAMILY family_large,
    release_date Uint64,
    PRIMARY KEY (series_id),
    FAMILY default (
        DATA = "ssd",
        COMPRESSION = "off",
        CACHE_MODE = "in_memory"
    ),
    FAMILY family_large (
        DATA = "rot",
        COMPRESSION = "lz4",
        CACHE_MODE = "regular"
    )
);
```

> [!NOTE]
> Available types of storage devices depend on the YDB cluster configuration.
