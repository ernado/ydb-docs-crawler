---
title: "ru/analyst/olap_quickstart"
url: "https://ydb.tech/docs/ru/analyst/olap_quickstart?version=v26.1"
doc_path: "ru/analyst/olap_quickstart"
version: "v26.1"
lang: "ru"
source_path: "ru/core/analyst/olap_quickstart.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/analyst/olap_quickstart.md"
description: "Quickstart: Загрузка данных TPC-H из Object Storage и выполнение аналитического запроса."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ru/analyst/olap_quickstart

## Quickstart: Загрузка данных TPC-H из Object Storage и выполнение аналитического запроса {#quickstart-zagruzka-dannyh-tpc-h-iz-object-storage-i-vypolnenie-analiticheskogo-zaprosa}

В этом quickstart описывается процесс загрузки тестового набора данных TPC-H (scale factor 10, 10 ГБ) в YDB из внешнего S3-совместимого хранилища и выполнение аналитического запроса.

После выполнения шагов в базе данных будут созданы:

- Внешний источник данных [`EXTERNAL DATA SOURCE`](../concepts/datamodel/external_data_source.md).
- Внешние таблицы [`EXTERNAL TABLE`](../concepts/datamodel/external_table.md) для схем Parquet-файлов.
- [Колоночные таблицы](../concepts/datamodel/table.md#column-oriented-tables) YDB, оптимизированные для аналитических запросов.

Действия включают:

- Загрузку данных из Object Storage в таблицы YDB с помощью [`UPSERT INTO... SELECT FROM`](../yql/reference/syntax/upsert_into.md).
- Выполнение тестового запроса (TPC-H Q0) для проверки.

### Предварительные требования {#predvaritelnye-trebovaniya}

- Наличие созданной базы данных YDB.
- Наличие инструмента для выполнения YQL/SQL-запросов (YDB UI или [CLI](../reference/ydb-cli/index.md)).

### Создание внешнего источника данных {#sozdanie-vneshnego-istochnika-dannyh}

В данном этапе будет создан объект [`EXTERNAL DATA SOURCE`](../concepts/datamodel/external_data_source.md), который является именованной ссылкой на внешнее хранилище данных. Он содержит в себе информацию о местоположении данных и способе доступа к ним.

**`EXTERNAL DATA SOURCE`** — это сущность в YDB, которая описывает подключение к внешнему хранилищу, например, к S3-совместимому Object Storage.

```sql
CREATE EXTERNAL DATA SOURCE IF NOT EXISTS `external/tpc` WITH (
    SOURCE_TYPE="ObjectStorage",
    LOCATION="https://storage.yandexcloud.net/tpc/",
    AUTH_METHOD="NONE"
);
```

Параметры:

- `SOURCE_TYPE="ObjectStorage"`: тип хранилища (S3-совместимое).
- `LOCATION="https://storage.yandexcloud.net/tpc/"`: URL бакета.
- `AUTH_METHOD="NONE"`: публичный доступ без аутентификации.

### Создание внешних таблиц {#sozdanie-vneshnih-tablic}

На этом шаге определяются схемы (колонки и типы) для Parquet-файлов во внешнем источнике. Это позволяет обращаться к данным через SQL-запросы в YDB, связывая логическую структуру с физическими файлами.

[`EXTERNAL TABLE`](../concepts/datamodel/external_table.md) — это "виртуальная" таблица, которая описывает структуру данных, находящихся во внешнем источнике. Это связывает логическую схему таблицы с физическими файлами.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/customer` (
    c_acctbal Double NOT NULL,
    c_mktsegment String NOT NULL,
    c_phone String NOT NULL,
    c_nationkey Int32 NOT NULL,
    c_custkey Int32 NOT NULL,
    c_name String NOT NULL,
    c_comment String NOT NULL,
    c_address String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/customer/",
    FORMAT="parquet"
);
```

Параметры:

- `DATA_SOURCE="external/tpc"`: ссылка на источник.
- `LOCATION="/h/s10/parquet/customer/"`: путь к файлам.
- `FORMAT="parquet"`: формат данных.

<details>
<summary>Создайте остальные таблицы</summary>

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/customer` (
    c_acctbal Double NOT NULL,
    c_mktsegment String NOT NULL,
    c_phone String NOT NULL,
    c_nationkey Int32 NOT NULL,
    c_custkey Int32 NOT NULL,
    c_name String NOT NULL,
    c_comment String NOT NULL,
    c_address String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/customer/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/lineitem` (
    l_orderkey Int64 NOT NULL,
    l_partkey Int32 NOT NULL,
    l_suppkey Int32 NOT NULL,
    l_linenumber Int32 NOT NULL,
    l_quantity Double NOT NULL,
    l_extendedprice Double NOT NULL,
    l_discount Double NOT NULL,
    l_tax Double NOT NULL,
    l_returnflag String NOT NULL,
    l_linestatus String NOT NULL,
    l_shipdate Date NOT NULL,
    l_commitdate Date NOT NULL,
    l_receiptdate Date NOT NULL,
    l_shipinstruct String NOT NULL,
    l_shipmode String NOT NULL,
    l_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/lineitem/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/nation` (
    n_nationkey Int32 NOT NULL,
    n_name String NOT NULL,
    n_regionkey Int32 NOT NULL,
    n_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/nation/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/orders` (
    o_orderkey Int64 NOT NULL,
    o_custkey Int32 NOT NULL,
    o_orderstatus String NOT NULL,
    o_totalprice Double NOT NULL,
    o_orderdate Date NOT NULL,
    o_orderpriority String NOT NULL,
    o_clerk String NOT NULL,
    o_shippriority Int32 NOT NULL,
    o_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/orders/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/part` (
    p_partkey Int32 NOT NULL,
    p_name String NOT NULL,
    p_mfgr String NOT NULL,
    p_brand String NOT NULL,
    p_type String NOT NULL,
    p_size Int32 NOT NULL,
    p_container String NOT NULL,
    p_retailprice Double NOT NULL,
    p_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/part/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/partsupp` (
    ps_partkey Int32 NOT NULL,
    ps_suppkey Int32 NOT NULL,
    ps_availqty Int32 NOT NULL,
    ps_supplycost Double NOT NULL,
    ps_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/partsupp/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/region` (
    r_regionkey Int32 NOT NULL,
    r_name String NOT NULL,
    r_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/region/",
    FORMAT="parquet"
);

CREATE EXTERNAL TABLE IF NOT EXISTS `external/tpch/s10/supplier` (
    s_suppkey Int32 NOT NULL,
    s_name String NOT NULL,
    s_address String NOT NULL,
    s_nationkey Int32 NOT NULL,
    s_phone String NOT NULL,
    s_acctbal Double NOT NULL,
    s_comment String NOT NULL
) WITH (
    DATA_SOURCE="external/tpc",
    LOCATION="/h/s10/parquet/supplier/",
    FORMAT="parquet"
);
```

</details>

### Создание колоночных таблиц {#sozdanie-kolonochnyh-tablic}

В данном этапе создаются внутренние таблицы YDB для хранения данных. Они используют колоночный формат и партиционирование, что обеспечивает высокую производительность для аналитических запросов за счет параллельной обработки.

```sql
CREATE TABLE IF NOT EXISTS `tpch/s10/customer` (
    c_acctbal Double NOT NULL,
    c_mktsegment String NOT NULL,
    c_phone String NOT NULL,
    c_nationkey Int32 NOT NULL,
    c_custkey Int32 NOT NULL,
    c_name String NOT NULL,
    c_comment String NOT NULL,
    c_address String NOT NULL,
    PRIMARY KEY (c_custkey)
)
PARTITION BY HASH (c_custkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);
```

Параметры:

- `PRIMARY KEY (c_custkey)`: первичный ключ таблицы.
- `PARTITION BY HASH (c_custkey)`: хеш-партиционирование для параллелизма.
- `STORE = COLUMN`: колоночный формат хранения данных для ускорения аналитических запросов.
- `PARTITION_COUNT = 64`: количество партиций для распределения данных.

<details>
<summary>Создайте остальные таблицы</summary>

```sql
CREATE TABLE IF NOT EXISTS `tpch/s10/customer` (
    c_acctbal Double NOT NULL,
    c_mktsegment String NOT NULL,
    c_phone String NOT NULL,
    c_nationkey Int32 NOT NULL,
    c_custkey Int32 NOT NULL,
    c_name String NOT NULL,
    c_comment String NOT NULL,
    c_address String NOT NULL,
    PRIMARY KEY (c_custkey)
)
PARTITION BY HASH (c_custkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/lineitem` (
    l_orderkey Int64 NOT NULL,
    l_partkey Int32 NOT NULL,
    l_suppkey Int32 NOT NULL,
    l_linenumber Int32 NOT NULL,
    l_quantity Double NOT NULL,
    l_extendedprice Double NOT NULL,
    l_discount Double NOT NULL,
    l_tax Double NOT NULL,
    l_returnflag String NOT NULL,
    l_linestatus String NOT NULL,
    l_shipdate Date NOT NULL,
    l_commitdate Date NOT NULL,
    l_receiptdate Date NOT NULL,
    l_shipinstruct String NOT NULL,
    l_shipmode String NOT NULL,
    l_comment String NOT NULL,
    PRIMARY KEY (l_orderkey, l_linenumber)
)
PARTITION BY HASH (l_orderkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/nation` (
    n_nationkey Int32 NOT NULL,
    n_name String NOT NULL,
    n_regionkey Int32 NOT NULL,
    n_comment String NOT NULL,
    PRIMARY KEY (n_nationkey)
)
PARTITION BY HASH (n_nationkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/orders` (
    o_orderkey Int64 NOT NULL,
    o_custkey Int32 NOT NULL,
    o_orderstatus String NOT NULL,
    o_totalprice Double NOT NULL,
    o_orderdate Date NOT NULL,
    o_orderpriority String NOT NULL,
    o_clerk String NOT NULL,
    o_shippriority Int32 NOT NULL,
    o_comment String NOT NULL,
    PRIMARY KEY (o_orderkey)
)
PARTITION BY HASH (o_orderkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/part` (
    p_partkey Int32 NOT NULL,
    p_name String NOT NULL,
    p_mfgr String NOT NULL,
    p_brand String NOT NULL,
    p_type String NOT NULL,
    p_size Int32 NOT NULL,
    p_container String NOT NULL,
    p_retailprice Double NOT NULL,
    p_comment String NOT NULL,
    PRIMARY KEY (p_partkey)
)
PARTITION BY HASH (p_partkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/partsupp` (
    ps_partkey Int32 NOT NULL,
    ps_suppkey Int32 NOT NULL,
    ps_availqty Int32 NOT NULL,
    ps_supplycost Double NOT NULL,
    ps_comment String NOT NULL,
    PRIMARY KEY (ps_partkey, ps_suppkey)
)
PARTITION BY HASH (ps_partkey, ps_suppkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/region` (
    r_regionkey Int32 NOT NULL,
    r_name String NOT NULL,
    r_comment String NOT NULL,
    PRIMARY KEY (r_regionkey)
)
PARTITION BY HASH (r_regionkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);

CREATE TABLE IF NOT EXISTS `tpch/s10/supplier` (
    s_suppkey Int32 NOT NULL,
    s_name String NOT NULL,
    s_address String NOT NULL,
    s_nationkey Int32 NOT NULL,
    s_phone String NOT NULL,
    s_acctbal Double NOT NULL,
    s_comment String NOT NULL,
    PRIMARY KEY (s_suppkey)
)
PARTITION BY HASH (s_suppkey)
WITH (
    STORE = COLUMN,
    PARTITION_COUNT = 64
);
```

</details>

### Загрузка данных в колоночные таблицы {#zagruzka-dannyh-v-kolonochnye-tablicy}

На данном этапе выполняется копирование данных из внешнего хранилища в внутренние таблицы YDB. Это обеспечивает локальное хранение для быстрой аналитики. Процесс может занять время (для 10 ГБ — порядка минут, в зависимости от ресурсов).

```sql
UPSERT INTO `tpch/s10/customer` SELECT * FROM `external/tpch/s10/customer`;
UPSERT INTO `tpch/s10/lineitem` SELECT * FROM `external/tpch/s10/lineitem`;
UPSERT INTO `tpch/s10/nation`   SELECT * FROM `external/tpch/s10/nation`;
UPSERT INTO `tpch/s10/orders`   SELECT * FROM `external/tpch/s10/orders`;
UPSERT INTO `tpch/s10/part`     SELECT * FROM `external/tpch/s10/part`;
UPSERT INTO `tpch/s10/partsupp` SELECT * FROM `external/tpch/s10/partsupp`;
UPSERT INTO `tpch/s10/region`   SELECT * FROM `external/tpch/s10/region`;
UPSERT INTO `tpch/s10/supplier` SELECT * FROM `external/tpch/s10/supplier`;
```

### Выполнение тестового аналитического запроса {#vypolnenie-testovogo-analiticheskogo-zaprosa}

На данном этапе выполняется тестовый запрос TPC-H Q0 для проверки корректности загрузки и производительности. Запрос агрегирует метрики по таблице `lineitem` (около 6 млн строк), с группировкой и последующей сортировкой данных, демонстрируя эффективность колоночных таблиц.

```sql
SELECT
    l_returnflag,
    l_linestatus,
    SUM(l_quantity) AS sum_qty,
    SUM(l_extendedprice) AS sum_base_price,
    SUM(l_extendedprice * (1 - l_discount)) AS sum_disc_price,
    SUM(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge,
    AVG(l_quantity) AS avg_qty,
    AVG(l_extendedprice) AS avg_price,
    AVG(l_discount) AS avg_disc,
    COUNT(*) AS count_order
FROM
    `tpch/s10/lineitem`
WHERE
    l_shipdate <= Date('1998-12-01') - Interval("P90D")
GROUP BY
    l_returnflag,
    l_linestatus
ORDER BY
    l_returnflag,
    l_linestatus;
```

### Дальнейшие шаги {#dalnejshie-shagi}

- Выполнение других запросов из набора TPC-H к загруженным таблицам с помощью YDB CLI и [тестовой нагрузки TPC-H](../reference/ydb-cli/workload-tpch.md).
- Интеграция с BI-системами для [визуализации](../integrations/visualization/index.md) и [анализа](../integrations/gui/index.md) данных.
