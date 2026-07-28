---
title: "State Storage Move"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v1/state-storage-move?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v1/state-storage-move"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v1/state-storage-move.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/state-storage-move.md"
description: "If you need to decommission a YDB cluster host that contains part of State Storage, you need to move it to another host. Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# State Storage Move

If you need to decommission a YDB cluster host that contains part of [State Storage](../../../reference/configuration/domains_config.md#domains-state), you need to move it to another host.

> [!WARNING]
> Incorrect sequence of actions or configuration errors can lead to YDB cluster unavailability.

As an example, consider a YDB cluster with the following State Storage configuration:

```yaml
...
domains_config:
  ...
  state_storage:
  - ring:
      node: [1, 2, 3, 4, 5, 6, 7, 8, 9]
      nto_select: 9
    ssid: 1
  ...
...
```

On the host with `node_id:1`, a cluster [static node](../../../reference/configuration/hosts.md#hosts) is configured and running, which serves part of State Storage. Suppose we need to decommission this host.

To replace `node_id:1`, we [added](cluster-expansion.md#add-host) a new host with `node_id:10` to the cluster and [deployed](cluster-expansion.md#add-static-node) a static node on it.

To move State Storage from host `node_id:1` to `node_id:10`:

1. Stop the cluster static nodes on hosts with `node_id:1` and `node_id:10`.

   > [!NOTE]
   > A YDB cluster is fault-tolerant. Temporary node shutdown does not lead to cluster unavailability. For more details, see [YDB Cluster Topology](../../../concepts/topology.md).

2. In the configuration file `config.yaml`, change the `node` host list, replacing the identifier of the host being removed with the identifier of the host being added:

   ```yaml
   domains_config:
   ...
     state_storage:
     - ring:
         node: [2, 3, 4, 5, 6, 7, 8, 9, 10]
         nto_select: 9
       ssid: 1
   ...
   ```

3. Update the configuration files `config.yaml` for all cluster nodes, including dynamic ones.

4. Using the [rolling-restart](../../../maintenance/manual/node_restarting.md) procedure, restart all cluster nodes, including dynamic ones, except for static nodes on hosts with `node_id:1` and `node_id:10`. Note that a delay of at least 15 seconds is required between host restarts.

5. Start the cluster static nodes on hosts `node_id:1` and `node_id:10`.
