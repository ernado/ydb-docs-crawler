---
title: "UPSERT OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/upsert-object-type-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/upsert-object-type-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/upsert-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/upsert-object-type-secret.md"
description: "Warning. The syntax for managing secrets will change in future YDB releases. To change the contents of a secret, use the following statement:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# UPSERT OBJECT (TYPE SECRET)

> [!WARNING]
> The syntax for managing secrets will change in future YDB releases.

To change the contents of a [secret](../../../concepts/datamodel/secrets.md), use the following statement:

```yql
UPSERT OBJECT `secret_name` (TYPE SECRET) WITH value = `secret_value`;
```

Where:

- `secret_name` — Name of the secret.
- `secret_value` — Secret payload.

## Example

The following statement sets the secret named `MySecretName` to `MySecretData`:

```yql
UPSERT OBJECT `MySecretName` (TYPE SECRET) WITH value = `MySecretData`;
```
