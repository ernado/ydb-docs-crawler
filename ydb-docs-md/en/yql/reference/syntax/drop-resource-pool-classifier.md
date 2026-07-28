---
title: "DROP RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-resource-pool-classifier?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-resource-pool-classifier"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-resource-pool-classifier.md"
description: "DROP RESOURCE POOL CLASSIFIER removes a resource pool classifier. Syntax. DROP RESOURCE POOL CLASSIFIER <name>. Parameters."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DROP RESOURCE POOL CLASSIFIER

`DROP RESOURCE POOL CLASSIFIER` removes a [resource pool classifier](../../../concepts/glossary.md#resource-pool-classifier).

## Syntax

```yql
DROP RESOURCE POOL CLASSIFIER <name>
```

### Parameters

- `name` — name of the resource pool classifier to drop.

## Permissions

The `ALL` [permission](grant.md#permissions-list) on the database is required. Example:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Examples

The following removes the classifier named `olap_classifier`:

```yql
DROP RESOURCE POOL CLASSIFIER olap_classifier;
```

## See also

- [Workload Manager — resource consumption management](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL CLASSIFIER](create-resource-pool-classifier.md)
- [ALTER RESOURCE POOL CLASSIFIER](alter-resource-pool-classifier.md)
