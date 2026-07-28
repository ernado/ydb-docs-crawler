---
title: "CREATE SECRET"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/create-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-secret.md"
description: "The CREATE SECRET statement creates a secret. Syntax. CREATE SECRET secret_name WITH (option = value [,...]). secret_name — the name of the secret to create."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE SECRET

The `CREATE SECRET` statement creates a [secret](../../../concepts/datamodel/secrets.md).

## Syntax

```sql
CREATE SECRET secret_name
WITH (option = value[, ...])
```

- `secret_name` — the name of the secret to create.

- `option` — command option:

  - `value` — string with the secret value.
  - `inherit_permissions` — when enabled, [rights](grant.md) on the secret are inherited from the directory where the secret is created. When disabled, only the [right](grant.md#permissions-list) `DESCRIBE SCHEMA` is inherited from the directory. The secret owner gets all possible rights on it in any case. Default is `False`.

## Permissions

Creating a secret requires the [right](grant.md#permissions-list) `CREATE TABLE`.

## Examples

Create a secret in the database root named `secret_name` with value `secret_value`:

```sql
CREATE SECRET secret_name WITH (value = "secret_value");
```

Create a secret in directory `dir` in the database root named `secret_name` with value `secret_value`. If directory `dir` does not exist, it will be created:

```sql
CREATE SECRET `dir/secret_name` WITH (value = "secret_value");
```

Create a secret in the database root named `secret_name` with value `secret_value` with the same rights as the secret's parent directory:

```sql
CREATE SECRET secret_name WITH (value = "secret_value", inherit_permissions = True);
```

## See also

- [ALTER SECRET](alter-secret.md)
- [DROP SECRET](drop-secret.md)
