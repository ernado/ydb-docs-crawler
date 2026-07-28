---
title: "CREATE OBJECT (TYPE SECRET_ACCESS)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-object-type-secret-access?version=v26.1"
doc_path: "en/yql/reference/syntax/create-object-type-secret-access"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-object-type-secret-access.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-object-type-secret-access.md"
description: "Alert."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE OBJECT (TYPE SECRET_ACCESS)

> [!CAUTION]
> **This command is deprecated** and will be removed in future versions of YDB. The recommended syntax for working with secrets is described in the [Secrets](../../../concepts/datamodel/secrets.md) section.

All rights to use a secret belong to the secret's creator. The creator can grant another user read access to the secret through secret access management.

Access to secrets is managed using special `SECRET_ACCESS` objects. To grant permission to use the secret `secret_name` to the user `user_name`, create a `SECRET_ACCESS` object named `secret_name:user_name`.

```yql
CREATE OBJECT `secret_name:user_name` (TYPE SECRET_ACCESS);
```

Where:

- `secret_name` — the name of the [secret](create-object-type-secret.md).
- `user_name` — the name of the user who receives access.

## Example

The following statement grants access to the secret `MySecretName` to the user `another_user`:

```yql
CREATE OBJECT `MySecretName:another_user` (TYPE SECRET_ACCESS);
```
