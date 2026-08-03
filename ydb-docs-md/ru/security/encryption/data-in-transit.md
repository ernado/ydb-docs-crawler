---
title: "Шифрование данных при передаче"
url: "https://ydb.tech/docs/ru/security/encryption/data-in-transit?version=v26.1"
doc_path: "ru/security/encryption/data-in-transit"
version: "v26.1"
lang: "ru"
source_path: "ru/core/security/encryption/data-in-transit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/security/encryption/data-in-transit.md"
description: "Так как YDB является распределённой системой, обычно работающей на кластере, часто расположенным в нескольких датацентрах или зонах доступности, пользовательски"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Шифрование данных при передаче

Так как YDB является распределённой системой, обычно работающей на кластере, часто расположенным в нескольких датацентрах или зонах доступности, пользовательские данные регулярно передаются по сети. Могут использоваться различные протоколы, каждый из которых может быть настроен для работы с использованием [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security). Ниже приведён список протоколов, поддерживаемых YDB:

- [Интерконнект](../../concepts/glossary.md#actor-system-interconnect) — специализированный протокол для общения между узлами YDB.

- YDB в роли сервера:

  - [gRPC](../../reference/ydb-sdk/overview-grpc-api.md) — для внешнего взаимодействия с клиентскими приложениями, разработанными для нативной работы с YDB через [SDK](../../reference/ydb-sdk/index.md) или [CLI](../../reference/ydb-cli/index.md).
  - [Протокол Kafka](../../reference/kafka-api/index.md) — для внешнего взаимодействия с клиентскими приложениями, изначально разработанными для работы с [Apache Kafka](https://kafka.apache.org/).
  - HTTP — для работы с [встроенным UI](../../reference/embedded-ui/index.md), публикации [метрик](../../devops/observability/monitoring.md) и других вспомогательных конечных эндпоинтов.

- YDB в роли клиента:

  - [LDAP](../authentication.md#ldap) — для аутентификации пользователей.
  - [Федеративные запросы](../../concepts/query_execution/federated_query/index.md) — функциональность, позволяющая YDB выполнять запросы к различным внешним источникам данных. Запросы к некоторым источникам отправляются напрямую из процесса `ydbd`, в то время как другие проксируются через отдельный процесс-коннектор.
  - [Трассировочные](../../reference/observability/tracing/setup.md) данные отправляются во внешний сборщик через gRPC.

- В [асинхронной репликации](../../concepts/async-replication.md) между двумя базами данных YDB одна из них выступает в роли клиента по отношению к другой.

- В [трансфере](../../concepts/transfer.md) между двумя базами данных YDB одна из них выступает в роли клиента по отношению к другой.

По умолчанию шифрование данных при передаче отключено и должно быть включено отдельно для каждого протокола. Они могут использовать общий набор TLS-сертификатов или отдельные. Инструкции по включению TLS можно найти в разделе [tls](../../reference/configuration/tls.md).
