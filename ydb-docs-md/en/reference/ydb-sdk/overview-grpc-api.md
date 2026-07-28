---
title: "gRPC API overview"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/overview-grpc-api?version=v26.1"
doc_path: "en/reference/ydb-sdk/overview-grpc-api"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/overview-grpc-api.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/overview-grpc-api.md"
description: "YDB provides the gRPC API, which you can use to manage your DB resources and data. API methods and data structures are described using Protocol Buffers (proto 3"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# gRPC API overview

YDB provides the gRPC API, which you can use to manage your DB [resources](../../concepts/datamodel/index.md) and data. API methods and data structures are described using [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/proto3) (proto 3). For more information, see [.proto specifications with comments](https://github.com/ydb-platform/ydb-api-protos). Also YDB uses special [gRPC metadata headers](grpc-headers.md).

The following services are available:

- [Health Check API](health-check-api.md).
