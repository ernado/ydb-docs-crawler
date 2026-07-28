---
title: "Checking Configuration Version"
url: "https://ydb.tech/docs/en/devops/configuration-management/check-config-version?version=v26.1"
doc_path: "en/devops/configuration-management/check-config-version"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/check-config-version.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/check-config-version.md"
description: "There are two main ways to check which configuration mechanism version ( V1 or V2 ) the nodes of your YDB cluster are using: Embedded UI. Cluster metrics."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Checking Configuration Version

There are two main ways to check which configuration mechanism version ([V1](configuration-v1/config-overview.md) or [V2](configuration-v2/config-overview.md)) the nodes of your YDB cluster are using:

1. [Embedded UI](check-config-version.md#embedded-ui)
2. [Cluster metrics](check-config-version.md#metrics)

## With Embedded UI {#embedded-ui}

This method can be used if metrics collection from the YDB cluster to the monitoring system is not configured. You can check the configuration version for a specific node or switch between nodes in the built-in web interface [Embedded UI](../../reference/embedded-ui/index.md):

1. Open the `configs_dispatcher` actor page for any cluster node in your browser:

   ```text
   http://<endpoint>:8765/actors/configs_dispatcher
   ```

   where `<endpoint>` is the address of any YDB cluster node.

2. In the upper part of the opened page, find the `Configuration version` field. It shows the configuration version (`v1` or `v2`) used by this node.

   This is how the page of a node using configuration V1 looks:

   ![configs-dispatcher-page-v1](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/devops/configuration-management/_assets/viewer-v1.png)

3. To check other nodes, use the `Nodes...` search field in the upper right corner of the page to switch between nodes.

## With Cluster Metrics {#metrics}

This method is convenient when there are a large number of nodes in the YDB cluster. If you have configured [metrics collection from the YDB cluster to the monitoring system](../../reference/observability/metrics/index.md), perform the following actions:

1. Find the dashboard displaying cluster metrics.
2. Go to the `config` sensor group and the `configs_dispatcher` subsystem.
3. Pay attention to the `ConfigurationV1` and `ConfigurationV2` sensors. The values of these sensors show the number of cluster nodes running with configuration V1 and V2 respectively.

For example, if `ConfigurationV1 > 0`, it means there are nodes in the cluster that use configuration V1. If `ConfigurationV1 = 0` and `ConfigurationV2` equals the total number of nodes, it means all nodes use configuration V2.
