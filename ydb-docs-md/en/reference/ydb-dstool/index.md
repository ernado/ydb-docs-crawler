---
title: "YDB DSTool overview"
url: "https://ydb.tech/docs/en/reference/ydb-dstool/?version=v26.1"
doc_path: "en/reference/ydb-dstool/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-dstool/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-dstool/index.md"
description: "With the YDB DSTool utility, you can manage your YDB cluster's disk subsystem. To install and configure the utility, follow the instructions."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB DSTool overview

With the YDB DSTool utility, you can manage your YDB cluster's disk subsystem. To install and configure the utility, follow the [instructions](install.md).

YDB DSTool includes the following commands:

| Command | Description |
| --- | --- |
| [device list](device-list.md) | List storage devices. |
| pdisk add-by-serial | Add a PDisk to a set by serial number. |
| pdisk remove-by-serial | Remove a PDisk from the set by serial number. |
| pdisk set | Set PDisk parameters. |
| pdisk list | List PDisks. |
| vdisk evict | Move VDisks to different PDisks. |
| vdisk remove-donor | Remove a donor VDisk. |
| vdisk wipe | Wipe VDisks. |
| vdisk list | List VDisks. |
| group add | Add storage groups to a pool. |
| group check | Check storage groups. |
| group show blob-info | Display blob information. |
| group show usage-by-tablets | Display information about tablet usage by groups. |
| group state | Show or change a storage group's state. |
| group take-snapshot | Take a snapshot of storage group metadata. |
| group list | List storage groups. |
| pool list | List pools. |
| box list | List sets of PDisks. |
| node list | List nodes. |
| cluster balance | Move VDisks from overloaded PDisks. |
| cluster get | Show cluster parameters. |
| cluster set | Set cluster parameters. |
| cluster workload run | Run a workload to test the failure model. |
| cluster list | Display cluster information. |
