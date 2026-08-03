---
title: "Hardware issues"
url: "https://ydb.tech/docs/en/troubleshooting/performance/infrastructure/hardware?version=v26.1"
doc_path: "en/troubleshooting/performance/infrastructure/hardware"
version: "v26.1"
lang: "en"
source_path: "en/core/troubleshooting/performance/infrastructure/hardware.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/troubleshooting/performance/infrastructure/hardware.md"
description: "Malfunctioning storage drives and network cards, until replaced, significantly impact database performance up to total unavailability of the affected server. CP"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Hardware issues

Malfunctioning storage drives and network cards, until replaced, significantly impact database performance up to total unavailability of the affected server. CPU issues might lead to server failure and higher load on the remaining YDB nodes.

## Diagnostics

Use the hardware monitoring tools that your operating system and data center provide to diagnose hardware issues.

You can also use the **Healthcheck** in [Embedded UI](../../../reference/embedded-ui/index.md) to diagnose some hardware issues:

- **Storage issues**

  1. On the **Storage** tab, select the **Degraded** filter to list storage groups or nodes that contain degraded or failed storage.
  2. Check for any degradation in the storage system performance on the **Distributed Storage Overview** and **PDisk Device single disk** dashboards in Grafana.

- **Network issues**

  Refer to [Network issues](network.md).

## Recommendations

Contact the responsible party for the affected hardware to resolve the underlying issue. If you are part of a larger organization, this could be an in-house team managing low-level infrastructure. Otherwise, contact the cloud service or hosting provider's support service.
