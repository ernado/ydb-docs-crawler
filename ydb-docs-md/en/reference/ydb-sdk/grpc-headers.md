---
title: "en/reference/ydb-sdk/grpc-headers"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/grpc-headers?version=v26.1"
doc_path: "en/reference/ydb-sdk/grpc-headers"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/grpc-headers.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/grpc-headers.md"
description: "gRPC metadata headers. YDB uses the following gRPC metadata headers: gRPC headers which a client sends to YDB: x-ydb-database - database."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# en/reference/ydb-sdk/grpc-headers

## gRPC metadata headers

YDB uses the following gRPC metadata headers:

- gRPC headers which a client sends to YDB:

  - `x-ydb-database` - database
  - `x-ydb-auth-ticket` - auth token from a credentials provider
  - `x-ydb-sdk-build-info` - YDB SDK build info
  - `x-ydb-trace-id` - user-defined request ID. If not defined by client YDB SDK generates automatically using [UUID](https://en.wikipedia.org/wiki/UUID) format
  - `x-ydb-application-name` - optional user-defined application name
  - `x-ydb-client-capabilities` - supported client SDK capabilities (`session-balancer` and other)
  - `x-ydb-client-pid` - client application process ID
  - `traceparent` - OpenTelemetry trace ID ([specification](https://w3c.github.io/trace-context/#header-name))

- gRPC headers which YDB sends to client with responses:

  - `x-ydb-server-hints` - notifications from YDB (such as `session-close` and other)
  - `x-ydb-consumed-units` - consumed units on the current request
