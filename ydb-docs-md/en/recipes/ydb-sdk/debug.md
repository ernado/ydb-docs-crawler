---
title: "Troubleshooting"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/debug?version=v26.1"
doc_path: "en/recipes/ydb-sdk/debug"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/debug.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/debug.md"
description: "When troubleshooting issues with YDB, diagnostics tools such as logging, metrics, and distributed tracing are helpful. We strongly recommend that you enable the"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Troubleshooting

When troubleshooting issues with YDB, diagnostics tools such as logging, metrics, and distributed tracing are helpful. We strongly recommend that you enable them in advance, before any problems occur, to see the full picture of the system's state before, during, and after a failure when investigating an incident.

This section contains code recipes for enabling diagnostics tools in different YDB SDKs.

Table of contents:

- [Enable logging](debug-logs.md)
- [Enable metrics in Prometheus](debug-prometheus.md)
- [Enable tracing in OpenTelemetry](debug-otel.md)
- [Enable tracing in Jaeger](debug-jaeger.md)
