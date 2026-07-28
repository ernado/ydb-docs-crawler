---
title: "Video Game Sales"
url: "https://ydb.tech/docs/ru/analyst/datasets/video-games?version=v26.1"
doc_path: "ru/analyst/datasets/video-games"
version: "v26.1"
lang: "ru"
source_path: "ru/core/analyst/datasets/video-games.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/analyst/datasets/video-games.md"
description: "Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Video Game Sales

> [!NOTE]
> Эта страница является частью раздела [Импорт датасетов](index.md), где описаны примеры загрузки популярных наборов данных в YDB. Перед началом работы ознакомьтесь с [общей информацией](index.md#general-info) о требованиях и процессе импорта.

Данные о продажах видеоигр.

**Источник**: [Kaggle - Video Game Sales](https://www.kaggle.com/datasets/gregorut/videogamesales)

**Размер**: 1.36 MB

## Пример загрузки {#primer-zagruzki}

1. Скачайте и разархивируйте файл `vgsales.csv` с Kaggle
2. Создайте таблицу в YDB одним из следующих способов:

{% list tabs %}

- Embedded UI

  Подробнее про [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

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

3. Выполните команду импорта:

```bash
ydb import file csv --header --null-value "" --path vgsales vgsales.csv
```

## Пример аналитического запроса {#primer-analiticheskogo-zaprosa}

Чтобы определить издателя, у которого наибольшая средняя продажа игр в Северной Америке, выполните запрос:

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

Результат:

```bash
┌───────────┬──────────────────┐
│ Publisher │ average_na_sales │
├───────────┼──────────────────┤
│ "Palcom"  │ 3.38             │
└───────────┴──────────────────┘
```

Запрос позволит найти, какой издатель достиг наибольшего успеха в Северной Америке по средней продаже.
