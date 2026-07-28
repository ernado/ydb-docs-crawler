---
title: "CREATE TRANSFER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-transfer?version=v26.1"
doc_path: "en/yql/reference/syntax/create-transfer"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-transfer.md"
description: "Creates a transfer from a topic to a table. Syntax: CREATE TRANSFER transfer_name FROM topic_name TO table_name USING lambda WITH ( option = value[,...])."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE TRANSFER

Creates a [transfer](../../../concepts/transfer.md) from a [topic](../../../concepts/datamodel/topic.md) to a [table](../../../concepts/datamodel/table.md).

Syntax:

```yql
CREATE TRANSFER transfer_name 
FROM topic_name TO table_name USING lambda
WITH (option = value[, ...])
```

- `transfer_name` — the name of the transfer to be created.

- `topic_name` — the name of the topic containing the source messages for transformation and writing to the table.

- `table_name` — the name of the table where the data will be written.

- `lambda` — [lambda-function](create-transfer.md#lambda) for message transformation.

- `option` — a command option:

  - `CONNECTION_STRING` — [the connection string](../../../concepts/connect.md#connection_string) to the database containing the topic. This is only specified if the topic is located in a different YDB database.

  - Authentication settings for the topic's database (required if the topic is in another database), using one of the following methods:

    - Using a [token](../../../recipes/ydb-sdk/auth-access-token.md):

      - `TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the token.

    - Using a [username and password](../../../recipes/ydb-sdk/auth-static.md):

      - `USER` — the username.
      - `PASSWORD_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the password.

    - Using a [delegated service account](https://yandex.cloud/ru/docs/iam/concepts/service-control):

      - `SERVICE_ACCOUNT_ID` — the identificator of the service account.
      - `INITIAL_TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the account's token. It is used for initial authentication.

  - `CONSUMER` — the name of the source topic [consumer](../../../concepts/datamodel/topic.md#consumer). If a name is specified, a consumer with that name must already [exist](alter-topic.md#add-consumer) in the topic, and the transfer will start processing messages from the first uncommitted message in the topic. If no name is specified, a consumer will be added to the topic automatically, and the transfer will start processing messages from the first message stored in the topic. The name of the automatically created consumer can be obtained from the [description](../../../reference/ydb-cli/commands/scheme-describe.md) of the transfer instance.

  - Table write batching parameters let you balance the latency of records appearing in the table against the resources required by the transfer. Batching parameters affect the processing of each topic partition independently. Change batching parameters with caution, as this can either improve or degrade message stream processing speed, and may even lead to a denial of service if the parameters are misconfigured. For example, writing to the table in small batches can overload the table and degrade its performance, while an excessively large batch size can cause the server to run out of available memory.

    - `BATCH_SIZE_BYTES` — the batch size in bytes. Default: 8 MB.
    - `FLUSH_INTERVAL` — the table write interval. Default: 60 seconds. Data is written to the table at this interval, even if the batch has not reached the size specified in the `BATCH_SIZE_BYTES` parameter.

## Permissions

The following [permissions](grant.md#permissions-list) are required to create a transfer:

- `CREATE TABLE` — to create a transfer instance;
- `ALTER SCHEMA` — to automatically create a topic consumer (if applicable);
- `SELECT ROW` — to read messages from the source topic;
- `UPDATE ROW` — to update rows in the destination table.

## Examples

Creating a transfer instance from the `example_topic` topic to the `example_table` table in the current database:

```yql
CREATE TABLE example_table (
    partition Uint32 NOT NULL,
    offset Uint64 NOT NULL,
    message Utf8,
    PRIMARY KEY (partition, offset)
);

CREATE TOPIC example_topic;

$transformation_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            message: CAST($msg._data AS Utf8)
        |>
    ];
};

CREATE TRANSFER example_transfer
    FROM example_topic TO example_table USING $transformation_lambda;
```

Creating a transfer instance from the `example_topic` topic in the `/Root/another_database` database to the `example_table` table in the current database. Before creating the transfer, you need to create the destination table in the current database and create the source topic in the `/Root/another_database` database:

> [!TIP]
> Before performing the operation, [create](create-secret.md) a secret with authentication credentials to connect, or make sure it exists and you have access to it.

```yql
$transformation_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            message: CAST($msg._data AS Utf8)
        |>
    ];
};

CREATE TRANSFER example_transfer
    FROM example_topic TO example_table USING $transformation_lambda
WITH (
    CONNECTION_STRING = 'grpcs://example.com:2135/?database=/Root/another_database',
    TOKEN_SECRET_PATH = 'my_secret'
);
```

Creating a transfer instance and explicitly specifying the consumer `existing_consumer_of_topic`:

```yql
$transformation_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            message: CAST($msg._data AS Utf8)
        |>
    ];
};
CREATE TRANSFER example_transfer
    FROM example_topic TO example_table USING $transformation_lambda
WITH (
    CONSUMER = 'existing_consumer_of_topic'
);
```

Example of processing a message in JSON format:

```yql
// example message:
// {
//   "update": {
//     "operation":"value_1"
//   },
//   "key": [
//     "id_1",
//     "2019-01-01T15:30:00.000000Z"
//   ]
// }

$transformation_lambda = ($msg) -> {
    $json = CAST($msg._data AS JSON);
    return [
        <|
            timestamp: CAST(Yson::ConvertToString($json.key[1]) AS Timestamp),
            object_id: CAST(Yson::ConvertToString($json.key[0]) AS Utf8),
            operation: CAST(Yson::ConvertToString($json.update.operation) AS Utf8)
        |>
    ];
};

CREATE TRANSFER example_transfer
    FROM example_topic TO example_table USING $transformation_lambda;
```

Creating a transfer instance and explicitly specifying the batching option:

```yql
$transformation_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            message: CAST($msg._data AS Utf8)
        |>
    ];
};
CREATE TRANSFER example_transfer
    FROM example_topic TO example_table USING $transformation_lambda
WITH (
    BATCH_SIZE_BYTES = 1048576,
    FLUSH_INTERVAL = Interval('PT60S')
);
```

## Lambda function {#lambda}

A message transformation [lambda function](expressions.md#lambda) takes a single structured parameter containing the message from the topic and returns a list of structures corresponding to the table rows for insertion.

Example:

```yql
$lambda = ($msg) -> {
  return [
    <|
      column_1: $msg._create_timestamp,
      column_2: $msg._data
    |>
  ];
};
```

In this example:

- `$msg` — the message received from the topic.
- `column_1` and `column_2` — the names of the table columns.
- `$msg._create_timestamp` and `$msg._data` — the values that will be written to the table. The value types must match the table column types. For example, if the `column_2` table column has the `String` type, the type of `$msg._data` must also be `String`.

The following fields are available in a topic message:

| Attribute | Value type | Description |
| --- | --- | --- |
| `_create_timestamp` | `Timestamp` | Message creation time |
| `_data` | `String` | Message body |
| `_offset` | `Uint64` | [Message offset](../../../concepts/glossary.md#offset) |
| `_partition` | `Uint32` | Message's [partition](../../../concepts/glossary.md#partition) number |
| `_producer_id` | `String` | [Producer](../../../concepts/glossary.md#producer) ID |
| `_seq_no` | `Uint64` | Message sequence number |
| `_write_timestamp` | `Timestamp` | Message write time |

### Testing lambda functions

To test a lambda function during development, you can simulate a topic message by passing a structure with the same fields that the transfer will provide. Example:

```yql
$lambda = ($msg) -> {
  return [
    <|
      offset: $msg._offset,
      data: $msg._data
    |>
  ];
};

$msg = <|
  _data: "value",
  _offset: CAST(1 AS Uint64),
  _partition: CAST(2 AS Uint32),
  _producer_id: "producer",
  _seq_no: CAST(3 AS Uint64)
|>;

SELECT $lambda($msg);
```

If a lambda function contains complex transformation logic, you can extract it into a separate lambda function to simplify testing.

```yql
$extract_value = ($data) -> {
  -- complex transformations
  return $data;
};

$lambda = ($msg) -> {
  return [
    <|
      column: $extract_value($msg._data)
    |>
  ];
};

-- You can test the extract_value lambda function like this

SELECT $extract_value('converted value');
```

## See Also

- [ALTER TRANSFER](alter-transfer.md)
- [DROP TRANSFER](drop-transfer.md)
- [Data transfer](../../../concepts/transfer.md)
