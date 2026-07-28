---
title: "ALTER TRANSFER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-transfer?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-transfer"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-transfer.md"
description: "Вызов ALTER TRANSFER изменяет параметры и состояние экземпляра трансфера. Синтаксис. ALTER TRANSFER <name> [ SET USING lambda | SET ( option = value [,...])]."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER TRANSFER

Вызов `ALTER TRANSFER` изменяет параметры и состояние экземпляра [трансфера](../../../concepts/transfer.md).

## Синтаксис {#syntax}

```yql
ALTER TRANSFER <name> [SET USING lambda | SET (option = value [, ...])]
```

где:

- `name` — имя экземпляра трансфера.
- `lambda` — [lambda-функция](alter-transfer.md#lambda) преобразования сообщений.
- `SET (option = value [, ...])` — [параметры](alter-transfer.md#params) трансфера.

### Параметры {#params}

- `STATE` — [состояние](../../../concepts/transfer.md#pause-and-resume) трансфера. Возможные значения:

  - `PAUSED` — остановка трансфера.
  - `ACTIVE` — возобновление работы трансфера после приостановки.

- Параметры батчевания записи в таблицу позволяют настроить баланс между задержкой появления записей в таблице и ресурсами, требуемыми для работы трансфера. Параметры батчевания влияют на обработку каждой партиции топика независимо. К изменению параметров батчевания нужно подходить с осторожностью, так как их изменение может как улучшить скорость обработки потока сообщений, так и ухудшить её, и даже привести к отказу в обслуживании, если параметры будут подобраны неверно. Например, запись в таблицу маленькими по размеру батчами может привести к перегрузке таблицы и деградации скорости работы с ней, а слишком большой размер батча — к тому, что на сервере закончится вся доступная память.

  - `BATCH_SIZE_BYTES` — размер батча в байтах. По умолчанию — 8 МБ.
  - `FLUSH_INTERVAL` — периодичность записи в таблицу. По умолчанию — 60 секунд. Запись в таблицу будет осуществлена, даже если батч не достиг размера, заданного в параметре `BATCH_SIZE_BYTES`.

- Настройки для аутентификации в базе топика одним из способов:

  - С помощью [токена](../../../recipes/ydb-sdk/auth-access-token.md):

    - `TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен.

  - С помощью [логина и пароля](../../../recipes/ydb-sdk/auth-static.md):

    - `USER` — имя пользователя.
    - `PASSWORD_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий пароль.

  - С помощью [делегированного сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/service-control):

    - `SERVICE_ACCOUNT_ID` — идентификатор сервисного аккаунта.
    - `INITIAL_TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен от сервисного аккаунта. Используется для первоначальной инициализации.

## Разрешения {#razresheniya}

Для изменения трансфера требуется [право](grant.md#permissions-list) изменять схемные объекты (`ALTER SCHEMA`).

## Примеры {#examples}

Следующий запрос изменяет [lambda-функцию](expressions.md#lambda) преобразования сообщений топика:

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

Следующий запрос временно приостанавливает работу трансфера:

```yql
ALTER TRANSFER my_transfer SET (STATE = "PAUSED");
```

Следующий запрос изменяет параметры батчевания:

```yql
ALTER TRANSFER my_transfer SET (
    BATCH_SIZE_BYTES = 1048576,
    FLUSH_INTERVAL = Interval('PT60S')
);
```

Следующий запрос изменяет секрет:

```yql
ALTER TRANSFER my_transfer SET (
    TOKEN_SECRET_PATH = "my_token"
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

- [CREATE TRANSFER](create-transfer.md)
- [DROP TRANSFER](drop-transfer.md)
- [Трансфер данных](../../../concepts/transfer.md)
