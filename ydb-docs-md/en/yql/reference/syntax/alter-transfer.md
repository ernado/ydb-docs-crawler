---
title: "ALTER TRANSFER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-transfer?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-transfer"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-transfer.md"
description: "The ALTER TRANSFER statement modifies the parameters and state of a transfer instance. Syntax."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER TRANSFER

The `ALTER TRANSFER` statement modifies the parameters and state of a [transfer](../../../concepts/transfer.md) instance.

## Syntax

```yql
ALTER TRANSFER <name> [SET USING lambda | SET (option = value [, ...])]
```

where:

- `name` — the name of the transfer instance.
- `lambda` — the [lambda-function](alter-transfer.md#lambda) for message transformation.
- `SET (option = value [, ...])` — the transfer [parameters](alter-transfer.md#params).

### Parameters {#params}

- `STATE` — the transfer [state](../../../concepts/transfer.md#pause-and-resume). Possible values:

- `PAUSED` — pauses the transfer.

- `ACTIVE` — resumes a paused transfer.

- Table write batching parameters let you balance the latency of records appearing in the table against the resources required by the transfer. Batching parameters affect the processing of each topic partition independently. Change batching parameters with caution, as this can either improve or degrade message stream processing speed, and may even lead to a denial of service if the parameters are misconfigured. For example, writing to the table in small batches can overload the table and degrade its performance, while an excessively large batch size can cause the server to run out of available memory.

  - `BATCH_SIZE_BYTES` — the batch size in bytes. Default: 8 MB.
  - `FLUSH_INTERVAL` — the table write interval. Default: 60 seconds. Data is written to the table at this interval, even if the batch has not reached the size specified in the `BATCH_SIZE_BYTES` parameter.

- Authentication settings for the topic database (one of the following):

  - Using a [token](../../../recipes/ydb-sdk/auth-access-token.md):

    - `TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the token.

  - Using a [username and password](../../../recipes/ydb-sdk/auth-static.md):

    - `USER` — the username.
    - `PASSWORD_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the password.

  - Using a [delegated service account](https://yandex.cloud/ru/docs/iam/concepts/service-control):

    - `SERVICE_ACCOUNT_ID` — the identificator of the service account.
    - `INITIAL_TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the account's token. It is used for initial authentication.

## Permissions

Modifying a transfer requires the `ALTER SCHEMA` [permissions](grant.md#permissions-list).

## Examples

The following query modifies the message transformation [lambda-function](expressions.md#lambda):

```yql
$new_lambda = ($msg) -> {
    return [
        <|
            partition: $msg._partition,
            offset: $msg._offset,
            message: CAST($msg._data || ' altered' AS Utf8)
        |>
    ];
};

ALTER TRANSFER my_transfer SET USING $new_lambda;
```

The following query pauses the transfer:

```yql
ALTER TRANSFER my_transfer SET (STATE = "PAUSED");
```

The following query modifies the batching parameters:

```yql
ALTER TRANSFER my_transfer SET (
    BATCH_SIZE_BYTES = 1048576,
    FLUSH_INTERVAL = Interval('PT60S')
);
```

The following query changes the secret:

```yql
ALTER TRANSFER my_transfer SET (
    TOKEN_SECRET_PATH = "my_token"
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

- [CREATE TRANSFER](create-transfer.md)
- [DROP TRANSFER](drop-transfer.md)
- [Data transfer](../../../concepts/transfer.md)
