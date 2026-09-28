---
title: "DROP OBJECT (TYPE SECRET_ACCESS)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-object-type-secret-access?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-object-type-secret-access"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-object-type-secret-access.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-object-type-secret-access.md"
description: "Alert."
revision: "8c7501e02fd7c6de0c7110aafa90f78948400f1e"
---

# DROP OBJECT (TYPE SECRET_ACCESS)

> [!CAUTION]
> **This command is deprecated** and will be removed in future versions of YDB. The recommended syntax for working with secrets is described in the [Secrets](../../../concepts/datamodel/secrets.md) section.

Deletes the specified access rule for a [secret](../../../concepts/datamodel/secrets.md#secret_access).

If no rule with that name exists, an error is returned.

## Example

```yql
DROP OBJECT (TYPE SECRET_ACCESS) `MySecretName:another_user`;
```
