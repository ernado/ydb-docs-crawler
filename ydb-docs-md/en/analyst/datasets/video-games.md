---
title: "Video Game Sales"
url: "https://ydb.tech/docs/en/analyst/datasets/video-games?version=v26.1"
doc_path: "en/analyst/datasets/video-games"
version: "v26.1"
lang: "en"
source_path: "en/core/analyst/datasets/video-games.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/analyst/datasets/video-games.md"
description: "Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Video Game Sales

> [!NOTE]
> This page is part of the [Dataset Import](index.md) section, which includes examples of loading popular datasets into YDB. Before starting, please review the [general information](index.md#general-info) on requirements and the import process.

Data on video game sales.

**Source**: [Kaggle - Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)

**Size**: 1.36 MB

## Loading Example

1. Download and unzip the `vgsales.csv` file from Kaggle.

2. Create a table in YDB using one of the following methods:

   {% list tabs %}

   - Embedded UI

     For more information on [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

     ```sql
     CREATE TABLE `vgsales` (
         `Rank` Uint64 NOT NULL,
         `Name` Text NOT NULL,
         `Platform` Text NOT NULL,
         `Year` Text NOT NULL,
         `Genre` Text NOT NULL,
         `Publisher` Text NOT NULL,
         `NA_Sales` Double NOT NULL,
         `EU_Sales` Double NOT NULL,
         `JP_Sales` Double NOT NULL,
         `Other_Sales` Double NOT NULL,
         `Global_Sales` Double NOT NULL,
         PRIMARY KEY (`Rank`)
     )
     WITH (
         STORE = COLUMN
     );
     ```

   - YDB CLI

     ```bash
     ydb sql -s \
     'CREATE TABLE `vgsales` (
         `Rank` Uint64 NOT NULL,
         `Name` Text NOT NULL,
         `Platform` Text NOT NULL,
         `Year` Text NOT NULL,
         `Genre` Text NOT NULL,
         `Publisher` Text NOT NULL,
         `NA_Sales` Double NOT NULL,
         `EU_Sales` Double NOT NULL,
         `JP_Sales` Double NOT NULL,
         `Other_Sales` Double NOT NULL,
         `Global_Sales` Double NOT NULL,
         PRIMARY KEY (`Rank`)
     )
     WITH (
         STORE = COLUMN
     );'
     ```

   {% endlist %}

3. Execute the import command:

   ```bash
   ydb import file csv --header --null-value "" --path vgsales vgsales.csv
   ```

## Analytical Query Example

To identify the publisher with the highest average game sales in North America, execute the query:

{% list tabs %}

- Embedded UI

  ```sql
  SELECT
      Publisher,
      AVG(NA_Sales) AS average_na_sales
  FROM vgsales
  GROUP BY Publisher
  ORDER BY average_na_sales DESC
  LIMIT 1;
  ```

- YDB CLI

  ```bash
  ydb sql -s \
  'SELECT
      Publisher,
      AVG(NA_Sales) AS average_na_sales
  FROM vgsales
  GROUP BY Publisher
  ORDER BY average_na_sales DESC
  LIMIT 1;'
  ```

{% endlist %}

Result:

```
┌───────────┬──────────────────┐
│ Publisher │ average_na_sales │
├───────────┼──────────────────┤
│ "Palcom"  │ 3.38             │
└───────────┴──────────────────┘
```

This query helps find the publisher with the greatest success in North America by average sales.
