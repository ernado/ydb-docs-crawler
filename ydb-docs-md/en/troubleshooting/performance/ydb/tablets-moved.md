---
title: "Frequent tablet moves between nodes"
url: "https://ydb.tech/docs/en/troubleshooting/performance/ydb/tablets-moved?version=v26.1"
doc_path: "en/troubleshooting/performance/ydb/tablets-moved"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/ydb/tablets-moved.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/ydb/tablets-moved.md"
description: "YDB automatically balances the load by moving tablets from overloaded nodes to other nodes. This process is managed by Hive. When Hive moves tablets, queries af"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Frequent tablet moves between nodes

YDB automatically balances the load by moving tablets from overloaded nodes to other nodes. This process is managed by [Hive](../../../concepts/glossary.md#hive). When Hive moves tablets, queries affecting those tablets might experience increased latencies while they wait for the tablet to get initialized on the new node.

YDB considers usage of the following hardware resources for balancing nodes:

- CPU
- Memory
- Network
- *Counter*

Autobalancing occurs in the following cases:

- **Imbalanced Hardware Resource Usage**

  YDB uses the Scatter metric to evaluate the balance of hardware resource usage. For more details on the Scatter metric's calculation logic and balancing triggers, see the [Resource Usage Imbalance](../../../contributor/hive.md#scatter) section.

- **Overloaded nodes (CPU and memory usage)**

  Hive initiates balancing in case of a significant load asymmetry (for example, > 90% on one node and < 70% on another). Learn more here: [Node Overload](../../../contributor/hive.md#emergency).

- **Uneven distribution of database objects**

  For tablets with no explicit resource consumption, Hive uses a fake **Counter** resource to ensure their even distribution. Balancing is triggered if this distribution becomes skewed. Learn more: [Even Distribution for a Specific Object](../../../contributor/hive.md#imbalance).

## Diagnostics

1. See if the **Tablets moved by Hive** chart in the **[DB status](../../../reference/observability/metrics/grafana-dashboards.md#dbstatus)** Grafana dashboard shows any spikes.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/ydb/_assets/tablets-moved.png)

   ```
    This chart displays the time-series data for the number of tablets moved per second.
   ```

2. See the Hive balancer stats.

   1. Open [Embedded UI](../../../reference/embedded-ui/index.md).

   2. Click **Developer UI** in the upper right corner of the Embedded UI.

   3. In the **Developer UI**, navigate to **Tablets > Hive > App**.

      See the balancer stats in the upper right corner.

      ![cpu balancer](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/ydb/_assets/cpu-balancer.jpg)

   4. Additionally, to see the recently moved tablets, click the **Balancer** button.

      The **Balancer** window will appear. The list of recently moved tablets is displayed in the **Latest tablet moves** section.

## Recommendations

Adjust Hive balancer settings:

1. Open [Embedded UI](../../../reference/embedded-ui/index.md).

2. Click **Developer UI** in the upper right corner of the Embedded UI.

3. In the **Developer UI**, navigate to **Tablets > Hive > App**.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/ydb/_assets/hive-app.png)

4. Click **Settings**.

5. To reduce the likelihood of overly frequent balancing, increase the following Hive balancer thresholds:

   |  |  |  |
   | --- | --- | --- |
   | Parameter | Description | Default value |
   | MinCounterScatterToBalance | The threshold for the counter scatter value. When this value is reached, Hive starts balancing the load. | 0.02 |
   | MinCPUScatterToBalance | The threshold for the CPU scatter value. When this value is reached, Hive starts balancing the load. | 0.5 |
   | MinMemoryScatterToBalance | The threshold for the memory scatter value. When this value is reached, Hive starts balancing the load. | 0.5 |
   | MinNetworkScatterToBalance | The threshold for the network scatter value. When this value is reached, Hive starts balancing the load. | 0.5 |
   | MaxNodeUsageToKick | The threshold for the node resource usage. When this value is reached, Hive starts emergency balancing. | 0.9 |
   | ObjectImbalanceToBalance | The threshold for the database object imbalance metric. | 0.02 |

   > [!NOTE]
   > These parameters use relative values, where 1.0 represents 100% and effectively disables balancing. If the total hardware resource value can exceed 100%, adjust the ratio accordingly.

*Counter - a fake resource representing a count of tablets of a certain type on a node, used to ensure such tablets are distributed evenly across nodes.*
