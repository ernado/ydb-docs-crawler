---
title: "Service discovery"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/service-discovery?version=v26.1"
doc_path: "en/recipes/ydb-sdk/service-discovery"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/service-discovery.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/service-discovery.md"
description: "Consider a scenario where application instances are dynamically started and publish their endpoints, while other clients need to receive this list and respond t"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Service discovery

Consider a scenario where application instances are dynamically started and publish their endpoints, while other clients need to receive this list and respond to its changes.

This scenario can be implemented using semaphores in [YDB coordination nodes](../../reference/ydb-sdk/coordination.md) as follows:

1. Create a semaphore (for example, named `my-service-endpoints`) with `Limit=Max<ui64>()`.
2. All application instances call `AcquireSemaphore` with `Count=1`, specifying their endpoint in the `Data` field.
3. Since the semaphore limit is very high, all `AcquireSemaphore` calls should complete quickly.
4. At this point, publication is complete, and application instances only need to respond to session stops by republishing themselves through a new session.
5. Clients call `DescribeSemaphore` with `IncludeOwners=true` and optionally with `WatchOwners=true`. In the result, the `Owners` field's `Data` will contain the endpoints of registered application instances.
6. When the list of endpoints changes, `OnChanged` is called. In this case, clients make a similar `DescribeSemaphore` call and receive the updated list.
