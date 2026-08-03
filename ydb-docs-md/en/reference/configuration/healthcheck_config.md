---
title: "healthcheck_config"
url: "https://ydb.tech/docs/en/reference/configuration/healthcheck_config?version=v26.1"
doc_path: "en/reference/configuration/healthcheck_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/healthcheck_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/healthcheck_config.md"
description: "The healthcheck_config section configures thresholds and timeout settings used by the YDB health check service. These parameters help configure detection of pot"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# healthcheck_config

The `healthcheck_config` section configures thresholds and timeout settings used by the YDB [health check service](../ydb-sdk/health-check-api.md). These parameters help configure detection of potential [issues](../ydb-sdk/health-check-api.md#issues), such as excessive restarts or time drift between dynamic nodes.

## Syntax

```yaml
healthcheck_config:
  thresholds:
    node_restarts_yellow: 10
    node_restarts_orange: 30
    nodes_time_difference_yellow: 5000
    nodes_time_difference_orange: 25000
    tablets_restarts_orange: 30
  timeout: 20000
```

## Parameters

| Parameter | Default | Description |
| --- | --- | --- |
| `thresholds.node_restarts_yellow` | `10` | Number of node restarts to trigger a `YELLOW` warning |
| `thresholds.node_restarts_orange` | `30` | Number of node restarts to trigger an `ORANGE` alert |
| `thresholds.nodes_time_difference_yellow` | `5000` | Max allowed time difference (in us) between dynamic nodes for `YELLOW` issue |
| `thresholds.nodes_time_difference_orange` | `25000` | Max allowed time difference (in us) between dynamic nodes for `ORANGE` issue |
| `thresholds.tablets_restarts_orange` | `30` | Number of tablet restarts to trigger an `ORANGE` alert |
| `timeout` | `20000` | Maximum health check response time (in ms) |
