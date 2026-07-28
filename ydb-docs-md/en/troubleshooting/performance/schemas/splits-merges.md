---
title: "Excessive tablet splits and merges"
url: "https://ydb.tech/docs/en/troubleshooting/performance/schemas/splits-merges?version=v26.1"
doc_path: "en/troubleshooting/performance/schemas/splits-merges"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/schemas/splits-merges.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/schemas/splits-merges.md"
description: "Warning. Supported only for row-oriented tables. Support for column-oriented tables is currently under development."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Excessive tablet splits and merges

> [!WARNING]
> Supported only for [row-oriented](../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

Each [row-oriented table](../../../concepts/datamodel/table.md#row-oriented-tables) partition in YDB is processed by a [data shard](../../../concepts/glossary.md#data-shard) tablet. YDB supports automatic [splitting and merging](../../../concepts/datamodel/table.md#partitioning) of data shards which allows it to seamlessly adapt to changes in workloads. However, these operations are not free and might have a short-term negative impact on query latencies.

When YDB splits a partition, it replaces the original partition with two new partitions covering the same range of primary keys. Now, two data shards process the range of primary keys that was previously handled by a single data shard, thereby adding more computing resources for the table.

By default, YDB splits a table partition when it reaches 2 GB in size. However, it's recommended to also enable partitioning by load, allowing YDB to split overloaded partitions even if they are smaller than 2 GB.

A [scheme shard](../../../concepts/glossary.md#scheme-shard) takes approximately 15 seconds to assess whether a data shard requires splitting. By default, the CPU usage threshold for splitting a data shard is set at 50%.

When YDB merges adjacent partitions in a row-oriented table, they are replaced with a single partition that covers their range of primary keys. TThe corresponding data shards are also consolidated into a single data shard to manage the new partition.

For merging to occur, data shards must have existed for at least 10 minutes, and their CPU usage over the last hour must not exceed 35%.

When configuring [table partitioning](../../../concepts/datamodel/table.md#partitioning), you can also set limits for the [minimum](../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) and [maximum number of partitions](../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count). If the difference between the minimum and maximum limits exceeds 20% and the table load varies significantly over time, [Hive](../../../concepts/glossary.md#hive) may start splitting overloaded tables and then merging them back during periods of low load.

## Diagnostics

1. See if the **Split / Merge partitions** chart in the **[DB status](../../../reference/observability/metrics/grafana-dashboards.md#dbstatus)** Grafana dashboard shows any spikes.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/schemas/_assets/splits-merges.png)

   ```
    This chart displays the time-series data for the following values:

    - Number of split table partitions per second (blue)
    - Number of merged table partitions per second (green)
   ```

2. Check whether the user load increased when the tablet splits and merges spiked.

   - Review the diagrams on the **DataShard** dashboard in Grafana for any changes in the volume of data read or written by queries.
   - Examine the **Requests** chart on the **Query engine** dashboard in Grafana for any spikes in the number of requests.

3. To identify recently split or merged tablets, follow these steps:

   1. In the [Embedded UI](../../../reference/embedded-ui/index.md), click the **Developer UI** link in the upper right corner.

   2. Navigate to **Node Table Monitor** > **All tablets of the cluster**.

   3. To show only data shard tablets, in the **TabletType** filter, specify `DataShard`.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/schemas/_assets/node-tablet-monitor-data-shard.png)

   4. Sort the tablets by the **ChangeTime** column and review tablets, which change time values coincide with the spikes on the **Split / Merge partitions** chart.

   5. To identify the table associated with the data shard, in the data shard row, click the link in the **TabletID** column.

   6. On the **Tablets** page, click the **App** link.

      The information about the table is displayed in the **User table \<table-name>** section.

4. To pinpoint the schema issue, follow these steps:

   1. Retrieve information about the problematic table using the [YDB CLI](../../../reference/ydb-cli/index.md). Run the following command:

      ```bash
      ydb scheme describe <table_name>
      ```

   2. In the command output, analyze the **Auto partitioning settings**:

      - `Partitioning by load`
      - `Max partitions count`
      - `Min partitions count`

## Recommendations

If the user load on YDB has not changed, consider adjusting the gap between the min and max limits for the number of table partitions to the recommended 20% difference. Use the [`ALTER TABLE table_name SET (key = value)`](../../../yql/reference/syntax/alter_table/set.md) YQL statement to update the [`AUTO_PARTITIONING_MIN_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) and [`AUTO_PARTITIONING_MAX_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count) parameters.

If you want to avoid splitting and merging data shards, you can set the min limit to the max limit value or disable partitioning by load.
