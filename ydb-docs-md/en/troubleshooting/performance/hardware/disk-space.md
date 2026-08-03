---
title: "Disk space"
url: "https://ydb.tech/docs/en/troubleshooting/performance/hardware/disk-space?version=v26.1"
doc_path: "en/troubleshooting/performance/hardware/disk-space"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/hardware/disk-space.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/hardware/disk-space.md"
description: "A lack of available disk space can prevent the database from storing new data, resulting in the database becoming read-only. This can also cause slowdowns as th"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Disk space

A lack of available disk space can prevent the database from storing new data, resulting in the database becoming read-only. This can also cause slowdowns as the system tries to reclaim disk space by compacting existing data more aggressively.

## Diagnostics

1. See if the **[DB overview > Storage](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** charts in Grafana show any spikes.

2. In [Embedded UI](../../../reference/embedded-ui/index.md), on the **Storage** tab, analyze the list of available storage groups and nodes and their disk usage.

   > [!TIP]
   > Use the **Out of Space** filter to list only the storage groups with full disks.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/storage-groups-disk-space.png)

> [!NOTE]
> It is also recommended to use the [Healthcheck API](../../../reference/ydb-sdk/health-check-api.md) to get this information.

## Recommendations

Add more [storage groups](../../../concepts/glossary.md#storage-group) to the database.

If the cluster doesn't have spare storage groups, configure them first. Add additional [storage nodes](../../../concepts/glossary.md#storage-node), if necessary.
