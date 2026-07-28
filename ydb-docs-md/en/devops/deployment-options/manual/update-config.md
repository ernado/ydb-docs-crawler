---
title: "Updating configuration of manually deployed YDB clusters"
url: "https://ydb.tech/docs/en/devops/deployment-options/manual/update-config?version=v26.1"
doc_path: "en/devops/deployment-options/manual/update-config"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/manual/update-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/manual/update-config.md"
description: "When manually deploying a YDB cluster, configuration management is performed through YDB CLI. This article covers methods for changing cluster configuration aft"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Updating configuration of manually deployed YDB clusters

When manually deploying a YDB cluster, configuration management is performed through [YDB CLI](../../../reference/ydb-cli/index.md). This article covers methods for changing cluster configuration after initial deployment.

## Basic configuration operations

### Getting current configuration

To get the current cluster configuration, use the command:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config fetch > config.yaml
```

Use the address of any cluster node as `<endpoint>`.

### Applying new configuration

To upload updated configuration to the cluster, use the following command:

```bash
ydb -e grpcs://<endpoint>:2135 admin cluster config replace -f config.yaml
```

Some configuration parameters are applied on the fly after executing the command, however some require performing the [cluster restart procedure](../../../maintenance/manual/node_restarting.md).
