---
title: "ALTER ASYNC REPLICATION"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-async-replication?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-async-replication"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-async-replication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-async-replication.md"
description: "Вызов ALTER ASYNC REPLICATION изменяет параметры и состояние экземпляра асинхронной репликации. Синтаксис."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER ASYNC REPLICATION

Вызов `ALTER ASYNC REPLICATION` изменяет параметры и состояние экземпляра [асинхронной репликации](../../../concepts/async-replication.md).

## Синтаксис {#syntax}

```yql
ALTER ASYNC REPLICATION <name> SET (option = value [, ...])
```

где:

- `name` — имя экземпляра асинхронной репликации.
- `SET (option = value [, ...])` — [параметры](alter-async-replication.md#params) асинхронной репликации.

### Параметры {#params}

- `STATE` — состояние асинхронной репликации. Применимо только совместно с параметром `FAILOVER_MODE` (см. ниже). Возможные значения:

  - `DONE` — [завершение процесса асинхронной репликации](../../../concepts/async-replication.md#done).

- `FAILOVER_MODE` — режим переключения состояния. Применимо только совместно с параметром `STATE`. Возможные значения:

  - `FORCE` — принудительное переключение состояния.

- Настройки для аутентификации в базе-источнике одним из способов:

  - С помощью [токена](../../../recipes/ydb-sdk/auth-access-token.md):

    - `TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен.

  - С помощью [логина и пароля](../../../recipes/ydb-sdk/auth-static.md):

    - `USER` — имя пользователя.
    - `PASSWORD_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий пароль.

  - С помощью [делегированного сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/service-control):

    - `SERVICE_ACCOUNT_ID` — идентификатор сервисного аккаунта.
    - `INITIAL_TOKEN_SECRET_PATH` — [секрет](../../../concepts/datamodel/secrets.md), содержащий токен от сервисного аккаунта. Используется для первоначальной инициализации.

## Примеры {#examples}

Следующий запрос принудительно завершит процесс асинхронной репликации:

```yql
ALTER ASYNC REPLICATION my_replication SET (STATE = "DONE", FAILOVER_MODE = "FORCE");
```

Следующий запрос изменяет секрет:

```yql
ALTER ASYNC REPLICATION my_replication SET (TOKEN_SECRET_PATH = "my_token");
```

## См. также {#sm-takzhe}

- [CREATE ASYNC REPLICATION](create-async-replication.md)
- [DROP ASYNC REPLICATION](drop-async-replication.md)
