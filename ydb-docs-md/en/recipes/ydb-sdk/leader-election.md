---
title: "Leader election"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/leader-election?version=v26.1"
doc_path: "en/recipes/ydb-sdk/leader-election"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/leader-election.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/leader-election.md"
description: "Consider a scenario where multiple application instances need to elect a leader among themselves and be aware of the current leader at any given time."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Leader election

Consider a scenario where multiple application instances need to elect a leader among themselves and be aware of the current leader at any given time.

This scenario can be implemented using semaphores in [YDB coordination nodes](../../reference/ydb-sdk/coordination.md) as follows:

1. A semaphore is created (for example, named `my-service-leader`) with `Limit=1`.
2. All application instances call `AcquireSemaphore` with `Count=1`, specifying their endpoint in the `Data` field.
3. Only one application instance's call will complete quickly, while others will be queued. The application instance whose call completes successfully becomes the current leader.
4. All application instances call `DescribeSemaphore` with `WatchOwners=true` and `IncludeOwners=true`. The result's `Owners` field will contain at most one element, from which the current leader's endpoint can be determined via its `Data` field.
5. When the leader changes, `OnChanged` is called. In this case, application instances make a similar `DescribeSemaphore` call to learn about the new leader.
