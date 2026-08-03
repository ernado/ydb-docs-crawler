---
title: "I/O bandwidth"
url: "https://ydb.tech/docs/en/troubleshooting/performance/hardware/io-bandwidth?version=v26.1"
doc_path: "en/troubleshooting/performance/hardware/io-bandwidth"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/hardware/io-bandwidth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/hardware/io-bandwidth.md"
description: "A high rate of read and write operations can overwhelm the disk subsystem, leading to increased data access latencies. When the system cannot read or write data"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# I/O bandwidth

A high rate of read and write operations can overwhelm the disk subsystem, leading to increased data access latencies. When the system cannot read or write data quickly enough, queries that rely on disk access will experience delays.

## Diagnostics

1. Open the **[Distributed Storage Overview](../../../reference/observability/metrics/grafana-dashboards.md)** dashboard in Grafana.

2. On the **DiskTimeAvailable and total Cost relation** chart, see if the **Total Cost** spikes cross the **DiskTimeAvailable** level.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/disk-time-available--disk-cost.png)

   This chart shows the estimated total bandwidth capacity of the storage system in conventional units (green) and the total usage cost in conventional units (blue). When the total usage cost exceeds the total bandwidth capacity, the YDB storage system becomes overloaded, leading to increased latencies.

3. On the **Total burst duration** chart, check for any load spikes on the storage system. This chart displays microbursts of load on the storage system, measured in microseconds.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/hardware/_assets/microbursts.png)

   > [!NOTE]
   > This chart might show microbursts of the load that are not detected by the average usage cost in the **Cost and DiskTimeAvailable relation** chart.

## Recommendations

Add more [storage groups](../../../concepts/glossary.md#storage-group) to the database.

In cases of high microburst rates, balancing the load across storage groups might help.
