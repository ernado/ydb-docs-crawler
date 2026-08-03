---
title: "Overloaded shard example"
url: "https://ydb.tech/docs/en/troubleshooting/examples/schemas/overloaded-shard-simple-case?version=v26.1"
doc_path: "en/troubleshooting/examples/schemas/overloaded-shard-simple-case"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/examples/schemas/overloaded-shard-simple-case.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/examples/schemas/overloaded-shard-simple-case.md"
description: "This article describes an example of how to diagnose overloaded shards and resolve the issue."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Overloaded shard example

This article describes an example of how to diagnose overloaded shards and resolve the issue.

For more information about overloaded shards and their causes, see [Overloaded shards](../../performance/schemas/overloaded-shards.md).

The article begins by [stating the problem](overloaded-shard-simple-case.md#initial-issue). Then, we'll examine diagrams in Grafana and information on the **Diagnostics** tab in the [Embedded UI](../../../reference/embedded-ui/index.md) to [solve the problem](overloaded-shard-simple-case.md#solution) and [observe the solution in action](overloaded-shard-simple-case.md#aftermath).

At the end of the article, you can find the steps to [reproduce the situation](overloaded-shard-simple-case.md#testbed).

## Initial issue

You were notified that your system has started taking too long to process user requests.

> [!NOTE]
> These requests access a [row-oriented table](../../../concepts/datamodel/table.md#row-oriented-tables), which is managed by [data shards](../../../concepts/glossary.md#data-shard).

Let's examine the **Latency** diagrams in the [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview) Grafana dashboard to determine whether the problem is related to the YDB cluster:

![DB Overview > Latencies > R tx server latency percentiles](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-latency-percentiles.png)

<details>
<summary>See the diagram description</summary>

The diagram shows transaction latency percentiles. At approximately `10:19:30`, these values increased by two to three times.

</details>

![DB Overview > Latencies > Read only tx server latency](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-latencies.png)

<details>
<summary>See the diagram description</summary>

The diagram shows a heatmap of transaction latencies. Transactions are grouped into buckets based on their latency, with each bucket represented by a different color. This diagram displays both the number of transactions processed by YDB per second (on the vertical axis) and the latency distribution among them (with color).

By `10:20:30`, the share of transactions with the lowest latencies (`Bucket 1`, dark green) had dropped by four to five times. `Bucket 4` grew by approximately five times, and a new group of slower transactions, `Bucket 8`, appeared.

</details>

Indeed, the latencies have increased. Now, we need to localize the problem.

## Diagnostics

Let's determine why the latencies increased. Could the cause be an increased workload? Here is the **Requests** diagram from the **API details** section of the [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview) Grafana dashboard:

![API details](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-api-section-requests.png)

The number of user requests increased from approximately 27,000 to 35,000 at around `10:20:00`. But can YDB handle the increased load without additional hardware resources?

The CPU load has increased, as shown in the **CPU by execution pool** diagram.

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-by-execution-pool.png)

<details>
<summary>See the details on the CPU Grafana dashboard</summary>

Examining the **CPU** Grafana dashboard reveals that CPU usage increased [in the user pool and the interconnect pool](../../../concepts/glossary.md#actor-system-pool):

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-user-pool-by-actors.png)

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-ic-pool.png)

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-ic-pool-by-host.png)

</details>

We can also observe overall CPU usage on the **Diagnostics** tab of the [Embedded UI](../../../reference/embedded-ui/index.md):

![CPU diagnostics](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-cpu-usage.png)

The YDB cluster appears not to utilize all of its CPU capacity.

By inspecting the **DataShard** and **DataShard details** sections of the [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview) Grafana dashboard, we can see that after the cluster load increased, one of its data shards became overloaded.

![Throughput](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-throughput-rows.png)

<details>
<summary>See the diagram description</summary>

This diagram shows that the number of rows read per second in the YDB database increased from approximately 26,000 to 33,500 rows per second.

</details>

![Shard distribution by load](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-shard-distribution-by-workload.png)

<details>
<summary>See the diagram description</summary>

This diagram shows a heatmap of data shard distribution by workload. Data shards are grouped into ten buckets based on the ratio of their current workload to full computing capacity. This allows you to see how many data shards your YDB cluster currently runs and how loaded they are.

The diagram shows only one data shard whose workload changed at approximately `10:19:30`—the data shard moved to `Bucket 70`, which contains shards loaded to between 60% and 70% of their capacity.

</details>

![Overloaded shard](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-overloaded-shards.png)

<details>
<summary>See the diagram description</summary>

Similar to the previous diagram, the **Overloaded shard count** is a heatmap of data shard distribution by load. However, it displays only data shards with a workload exceeding 60%.

This diagram shows that the workload on one data shard increased to 70% at approximately `10:19:30`.

</details>

To determine which table the overloaded data shard is processing, let's open the **Diagnostics > Top shards** tab in the Embedded UI:

![Diagnostics > shards](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-top-shards.png)

We can see that one of the data shards processing queries for the `kv_test` table is loaded at 67%.

Next, let's examine the `kv_test` table on the **Info** tab:

![stock table info](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-table-info.png)

> [!WARNING]
> The `kv_test` table was created with partitioning by load disabled and has only one partition.
>
> This means that a single data shard processes all requests to this table. Since data shards are single-threaded and thus can handle only one request at a time, this is a poor practice.

## Solution

We should enable partitioning by load for the `kv_test` table:

1. In the Embedded UI, select the database.

2. Open the **Query** tab.

3. Run the following query:

   ```yql
   ALTER TABLE kv_test SET (
       AUTO_PARTITIONING_BY_LOAD = ENABLED
   );
   ```

## Aftermath

When we enable automatic partitioning for the `kv_test` table, the overloaded data shard splits into two.

![Shard distribution by load](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-shard-distribution-by-workload.png)

<details>
<summary>See the diagram description</summary>

The diagram shows that the number of data shards increased at about `10:28:00`. Based on the bucket color, their workload does not exceed 40%.

</details>

![overloaded shard count](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-overloaded-shards.png)

<details>
<summary>See the diagram description</summary>

The overloaded shard disappeared from the diagram at approximately `10:28:00`.

</details>

Now, two data shards are processing queries to the `kv_test` table, and neither is overloaded:

![Overloaded shard count](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-ui-top-shards.png)

Let's confirm that latencies have returned to normal:

![Final latency percentiles](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-latency-percentiles.png)

<details>
<summary>See the diagram description</summary>

At approximately `10:28:00`, the p50, p75, and p95 latency percentiles dropped almost to their original levels. The decrease in p99 latency is less pronounced but still shows a twofold reduction.

</details>

![Final latencies](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-latencies.png)

<details>
<summary>See the diagram description</summary>

The diagram shows that transactions are now grouped into six buckets. Approximately half of the transactions have returned to `Bucket 1`, meaning their latency is less than one millisecond. More than a third of the transactions are in `Bucket 2`, with latencies between one and two milliseconds. One-sixth of the transactions are in `Bucket 4`. The sizes of the other buckets are insignificant.

</details>

The latencies are almost as low as they were before the workload increased. We did not increase the system costs by introducing additional hardware resources. We've only enabled automatic partitioning by the load, which allowed us to use the existing resources more efficiently.

|  |  |  |  |
| --- | --- | --- | --- |
| Bucket name | Latencies, ms | Single overloaded data shard,  <br> transactions per second | Multiple data shards,  <br> transactions per second |
| 1 | 0-1 | 2110 | ▲ 16961 |
| 2 | 1-2 | 5472 | ▲ 13147 |
| 4 | 2-4 | 16437 | ▼ 6041 |
| 8 | 4-8 | 9430 | ▼ 432 |
| 16 | 8-16 | 98.8 | ▼ 52.4 |
| 32 | 16-32 | — | ▲ 0.578 |

## Testbed

### Topology

For this example, we used a YDB cluster consisting of three servers running Ubuntu 22.04 LTS. Each server runs one [storage node](../../../concepts/glossary.md#storage-node) and three [database nodes](../../../concepts/glossary.md#database-node) belonging to the same database.

### Hardware configuration

The servers are virtual machines with the following computing resources:

- Platform: Intel Broadwell

- Guaranteed vCPU performance: 100%

- vCPU: 28

- RAM: 32 GB

- Storage:

  - 3 x 93 GB SSD per storage node
  - 20 GB HDD for the operating system

### Test

The load on the YDB cluster was generated using the `ydb workload` CLI command. For more information, see [Load testing](../../../reference/ydb-cli/commands/workload/index.md).

To reproduce the load, follow these steps:

1. Initialize the tables for the workload test:

   ```shell
   ydb workload kv init --min-partitions 1 --auto-partition 0
   ```

   We deliberately disable automatic partitioning for the created tables by using the `--min-partitions 1 --auto-partition 0` options.

2. Emulate the standard workload on the YDB cluster:

   ```shell
   ydb workload kv run select -s 600 -t 100
   ```

   We ran a simple load type using a YDB database as a key-value storage. Specifically, we used the `select` load to create SELECT queries and retrieve rows based on an exact match of the primary key.

   The `-t 100` parameter is used to run the test in 100 threads.

3. Overload the YDB cluster:

   ```shell
   ydb workload kv run select -s 1200 -t 250
   ```

   As soon as the first test ended, we ran the same load test in 250 threads to simulate the overload.

## See also

- [Troubleshooting performance issues](../../performance/index.md)
- [Overloaded shards](../../performance/schemas/overloaded-shards.md)
- [Row-oriented tables](../../../concepts/datamodel/table.md#row-oriented-tables)
