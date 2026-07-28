---
title: "Cluster Configuration Migration"
url: "https://ydb.tech/docs/en/devops/configuration-management/migration/?version=v26.1"
doc_path: "en/devops/configuration-management/migration/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/migration/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/migration/index.md"
description: "YDB supports two configuration management mechanisms: V1 and V2 (experimental, available from version 25.1). Key differences between them are described in the a"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Cluster Configuration Migration

YDB supports two configuration management mechanisms: [V1](../configuration-v1/index.md) and [V2](../configuration-v2/config-overview.md) (experimental, available from version 25.1). Key differences between them are described in the article [Comparing configurations V1 and V2](../compare-configs.md).

> [!TIP]
> New YDB clusters are recommended to be deployed using [configuration V2](../configuration-v2/index.md). If a cluster was deployed using [configuration V1](../configuration-v1/index.md), it will still use it after updating to YDB version 25.1 or higher. After such an update, it is recommended to plan and perform [migration to V2](migration-to-v2.md), because support for V1 will be discontinued in future versions of YDB. For the instructions on how to determine the configuration version of the cluster, see [Checking Configuration Version](../check-config-version.md).

Depending on the current state of your cluster, you can perform migration:

- **[To configuration V2](migration-to-v2.md):** If your cluster is managed by configuration V1, you can switch to the experimental configuration V2 mechanism.
- **[To configuration V1](migration-to-v1.md):** If unexpected problems arose after switching to configuration V2, or you need to roll back the YDB version below 25.1, you can perform reverse migration to manual configuration management (V1).

> [!NOTE]
> **Problems during migration?**
>
> If unexpected problems arise when using migration instructions (especially when rolling back to V1), it is recommended to report them immediately as a [GitHub issue](https://github.com/ydb-platform/ydb/issues/new), providing maximum context and diagnostics for reproduction.

Before performing migration, make sure to determine which configuration version is currently used in your cluster using the [version check instructions](../check-config-version.md).
