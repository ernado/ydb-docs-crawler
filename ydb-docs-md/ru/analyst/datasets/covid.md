---
title: "COVID-19 Open Research Dataset"
url: "https://ydb.tech/docs/ru/analyst/datasets/covid?version=v26.1"
doc_path: "ru/analyst/datasets/covid"
version: "v26.1"
lang: "ru"
source_path: "ru/core/analyst/datasets/covid.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/analyst/datasets/covid.md"
description: "Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# COVID-19 Open Research Dataset

> [!NOTE]
> Эта страница является частью раздела [Импорт датасетов](index.md), где описаны примеры загрузки популярных наборов данных в YDB. Перед началом работы ознакомьтесь с [общей информацией](index.md#general-info) о требованиях и процессе импорта.

Открытый набор данных исследований COVID-19.

**Источник**: [Kaggle - COVID-19 Open Research Dataset Challenge](https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge?select=metadata.csv)

**Размер**: 1.65 GB (файл metadata.csv)

## Пример загрузки {#primer-zagruzki}

1. Скачайте и разархивируйте файл `metadata.csv` с Kaggle
2. Датасет включает в себя полностью идентичные строки. Поскольку YDB требует указания уникальных значений первичного ключа, добавим в файл новую колонку под названием `row_id`, где значение ключа будет равно номеру строки в исходном файле. Это позволит предотвратить удаление повторяющихся данных. Эту операцию можно осуществить с помощью команды awk:

```bash
awk 'NR==1 {print "row_id," $0; next} {print NR-1 "," $0}' metadata.csv > temp.csv && mv temp.csv metadata.csv
```

3. Создайте таблицу в YDB одним из следующих способов:

{% list tabs %}

- Embedded UI

  Подробнее про [Embedded UI](../../reference/embedded-ui/ydb-monitoring.md).

  ```sql
  CREATE TABLE `covid_research` (
      `row_id` Uint64 NOT NULL,
      `cord_uid` Text NOT NULL,
      `sha` Text NOT NULL,
      `source_x` Text NOT NULL,
      `title` Text NOT NULL,
      `doi` Text NOT NULL,
      `pmcid` Text NOT NULL,
      `pubmed_id` Text NOT NULL,
      `license` Text NOT NULL,
      `abstract` Text NOT NULL,
      `publish_time` Text NOT NULL,
      `authors` Text NOT NULL,
      `journal` Text NOT NULL,
      `mag_id` Text,
      `who_covidence_id` Text,
      `arxiv_id` Text,
      `pdf_json_files` Text NOT NULL,
      `pmc_json_files` Text NOT NULL,
      `url` Text NOT NULL,
      `s2_id` Uint64,
      PRIMARY KEY (`row_id`)
  )
  WITH (
      STORE = COLUMN
  );
  ```

- YDB CLI

  ```bash
  ydb sql -s \
  'CREATE TABLE `covid_research` (
      `row_id` Uint64 NOT NULL,
      `cord_uid` Text NOT NULL,
      `sha` Text NOT NULL,
      `source_x` Text NOT NULL,
      `title` Text NOT NULL,
      `doi` Text NOT NULL,
      `pmcid` Text NOT NULL,
      `pubmed_id` Text NOT NULL,
      `license` Text NOT NULL,
      `abstract` Text NOT NULL,
      `publish_time` Text NOT NULL,
      `authors` Text NOT NULL,
      `journal` Text NOT NULL,
      `mag_id` Text,
      `who_covidence_id` Text,
      `arxiv_id` Text,
      `pdf_json_files` Text NOT NULL,
      `pmc_json_files` Text NOT NULL,
      `url` Text NOT NULL,
      `s2_id` Uint64,
      PRIMARY KEY (`row_id`)
  )
  WITH (
      STORE = COLUMN
  );'
  ```

{% endlist %}

4. Выполните команду импорта:

```bash
ydb import file csv --header --null-value "" --path covid_research metadata.csv
```

## Пример аналитического запроса {#primer-analiticheskogo-zaprosa}

Выполните запрос для определения журналов с наибольшим количеством публикаций:

{% list tabs %}

- Embedded UI

  ```sql
  SELECT
      journal,
      COUNT(*) AS publication_count
  FROM covid_research
  WHERE journal IS NOT NULL AND journal != ''
  GROUP BY journal
  ORDER BY publication_count DESC
  LIMIT 10;
  ```

- YDB CLI

  ```bash
  ydb sql -s \
  'SELECT
      journal,
      COUNT(*) AS publication_count
  FROM covid_research
  WHERE journal IS NOT NULL AND journal != ""
  GROUP BY journal
  ORDER BY publication_count DESC
  LIMIT 10;'
  ```

{% endlist %}

Результат:

```
┌───────────────────────────────────┬───────────────────┐
│ journal                           │ publication_count │
├───────────────────────────────────┼───────────────────┤
│ "PLoS One"                        │ 9953              │
├───────────────────────────────────┼───────────────────┤
│ "bioRxiv"                         │ 8961              │
├───────────────────────────────────┼───────────────────┤
│ "Int J Environ Res Public Health" │ 8201              │
├───────────────────────────────────┼───────────────────┤
│ "BMJ"                             │ 6928              │
├───────────────────────────────────┼───────────────────┤
│ "Sci Rep"                         │ 5935              │
├───────────────────────────────────┼───────────────────┤
│ "Cureus"                          │ 4212              │
├───────────────────────────────────┼───────────────────┤
│ "Reactions Weekly"                │ 3891              │
├───────────────────────────────────┼───────────────────┤
│ "Front Psychol"                   │ 3541              │
├───────────────────────────────────┼───────────────────┤
│ "BMJ Open"                        │ 3515              │
├───────────────────────────────────┼───────────────────┤
│ "Front Immunol"                   │ 3442              │
└───────────────────────────────────┴───────────────────┘
```
