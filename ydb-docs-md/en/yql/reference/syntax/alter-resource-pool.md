---
title: "ALTER RESOURCE POOL"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter-resource-pool?version=v26.1"
doc_path: "en/yql/reference/syntax/alter-resource-pool"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter-resource-pool.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter-resource-pool.md"
description: "ALTER RESOURCE POOL changes the definition of a resource pool. Syntax Changing parameters. The syntax for changing any resource pool parameter is as follows:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER RESOURCE POOL

`ALTER RESOURCE POOL` changes the definition of a [resource pool](../../../concepts/glossary.md#resource-pool).

## Syntax

### Changing parameters

The syntax for changing any resource pool parameter is as follows:

```yql
ALTER RESOURCE POOL <name> SET (<key> = <value>);
```

`<key>` is the parameter name, `<value>` is its new value.

For example, the following command sets a limit of 100 concurrent queries:

```yql
ALTER RESOURCE POOL olap SET (CONCURRENT_QUERY_LIMIT = "100");
```

### Resetting parameters

The command to reset a resource pool parameter is as follows:

```yql
ALTER RESOURCE POOL <name> RESET (<key>);
```

`<key>` is the parameter name.

For example, the following command resets `TOTAL_CPU_LIMIT_PERCENT_PER_NODE` for the resource pool:

```yql
ALTER RESOURCE POOL olap RESET (TOTAL_CPU_LIMIT_PERCENT_PER_NODE);
```

## Permissions

The `ALTER SCHEMA` [permission](grant.md#permissions-list) on the resource pool under `.metadata/workload_manager/pools` is required. Example:

```yql
GRANT 'ALTER SCHEMA' ON `.metadata/workload_manager/pools/olap_pool` TO `user1@domain`;
```

## Parameters

- `CONCURRENT_QUERY_LIMIT` (Int32) — Optional: maximum number of queries executing in parallel in the resource pool. If `-1`, there is no limit. Default: `-1`. Allowed values: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `QUEUE_SIZE` (Int32) — Optional: wait queue size. The system may hold at most CONCURRENT_QUERY_LIMIT+QUEUE_SIZECONCURRENT\\_QUERY\\_LIMIT + QUEUE\\_SIZECONCURRENT_QUERY_LIMIT+QUEUE_SIZE queries at once. If `-1`, there is no limit. Default: `-1`. Allowed values: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `DATABASE_LOAD_CPU_THRESHOLD` (Int32) — Optional: database-wide CPU load threshold above which queries are not started and remain queued. If `-1`, there is no limit. Default: `-1`. Allowed values: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_MEMORY_LIMIT_PERCENT_PER_NODE` (Double) — Optional: percentage of available memory on a node that a single query in this pool may use. If `-1`, the limit is shared total available memory across all queries. Default: `-1`. Allowed values: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `TOTAL_CPU_LIMIT_PERCENT_PER_NODE` (Double) — Optional: percentage of available CPU on a node that all queries in this pool may use together. If `-1`, there is no limit. Default: `-1`. Allowed values: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_CPU_LIMIT_PERCENT_PER_NODE` (Double) — Optional: percentage of available CPU on a node for a single query in the pool. If `-1`, there is no limit. Default: `-1`. Allowed values: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `RESOURCE_WEIGHT` (Int32) — Optional: weight for distributing resources among pools. If `-1`, weights are not used. Default: `-1`. Allowed values: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].

## See also

- [Workload Manager — resource consumption management](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL](create-resource-pool.md)
- [DROP RESOURCE POOL](drop-resource-pool.md)
