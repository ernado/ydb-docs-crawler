---
title: "DROP OBJECT (TYPE SECRET)"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-object-type-secret?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-object-type-secret"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-object-type-secret.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-object-type-secret.md"
description: "Alert."
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# DROP OBJECT (TYPE SECRET)

> [!CAUTION]
> **This command is deprecated** and will be removed in future versions of YDB. The recommended syntax for working with secrets is described in the [Secrets](../../../concepts/datamodel/secrets.md) section.

Deletes the specified [secret](../../../concepts/datamodel/secrets.md).

If no secret with that name exists, an error is returned.

## Example

```yql
DROP OBJECT my_secret (TYPE SECRET);
```
