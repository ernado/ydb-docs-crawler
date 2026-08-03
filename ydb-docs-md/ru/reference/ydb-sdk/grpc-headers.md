---
title: "ru/reference/ydb-sdk/grpc-headers"
url: "https://ydb.tech/docs/ru/reference/ydb-sdk/grpc-headers?version=v26.1"
doc_path: "ru/reference/ydb-sdk/grpc-headers"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-sdk/grpc-headers.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-sdk/grpc-headers.md"
description: "Заголовки метаданных gRPC. YDB использует следующие gRPC metadata заголовки: gRPC заголовки, отправляемые клиентом в YDB: x-ydb-database - база данных."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ru/reference/ydb-sdk/grpc-headers

## Заголовки метаданных gRPC {#zagolovki-metadannyh-grpc}

YDB использует следующие gRPC metadata заголовки:

- gRPC заголовки, отправляемые клиентом в YDB :

  - `x-ydb-database` - база данных
  - `x-ydb-auth-ticket` - токен авторизации, полученный от провайдера авторизации
  - `x-ydb-sdk-build-info` - информация о YDB SDK
  - `x-ydb-trace-id` - идентификатор запроса, устанавливаемый пользователем. Если не задано пользователем - YDB SDK генерирует автоматически в формате [UUID](https://ru.wikipedia.org/wiki/UUID)
  - `x-ydb-application-name` - опциональное имя приложения, устанавливаемое пользователем
  - `x-ydb-client-capabilities` - поддерживаемые клиентским SDK возможности (`session-balancer` и другие)
  - `x-ydb-client-pid` - идентификатор процесса клиентского приложения
  - `traceparent` - заголовок для передачи родительского идентификатора трассы OpenTelemetry ([спецификация](https://w3c.github.io/trace-context/#header-name))

- gRPC заголовки, отправляемые клиенту YDB вместе с ответом на текущий запрос:

  - `x-ydb-server-hints` - уведомления YDB (`session-close` и другие)
  - `x-ydb-consumed-units` - потребленные ресурсов YDB на текущем запросе
