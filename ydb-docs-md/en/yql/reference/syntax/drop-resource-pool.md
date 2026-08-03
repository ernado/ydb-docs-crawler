---
title: "DROP RESOURCE POOL"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-resource-pool?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-resource-pool"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-resource-pool.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-resource-pool.md"
description: "DROP RESOURCE POOL removes a resource pool. Syntax. DROP RESOURCE POOL <name>. Parameters. name — name of the resource pool to drop. Permissions."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP RESOURCE POOL

`DROP RESOURCE POOL` removes a [resource pool](../../../concepts/glossary.md#resource-pool).

## Syntax

```yql
DROP RESOURCE POOL <name>
```

### Parameters

- `name` — name of the resource pool to drop.

## Permissions

The `REMOVE SCHEMA` [permission](grant.md#permissions-list) on the pool under `.metadata/workload_manager/pools` is required. Example:

```yql
GRANT 'REMOVE SCHEMA' ON `.metadata/workload_manager/pools` TO `user1@domain`;
```

## Examples

The following removes the resource pool named `olap`:

```yql
DROP RESOURCE POOL olap;
```

## See also

- [Workload Manager — resource consumption management](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL](create-resource-pool.md)
- [ALTER RESOURCE POOL](alter-resource-pool.md)
