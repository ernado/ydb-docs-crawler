---
title: "Animal Crossing New Horizons Catalog"
url: "https://ydb.tech/docs/en/analyst/datasets/animal-crossing?version=v26.1"
doc_path: "en/analyst/datasets/animal-crossing"
version: "v26.1"
lang: "en"
source_path: "en/core/analyst/datasets/animal-crossing.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/analyst/datasets/animal-crossing.md"
description: "Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Animal Crossing New Horizons Catalog

> [!NOTE]
> This page is part of the [Dataset Import](index.md) section, which includes examples of loading popular datasets into YDB. Before starting, please review the [general information](index.md#general-info) on requirements and the import process.

A catalog of items from the popular game Animal Crossing: New Horizons.

**Source**: [Kaggle - Animal Crossing New Horizons Catalog](https://www.kaggle.com/datasets/jessicali9530/animal-crossing-new-horizons-nookplaza-dataset/)

**Size**: 51 KB

## Loading Example

1. Download and unzip the `accessories.csv` file from Kaggle.

2. This file includes a BOM (Byte Order Mark). However, the import command does not support files with a BOM. To resolve this, remove the BOM bytes from the beginning of the file by executing the following command:

   ```bash
   sed -i '1s/^\xEF\xBB\xBF//' accessories.csv
   ```

3. The column names in the file contain spaces, which are incompatible with YDB since YDB does not support spaces in column names. Replace spaces in the column names with underscores, for example, by executing the following command:

   ```bash
   sed -i '1s/ /_/g' accessories.csv
   ```

4. Create a table in YDB using one of the following methods:

   {% list tabs %}

   - Embedded UI

     For more information on [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

     ```sql
     CREATE TABLE `accessories` (
         `Name` Text NOT NULL,
         `Variation` Text NOT NULL,
         `DIY` Text NOT NULL,
         `Buy` Text NOT NULL,
         `Sell` Uint64 NOT NULL,
         `Color_1` Text NOT NULL,
         `Color_2` Text NOT NULL,
         `Size` Text NOT NULL,
         `Miles_Price` Text NOT NULL,
         `Source` Text NOT NULL,
         `Source_Notes` Text NOT NULL,
         `Seasonal_Availability` Text NOT NULL,
         `Mannequin_Piece` Text NOT NULL,
         `Version` Text NOT NULL,
         `Style` Text NOT NULL,
         `Label_Themes` Text NOT NULL,
         `Type` Text NOT NULL,
         `Villager_Equippable` Text NOT NULL,
         `Catalog` Text NOT NULL,
         `Filename` Text NOT NULL,
         `Internal_ID` Uint64 NOT NULL,
         `Unique_Entry_ID` Text NOT NULL,
         PRIMARY KEY (`Unique_Entry_ID`)
     )
     WITH (
         STORE = COLUMN
     );
     ```

   - YDB CLI

     ```bash
     ydb sql -s \
     'CREATE TABLE `accessories` (
         `Name` Text NOT NULL,
         `Variation` Text NOT NULL,
         `DIY` Text NOT NULL,
         `Buy` Text NOT NULL,
         `Sell` Uint64 NOT NULL,
         `Color_1` Text NOT NULL,
         `Color_2` Text NOT NULL,
         `Size` Text NOT NULL,
         `Miles_Price` Text NOT NULL,
         `Source` Text NOT NULL,
         `Source_Notes` Text NOT NULL,
         `Seasonal_Availability` Text NOT NULL,
         `Mannequin_Piece` Text NOT NULL,
         `Version` Text NOT NULL,
         `Style` Text NOT NULL,
         `Label_Themes` Text NOT NULL,
         `Type` Text NOT NULL,
         `Villager_Equippable` Text NOT NULL,
         `Catalog` Text NOT NULL,
         `Filename` Text NOT NULL,
         `Internal_ID` Uint64 NOT NULL,
         `Unique_Entry_ID` Text NOT NULL,
         PRIMARY KEY (`Unique_Entry_ID`)
     )
     WITH (
         STORE = COLUMN
     );'
     ```

   {% endlist %}

5. Execute the import command:

   ```bash
   ydb import file csv --header --path accessories accessories.csv
   ```

## Analytical Query Example

Identify the top five most popular primary colors of accessories:

{% list tabs %}

- Embedded UI

  ```sql
  SELECT
      Color_1,
      COUNT(*) AS color_count
  FROM accessories
  GROUP BY Color_1
  ORDER BY color_count DESC
  LIMIT 5;
  ```

- YDB CLI

  ```bash
  ydb sql -s \
  'SELECT
      Color_1,
      COUNT(*) AS color_count
  FROM accessories
  GROUP BY Color_1
  ORDER BY color_count DESC
  LIMIT 5;'
  ```

{% endlist %}

Result:

```
┌──────────┬─────────────┐
│ Color_1  │ color_count │
├──────────┼─────────────┤
│ "Black"  │ 31          │
├──────────┼─────────────┤
│ "Green"  │ 27          │
├──────────┼─────────────┤
│ "Pink"   │ 20          │
├──────────┼─────────────┤
│ "Red"    │ 20          │
├──────────┼─────────────┤
│ "Yellow" │ 19          │
└──────────┴─────────────┘
```
