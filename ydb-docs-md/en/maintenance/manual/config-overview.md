---
title: "Configuration V1 Overview"
url: "https://ydb.tech/docs/en/maintenance/manual/config-overview?version=v26.1"
doc_path: "en/maintenance/manual/config-overview"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v1/config-overview.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/config-overview.md"
description: "To start a YDB node, configuration is required. There are two types of configuration: Static — a YAML format file stored on the node's local disk."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Configuration V1 Overview

To start a YDB node, configuration is required. There are two types of configuration:

- **Static** — a YAML format file stored on the node's local disk.
- **Dynamic** — a YAML format document stored in the YDB configuration storage.

Static cluster nodes use static configuration. Dynamic nodes can use static configuration, dynamic configuration, or their combination.

## Static Configuration {#static-config}

Static configuration is a YAML file stored on cluster nodes. This file lists all system settings. The path to the file is passed to the `ydbd` process at startup through a command line parameter. Distribution of static configuration across the cluster and maintaining it in a consistent state on all nodes is the responsibility of the cluster administrator. Details on using static configuration can be found in the [YDB Cluster Configuration](../../devops/configuration-management/configuration-v1/static-config.md) section. This configuration is **required** to start static nodes.

![data tab](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/_assets/config-chart-1.png "static configs")

### Basic Usage Scenario

1. Copy [standard configuration](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/) from GitHub.
2. Modify the configuration according to your requirements.
3. Place identical configuration files on all cluster nodes.
4. Start all cluster nodes, explicitly specifying the path to the configuration file using the `--yaml-config` command line argument.

## Dynamic Configuration {#dynamic-config}

Dynamic configuration is a YAML document reliably stored in the cluster in the [Console tablet](../../concepts/glossary.md#console). Unlike static configuration, it is sufficient to load it into the cluster, as YDB will be responsible for its distribution and maintaining it in a consistent state. At the same time, dynamic configuration using selectors allows handling complex scenarios while remaining within a single configuration file. A description of dynamic configuration is presented in the [Dynamic Cluster Configuration](../../devops/configuration-management/configuration-v1/dynamic-config.md) section.

![data tab](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/_assets/config-chart-2.png "static and dynamic configs")

### Basic Usage Scenario {#basic-usage-scenario1}

1. Copy [standard configuration](https://github.com/ydb-platform/ydb/tree/main/ydb/deploy/yaml_config_examples/) from GitHub.
2. Modify the configuration according to your requirements.
3. Place identical configuration files on all static cluster nodes.
4. Start all static cluster nodes, explicitly specifying the path to the configuration file using the `--yaml-config` command line argument.
5. Supplement the configuration file to [dynamic configuration format](../../devops/configuration-management/configuration-v1/dynamic-config.md#example).
6. Load the resulting configuration to the cluster using `ydb admin config replace -f dynconfig.yaml`.
