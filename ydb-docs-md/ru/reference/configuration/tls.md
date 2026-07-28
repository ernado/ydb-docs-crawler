---
title: "tls"
url: "https://ydb.tech/docs/ru/reference/configuration/tls?version=v26.1"
doc_path: "ru/reference/configuration/tls"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/tls.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/tls.md"
description: "Секция tls настраивает параметры TLS для шифрования данных при передаче по сети в YDB. Каждый сетевой протокол может иметь различные настройки TLS для обеспечен"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# tls

Секция `tls` настраивает параметры [TLS](https://ru.wikipedia.org/wiki/Transport_Layer_Security) для [шифрования данных при передаче по сети](../../security/encryption/data-in-transit.md) в YDB. Каждый сетевой протокол может иметь различные настройки TLS для обеспечения безопасной связи между компонентами кластера и клиентами.

## Interconnect

[Интерконнект акторной системы YDB](../../concepts/glossary.md#actor-system-interconnect) — это специализированный протокол для обмена данными между узлами YDB.

Пример включения TLS для интерконнекта:

```yaml
interconnect_config:
   start_tcp: true
   encryption_mode: REQUIRED # или OPTIONAL
   path_to_certificate_file: "/opt/ydb/certs/node.crt"
   path_to_private_key_file: "/opt/ydb/certs/node.key"
   path_to_ca_file: "/opt/ydb/certs/ca.crt"
```

## YDB в роли сервера {#ydb-v-roli-servera}

### gRPC

[Основной API YDB](../ydb-sdk/overview-grpc-api.md) основан на [gRPC](https://grpc.io/). Он используется для внешнего взаимодействия с клиентскими приложениями, которые работают напрямую с YDB через [SDK](../ydb-sdk/index.md) или [CLI](../ydb-cli/index.md).

Пример включения TLS для gRPC API:

```yaml
grpc_config:
   cert: "/opt/ydb/certs/node.crt"
   key: "/opt/ydb/certs/node.key"
   ca: "/opt/ydb/certs/ca.crt"
```

### Протокол Kafka {#protokol-kafka}

YDB открывает отдельный сетевой порт для [протокола Kafka](../kafka-api/index.md). Этот протокол используется для внешнего взаимодействия с клиентскими приложениями, изначально разработанными для работы с [Apache Kafka](https://kafka.apache.org/).

Пример включения TLS для протокола Kafka с использованием файла, содержащего как сертификат, так и закрытый ключ:

```yaml
kafka_proxy_config:
    ssl_certificate: "/opt/ydb/certs/node.crt"
```

Пример включения TLS для протокола Kafka с раздельными файлами сертификата и закрытого ключа:

```yaml
kafka_proxy_config:
    cert: "/opt/ydb/certs/node.crt"
    key: "/opt/ydb/certs/node.key"
```

### HTTP

YDB открывает отдельный HTTP-порт для работы [встроенного интерфейса](../embedded-ui/index.md), отображения [метрик](../../devops/observability/monitoring.md) и других вспомогательных команд.

Пример включения TLS на HTTP-порту, что делает его использования HTTPS:

```yaml
monitoring_config:
    monitoring_certificate_file: "/opt/ydb/certs/node.crt"
```

## YDB в роли клиента {#ydb-v-roli-klienta}

### LDAP

YDB поддерживает [LDAP](../../security/authentication.md#ldap) для аутентификации пользователей. Протокол LDAP имеет два варианта включения TLS.

Пример включения TLS для LDAP через расширение протокола `StartTls`:

```yaml
auth_config:
  ldap_authentication:
    use_tls:
      enable: true
      ca_cert_file: "/path/to/ca.pem"
      cert_require: DEMAND
  scheme: "ldap"
```

Пример включения TLS для LDAP через `ldaps`:

```yaml
auth_config:
  ldap_authentication:
    use_tls:
      enable: false
      ca_cert_file: "/path/to/ca.pem"
      cert_require: DEMAND
  scheme: "ldaps"
```

Подробнее этот механизм описан в [{#T}](../../devops/configuration-management/configuration-v1/index.md#ldap-auth-config).

### Федеративные запросы {#federativnye-zaprosy}

[Федеративные запросы](../../concepts/query_execution/federated_query/index.md) позволяют YDB выполнять запросы к различным внешним источникам данных. Использование TLS при выполнении таких запросов контролируется параметром `USE_TLS` в запросах [CREATE EXTERNAL DATA SOURCE](../../yql/reference/syntax/create-external-data-source.md). Изменения в серверной конфигурации не требуются.

### Трассировка {#trassirovka}

YDB может отправлять данные [трассировки](../observability/tracing/setup.md) на внешний коллектор через gRPC.

Пример включения TLS для данных трассировки посредством указания протокола `grpcs://`:

```yaml
tracing_config:
  backend:
    opentelemetry:
      collector_url: grpcs://example.com:4317
      service_name: ydb
```

## Асинхронная репликация {#asinhronnaya-replikaciya}

[Асинхронная репликация](../../concepts/async-replication.md) синхронизирует данные между двумя базами данных YDB, одна из них выступает в роли клиента по отношению к другой. Использование TLS при такой коммуникации контролируется параметром `CONNECTION_STRING` в запросах [CREATE ASYNC REPLICATION](../../yql/reference/syntax/create-async-replication.md). Для TLS-соединений используйте протокол `grpcs://`. Изменения в серверной конфигурации не требуются.

При использовании пользовательского удостоверяющего центра (Certificate Authority, CA) передайте его сертификат в параметре `CA_CERT` при создании экземпляра асинхронной репликации.
