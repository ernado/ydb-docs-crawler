---
title: "Форматы данных и алгоритмы сжатия"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/s3/formats?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/s3/formats"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/s3/formats.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/s3/formats.md"
description: "В данном разделе описываются поддерживаемые в YDB форматы данных, хранимых в S3, поддерживаемые алгоритмы сжатия и список поддерживаемых YQL типов для каждого ф"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Форматы данных и алгоритмы сжатия

В данном разделе описываются поддерживаемые в YDB форматы данных, хранимых в S3, поддерживаемые алгоритмы сжатия и список поддерживаемых [YQL типов](../../../../yql/reference/types/index.md) для каждого формата данных.

## Поддерживаемые форматы данных {#formats}

Список поддерживаемых в YDB форматов данных приведен в таблице ниже.

| Формат | Чтение | Запись |
| --- | --- | --- |
| [`csv_with_names`](formats.md#csv_with_names) | ✓ | ✓ |
| [`tsv_with_names`](formats.md#tsv_with_names) | ✓ | ✓ |
| [`json_list`](formats.md#json_list) | ✓ | ✓ |
| [`json_each_row`](formats.md#json_each_row) | ✓ | ✓ |
| [`json_as_string`](formats.md#json_as_string) | ✓ |  |
| [`parquet`](formats.md#parquet) | ✓ | ✓ |
| [`raw`](formats.md#raw) | ✓ | ✓ |

### Формат csv_with_names {#csv_with_names}

Данный формат основан на формате [CSV](https://ru.wikipedia.org/wiki/CSV). Данные размещены в колонках, разделены запятыми, в первой строке файла находятся имена колонок.

Пример данных:

```text
Year,Manufacturer,Model,Price
1997,Man_1,Model_1,3000.00
1999,Man_2,Model_2,4900.00
```

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    *
FROM external_source.path
WITH
(
    FORMAT = "csv_with_names",
    SCHEMA =
    (
        Year Int32,
        Manufacturer Utf8,
        Model Utf8,
        Price Double
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат tsv_with_names {#tsv_with_names}

Данный формат основан на формате [TSV](https://ru.wikipedia.org/wiki/TSV). Данные размещены в колонках, разделены символами табуляции (код `0x9`), в первой строке файла находятся имена колонок.

Пример данных:

```text
Year    Manufacturer    Model   Price
1997    Man_1   Model_1    3000.00
1999    Man_2   Model_2    4900.00
```

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    *
FROM external_source.path
WITH
(
    FORMAT = "tsv_with_names",
    SCHEMA =
    (
        Year Int32,
        Manufacturer Utf8,
        Model Utf8,
        Price Double
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат json_list {#json_list}

Данный формат основан на [JSON-представлении](https://ru.wikipedia.org/wiki/JSON) данных. В этом формате внутри каждого файла должен находиться объект в корректном JSON-представлении.

Пример корректных данных (данные представлены в виде списка объектов JSON):

```json
[
    { "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 },
    { "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
]
```

Пример **НЕ**корректных данных (на каждой отдельной строке находится отдельный объект в формате JSON, но эти объекты не объединены в список):

```json
{ "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 }
{ "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
```

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    *
FROM external_source.path
WITH
(
    FORMAT = "json_list",
    SCHEMA =
    (
        Year Int32,
        Manufacturer Utf8,
        Model Utf8,
        Price Double
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат json_each_row {#json_each_row}

Данный формат основан на [JSON-представлении](https://ru.wikipedia.org/wiki/JSON) данных. В этом формате внутри каждого файла на каждой отдельной строке файла должен находиться объект в корректном JSON-представлении, но эти объекты не объединены в JSON-список. Такой формат используется при передаче данных через потоковые системы, например, Apache Kafka или [Топики YDB](../../../datamodel/topic.md).

Пример корректных данных (на каждой отдельной строке находится отдельный объект в формате JSON, но эти объекты не объединены в список):

```json
{ "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 },
{ "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
```

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    *
FROM external_source.path
WITH
(
    FORMAT = "json_each_row",
    SCHEMA =
    (
        Year Int32,
        Manufacturer Utf8,
        Model Utf8,
        Price Double
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат json_as_string {#json_as_string}

Данный формат основан на [JSON-представлении](https://ru.wikipedia.org/wiki/JSON) данных. Формат `json_as_string` не разбивает входной JSON-документ на поля, а представляет каждую строку файла в виде одного объекта JSON (или одной строки). Такой формат удобен, если список полей не одинаков во всех строках, а может изменяться.

В этом формате внутри каждого файла должен находиться:

- объект в корректном JSON-представлении в каждой отдельной строке файла;
- объекты в корректном JSON-представлении, объединенные в список.

Пример корректных данных (данные представлены в виде списка объектов JSON):

```json
{ "Year": 1997, "Attrs": { "Manufacturer": "Man_1", "Model": "Model_1" }, "Price": 3000.0 }
{ "Year": 1999, "Attrs": { "Manufacturer": "Man_2", "Model": "Model_2" }, "Price": 4900.00 }
```

В этом формате [схема](external_data_source.md#schema) читаемых данных должна состоять только из одной колонки с одним из разрешённых типов данных, подробнее см. [ниже](formats.md#types).

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    CAST(JSON_VALUE(Data, "$.Year") AS Int32) AS Year,
    JSON_VALUE(Data, "$.Attrs.Manufacturer") AS Manufacturer,
    JSON_VALUE(Data, "$.Attrs.Model") AS Model,
    CAST(JSON_VALUE(Data, "$.Price") AS Double) AS Price
FROM external_source.path
WITH
(
    FORMAT = "json_as_string",
    SCHEMA =
    (
        Data Json
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат parquet {#parquet}

Данный формат позволяет считывать содержимое файлов в формате [Apache Parquet](https://parquet.apache.org).

Поддерживаемые алгоритмы сжатия данных внутри файлов Parquet для чтения из S3:

- Без сжатия
- SNAPPY
- GZIP
- BROTLI
- LZ4
- ZSTD
- LZ4_RAW

> [!NOTE]
> Запись в формате Parquet будет производится с использованием алгоритма сжатия [Snappy](<https://ru.wikipedia.org/wiki/Snappy_(%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0)>).

<details>
<summary>Пример запроса</summary>

```yql
SELECT
    *
FROM external_source.path
WITH
(
    FORMAT = "parquet",
    SCHEMA =
    (
        Year Int32,
        Manufacturer Utf8,
        Model Utf8,
        Price Double
    )
)
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

### Формат raw {#raw}

Данный формат позволяет считывать содержимое файлов как есть, в "сыром" виде. Считанные таким образом данные можно обработать средствами [YQL](../../../../yql/reference/udf/list/string.md), разделив на строки и столбцы.

Этот формат стоит использовать, если встроенных возможностей парсинга исходных данных в YDB недостаточно. В этом формате [схема](external_data_source.md#schema) данных для чтения и записи должна состоять только из одной колонки с одним из разрешённых типов данных, подробнее см. [ниже](formats.md#types).

> [!NOTE]
> Размер каждого из считываемых файлов в формате `raw` не может превышать общего ограничения на потребление памяти одним запросом в YDB.

<details>
<summary>Пример запроса</summary>

Для парсинга следующих данных, где строки разделены точкой с запятой, а значения запятой:

```text
1997,Man_1,Model_1,3000.00;
1999,Man_2,Model_2,4900.00;
```

Можно использовать запрос:

```yql
$input = SELECT
    String::SplitToList(        -- разделение каждой строки по ','
        String::Strip(RowData), -- удаление всех пробельных символов из начала и конца строк
        ","
    ) AS Row
FROM external_source.path
WITH
(
    FORMAT = "raw",
    SCHEMA =
    (
        FileData Utf8
    )
)
FLATTEN LIST BY (String::SplitToList(FileData, ";", TRUE AS SkipEmpty) AS RowData); -- разделение файла по ';'

SELECT -- Получение нужных колонок
    CAST(Row[0] AS Int32) AS Year,
    Row[1] AS Manufacturer,
    Row[2] AS Model,
    CAST(Row[3] AS Double) AS Price
FROM $input
```

Результат выполнения запроса:

| # | Manufacturer | Model | Price | Year |
| --- | --- | --- | --- | --- |
| 1 | Man_1 | Model_1 | 3000 | 1997 |
| 2 | Man_2 | Model_2 | 4900 | 1999 |

</details>

## Поддерживаемые алгоритмы сжатия {#compression}

Использование алгоритмов сжатия зависит от форматов файлов. Для всех форматов файлов за исключением Parquet возможно использование следующих алгоритмов сжатия:

| Алгоритм | Название в YDB | Чтение | Запись |
| --- | --- | --- | --- |
| [Gzip](https://ru.wikipedia.org/wiki/Gzip) | gzip | ✓ | ✓ |
| [Zstd](https://ru.wikipedia.org/wiki/Zstandard) | zstd | ✓ | ✓ |
| [LZ4](https://ru.wikipedia.org/wiki/LZ4) | lz4 | ✓ | ✓ |
| [Brotli](https://ru.wikipedia.org/wiki/Brotli) | brotli | ✓ | ✓ |
| [Bzip2](https://ru.wikipedia.org/wiki/Bzip2) | bzip2 | ✓ | ✓ |
| [Xz](https://ru.wikipedia.org/wiki/XZ) | xz | ✓ | ✓ |

Для формата файлов Parquet поддерживаются собственные внутренние алгоритмы сжатия:

| Формат сжатия | Чтение | Запись |
| --- | --- | --- |
| Без сжатия | ✓ |  |
| [Snappy](<https://ru.wikipedia.org/wiki/Snappy_(%D0%B1%D0%B8%D0%B1%D0%BB%D0%B8%D0%BE%D1%82%D0%B5%D0%BA%D0%B0)>) | ✓ | ✓ |
| [Gzip](https://ru.wikipedia.org/wiki/Gzip) | ✓ |  |
| [Brotli](https://ru.wikipedia.org/wiki/Brotli) | ✓ |  |
| [LZ4](https://ru.wikipedia.org/wiki/LZ4) | ✓ |  |
| [Zstd](https://ru.wikipedia.org/wiki/Zstandard) | ✓ |  |
| LZ4_RAW | ✓ |  |

В YDB не поддерживается работа со сжатыми "снаружи" parquet-файлами, например, с файлами вида `<myfile>.parquet.gz` или аналогичными. Все файлы в формате Parquet должны быть без внешнего сжатия.

## Поддерживаемые типы данных {#types}

Таблица всех поддерживаемых типов при чтении из S3 в [схеме](external_data_source.md#schema) запроса:

| Тип | csv_with_names | tsv_with_names | json_list | json_each_row | json_as_string | parquet | raw |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Bool`,  <br>`Int8`, `Int16`, `Int32`, `Int64`,  <br>`Uint8`, `Uint16`, `Uint32`, `Uint64`,  <br>`Float`, `Double` | ✓ | ✓ | ✓ | ✓ |  | ✓ |  |
| `DyNumber` |  |  | ✓ |  |  |  |  |
| `String`, `Utf8`, `Json` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `JsonDocument` |  |  |  |  |  | ✓ |  |
| `Yson` |  |  | ✓ |  |  | ✓ | ✓ |
| `Uuid` | ✓ | ✓ |  | ✓ |  |  |  |
| `Date`, `Datetime`, `Timestamp`,  <br>`TzDate`, `TzDateTime`, `TzTimestamp` | ✓ | ✓ |  | ✓ |  | ✓ |  |
| `Interval` | ✓ | ✓ |  | ✓ |  | ✓ |  |
| `Date32`, `Datetime64`, `Timestamp64`,  <br>`Interval64`,  <br>`TzDate32`, `TzDateTime64`, `TzTimestamp64` |  |  |  |  |  | ✓ |  |
| `Optional<T>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Таблица всех поддерживаемых типов при записи в S3:

| Тип | csv_with_names | tsv_with_names | json_list | json_each_row | parquet | raw |
| --- | --- | --- | --- | --- | --- | --- |
| `Bool`,  <br>`Int8`, `Int16`, `Int32`, `Int64`,  <br>`Uint8`, `Uint16`, `Uint32`, `Uint64`,  <br>`Float`, `Double` | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| `DyNumber` |  |  | ✓ |  |  |  |
| `String`, `Utf8`, `Json` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `JsonDocument` |  |  |  |  |  |  |
| `Yson` |  |  | ✓ |  |  | ✓ |
| `Uuid` | ✓ | ✓ |  | ✓ |  |  |
| `Date`, `Datetime`, `Timestamp`,  <br>`TzDate`, `TzDateTime`, `TzTimestamp` | ✓ | ✓ |  | ✓ | ✓ |  |
| `Interval` |  |  |  |  |  |  |
| `Date32`, `Datetime64`, `Timestamp64`,  <br>`Interval64`,  <br>`TzDate32`, `TzDateTime64`, `TzTimestamp64` |  |  |  |  |  |  |
| `Optional<T>` | ✓ | ✓ | ✓ | ✓ | ✓ |  |

Для всех форматов чтения из S3 и записи в S3, кроме `json_list`, разрешено использовать тип `Optional<T>` только в том случае, если `T` — [примитивный YQL тип](../../../../yql/reference/types/primitive.md). Подробнее об опциональных типах см. в статье [column0](../../../../yql/reference/types/optional.md).
