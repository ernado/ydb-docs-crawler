---
title: "Static Group Move"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v2/static-group-move?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v2/static-group-move"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v2/static-group-move.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v2/static-group-move.md"
description: "Article under development. Warning."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Static Group Move

<details>
<summary>Article under development</summary>

> [!WARNING]
> This article is dedicated to YDB clusters that use [configuration V2](index.md). This configuration method is currently experimental and is only available for YDB versions starting from v25.1. For production use, we recommend choosing [configuration V1](../index.md) — it is the main method and is officially supported for all YDB clusters.

When using Configuration V2, static group management is performed automatically and the Self Heal mechanism will perform reconfiguration when one static group node fails.

When manual static group configuration management is needed, you need to disable automatic static group management, get the current static group configuration, make changes and apply the modified configuration as the target static group configuration. Then you need to remove the target static group configuration from the configuration file and enable automatic static group configuration management.

> [!WARNING]
> Incorrect sequence of actions or configuration errors can lead to YDB cluster unavailability.

As an example, consider a YDB cluster where a [static node](config-settings.md#hosts) is configured and running on the host with `node_id:1`. This node serves part of the static group.

Static group configuration fragment:

```yaml
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
```

To replace `node_id:1`, we use another host with a static node deployed on it with `node_id:10`.

To move part of the static group from host `node_id:1` to `node_id:10`:

1. Disable automatic static group management.

2. Get the current static group configuration.

3. Make changes and apply the modified configuration as the target static group configuration.
    In the configuration file `config.yaml`, change the `node_id` value, replacing the identifier of the host being removed with the identifier of the host being added:

   ```yaml
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
   ```

   Change the `path` and disk `pdisk_category` if they differ on the host with `node_id: 10`.

4. Go to the Embedded UI monitoring page and ensure that the static group VDisk appeared on the target physical disk and is replicating. For more details, see [Monitoring static groups](../../../reference/embedded-ui/ydb-monitoring.md#static-group).

5. Remove the target static group configuration from the configuration file and enable automatic static group configuration management.

</details>
