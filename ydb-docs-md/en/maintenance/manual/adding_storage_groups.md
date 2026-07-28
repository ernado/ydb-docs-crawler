---
title: "Adding storage groups"
url: "https://ydb.tech/docs/en/maintenance/manual/adding_storage_groups?version=v26.1"
doc_path: "en/maintenance/manual/adding_storage_groups"
version: "v26.1"
lang: "en"
source_path: "en/core/maintenance/manual/adding_storage_groups.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/maintenance/manual/adding_storage_groups.md"
description: "As the amount of stored data grows, you may need to add disks to your YDB cluster. You can add disks either to existing nodes or along with new nodes. To make t"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Adding storage groups

As the amount of stored data grows, you may need to add disks to your YDB cluster. You can add disks either to existing nodes or along with new nodes. To make the resources of new disks available to the database, add [storage groups](../../concepts/glossary.md#storage-groups).

To add new storage groups, use [YDB DSTool](../../reference/ydb-dstool/index.md).

View a list of cluster storage pools:

```bash
ydb-dstool -e <bs_endpoint> pool list
```

> Result example:
>
> ```text
> ┌──────────────┬──────────────────┬────────────────┬──────┬──────────────┬──────────────┐
> │ BoxId:PoolId │ PoolName         │ ErasureSpecies │ Kind │ Groups_TOTAL │ VDisks_TOTAL │
> ├──────────────┼──────────────────┼────────────────┼──────┼──────────────┼──────────────┤
> │ [1:1]        │ /Root/testdb:ROT │ mirror-3-dc    │ ROT  │ 1            │ 9            │
> └──────────────┴──────────────────┴────────────────┴──────┴──────────────┴──────────────┘
> ```

The command below adds 10 groups to the `/Root/testdb:ROT` pool:

```bash
ydb-dstool -e <bs_endpoint> group add --pool-name /Root/testdb:ROT --groups 10
```

If successful, the command returns a zero `exit status`. Or else, it returns a non-zero exit status and  
 outputs an error message to `stderr`.

To check if groups can be added without actually adding them, use the `--dry-run` global parameter. The command below checks if 100 groups can be added to the `/Root/testdb:ROT` pool:

```bash
ydb-dstool --dry-run -e <bs_endpoint> group add --pool-name /Root/testdb:ROT --groups 100
```

The `--dry-run` parameter lets you estimate the maximum number of groups that you can add to the pool.
