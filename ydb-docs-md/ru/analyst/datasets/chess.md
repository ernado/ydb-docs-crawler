---
title: "Chess Position Evaluations"
url: "https://ydb.tech/docs/ru/analyst/datasets/chess?version=v26.1"
doc_path: "ru/analyst/datasets/chess"
version: "v26.1"
lang: "ru"
source_path: "ru/core/analyst/datasets/chess.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/analyst/datasets/chess.md"
description: "Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Chess Position Evaluations

> [!NOTE]
> Эта страница является частью раздела [Импорт датасетов](index.md), где описаны примеры загрузки популярных наборов данных в YDB. Перед началом работы ознакомьтесь с [общей информацией](index.md#general-info) о требованиях и процессе импорта.

Датасет включает 513 миллионов оценок шахматных позиций, выполненных движком Stockfish для анализа на платформе Lichess.

**Источник**: [Kaggle - Chess Position Evaluations](https://www.kaggle.com/datasets/lichess/chess-evaluations)

**Размер**: 59.66 GB

## Пример загрузки {#primer-zagruzki}

1. Скачайте файл `evals.csv` с Kaggle
2. Создайте таблицу в YDB одним из следующих способов:

{% list tabs %}

- Embedded UI

  Подробнее про [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

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

3. Выполните команду импорта:

```bash
ydb import file csv --header --null-value "" --path evals evals.csv
```

## Пример аналитического запроса {#primer-analiticheskogo-zaprosa}

Определим позиции с наибольшим количеством ходов, проанализированных движком Stockfish:

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

Этот запрос выполняет следующие действия:

- Находит позиции (представленные в формате FEN) с максимальной глубиной анализа (depth).
- Суммирует количество проанализированных узлов (knodes) для каждой позиции.
- Сортирует результаты по максимальной глубине анализа в порядке убывания.
- Выводит топ-10 позиций с наибольшей глубиной анализа.
