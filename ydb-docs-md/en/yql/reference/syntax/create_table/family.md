---
title: "Column groups"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create_table/family?version=v26.1"
doc_path: "en/yql/reference/syntax/create_table/family"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create_table/family.md"
description: "Columns of the same table can be grouped to set the following parameters:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Column groups

Columns of the same table can be grouped to set the following parameters:

- `DATA`: A storage device type for the data in this column group. Acceptable values: `ssd`, `rot`.

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables.

- `COMPRESSION`: A data compression codec. Acceptable values: `off`, `lz4`, `zstd`.

> [!WARNING]
> Codec `"zstd"` is supported only for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.

- `COMPRESSION_LEVEL` — compression level of codec if it supports different compression levels.

> [!WARNING]
> Supported only for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables.

By default, all columns are in the same group named `default`. If necessary, the parameters of this group can also be redefined, if they are not redefined, then predefined values are applied.

## Example

In the example below, for the created table, the `family_large` group of columns is added and set for the `series_info` column, and the parameters for the default group, which is set by `default` for all other columns, are also redefined.

{% list tabs %}

- Creating a row-oriented table

  ```sql
  CREATE TABLE series_with_families (
      series_id Uint64,
      title Utf8,
      series_info Utf8 FAMILY family_large,
      release_date Uint64,
      PRIMARY KEY (series_id),
      FAMILY default (
          DATA = "ssd",
          COMPRESSION = "off"
      ),
      FAMILY family_large (
          DATA = "rot",
          COMPRESSION = "lz4"
      )
  );
  ```

- Creating a column-oriented table

  ```sql
  CREATE TABLE series_with_families (
      series_id Uint64 NOT NULL,
      title Utf8,
      series_info Utf8 FAMILY family_large,
      release_date Uint64,
      PRIMARY KEY (series_id),
      FAMILY default (
          COMPRESSION = "lz4"
      ),
      FAMILY family_large (
          COMPRESSION = "zstd",
          COMPRESSION_LEVEL = 5
      )
  )
  WITH (STORE = COLUMN);
  ```

{% endlist %}

> [!NOTE]
> Available types of storage devices depend on the YDB cluster configuration.
