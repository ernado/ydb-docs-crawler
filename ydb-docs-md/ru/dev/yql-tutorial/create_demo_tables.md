---
title: "Создание таблиц"
url: "https://ydb.tech/docs/ru/dev/yql-tutorial/create_demo_tables?version=v26.1"
doc_path: "ru/dev/yql-tutorial/create_demo_tables"
version: "v26.1"
lang: "ru"
source_path: "ru/core/dev/yql-tutorial/create_demo_tables.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/dev/yql-tutorial/create_demo_tables.md"
description: "Создайте строковые таблицы для OLTP-операций или колоночные таблицы для OLAP-нагрузок и задайте для них схемы данных с помощью конструкции CREATE TABLE. Подробн"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Создание таблиц

Создайте строковые таблицы для OLTP-операций или колоночные таблицы для OLAP-нагрузок и задайте для них схемы данных с помощью конструкции [CREATE TABLE](../../yql/reference/syntax/create_table/index.md). Подробнее о типах таблиц в YDB и области их применения можно прочесть в статье [Таблица](../../concepts/datamodel/table.md)

> [!NOTE]
> Ключевые слова не чувствительны к регистру и написаны заглавными буквами для наглядности.

{% list tabs %}

- Создание строковых таблиц

  ```sql
  CREATE TABLE series         -- series — имя таблицы.
  (                           -- Должно быть уникальным в пределах каталога.
      series_id Uint64,
      title Utf8,
      series_info Utf8,
      release_date Uint64,
      PRIMARY KEY (series_id) -- Первичный ключ — это столбец или
                              -- комбинация столбцов, однозначно идентифицирующих
                              -- каждую строку в таблице (может содержать только
                              -- неповторяющиеся значения). Для таблицы может быть
                              -- указан только один первичный ключ. Для каждой таблицы
                              -- YDB указание первичного ключа является обязательным.
  );

  CREATE TABLE seasons
  (
      series_id Uint64,
      season_id Uint64,
      title Utf8,
      first_aired Uint64,
      last_aired Uint64,
      PRIMARY KEY (series_id, season_id)
  );

  CREATE TABLE episodes
  (
      series_id Uint64,
      season_id Uint64,
      episode_id Uint64,
      title Utf8,
      air_date Uint64,
      PRIMARY KEY (series_id, season_id, episode_id)
  );
  ```

- Создание колоночных таблиц

  Колоночная таблица в YQL создаётся путём указания в конструкции `CREATE TABLE` блока `WITH` с параметром `STORE = COLUMN`.

  ```sql
  CREATE TABLE series         -- series — имя таблицы.
  (                           -- Должно быть уникальным в пределах каталога.
      series_id Uint64 NOT NULL, -- первичный ключ колоночной таблицы не может быть NULLABLE
      title Utf8,
      series_info Utf8,
      release_date Uint64,
      PRIMARY KEY (series_id) -- Первичный ключ — это столбец или
                              -- комбинация столбцов, однозначно идентифицирующих
                              -- каждую строку в таблице (может содержать только
                              -- неповторяющиеся значения). Для таблицы может быть
                              -- указан только один первичный ключ. Для каждой таблицы
                              -- YDB указание первичного ключа является обязательным.
  )
  PARTITION BY HASH(series_id) -- Партиционирование таблицы по хешу от набора колонок
  WITH (
      STORE = COLUMN         -- STORE указывает на тип таблицы
                             -- если указан COLUMN, то будет создана колоночная таблица
  );

  CREATE TABLE seasons
  (
      series_id Uint64 NOT NULL,
      season_id Uint64 NOT NULL,
      title Utf8,
      first_aired Uint64,
      last_aired Uint64,
      PRIMARY KEY (series_id, season_id)
  )
  WITH (
      STORE = COLUMN
  );

  CREATE TABLE episodes
  (
      series_id Uint64 NOT NULL,
      season_id Uint64 NOT NULL,
      episode_id Uint64 NOT NULL,
      title Utf8,
      air_date Uint64,
      PRIMARY KEY (series_id, season_id, episode_id)
  )
  WITH (
      STORE = COLUMN
  );
  ```

{% endlist %}
