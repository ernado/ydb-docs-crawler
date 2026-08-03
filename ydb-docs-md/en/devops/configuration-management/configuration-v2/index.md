---
title: "Configuration V2"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v2/?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v2/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v2/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v2/index.md"
description: "This section of the documentation describes the YDB clusters configuration method called V2, which is the experimental way to configure YDB clusters version v25"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Configuration V2

This section of the documentation describes the YDB clusters configuration method called V2, which is the experimental way to configure YDB clusters version v25.1 and above.

> [!WARNING]
> This article is dedicated to YDB clusters that use [configuration V2](index.md). This configuration method is currently experimental and is only available for YDB versions starting from v25.1. For production use, we recommend choosing [configuration V1](../index.md) — it is the main method and is officially supported for all YDB clusters.

Main materials:

- [Configuration V2 Overview](config-overview.md)
- [Updating YDB Cluster Configuration](update-config.md)
- [Cluster Configuration Domain-Specific Language (DSL)](dynamic-config-selectors.md)
- [YDB Cluster Configuration](config-settings.md)
- [Cluster Expansion](cluster-expansion.md)
- [State Storage Move](state-storage-move.md)
- [Static Group Move](static-group-move.md)
- [Replacing Node FQDN](replacing-nodes.md)
- [Database Node Authentication and Authorization](node-authorization.md)
