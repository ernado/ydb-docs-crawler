---
title: "ALTER RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-resource-pool-classifier?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-resource-pool-classifier"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-resource-pool-classifier.md"
description: "ALTER RESOURCE POOL CLASSIFIER changes the definition of a resource pool classifier. Syntax Changing parameters."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER RESOURCE POOL CLASSIFIER

`ALTER RESOURCE POOL CLASSIFIER` changes the definition of a [resource pool classifier](../../../concepts/glossary.md#resource-pool-classifier).

## Syntax

### Changing parameters

The syntax for changing any resource pool classifier parameter is as follows:

```yql
ALTER RESOURCE POOL CLASSIFIER <name> SET (<key> = <value>);
```

`<key>` is the parameter name, `<value>` is its new value.

For example, the following command changes the user to which the rule applies:

```yql
ALTER RESOURCE POOL CLASSIFIER olap_classifier SET (MEMBER_NAME = "user2@domain");
```

### Resetting parameters

The command to reset a resource pool classifier parameter is as follows:

```yql
ALTER RESOURCE POOL CLASSIFIER <name> RESET (<key>);
```

`<key>` is the parameter name.

For example, the following command resets the `MEMBER_NAME` setting:

```yql
ALTER RESOURCE POOL CLASSIFIER olap_classifier RESET (MEMBER_NAME);
```

## Permissions

The `ALL` [permission](grant.md#permissions-list) on the database is required. Example of granting it:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Parameters

- `RANK` (Int64) — Optional field that defines the order in which resource pool classifiers are chosen. If omitted, the maximum existing `RANK` is taken and 1000 is added. Allowed values: a unique number in the range \[0,263−1\]\[0, 2^{63}-1\]\[0,263−1\].
- `RESOURCE_POOL` (String) — Required field: name of the resource pool to which queries matching the classifier criteria are sent.
- `MEMBER_NAME` (String) — Optional field specifying which user or group is routed to the given resource pool. If omitted, the classifier ignores `MEMBER_NAME` and classification uses other criteria.

## See also

- [Workload Manager — resource consumption management](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL CLASSIFIER](create-resource-pool-classifier.md)
- [DROP RESOURCE POOL CLASSIFIER](drop-resource-pool-classifier.md)
