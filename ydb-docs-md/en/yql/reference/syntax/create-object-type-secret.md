---
title: "CREATE OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-object-type-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/create-object-type-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-object-type-secret.md"
description: "Alert."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE OBJECT (TYPE SECRET)

> [!CAUTION]
> **This command is deprecated** and will be removed in future versions of YDB. The recommended syntax for working with secrets is described in the [Secrets](../../../concepts/datamodel/secrets.md) section.

The following SQL statement creates a [secret](../../../concepts/datamodel/secrets.md):

```yql
CREATE OBJECT <secret_name> (TYPE SECRET) WITH value = "<secret_value>";
```

Where:

- `secret_name` - the name of the secret.
- `secret_value` - the contents of the secret.

## Example {#examples}

The following statement creates a secret named `MySecretName` with `MySecretData` as a value.

```yql
CREATE OBJECT MySecretName (TYPE SECRET) WITH value = "MySecretData";
```
