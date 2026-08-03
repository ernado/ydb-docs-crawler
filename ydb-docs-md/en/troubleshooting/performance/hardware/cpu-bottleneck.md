---
title: "CPU bottleneck"
url: "https://ydb.tech/docs/en/troubleshooting/performance/hardware/cpu-bottleneck?version=v26.1"
doc_path: "en/troubleshooting/performance/hardware/cpu-bottleneck"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/hardware/cpu-bottleneck.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/hardware/cpu-bottleneck.md"
description: "High CPU usage can lead to slow query processing and increased response times. When CPU resources are constrained, the database may have difficulty handling com"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# CPU bottleneck

High CPU usage can lead to slow query processing and increased response times. When CPU resources are constrained, the database may have difficulty handling complex queries or large transaction volumes.

YDB nodes primarily consume CPU resources for running [actors](../../../concepts/glossary.md#actor). On each node, actors are executed using multiple [actor system pools](../../../concepts/glossary.md#actor-system-pools). The resource consumption of each pool is measured separately which allows to identify what kind of activity changed its behavior.

## Diagnostics

1. Use **Diagnostics** in the [Embedded UI](../../../reference/embedded-ui/index.md) to analyze CPU utilization in all pools:

   1. In the [Embedded UI](../../../reference/embedded-ui/index.md), go to the **Databases** tab and click on the database.

   2. On the **Navigation** tab, ensure the required database is selected.

   3. Open the **Diagnostics** tab.

   4. On the **Info** tab, click the **CPU** button and see if any pools show high CPU usage.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/embedded-ui-cpu-system-pool.png)

2. Use Grafana charts to analyze CPU utilization in all pools:

   1. Open the **[CPU](../../../reference/observability/metrics/grafana-dashboards.md#cpu)** dashboard in Grafana.

   2. See if the following charts show any spikes:

      - **CPU by execution pool** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-by-pool.png)

      - **User pool - CPU by host** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-user-pool.png)

      - **System pool - CPU by host** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-system-pool.png)

      - **Batch pool - CPU by host** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-batch-pool.png)

      - **IC pool - CPU by host** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-ic-pool.png)

      - **IO pool - CPU by host** chart

        ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/cpu-io-pool.png)

3. If the spike is in the user pool, analyze changes in the user load that might have caused the CPU bottleneck. See the following charts on the **DB overview** dashboard in Grafana:

   - **Requests** chart

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/requests.png)

   - **Request size** chart

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/request-size.png)

   - **Response size** chart

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/response-size.png)

   Also, see all of the charts in the **Operations** section of the **DataShard** dashboard.

4. If the spike is in the batch pool, check if there are any backups running.

## Recommendation

Add additional [database nodes](../../../concepts/glossary.md#database-node) to the cluster or allocate more CPU cores to the existing nodes. If that's not possible, consider distributing CPU cores between pools differently.
