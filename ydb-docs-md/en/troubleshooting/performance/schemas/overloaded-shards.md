---
title: "Overloaded shards"
url: "https://ydb.tech/docs/en/troubleshooting/performance/schemas/overloaded-shards?version=v26.1"
doc_path: "en/troubleshooting/performance/schemas/overloaded-shards"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/schemas/overloaded-shards.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/schemas/overloaded-shards.md"
description: "Data shards serving row-oriented tables may become overloaded for the following reasons: A table is created without the AUTO_PARTITIONING_BY_LOAD clause."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Overloaded shards

[Data shards](../../../concepts/glossary.md#data-shard) serving [row-oriented tables](../../../concepts/datamodel/table.md#row-oriented-tables) may become overloaded for the following reasons:

- A table is created without the [AUTO_PARTITIONING_BY_LOAD](../../../concepts/datamodel/table.md#AUTO_PARTITIONING_BY_LOAD) clause.

  In this case, YDB does not split overloaded shards.

  Data shards are single-threaded and process queries sequentially. Each data shard can accept up to 10,000 operations. Accepted queries wait for their turn to be executed. So the longer the queue, the higher the latency.

  If a data shard already has 10000 operations in its queue, new queries will return an "overloaded" error. Retry such queries using a randomized exponential back-off strategy. For more information, see [Overloaded errors](../queries/overloaded-errors.md).

- A table was created with the [AUTO_PARTITIONING_MAX_PARTITIONS_COUNT](../../../concepts/datamodel/table.md#AUTO_PARTITIONING_MAX_PARTITIONS_COUNT) setting and has already reached its partition limit.

- An inefficient [primary key](../../../concepts/glossary.md#primary-key) that causes an imbalance in the distribution of queries across shards. A typical example is ingestion with a monotonically increasing primary key, which may lead to the overloaded "last" partition. For example, this could occur with an autoincrementing primary key using the serial data type.

## Diagnostics

1. Use the Embedded UI or Grafana to see if the YDB nodes are overloaded:

   - In the **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** Grafana dashboard, analyze the **Overloaded shard count** chart.

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/schemas/_assets/overloaded-shards-dashboard.png)

     The chart indicates whether the YDB cluster has overloaded shards, but it does not specify which table's shards are overloaded.

     > [!TIP]
     > Use Grafana to set up alert notifications when YDB data shards get overloaded.

   - In the [Embedded UI](../../../reference/embedded-ui/index.md):

     1. Go to the **Databases** tab and click on the database.
     2. On the **Navigation** tab, ensure the required database is selected.
     3. Open the **Diagnostics** tab.
     4. Open the **Top shards** tab.
     5. In the **Immediate** and **Historical** tabs, sort the shards by the **CPUCores** column and analyze the information.

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/schemas/_assets/partitions-by-cpu.png)

     Additionally, the information about overloaded shards is provided as a system table. For more information, see [History of overloaded partitions](../../../dev/system-views.md#top-overload-partitions).

2. To pinpoint the schema issue, use the [Embedded UI](../../../reference/embedded-ui/index.md) or [YDB CLI](../../../reference/ydb-cli/index.md):

   - In the [Embedded UI](../../../reference/embedded-ui/index.md):

     1. On the **Databases** tab, click on the database.

     2. On the **Navigation** tab, select the required table.

     3. Open the **Diagnostics** tab.

     4. On the **Describe** tab, navigate to `root > PathDescription > Table > PartitionConfig > PartitioningPolicy`.

        ![Describe](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/schemas/_assets/describe.png)

     5. Analyze the **PartitioningPolicy** values:

        - `SizeToSplit`
        - `SplitByLoadSettings`
        - `MaxPartitionsCount`

        If the table does not have these options, see [Recommendations for table configuration](overloaded-shards.md#table-config).

     > [!NOTE]
     > You can also find this information on the **Diagnostics > Info** tab.

   - In the [YDB CLI](../../../reference/ydb-cli/index.md):

     1. To retrieve information about the problematic table, run the following command:

        ```bash
        ydb scheme describe <table_name>
        ```

     2. In the command output, analyze the **Auto partitioning settings**:

        - `Partitioning by size`
        - `Partitioning by load`
        - `Max partitions count`

        If the table does not have these options, see [Recommendations for table configuration](overloaded-shards.md#table-config).

3. Analyze whether primary key values increment monotonically:

   - Check the data type of the primary key column. `Serial` data types are used for autoincrementing values.
   - Check the application logic.
   - Calculate the difference between the minimum and maximum values of the primary key column. Then compare this value to the number of rows in a given table. If these values match, the primary key might be incrementing monotonically.

   If primary key values do increase monotonically, see [Recommendations for the imbalanced primary key](overloaded-shards.md#pk-recommendations).

## Recommendations

### For table configuration {#table-config}

Consider the following solutions to address shard overload:

- If the problematic table is not partitioned by load, enable partitioning by load.

  > [!TIP]
  > A table is not partitioned by load, if you see the `Partitioning by load: false` line on the **Diagnostics > Info** tab in the **Embedded UI** or the `ydb scheme describe` command output.

- If the table has reached the maximum number of partitions, increase the partition limit.

  > [!TIP]
  > To determine the number of partitions in the table, see the `PartCount` value on the **Diagnostics > Info** tab in the **Embedded UI**.

Both operations can be performed by executing an [`ALTER TABLE ... SET`](../../../yql/reference/syntax/alter_table/set.md) query.

### For the imbalanced primary key {#pk-recommendations}

Consider modifying the primary key to distribute the load evenly across table partitions. You cannot change the primary key of an existing table. To do that, you will have to create a new table with the modified primary key and then migrate the data to the new table.

> [!NOTE]
> Also, consider changing your application logic for generating primary key values for new rows. For example, use hashes of values instead of values themselves.

## Example

For a practical demonstration of how to follow these instructions, see [Overloaded shard example](../../examples/schemas/overloaded-shard-simple-case.md).
