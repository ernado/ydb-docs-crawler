---
title: "Configuration publication"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/config-publication?version=v26.1"
doc_path: "en/recipes/ydb-sdk/config-publication"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/config-publication.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/config-publication.md"
description: "Let's consider a scenario where we need to publish a small configuration for multiple application instances that should promptly react to its changes."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Configuration publication

Let's consider a scenario where we need to publish a small configuration for multiple application instances that should promptly react to its changes.

This scenario can be implemented using semaphores in [YDB coordination nodes](../../reference/ydb-sdk/coordination.md) as follows:

1. A semaphore is created (for example, named `my-service-config`).
2. The updated configuration is published through `UpdateSemaphore`.
3. Application instances call `DescribeSemaphore` with `WatchData=true`. In the result, the `Data` field will contain the current version of the configuration.
4. When the configuration changes, `OnChanged` is called. In this case, application instances make a similar `DescribeSemaphore` call and receive the updated configuration.
