---
title: "Chess Position Evaluations"
url: "https://ydb.tech/docs/en/analyst/datasets/chess?version=v26.1"
doc_path: "en/analyst/datasets/chess"
version: "v26.1"
lang: "en"
source_path: "en/core/analyst/datasets/chess.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/analyst/datasets/chess.md"
description: "Note."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Chess Position Evaluations

> [!NOTE]
> This page is part of the [Dataset Import](index.md) section, which includes examples of loading popular datasets into YDB. Before starting, please review the [general information](index.md#general-info) on requirements and the import process.

The dataset includes 513 million chess position evaluations performed by the Stockfish engine for analysis on the Lichess platform.

**Source**: [Kaggle - Chess Position Evaluations](https://www.kaggle.com/datasets/lichess/chess-evaluations)

**Size**: 59.66 GB

## Loading Example

1. Download the `evals.csv` file from Kaggle.

2. Create a table in YDB using one of the following methods:

   {% list tabs %}

   - Embedded UI

     For more information on [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

     ```sql
     CREATE TABLE `evals` (
         `fen` Text NOT NULL,
         `line` Text NOT NULL,
         `depth` Uint64,
         `knodes` Uint64,
         `cp` Double,
         `mate` Double,
         PRIMARY KEY (`fen`, `line`)
     )
     WITH (
         STORE = COLUMN,
         UNIFORM_PARTITIONS = 50
     );
     ```

   - YDB CLI

     ```bash
     ydb sql -s \
     'CREATE TABLE `evals` (
         `fen` Text NOT NULL,
         `line` Text NOT NULL,
         `depth` Uint64,
         `knodes` Uint64,
         `cp` Double,
         `mate` Double,
         PRIMARY KEY (`fen`, `line`)
     )
     WITH (
         STORE = COLUMN,
         UNIFORM_PARTITIONS = 50
     );'
     ```

   {% endlist %}

3. Execute the import command:

   ```bash
   ydb import file csv --header --null-value "" --path evals evals.csv
   ```

## Analytical Query Example

Identify positions with the highest number of moves analyzed by the Stockfish engine:

{% list tabs %}

- Embedded UI

  ```sql
  SELECT
      fen,
      MAX(depth) AS max_depth,
      SUM(knodes) AS total_knodes
  FROM evals
  GROUP BY fen
  ORDER BY max_depth DESC
  LIMIT 10;
  ```

- YDB CLI

  ```bash
  ydb sql -s \
  'SELECT
      fen,
      MAX(depth) AS max_depth,
      SUM(knodes) AS total_knodes
  FROM evals
  GROUP BY fen
  ORDER BY max_depth DESC
  LIMIT 10;'
  ```

{% endlist %}

This query performs the following actions:

- Finds positions (represented in FEN format) with the maximum analysis depth.
- Sums the number of analyzed nodes (knodes) for each position.
- Sorts results by maximum analysis depth in descending order.
- Outputs the top 10 positions with the highest analysis depth.
