---
title: "Topic read and write formats"
url: "https://ydb.tech/docs/en/dev/streaming-query/streaming-query-formats?version=v26.1"
doc_path: "en/dev/streaming-query/streaming-query-formats"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/streaming-query/streaming-query-formats.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/streaming-query/streaming-query-formats.md"
description: "This section describes data formats for streaming queries supported in YDB when reading from topics, and supported YQL types for each format. Supported formats."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Topic read and write formats

This section describes data formats for [streaming queries](../../concepts/glossary.md#streaming-query) supported in YDB when reading from topics, and supported [YQL types](../../yql/reference/types/index.md) for each format.

## Supported formats {#formats}

YDB supports built-in formats (predefined defaults) and custom formats that you configure for specific tasks.

Built-in formats:

- [`csv_with_names`](streaming-query-formats.md#csv_with_names)
- [`tsv_with_names`](streaming-query-formats.md#tsv_with_names)
- [`json_list`](streaming-query-formats.md#json_list)
- [`json_each_row`](streaming-query-formats.md#json_each_row)
- [`json_as_string`](streaming-query-formats.md#json_as_string)
- [`parquet`](streaming-query-formats.md#parquet)
- [`raw`](streaming-query-formats.md#raw)

[Examples of parsing custom formats](streaming-query-formats.md#parsing).

In the examples on this page, `ydb_source` is a pre-created [external data source](../../concepts/datamodel/external_data_source.md), `input_topic` and `output_topic` are topics available through it, and `output_table` is a YDB table.

## Write formats {#write_formats}

When writing to a topic, `SELECT` must return a single column of type `String`, `Utf8`, `Json`, or `Yson`. The column cannot be `Optional`.

Single-column write:

```sql
CREATE STREAMING QUERY write_string_example AS
DO BEGIN

    INSERT INTO ydb_source.output_topic
    SELECT
        CAST(Data AS String)
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = raw,
        SCHEMA = (
            Data String
        )
    );

END DO
```

To write multiple columns, serialize them to JSON:

```sql
CREATE STREAMING QUERY write_json_example AS
DO BEGIN

    INSERT INTO ydb_source.output_topic
    SELECT
        ToBytes(Unwrap(Yson::SerializeJson(Yson::From(TableRow()))))
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = json_each_row,
        SCHEMA = (
            Id Uint64 NOT NULL,
            Name Utf8 NOT NULL
        )
    );

END DO
```

See also: [TableRow](../../yql/reference/builtins/basic.md#tablerow), [Yson::From](../../yql/reference/udf/list/yson.md#ysonfrom), [Yson::SerializeJson](../../yql/reference/udf/list/yson.md#ysonserializejson), [Unwrap](../../yql/reference/builtins/basic.md#unwrap), [ToBytes](../../yql/reference/builtins/basic.md#to-from-bytes).

## Read formats {#read_formats}

### `csv_with_names` {#csv_with_names}

Based on [CSV](https://en.wikipedia.org/wiki/Comma-separated_values). Values are comma-separated; the first line contains column names.

Example payload (one message):

```text
Year,Manufacturer,Model,Price
1997,Man_1,Model_1,3000.00
1999,Man_2,Model_2,4900.00
```

Example query:

```sql
CREATE STREAMING QUERY csv_example AS
DO BEGIN

    UPSERT INTO output_table
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = csv_with_names,
        SCHEMA = (
            Year Int32 NOT NULL,
            Manufacturer String NOT NULL,
            Model String NOT NULL,
            Price Double NOT NULL
        )
    );

END DO
```

### `tsv_with_names` {#tsv_with_names}

Based on [TSV](https://en.wikipedia.org/wiki/Tab-separated_values). Values are tab-separated (`0x9`); the first line contains column names.

Example payload (one message):

```text
Year    Manufacturer    Model   Price
1997    Man_1   Model_1    3000.00
1999    Man_2   Model_2    4900.00
```

Example query:

```sql
CREATE STREAMING QUERY tsv_example AS
DO BEGIN

    UPSERT INTO output_table
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = tsv_with_names,
        SCHEMA = (
            Year Int32 NOT NULL,
            Manufacturer String NOT NULL,
            Model String NOT NULL,
            Price Double NOT NULL
        )
    );

END DO
```

### `json_list` {#json_list}

Based on [JSON](https://en.wikipedia.org/wiki/JSON). Each message must be a JSON **array** of objects.

Valid example:

```json
[
    { "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 },
    { "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
]
```

Invalid example (separate objects per line, not wrapped in an array):

```json
{ "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 }
{ "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
```

Example query:

```sql
CREATE STREAMING QUERY json_list_example AS
DO BEGIN

    UPSERT INTO output_table
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = json_list,
        SCHEMA = (
            Year Int32 NOT NULL,
            Manufacturer String NOT NULL,
            Model String NOT NULL,
            Price Double NOT NULL
        )
    );

END DO
```

### `json_each_row` {#json_each_row}

Based on [JSON](https://en.wikipedia.org/wiki/JSON). Each message must be a single JSON **object**. Common for systems like Apache Kafka or [YDB topics](../../concepts/datamodel/topic.md).

Multiple separate JSON objects in one message are not supported; a JSON array is also not supported.

Valid example (one message):

```json
{ "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 }
```

Invalid example (two objects in one message):

```json
{ "Year": 1997, "Manufacturer": "Man_1", "Model": "Model_1", "Price": 3000.0 }
{ "Year": 1999, "Manufacturer": "Man_2", "Model": "Model_2", "Price": 4900.00 }
```

Example query:

```sql
CREATE STREAMING QUERY json_each_row_example AS
DO BEGIN

    UPSERT INTO output_table
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = json_each_row,
        SCHEMA = (
            Year Int32 NOT NULL,
            Manufacturer Utf8 NOT NULL,
            Model Utf8 NOT NULL,
            Price Double NOT NULL
        )
    );

END DO
```

### `json_as_string` {#json_as_string}

Based on [JSON](https://en.wikipedia.org/wiki/JSON).

Each message may contain:

- One JSON object per line in valid JSON representation;
- Or objects combined into a list.

`json_as_string` does not split the JSON document into fields; each message is one JSON object (or one line). Useful when the set of fields varies between rows.

Valid examples:

```json
{ "Year": 1997, "Attrs": { "Manufacturer": "Man_1", "Model": "Model_1" }, "Price": 3000.0 }
{ "Year": 1999, "Attrs": { "Manufacturer": "Man_2", "Model": "Model_2" }, "Price": 4900.00 }
```

In this format the schema must be a single column of an allowed type — see [below](streaming-query-formats.md#schema).

Example query:

```sql
CREATE STREAMING QUERY json_as_string_example AS
DO BEGIN

    INSERT INTO ydb_source.output_topic
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = json_as_string,
        SCHEMA = (
            Data Json
        )
    );

END DO
```

### `parquet`

Reads message payloads in [Apache Parquet](https://parquet.apache.org) format.

Example query:

```sql
CREATE STREAMING QUERY parquet_example AS
DO BEGIN

    UPSERT INTO output_table
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = parquet,
        SCHEMA = (
            Year Int32 NOT NULL,
            Manufacturer Utf8 NOT NULL,
            Model Utf8 NOT NULL,
            Price Double NOT NULL
        )
    );

END DO
```

### `raw`

Reads message payloads as raw bytes. Default schema: `SCHEMA(Data String)`.

Example query:

```sql
CREATE STREAMING QUERY raw_example AS
DO BEGIN

    INSERT INTO ydb_source.output_topic
    SELECT
        *
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = raw,
        SCHEMA = (
            Data String
        )
    );

END DO
```

### Supported schema types {#schema}

| Type | csv_with_names | tsv_with_names | json_list | json_each_row | json_as_string | parquet | raw |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Int8`, `Int16`, `Int32`, `Int64`,  <br>`Uint8`, `Uint16`, `Uint32`, `Uint64`,  <br>`Float`, `Double` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| `Bool` | ✓ | ✓ | ✓ | ✓ |  | ✓ |  |
| `DyNumber` |  |  |  |  |  |  |  |
| `String`, `Utf8` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `Json` |  |  |  |  | ✓ |  | ✓ |
| `JsonDocument` |  |  |  |  |  |  |  |
| `Yson` |  |  |  |  |  |  |  |
| `Uuid` |  |  |  | ✓ |  |  |  |
| `Date`, `Datetime`, `Timestamp`,  <br>`TzDate`, `TzDatetime`, `TzTimestamp` |  |  |  |  |  |  |  |
| `Interval` |  |  |  |  |  |  |  |
| `Date32`, `Datetime64`, `Timestamp64`,  <br>`Interval64`,  <br>`TzDate32`, `TzDatetime64`, `TzTimestamp64` |  |  |  |  |  |  |  |
| `Optional<T>` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Parsing custom formats {#parsing}

### JSON with built-in functions {#json_builtins}

Sample data:

```json
{"key": 1997, "value": "42"}
```

Example query:

```sql
CREATE STREAMING QUERY json_builtins_example AS
DO BEGIN

    INSERT INTO ydb_source.output_topic
    SELECT
        JSON_VALUE(Data, "$.key") AS Key,
        JSON_VALUE(Data, "$.value") AS Value
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = raw,
        SCHEMA = (
            Data Json
        )
    );

END DO
```

See [JSON_VALUE](../../yql/reference/builtins/json.md#json_value).

### JSON with Yson {#json_yson}

Sample data ([Change Data Capture](../../concepts/cdc.md) style):

```json
{"update":{"volume":10,"product":"bWlsaw=="},"key":[6],"ts":[1765192622420,18446744073709551615]}
```

Example query:

```sql
CREATE STREAMING QUERY json_yson_example AS
DO BEGIN

    $input = SELECT
        Yson::ConvertTo(
            Data, Struct<
                update: Struct<volume: Uint64>,
                key: List<Uint64>,
                ts: List<Uint64>
            >
        )
    FROM
        ydb_source.input_topic
    WITH (
        FORMAT = json_as_string,
        SCHEMA = (
            Data Json
        )
    );

    INSERT INTO ydb_source.output_topic
    SELECT
        ts[0] AS Ts,
        update.volume AS Volume
    FROM
        $input
    FLATTEN COLUMNS;

END DO
```

See also:

- [Yson::ConvertTo](../../yql/reference/udf/list/yson.md#ysonconvertto)
- [FLATTEN COLUMNS](../../yql/reference/syntax/select/flatten.md#flatten-columns).

### DSV (TSKV) {#dsv}

Sample data:

```text
name=Elena  uid=95792365232151958
name=Denis  uid=78086244452810046
name=Mikhail    uid=70609792906901286
```

Example query:

```sql
CREATE STREAMING QUERY dsv_example AS
DO BEGIN

    $input = SELECT
        Dsv::Parse(Data, "\t") AS Data
    FROM
        ydb_source.input_topic
    FLATTEN LIST BY (
        String::SplitToList(Data, "\n", TRUE AS SkipEmpty) AS Data
    );

    INSERT INTO ydb_source.output_topic
    SELECT
        DictLookup(Data, "name") AS Name,
        DictLookup(Data, "uid") AS Uid
    FROM
        $input;

END DO
```

See also:

- [String::SplitToList](../../yql/reference/udf/list/string.md#splittolist)
- [DictLookup](../../yql/reference/builtins/dict.md#dictlookup)
- [FLATTEN LIST BY](../../yql/reference/syntax/select/flatten.md#flatten-by).
