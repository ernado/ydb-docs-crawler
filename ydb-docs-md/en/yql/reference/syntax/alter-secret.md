---
title: "ALTER SECRET"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-secret.md"
description: "The ALTER SECRET statement modifies an existing secret. Syntax. ALTER SECRET secret_name WITH (option = value [,...])."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER SECRET

The `ALTER SECRET` statement modifies an existing [secret](../../../concepts/datamodel/secrets.md).

## Syntax

```sql
ALTER SECRET secret_name
WITH (option = value[, ...])
```

- `secret_name` — the name of the secret to modify.

- `option` — command option:

  - `value` — string with the secret value.

## Permissions

Modifying a secret requires the [right](grant.md#permissions-list) `ALTER SCHEMA`.

## Examples

Change the value of secret `secret_name` to `secret_value_new`:

```sql
ALTER SECRET secret_name WITH (value = "secret_value_new");
```

## See also

- [CREATE SECRET](create-secret.md)
- [DROP SECRET](drop-secret.md)
