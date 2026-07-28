---
title: "Passing external trace-id in YDB"
url: "https://ydb.tech/docs/en/reference/observability/tracing/external-traces?version=v26.1"
doc_path: "en/reference/observability/tracing/external-traces"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/observability/tracing/external-traces.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/observability/tracing/external-traces.md"
description: "gRPC API."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Passing external trace-id in YDB

## gRPC API

YDB supports the transmission of external trace-ids to construct a comprehensive operation trace. The transmission of trace-ids is carried out according to the [trace context specification](https://w3c.github.io/trace-context/#traceparent-header). The `traceparent` header of the gRPC request should contain a string of the form `00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01`. It consists of four parts, separated by the `-` character:

1. Version – at the time of writing, the specification defines only version 00.
2. Trace id – the identifier of the trace that the request is part of.
3. Parent id – the identifier of the parent span.
4. Flags – a set of recommendations for working with the data transmitted in the header.

Only version 00 is supported, and flags are ignored. If the header does not comply with the specification, it is ignored. All traces obtained in this way have a [tracing level](setup.md#tracing-levels) of 13 (all components are traced at the `Detailed` level).

> [!WARNING]
> If the [`external_throttling`](setup.md#external-throttling) section is present and the request flow exceeds the established limits, not all requests may be traced. If the [`external_throttling`](setup.md#external-throttling) section is absent, the `traceparent` header is **ignored** and no external traces are continued.

## SDK support

Some SDKs support the transmission of trace-ids. You can find their list and usage examples on the [Enabling tracing in Jaeger](../../../recipes/ydb-sdk/debug-otel.md) page.
