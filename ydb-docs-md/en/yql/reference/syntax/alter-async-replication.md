---
title: "ALTER ASYNC REPLICATION"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-async-replication?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-async-replication"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-async-replication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-async-replication.md"
description: "The ALTER ASYNC REPLICATION statement modifies the status and parameters of an asynchronous replication instance. Syntax."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER ASYNC REPLICATION

The `ALTER ASYNC REPLICATION` statement modifies the status and parameters of an [asynchronous replication instance](../../../concepts/async-replication.md).

## Syntax

```yql
ALTER ASYNC REPLICATION <name> SET (option = value [, ...])
```

### Parameters {#params}

- `name` — a name of the asynchronous replication instance.

- `SET (option = value [, ...])` — asynchronous replication parameters:

  - `STATE` — the state of asynchronous replication. This parameter can only be used in combination with the `FAILOVER_MODE` parameter (see below). Valid values are:

    - `DONE` — [completion of the asynchronous replication process](../../../concepts/async-replication.md#done).

  - `FAILOVER_MODE` — the mode for changing the replication state. This parameter can only be used in combination with the `STATE` parameter. Valid values are:

    - `FORCE` — forced failover.

- Authentication settings for the source database (one of the following):

  - Using a [token](../../../recipes/ydb-sdk/auth-access-token.md):

    - `TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the token.

  - Using a [username and password](../../../recipes/ydb-sdk/auth-static.md):

    - `USER` — the username.
    - `PASSWORD_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the password.

  - Using a [delegated service account](https://yandex.cloud/ru/docs/iam/concepts/service-control):

    - `SERVICE_ACCOUNT_ID` — the identificator of the service account.
    - `INITIAL_TOKEN_SECRET_PATH` — the [secret](../../../concepts/datamodel/secrets.md) that contains the account's token. It is used for initial authentication.

## Examples

The following statement forces the asynchronous replication process to complete:

```yql
ALTER ASYNC REPLICATION my_replication SET (STATE = "DONE", FAILOVER_MODE = "FORCE");
```

The following query changes the secret:

```yql
ALTER ASYNC REPLICATION my_replication SET (TOKEN_SECRET_PATH = "my_token");
```

## See also

- [CREATE ASYNC REPLICATION](create-async-replication.md)
- [DROP ASYNC REPLICATION](drop-async-replication.md)
