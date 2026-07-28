---
title: "DROP TRANSFER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-transfer?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-transfer"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-transfer.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-transfer.md"
description: "The DROP TRANSFER statement deletes a transfer instance. If a consumer was created automatically when the transfer was created, it is also deleted. The system w"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP TRANSFER

The `DROP TRANSFER` statement deletes a [transfer](../../../concepts/transfer.md) instance. If a [consumer](../../../concepts/datamodel/topic.md#consumer) was created automatically when the transfer was created, it is also deleted. The system will keep trying to delete the consumer until the operation is successful.

The `DROP TRANSFER` statement does not delete the destination table or the source topic.

## Syntax

```yql
DROP TRANSFER <name>
```

where:

- `name` — the name of the transfer instance.

## Permissions

The following [permissions](grant.md#permissions-list) are required to delete a transfer:

- `REMOVE SCHEMA` — to delete the transfer instance;
- `ALTER SCHEMA` — to delete the automatically created topic consumer (if applicable).

## Examples

The following query deletes the transfer named `my_transfer`:

```yql
DROP TRANSFER my_transfer;
```

## See Also

- [CREATE TRANSFER](create-transfer.md)
- [ALTER TRANSFER](alter-transfer.md)
- [Data transfer](../../../concepts/transfer.md)
