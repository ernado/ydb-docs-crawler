---
title: "Updating YDB"
url: "https://ydb.tech/docs/en/devops/deployment-options/manual/update-executable?version=v26.1"
doc_path: "en/devops/deployment-options/manual/update-executable"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/manual/update-executable.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/manual/update-executable.md"
description: "YDB is a distributed system that supports rolling restart without downtime or performance degradation. Update Procedure."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Updating YDB

YDB is a distributed system that supports rolling restart without downtime or performance degradation.

## Update Procedure {#upgrade-order}

The basic scenario is updating the executable file and restarting each node one by one:

1. Updating and restarting storage nodes.
2. Updating and restarting dynamic nodes.

The shutdown and startup process is described on the [Safe restart and shutdown of nodes](../../../maintenance/manual/node_restarting.md) page.  
 You must update YDB nodes one by one and monitor the cluster status after each step in [YDB Monitoring](../../../reference/embedded-ui/ydb-monitoring.md): make sure the `Storage` tab has no pools in the `Degraded` status (as shown in the example below). Otherwise, stop the update process.

![Monitoring_storage_state](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/embedded-ui/_assets/monitoring_storage_state.png)

## Version Compatibility {#version-compatability}

All minor versions within a major version are compatible for updates. Major versions are consecutively compatible. To update to the next major version, you must first update to the latest minor release of the current major version. For example:

- `X.Y.* → X.Y.*`: Update is possible, all minor versions within a single major version are compatible.
- `X.Y.Z` (the latest available version in `X.Y.*`) → `X.Y+1.*` : Update is possible, major versions are consistent.
- `X.Y.* → X.Y+2.*`: Update is impossible, major versions are inconsistent.
- `X.Y.* → X.Y-2.*`: Update is impossible, major versions are inconsistent.

A list of available versions can be found on the [download page](../../../downloads/index.md). The YDB release policy is described in more details in the [Release management](../../../contributor/manage-releases.md) article of the YDB development documentation.

> [!WARNING]
> Also, in any case, you cannot roll back more than 2 major versions relative to the version that was deployed at least once. This is because such an old version may not know how to work with data on the disks that the newer version persisted.

### Examples of Version Compatibility

- `v.22.2.5  →  v.22.2.47`: Update is possible.
- `v.22.2.47  →  v.22.3.21`: Update is possible.
- `v.22.2.40  →  v.22.3.21`: Update is impossible, first upgrade to the latest minor version (v.22.2.47).
- `v.22.2.47  →  v.22.4.5`: Update is impossible, upgrade to the next major version first (v.22.3.\*).

## Checking Update Results {#upgrade_check}

You can check the updated node versions on the `Nodes` page in Monitoring.
