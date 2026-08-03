---
title: "Обзор gRPC API"
url: "https://ydb.tech/docs/ru/reference/ydb-sdk/overview-grpc-api?version=v26.1"
doc_path: "ru/reference/ydb-sdk/overview-grpc-api"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-sdk/overview-grpc-api.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-sdk/overview-grpc-api.md"
description: "YDB предоставляет gRPC API, с помощью которого вы можете управлять ресурсами и данными БД. Для описания методов и структур данных API используется Protocol Buff"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Обзор gRPC API

YDB предоставляет gRPC API, с помощью которого вы можете управлять [ресурсами](../../concepts/datamodel/index.md) и данными БД. Для описания методов и структур данных API используется [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/proto3) (proto 3). Подробнее смотрите [.proto-спецификации с комментариями](https://github.com/ydb-platform/ydb-api-protos). Также YDB использует специальные [заголовки метаданных gRPC](grpc-headers.md).

Доступны следующие сервисы:

- [Health Check API](health-check-api.md).
