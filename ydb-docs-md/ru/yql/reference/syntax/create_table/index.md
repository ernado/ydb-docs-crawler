---
title: "CREATE TABLE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/index.md"
description: "Вызов CREATE TABLE создает таблицу с указанной схемой данных и ключевыми колонками ( PRIMARY KEY ). Позволяет определить вторичные индексы на создаваемой таблиц"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE TABLE

Вызов `CREATE TABLE` создает [таблицу](../../../../concepts/datamodel/table.md) с указанной схемой данных и ключевыми колонками (`PRIMARY KEY`). Позволяет определить вторичные индексы на создаваемой таблице.

```yql
CREATE TABLE [IF NOT EXISTS] <table_name> (
  [<column_name> <column_data_type>] [FAMILY <family_name>] [NULL | NOT NULL] [DEFAULT <default_value>]
  [COMPRESSION([algorithm=<algorithm_name>[, level=<value>]])]
  [, ...],
    INDEX <index_name>
      [GLOBAL]
      [SYNC|ASYNC]
      [USING <index_type>]
      ON ( <index_columns> )
      [COVER ( <cover_columns> )]
      [WITH ( <parameter_name> = <parameter_value>[, ...])]
    [, ...]
  PRIMARY KEY ( <column>[, ...]),
  [FAMILY <column_family> ( family_options[, ...])]
)
[PARTITION BY HASH ( <column>[, ...])]
[WITH (<setting_name> = <setting_value>[, ...])]

[AS SELECT ...]
```

## Параметры запроса {#parametry-zaprosa}

### table_name {#table_name}

Путь создаваемой таблицы.

При выборе имени для таблицы учитывайте общие [правила именования схемных объектов](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

### IF NOT EXISTS

Если таблица с указанным именем уже существует, выполнение оператора полностью пропускается — не происходит никаких проверок или сопоставления схемы, и никакой ошибки не возникает. Обратите внимание, что существующая таблица может отличаться по структуре от той, которую вы хотели бы создать этим запросом — сравнение или проверка эквивалентности не производится.

### column_name {#column_name}

Имя колонки, создаваемой в новой таблице.

При выборе имени для колонки учитывайте общие [правила именования колонок](../../../../concepts/datamodel/table.md#column-naming-rules).

### column_data_type {#column_data_type}

Тип данных колонки. Полный список типов данных, которые поддерживает YDB доступен в разделе [Типы данных YQL](../../types/index.md).

### FAMILY \<family_name> (настройка колонки) {#family-lessfamily_namegreater-nastrojka-kolonki}

Указание принадлежности данной колонки к указанной группе колонок. Подробнее в разделе [Группы колонок](family.md).

### DEFAULT \<default_value> {#default-lessdefault_valuegreater}

> [!WARNING]
> Опция `DEFAULT` поддерживается:
>
> - Только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.
> - Только с литеральными значениями. Поддержка функциональности для вычислимых выражений находится в разработке.

Позволяет задать значение по умолчанию для колонки. Если при вставке строки значение для данной колонки не указано, будет использовано указанное значение по умолчанию. Значение по умолчанию должно соответствовать типу данных колонки.

Конструкция `DEFAULT false NOT NULL` недопустима по причине неоднозначности интерпретации. В таком случае следует использовать перечисление через запятые или изменить порядок опций.

### NULL

Данная колонка может содержать значения `NULL` (по умолчанию).

### NOT NULL

Данная колонка не принимает значения `NULL`.

### COMPRESSION(\[algorithm=\<algorithm_name>\[, level=\]\]) {#]]}

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц.

Для колонок можно задать следующие параметры сжатия:

- `algorithm` — алгоритм сжатия данных. Допустимые значения: `off` (отключение сжатия), `lz4`, `zstd`.
- `level` — уровень сжатия, поддерживается только для алгоритма `zstd` (допустимы значения от 0 до 22).

Если `COMPRESSION()` указан без параметров, для колонки используется сжатие по умолчанию. Сейчас это `lz4`; в будущих версиях появится возможность настраивать сжатие по умолчанию на уровне кластера или таблицы.

### INDEX

Определение индекса на таблице. Поддерживаются [вторичные индексы](secondary_index.md) и [векторные индексы](vector_index.md).

### PRIMARY KEY

Определение первичного ключа таблицы. Указывает колонки, которые составляют первичный ключ в порядке перечисления. Подробнее о выборе первичного ключа в разделе [Выбор первичного ключа](../../../../dev/primary-key/index.md).

### PARTITION BY HASH

Определение ключей партиционирования для **колоночных** таблиц. Указывает колонки, по хэшу которых выполняется [партиционирование](../../../../concepts/glossary.md#partition) данных. Колонки должны быть частью первичного ключа. При этом колонки не обязательно должны быть префиксом или суффиксом -- требование быть частью первичного ключа.

Если параметр не будет указан, таблица будет разбита на партиции по тем же колонкам, которые входят в первичный ключ. Как правильно выбирать ключи для партиционирования в колоночных таблицах, читайте в статье [Выбор ключей для максимальной производительности колоночных таблиц](../../../../dev/primary-key/column-oriented.md).

Подробнее о партиционировании колоночных таблиц читайте в разделе [Партицирование колоночной таблицы](../../../../concepts/datamodel/table.md#olap-tables-partitioning).

### FAMILY \<column_family> (настройка группы колонок) {#family-lesscolumn_familygreater-nastrojka-gruppy-kolonok}

Определение группы колонок с заданными параметрами. Подробнее в разделе [Группы колонок](family.md).

### WITH

Дополнительные параметры создания таблицы. Подробнее в разделе [Дополнительные параметры (WITH)](with.md).

> [!NOTE]
> YDB поддерживает два типа таблиц:
>
> - [Строковые](../../../../concepts/datamodel/table.md#row-oriented-tables).
> - [Колоночные](../../../../concepts/datamodel/table.md#column-oriented-tables).
>
> Тип таблицы при создании задается параметром `STORE` в блоке `WITH`, где `ROW` означает [строковую таблицу](../../../../concepts/datamodel/table.md#row-oriented-tables), а `COLUMN` — [колоночную](../../../../concepts/datamodel/table.md#column-oriented-tables):
>
> ```yql
> CREATE <table_name> (
>   columns
>   ...
> )
>
> WITH (
>   STORE = COLUMN -- Default value ROW
> )
> ```
>
> По умолчанию, если параметр `STORE` не указан, создается строковая таблица.

> [!NOTE]
> При выборе имени для таблицы учитывайте общие [правила именования схемных объектов](../../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

### AS SELECT

Создание и заполнение таблицы на основе результатов запроса `SELECT`. Подробнее в разделе [Создание и заполнение таблицы на основе результатов запроса](as_select.md).

## Примеры создания таблиц {#primery-sozdaniya-tablic}

{% list tabs %}

- Создание строковой таблицы

  ```yql
    CREATE TABLE <table_name> (
      a Uint64,
      b Uint64,
      c Float,
      PRIMARY KEY (a, b)
    );
  ```

  Пример создания таблицы с использованием значения по умолчанию (DEFAULT):

  ```yql
    CREATE TABLE table_with_default (
    id Uint64,
    name String DEFAULT "unknown",
    score Double NOT NULL DEFAULT 0.0,
    PRIMARY KEY (id)
  );
  ```

  Для ключевых колонок допускаются только [примитивные](../../types/primitive.md) и [серийные](../../types/serial.md) типы данных, для неключевых колонок допускаются только [примитивные](../../types/primitive.md).

  Без дополнительных модификаторов колонка приобретает [опциональный тип](../../types/optional.md), и допускает запись `NULL` в качестве значений. Для получения неопционального типа необходимо использовать `NOT NULL`.

  Обязательно указание `PRIMARY KEY` с непустым списком колонок. Эти колонки становятся частью ключа в порядке перечисления.

  Пример создания строковой таблицы с использованием опций партиционирования:

  ```yql
  CREATE TABLE <table_name> (
    a Uint64,
    b Uint64,
    c Float,
    PRIMARY KEY (a, b)
  )
  WITH (
    AUTO_PARTITIONING_BY_SIZE = ENABLED,
    AUTO_PARTITIONING_PARTITION_SIZE_MB = 512
  );
  ```

  Такой код создаст строковую таблицу с включенным автоматическим партиционированием по размеру партиции (`AUTO_PARTITIONING_BY_SIZE`) и предпочитаемым размером каждой партиции (`AUTO_PARTITIONING_PARTITION_SIZE_MB`) в 512 мегабайт. Полный список опций партиционирования строковой таблицы находится в разделе [Партиционирование строковой таблицы](../../../../concepts/datamodel/table.md#partitioning_row_table) статьи [Таблица](../../../../concepts/datamodel/table.md).

- Создание колоночной таблицы

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

  Для колоночных таблиц можно явно указать, по каким колонкам будет происходить партиционирование, с помощью конструкции `PARTITION BY HASH`. Обычно для этого выбирают колонки первичного ключа с большим числом уникальных значений, например, `Timestamp`. Если `PARTITION BY HASH` не указать, партиционирование произойдёт автоматически по всем колонкам, входящим в первичный ключ. Подробнее о выборе и работе ключей партиционирования в колоночных таблицах читайте в статье [Выбор ключей для максимальной производительности колоночных таблиц](../../../../dev/primary-key/column-oriented.md).

  В настоящий момент колоночные таблицы не поддерживают автоматического репартицирования, поэтому важно указывать правильное число партиций при создании таблицы с помощью параметра `AUTO_PARTITIONING_MIN_PARTITIONS_COUNT`:

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
    AUTO_PARTITIONING_MIN_PARTITIONS_COUNT = 10
  );
  ```

  Такой код создаст колоночную таблицу с 10-ю партициями. С полным списком опций партиционирования колоночных таблиц можно ознакомиться в разделе [Партицирование колоночной таблицы](../../../../concepts/datamodel/table.md#olap-tables-partitioning) статьи [Таблица](../../../../concepts/datamodel/table.md).

{% endlist %}

При создании строковых таблиц возможно задать:

- [Вторичный индекс](secondary_index.md).
- [Векторный индекс](vector_index.md).
- [Группы колонок](family.md).
- [Дополнительные параметры](with.md).
- [Создание и заполнение таблицы на основе результатов запроса](as_select.md).

Для колоночных таблиц при их создании возможно задать:

- [Группы колонок](family.md).
- [Дополнительные параметры](with.md).
- [Создание и заполнение таблицы на основе результатов запроса](as_select.md).
