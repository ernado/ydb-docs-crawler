---
title: "Updating YDB Cluster Configuration"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v2/update-config?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v2/update-config"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v2/update-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v2/update-config.md"
description: "This article covers changing cluster configuration after initial deployment. Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Updating YDB Cluster Configuration

This article covers changing cluster configuration after initial deployment.

> [!WARNING]
> This article is dedicated to YDB clusters that use [configuration V2](index.md). This configuration method is currently experimental and is only available for YDB versions starting from v25.1. For production use, we recommend choosing [configuration V1](../index.md) — it is the main method and is officially supported for all YDB clusters.

YDB cluster configuration management is performed using [YDB CLI](../../../reference/ydb-cli/index.md). The standard approach to updating a configuration is to get the current configuration from the cluster using YDB CLI, modify it locally, and then load the updated configuration back to the cluster.

To prevent accidental overwriting of changes when multiple administrators work simultaneously, YDB configuration contains metadata with a version number. With each successful configuration upload, this number is automatically incremented. If another administrator tries to upload a configuration based on a previous (outdated) version (i.e., with the same or lower version number in metadata), the system will reject this attempt. This ensures that changes by one administrator will not be silently overwritten by changes from another.

To update a configuration, you need to get the current configuration, modify it, and apply the updated configuration. During the configuration application process, it will be reliably saved by the cluster and distributed to all its nodes. As configuration is delivered to cluster nodes, the configuration begins to be applied by these nodes. Some configuration parameters change node behavior immediately after configuration delivery, while others only take effect when the node starts, and changing such parameters requires a cluster restart for them to take effect.

## Basic Configuration Operations

### Getting Current Configuration

To get the current cluster configuration, use the command:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config fetch > config.yaml
```

Specify the address of any cluster node as `<endpoint>`.

### Applying New Configuration

To load updated configuration to the cluster, use the following command:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config replace -f config.yaml
```

Specify the address of any cluster node as `<endpoint>`.

Some configuration parameters are applied on the fly after executing the command, however some require performing the [cluster restart](../../../reference/ydbops/rolling-restart-scenario.md) procedure.
