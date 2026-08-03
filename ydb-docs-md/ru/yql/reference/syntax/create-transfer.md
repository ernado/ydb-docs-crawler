---
title: "CREATE TRANSFER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-transfer?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-transfer"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-transfer.md"
description: "Создает трансфер из топика в таблицу. Синтаксис: CREATE TRANSFER transfer_name FROM topic_name TO table_name USING lambda WITH ( option = value[,...])."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CREATE TRANSFER

Создает [трансфер](../../../concepts/transfer.md) из [топика](../../../concepts/datamodel/topic.md) в [таблицу](../../../concepts/datamodel/table.md).

Синтаксис:

```yql
CREATE TRANSFER transfer_name 
FROM topic_name TO table_name USING lambda
WITH (option = value[, ...])
```

- `transfer_name` — имя создаваемого трансфера.

- `topic_name` — имя топика, содержащего исходные сообщения для последующего преобразования и записи в таблицу.

- `table_name` — имя таблицы, в которую будут записываться данные.

- `lambda` — [lambda-функция](create-transfer.md#lambda) преобразования сообщений.

- `option` — опция команды:

  - `CONNECTION_STRING` — [строка соединения](../../../concepts/connect.md#connection_string) с базой данных, содержащей топик. Указывается только если топик находится в другой базе YDB.

  - Настройки для аутентификации в базе топика одним из способов (обязательно, если топик находится в другой базе):

    - С помощью [токена](../../../recipes/ydb-sdk/auth-access-token.md):

      - `TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен.

    - С помощью [логина и пароля](../../../recipes/ydb-sdk/auth-static.md):

      - `USER` — имя пользователя.
      - `PASSWORD_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий пароль.

    - С помощью [делегированного сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/service-control):

      - `SERVICE_ACCOUNT_ID` — идентификатор сервисного аккаунта.
      - `INITIAL_TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен от сервисного аккаунта. Используется для первоначальной инициализации.

  - `CONSUMER` — имя [читателя](../../../concepts/datamodel/topic.md#consumer) топика-источника. Если имя задано, то в топике уже должен [существовать](alter-topic.md#add-consumer) читатель с указанным именем, и трансфер начнёт обрабатывать сообщения, начиная с первого незакоммиченного сообщения в топике. Если имя не задано, то читатель будет добавлен в топик автоматически, и трансфер начнёт обрабатывать сообщения, начиная с первого хранящегося сообщения в топике. Имя автоматически созданного читателя можно получить из [описания](../../../reference/ydb-cli/commands/scheme-describe.md) экземпляра трансфера.

  - Параметры батчевания записи в таблицу позволяют настроить баланс между задержкой появления записей в таблице и ресурсами, требуемыми для работы трансфера. Параметры батчевания влияют на обработку каждой партиции топика независимо. К изменению параметров батчевания нужно подходить с осторожностью, так как их изменение может как улучшить скорость обработки потока сообщений, так и ухудшить её, и даже привести к отказу в обслуживании, если параметры будут подобраны неверно. Например, запись в таблицу маленькими по размеру батчами может привести к перегрузке таблицы и деградации скорости работы с ней, а слишком большой размер батча — к тому, что на сервере закончится вся доступная память.

    - `BATCH_SIZE_BYTES` — размер батча в байтах. По умолчанию — 8 МБ.
    - `FLUSH_INTERVAL` — периодичность записи в таблицу. По умолчанию — 60 секунд. Запись в таблицу будет осуществлена, даже если батч не достиг размера, заданного в параметре `BATCH_SIZE_BYTES`.

  -

## Разрешения {#razresheniya}

Для создания трансфера требуются следующие [права](grant.md#permissions-list):

- `CREATE TABLE` — для создания экземпляра трансфера;
- `ALTER SCHEMA` — для автоматического создания читателя топика (если применимо);
- `SELECT ROW` — для чтения сообщений из топика, содержащего исходные сообщения;
- `UPDATE ROW` — для обновления строк в таблице, в которую будут записываться данные.

## Примеры {#examples}

Создание экземпляра трансфера из топика `example_topic` в таблицу `example_table` текущей базы данных:

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

Создание экземпляра трансфера из топика `example_topic` базы данных `/Root/another_database` в таблицу `example_table` текущей базы данных. Перед созданием трансфера необходимо в текущей базе создать таблицу в которую будут записываться данные; в базе данных `/Root/another_database` создать топик, из которого будут обрабатываться сообщения:

> [!TIP]
> Перед выполнением операции [создайте](create-secret.md) секрет с аутентификационными данными для подключения или убедитесь в его существовании и наличии доступа к нему.

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

Создание экземпляра трансфера с явным указанием имени консьюмера `existing_consumer_of_topic`:

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

Пример обработки сообщения в формате JSON

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

Создание экземпляра трансфера с явным указанием опции батчевания:

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

## lambda-функция {#lambda}

[Lambda-функция](expressions.md#lambda) преобразования сообщений принимает один параметр со структурой, содержащей сообщение из топика, и возвращает список структур, соответствующих строкам таблицы для вставки.

Пример:

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

В этом примере:

- `$msg` — сообщение, полученное из топика.
- `column_1` и `column_2` — названия колонок таблицы.
- `$msg._create_timestamp` и `$msg._data` — значения, которые будут записаны в таблицу. Типы значений должны совпадать с типами колонок таблицы. Например, если `column_2` имеет в таблице тип `String`, то и тип `$msg._data` должен быть именно `String`.

У сообщения топика доступны следующие поля:

| Атрибут | Тип значения | Описание |
| --- | --- | --- |
| `_create_timestamp` | `Timestamp` | Время создания сообщения |
| `_data` | `String` | Тело сообщения |
| `_offset` | `Uint64` | [Смещение сообщения](../../../concepts/glossary.md#offset) |
| `_partition` | `Uint32` | Номер [партиции](../../../concepts/glossary.md#partition) сообщения |
| `_producer_id` | `String` | Идентификатор [писателя](../../../concepts/glossary.md#producer) |
| `_seq_no` | `Uint64` | Порядковый номер сообщения |
| `_write_timestamp` | `Timestamp` | Время записи сообщения |

### Тестирование lambda-функций {#testirovanie-lambda-funkcij}

Для тестирования lambda-функции при её разработке можно в качестве сообщения топика передавать структуру с такими же полями, как будут передаваться в трансфере. Пример:

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

Если lambda-функция содержит сложную логику преобразования, то её можно выделить в отдельную lambda-функцию, что упростит тестирование.

```yql
$extract_value = ($data) -> {
  -- сложные преобразования
  return $data;
};

$lambda = ($msg) -> {
  return [
    <|
      column: $extract_value($msg._data)
    |>
  ];
};

-- Тестировать lambda-функцию extract_value можно так

SELECT $extract_value('преобразуемое значение');
```

## См. также {#sm-takzhe}

- [ALTER TRANSFER](alter-transfer.md)
- [DROP TRANSFER](drop-transfer.md)
- [Трансфер данных](../../../concepts/transfer.md)
