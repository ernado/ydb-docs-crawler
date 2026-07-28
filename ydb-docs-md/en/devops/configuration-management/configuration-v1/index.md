---
title: "Configuration V1"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v1/?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v1/"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v1/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/index.md"
description: "This section of the YDB documentation describes Configuration V1, which is the main way to configure YDB clusters deployed using YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Configuration V1

This section of the YDB documentation describes Configuration V1, which is the main way to configure YDB clusters deployed using YDB.

Configuration V1 is a two-level YDB cluster configuration system consisting of [static configuration](static-config.md) and [dynamic configuration](dynamic-config.md):

1. **Static configuration**: a YAML format file that is located locally on each static node and used when starting the `ydbd server` process. This configuration contains, among other things, [static group](../../../concepts/glossary.md#static-group) and [State Storage](../../../concepts/glossary.md#state-storage) settings.
2. **Dynamic configuration**: a YAML format file that is an extended version of static configuration. It is loaded via [CLI](../../../recipes/ydb-cli/index.md) and reliably stored in the [Console tablet](../../../concepts/glossary.md#console), which then distributes the configuration to all dynamic cluster nodes. Using dynamic configuration is optional.

You can learn more about Configuration V1 in the [Configuration V1 Overview](config-overview.md) section.

Starting from version v25.1, YDB supports [Configuration V2](../configuration-v2/index.md), a unified approach to configuration in a single file format. When using Configuration V2, automatic configuration of [static group](../../../concepts/glossary.md#static-group) and [State Storage](../../../concepts/glossary.md#state-storage) becomes possible. When deploying new clusters on YDB version v25.1 and above, it is recommended to use Configuration V2.

Main materials:

- [Configuration V1 Overview](config-overview.md)
- [YDB Cluster Configuration](static-config.md)
- [Dynamic Cluster Configuration](dynamic-config.md)
- [Volatile Configurations](dynamic-config-volatile-config.md)
- [Cluster Configuration Domain-Specific Language (DSL)](dynamic-config-selectors.md)
- [Changing Configurations via CMS](cms.md)
- [Changing Actor System Configuration](change_actorsystem_configs.md)
- [Expanding a Cluster](cluster-expansion.md)
- [State Storage Move](state-storage-move.md)
- [Static Group Move](static-group-move.md)
- [Replacing Node FQDN](replacing-nodes.md)
- [Database Node Authentication and Authorization](node-authorization.md)
