---
title: "DROP SECRET"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-secret.md"
description: "The DROP SECRET statement deletes an existing secret. Syntax. DROP SECRET secret_name. secret_name — the name of the secret to delete. Permissions."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP SECRET

The `DROP SECRET` statement deletes an existing [secret](../../../concepts/datamodel/secrets.md).

## Syntax

```sql
DROP SECRET secret_name
```

- `secret_name` — the name of the secret to delete.

## Permissions

Deleting a secret requires the [rights](grant.md#permissions-list) `REMOVE SCHEMA` and `ALTER SCHEMA`.

## Examples

Delete the secret named `secret_name`:

```sql
DROP SECRET secret_name;
```

## See also

- [CREATE SECRET](create-secret.md)
- [ALTER SECRET](alter-secret.md)
