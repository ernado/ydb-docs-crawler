---
title: "Network issues"
url: "https://ydb.tech/docs/en/troubleshooting/performance/infrastructure/network?version=v26.1"
doc_path: "en/troubleshooting/performance/infrastructure/network"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/infrastructure/network.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/network.md"
description: "Network performance issues, such as limited bandwidth, packet loss, and connection instability, can severely impact database performance by slowing query respon"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Network issues

Network performance issues, such as limited bandwidth, packet loss, and connection instability, can severely impact database performance by slowing query response times and leading to retriable errors like timeouts.

## Diagnostics

To diagnose network issues, use the healthcheck in the [Embedded UI](../../../reference/embedded-ui/index.md):

1. Open the [Embedded UI](../../../reference/embedded-ui/index.md):

   1. Navigate to the **Databases** tab and click on the desired database.

   2. In the **Navigation** tab, confirm the required database is selected.

   3. Switch to the **Diagnostics** tab.

   4. Under the **Network** tab, apply the **With problems** filter.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/_assets/diagnostics-network.png)

2. Use available third-party tools to monitor network performance metrics such as latency, jitter, packet loss, throughput, and others.

## Recommendations

Contact the responsible party for the network infrastructure the YDB cluster uses. If you are part of a larger organization, this could be an in-house network operations team. Otherwise, contact the cloud service or hosting provider's support service.
