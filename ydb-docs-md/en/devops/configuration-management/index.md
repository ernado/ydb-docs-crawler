---
title: "YDB Cluster Configuration"
url: "https://ydb.tech/docs/en/devops/configuration-management/?version=v26.1"
doc_path: "en/devops/configuration-management/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/index.md"
description: "This section presents materials on YDB cluster configuration management. You will learn about two versions of the configuration mechanism (V1 and V2), their dif"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB Cluster Configuration

This section presents materials on YDB cluster configuration management. You will learn about two versions of the configuration mechanism (V1 and V2), their differences, and how to check which version is used in your cluster.

Main subsections:

- [Configuration V1](configuration-v1/index.md) — section about configuration V1, used in YDB.
- [Configuration V2](configuration-v2/index.md) — section about configuration V2, experimental functionality for YDB versions 25.1 and above.
- [Cluster Configuration Migration](migration/index.md) — migration between configurations V1 and V2.
- [Checking Configuration Version](check-config-version.md) — checking which configuration version is used on the cluster.
- [Comparing YDB Cluster Configurations: V1 and V2](compare-configs.md) — detailed comparison of configurations V1 and V2.

> [!TIP]
> New YDB clusters are recommended to be deployed using [configuration V2](configuration-v2/index.md). If a cluster was deployed using [configuration V1](configuration-v1/index.md), it will still use it after updating to YDB version 25.1 or higher. After such an update, it is recommended to plan and perform [migration to V2](migration/migration-to-v2.md), because support for V1 will be discontinued in future versions of YDB. For the instructions on how to determine the configuration version of the cluster, see [Checking Configuration Version](check-config-version.md).
