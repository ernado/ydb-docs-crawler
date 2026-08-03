---
title: "cms_config"
url: "https://ydb.tech/docs/en/reference/configuration/cms_config?version=v26.1"
doc_path: "en/reference/configuration/cms_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/cms_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/cms_config.md"
description: "Cluster Management System (CMS) is a YDB component that enables safe cluster maintenance, for example, updating its version or replacing failed disks without lo"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# cms_config

[Cluster Management System (CMS)](../../concepts/glossary.md#cms) is a YDB component that enables [safe cluster maintenance](../../devops/concepts/maintenance-without-downtime.md), for example, updating its version or replacing failed disks without loss of availability. CMS behavior is configured in the `cms_config` section of the YDB configuration.

## Syntax

```yaml
cms_config:
  tenant_limits:
    disabled_nodes_limit: 2
    disabled_nodes_ratio_limit: 5
  cluster_limits:
    disabled_nodes_limit: 3
    disabled_nodes_ratio_limit: 5
  disable_maintenance: true
```

## Parameters

| Parameter | Default value | Description |
| --- | --- | --- |
| `tenant_limits.disabled_nodes_limit` | — | Maximum number of [database nodes](../../concepts/glossary.md#database-node) that can be simultaneously unavailable or blocked. |
| `tenant_limits.disabled_nodes_ratio_limit` | `13` | Maximum percentage of [database nodes](../../concepts/glossary.md#database-node) that can be simultaneously unavailable or blocked. |
| `cluster_limits.disabled_nodes_limit` | — | Maximum number of [cluster](../../concepts/glossary.md#cluster) nodes that can be simultaneously unavailable or blocked. |
| `cluster_limits.disabled_nodes_ratio_limit` | `13` | Maximum percentage of [cluster](../../concepts/glossary.md#cluster) nodes that can be simultaneously unavailable. |
| `disable_maintenance` | `false` | Flag that [suspends](../../devops/concepts/maintenance-without-downtime.md#disable-maintenance) new cluster maintenance operations. |
