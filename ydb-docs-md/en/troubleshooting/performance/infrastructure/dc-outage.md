---
title: "Data center outages"
url: "https://ydb.tech/docs/en/troubleshooting/performance/infrastructure/dc-outage?version=v26.1"
doc_path: "en/troubleshooting/performance/infrastructure/dc-outage"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/infrastructure/dc-outage.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/dc-outage.md"
description: "Data center outages are disruptions in data center operations that could cause service or data unavailability, but YDB has means to avoid it. Various factors, s"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Data center outages

Data center outages are disruptions in data center operations that could cause service or data unavailability, but YDB has means to avoid it. Various factors, such as power failures, natural disasters, or cyberattacks, may cause these outages. A common fault-tolerant setup for YDB spans three data centers or availability zones (AZs). In this case, YDB can maintain uninterrupted operation even if one data center and a server rack in another are lost. However, it will initiate the relocation of tablets from the offline AZ to the remaining online nodes, temporarily leading to higher query latencies.

## Diagnostics

To determine if one of the data centers of the YDB cluster is not available, follow these steps:

1. Open [Embedded UI](../../../reference/embedded-ui/index.md).

2. On the **Nodes** tab, analyze the [health indicators](../../../reference/embedded-ui/ydb-monitoring.md#colored_indicator) in the **Host** and **DC** columns.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/_assets/cluster-nodes.png)

   If all of the nodes in one of the data centers (DC) are not available, this data center is most likely offline.

   If not, review the **Rack** column to check if all YDB nodes are unavailable in one or more server racks. This could indicate that these racks are offline, which could be treated as a partial data center outage.

## Recommendations

Contact the responsible party for the affected data center to resolve the underlying issue. If you are part of a larger organization, this could be an in-house team managing low-level infrastructure. Otherwise, contact the cloud service or hosting provider's support service. Meanwhile, check the data center's status page if it has one.

Additionally, consider potential data center outages in the capacity planning process. YDB nodes in each data center should have sufficient spare hardware resources to take over the full workload typically handled by any data center experiencing an outage.
