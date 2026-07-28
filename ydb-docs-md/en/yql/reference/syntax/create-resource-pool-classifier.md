---
title: "CREATE RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/create-resource-pool-classifier?version=v26.1"
doc_path: "en/yql/reference/syntax/create-resource-pool-classifier"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/create-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/create-resource-pool-classifier.md"
description: "CREATE RESOURCE POOL CLASSIFIER creates a resource pool classifier. Syntax."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE RESOURCE POOL CLASSIFIER

`CREATE RESOURCE POOL CLASSIFIER` creates a [resource pool classifier](../../../concepts/glossary.md#resource-pool-classifier).

## Syntax

```yql
CREATE RESOURCE POOL CLASSIFIER <name>
WITH ( <parameter_name> [= <parameter_value>] [, ... ] )
```

- `name` — name of the resource pool classifier to create. Must be unique and must not contain characters forbidden for schema objects.
- `WITH ( <parameter_name> [= <parameter_value>] [, ... ] )` — parameters that define classifier behavior.

### Parameters

- `RANK` (Int64) — Optional: order in which classifiers are evaluated. If omitted, the maximum existing `RANK` plus 1000 is used. Allowed values: a unique number in \[0,263−1\]\[0, 2^{63}-1\]\[0,263−1\].
- `RESOURCE_POOL` (String) — Required: name of the resource pool for queries that match the classifier.
- `MEMBER_NAME` (String) — Optional: user or group routed to that pool. If omitted, the classifier ignores `MEMBER_NAME` and uses other criteria.

## Notes {#remarks}

If `RANK` is omitted in the DDL, the default is RANK=MAX(existing_ranks)+1000RANK = MAX(existing\\_ranks) + 1000RANK=MAX(existing_ranks)+1000. All `RANK` values must be unique so pool choice is deterministic when rules conflict. This allows inserting new classifiers between existing ones.

A classifier may reference a non-existent pool or a pool the user cannot access; such classifiers are skipped.

Classifier count limits are described on the [limits](../../../concepts/limits-ydb.md#resource_pool) page.

## Permissions

The `ALL` [permission](grant.md#permissions-list) on the database is required.

Example:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Examples

```yql
CREATE RESOURCE POOL CLASSIFIER olap_classifier WITH (
    RANK=1000,
    RESOURCE_POOL="olap",
    MEMBER_NAME="user1@domain"
)
```

The example above creates a resource pool classifier named `olap_classifier` that routes queries from user `user1@domain` to the resource pool named `olap`. Queries from all other users go to the `default` resource pool, assuming no other resource pool classifiers exist.

## See also

- [Workload Manager — resource consumption management](../../../dev/resource-consumption-management.md)
- [ALTER RESOURCE POOL CLASSIFIER](alter-resource-pool-classifier.md)
- [DROP RESOURCE POOL CLASSIFIER](drop-resource-pool-classifier.md)
