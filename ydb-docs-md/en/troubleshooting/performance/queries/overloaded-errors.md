---
title: "Overloaded errors"
url: "https://ydb.tech/docs/en/troubleshooting/performance/queries/overloaded-errors?version=v26.1"
doc_path: "en/troubleshooting/performance/queries/overloaded-errors"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/queries/overloaded-errors.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/queries/overloaded-errors.md"
description: "YDB returns OVERLOADED errors in the following cases: Overloaded table partitions with over 15000 queries in their queue."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Overloaded errors

YDB returns `OVERLOADED` errors in the following cases:

- Overloaded table partitions with over 15000 queries in their queue.
- The outbound [CDC](../../../concepts/glossary.md#cdc) queue exceeds the limit of 10000 elements or 125 MB.
- Table partitions in states other than normal, for example partitions in the process of splitting or merging.
- The number of sessions with a YDB node has reached the limit of 1000.

## Diagnostics

1. Open the **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** Grafana dashboard.

2. In the **API details** section, see if the **Soft errors (retriable)** chart shows any spikes in the rate of queries with the `OVERLOADED` status.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/queries/_assets/soft-errors.png)

3. To check if the spikes in overloaded errors were caused by exceeding the limit of 15000 queries in table partition queues:

   1. In the [Embedded UI](../../../reference/embedded-ui/index.md), go to the **Databases** tab and click on the database.
   2. On the **Navigation** tab, ensure the required database is selected.
   3. Open the **Diagnostics** tab.
   4. Open the **Top shards** tab.
   5. In the **Immediate** and **Historical** tabs, sort the shards by the **InFlightTxCount** column and see if the top values reach the 15000 limit.

4. To check if the spikes in overloaded errors were caused by tablet splits and merges, see [Excessive tablet splits and merges](../schemas/splits-merges.md).

5. To check if the spikes in overloaded errors were caused by exceeding the 1000 limit of open sessions, in the Grafana **[DB status](../../../reference/observability/metrics/grafana-dashboards.md#dbstatus)** dashboard, see the **Session count by host** chart.

6. See the [overloaded shards](../schemas/overloaded-shards.md) issue.

## Recommendations

If a YQL query returns an `OVERLOADED` error, retry the query using a randomized exponential back-off strategy. The YDB SDK provides a built-in mechanism for handling temporary failures. For more information, see [Handling errors](../../../reference/ydb-sdk/error_handling.md).

Exceeding the limit of open sessions per node may indicate a problem in the application logic.
