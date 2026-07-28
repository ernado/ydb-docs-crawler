---
title: "Charts"
url: "https://ydb.tech/docs/en/reference/embedded-ui/charts?version=v26.1"
doc_path: "en/reference/embedded-ui/charts"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/embedded-ui/charts.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/embedded-ui/charts.md"
description: "To view charts, use Grafana. The main metrics of the system are displayed on the dashboard:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Charts

To view charts, use Grafana.

The main metrics of the system are displayed on the dashboard:

- **CPU Usage**: The total CPU utilization on all nodes (1 000 000 = 1 CPU).
- **Memory Usage**: RAM utilization by nodes.
- **Disk Space Usage**: Disk space utilization by nodes.
- **SelfPing**: The highest actual delivery time of deferred messages in the actor system over the measurement interval. Measured for messages with a 10 ms delivery delay. If this value grows, it might indicate microbursts of workload, high CPU utilization, or displacement of the YDB process from CPU cores by other processes.
