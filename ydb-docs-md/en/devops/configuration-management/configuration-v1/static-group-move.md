---
title: "Static Group Move"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v1/static-group-move?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v1/static-group-move"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v1/static-group-move.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v1/static-group-move.md"
description: "If you need to decommission a YDB cluster host that contains part of the static group, you need to move it to another host. Warning."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Static Group Move

If you need to decommission a YDB cluster host that contains part of the [static group](../../../reference/configuration/blob_storage_config.md#blob_storage_config), you need to move it to another host.

> [!WARNING]
> Incorrect sequence of actions or configuration errors can lead to YDB cluster unavailability.

As an example, consider a YDB cluster where a [static node](../../../reference/configuration/hosts.md#hosts) is configured and running on the host with `node_id:1`. This node serves part of the static group.

Static group configuration fragment:

```yaml
...
blob_storage_config:
  ...
  service_set:
    ...
    groups:
      ...
      rings:
        ...
        fail_domains:
        - vdisk_locations:
          - node_id: 1
            path: /dev/vda
            pdisk_category: SSD
        ...
      ...
    ...
  ...
...
```

To replace `node_id:1`, we [added](cluster-expansion.md#add-static-node) a new host with `node_id:10` to the cluster and [deployed](cluster-expansion.md#add-static-node) a static node on it.

To move part of the static group from host `node_id:1` to `node_id:10`:

1. Stop the cluster static node on the host with `node_id:1`.

   > [!NOTE]
   > A YDB cluster is fault-tolerant. Temporary node shutdown does not lead to cluster unavailability. For more details, see [YDB Cluster Topology](../../../concepts/topology.md).

2. In the configuration file `config.yaml`, change the `node_id` value, replacing the identifier of the host being removed with the identifier of the host being added:

   ```yaml
   ...
   blob_storage_config:
     ...
     service_set:
       ...
       groups:
         ...
         rings:
           ...
           fail_domains:
           - vdisk_locations:
             - node_id: 10
               path: /dev/vda
               pdisk_category: SSD
           ...
         ...
       ...
     ...
   ...
   ```

   Change the `path` and disk `pdisk_category` if they differ on the host with `node_id: 10`.

3. Update the configuration files `config.yaml` for all cluster nodes, including dynamic ones.

4. Using the [rolling-restart](../../../maintenance/manual/node_restarting.md) procedure, restart all static cluster nodes.

5. Go to the Embedded UI monitoring page and ensure that the static group VDisk appeared on the target physical disk and is replicating. For more details, see [Monitoring static groups](../../../reference/embedded-ui/ydb-monitoring.md#static-group).

6. Using the [rolling-restart](../../../maintenance/manual/node_restarting.md) procedure, restart all dynamic cluster nodes.
