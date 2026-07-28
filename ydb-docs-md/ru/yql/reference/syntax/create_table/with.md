---
title: "Дополнительные параметры (WITH)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/with?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/with"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/with.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/with.md"
description: "Для таблицы может быть указан ряд специфичных для YDB параметров. При создании таблицы такие параметры перечисляются в блоке WITH:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Дополнительные параметры (WITH)

Для таблицы может быть указан ряд специфичных для YDB параметров. При создании таблицы такие параметры перечисляются в блоке `WITH`:

```yql
CREATE TABLE table_name (...)
WITH (
    key1 = value1,
    key2 = value2,
    ...
)
```

Здесь key — это название параметра, а value — его значение.

Перечень допустимых имен параметров и их значений приведен на странице [описания таблицы YDB](../../../../concepts/datamodel/table.md).

Например, такой запрос создаст строковую таблицу с включенным автоматическим партиционированием по размеру партиции и предпочитаемым размером каждой партиции 512 мегабайт:

```yql
CREATE TABLE my_table (
    id Uint64,
    title Utf8,
    PRIMARY KEY (id)
)
WITH (
    AUTO_PARTITIONING_BY_SIZE = ENABLED,
    AUTO_PARTITIONING_PARTITION_SIZE_MB = 512
);
```

Колоночная таблица создаётся путём указанием параметра `STORE = COLUMN` в блоке `WITH`:

```yql
 CREATE TABLE table_name (
    a Uint64 NOT NULL,
    b Timestamp NOT NULL,
    c Float,
    PRIMARY KEY (a, b)
  )
  PARTITION BY HASH(b)
  WITH (
    STORE = COLUMN
  );
```

Свойства и возможности колоночных таблиц описаны в статье [Таблица](../../../../concepts/datamodel/table.md), а специфика их создания через YQL описана на странице [CREATE TABLE](index.md).

## Time to Live (TTL) и вытеснение данных во внешнее хранилище {#time-to-live}

В блоке `WITH` можно задать TTL (Time to Live) — время жизни строки для строковых и колоночных таблиц. [TTL](../../../../concepts/ttl.md) автоматически удаляет или вытесняет во внешнее хранилище строки, когда проходит указанное количество секунд от времени, записанного в TTL-колонку. TTL можно задать при создании строковой и колоночной таблицы или добавить позже командой `ALTER TABLE` только в строковую таблицу.

Краткая форма значения TTL для задания времени удаления строк:

```yql
Interval("<literal>") ON column [AS <unit>]
```

Общий вид значения TTL:

```yql
Interval("<literal1>") action1, Interval("<literal1>") action2, ..., Interval("<literal1>") actionN ON column [AS <unit>]
```

- `action` — действие, которое выполняется при срабатывании TTL-выражения. Допустимые значения:

  - `DELETE` — удалить строку;
  - `TO EXTERNAL DATA SOURCE <path>` — вытеснить строку во внешнее хранилище, заданное [внешним источником данных](../../../../concepts/datamodel/external_data_source.md) по пути `<path>`.

- `<unit>` — единица измерения, указывается только для колонок с [числовым типом](../../../../concepts/ttl.md#restrictions):

  - `SECONDS`;
  - `MILLISECONDS`;
  - `MICROSECONDS`;
  - `NANOSECONDS`.

Пример создания строковой и колоночной таблицы с TTL:

{% list tabs %}

- Создание строковой таблицы с TTL

  ```yql
  CREATE TABLE my_table (
      id Uint64,
      title Utf8,
      expire_at Timestamp,
      PRIMARY KEY (id)
  )
  WITH (
      TTL = Interval("PT0S") ON expire_at
  );
  ```

- Создание колоночной таблицы с TTL

  ```yql
  CREATE TABLE table_name (
      a Uint64 NOT NULL,
      b Timestamp NOT NULL,
      c Float,
      PRIMARY KEY (a, b)
  )
  PARTITION BY HASH(b)
  WITH (
      STORE = COLUMN,
      TTL = Interval("PT0S") ON b
  );
  ```

{% endlist %}

Пример создания колоночной таблицы с вытеснением строк во внешнее хранилище:

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц. Поддержка функциональности для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц находится в разработке.

```yql
CREATE TABLE table_name (
    a Uint64 NOT NULL,
    b Timestamp NOT NULL,
    c Float,
    PRIMARY KEY (a, b)
)
PARTITION BY HASH(b)
WITH (
    STORE = COLUMN,
    TTL =
        Interval("PT1D") TO EXTERNAL DATA SOURCE `/Root/s3`,
        Interval("P2D") DELETE
    ON b
);
```
