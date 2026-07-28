---
title: "kafka_proxy_config"
url: "https://ydb.tech/docs/en/reference/configuration/kafka?version=v26.1"
doc_path: "en/reference/configuration/kafka"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/kafka.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/kafka.md"
description: "The kafka_proxy_config section of the YDB configuration file enables and configures Kafka Proxy, which provides access to work with YDB Topics via Kafka API."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# kafka_proxy_config

The `kafka_proxy_config` section of the YDB configuration file enables and configures Kafka Proxy, which provides access to work with [YDB Topics](../../concepts/datamodel/topic.md) via [Kafka API](../kafka-api/index.md).

## Description of parameters

| Parameter | Type | Default value | Description |
| --- | --- | --- | --- |
| `enable_kafka_proxy` | bool | `false` | Enables or disables Kafka Proxy. |
| `listening_port` | int32 | `9092` | The port on which the Kafka API will be available. |
| `transaction_timeout_ms` | uint32 | `300000` (5 minutes) | The maximum timeout for Kafka transactions, after which the transaction will be cancelled. |
| `auto_create_topics_enable` | bool | `false` | Enables automatic creation of topics when they are accessed. Analogous to [the same option](https://kafka.apache.org/documentation/#brokerconfigs_auto.create.topics.enable) in Apache Kafka. |
| `auto_create_consumers_enable` | bool | `true` | Enables automatic registration of consumers when they are accessed. |
| `topic_creation_default_partitions` | uint32 | `1` | The number of partitions that will be created if the number of partitions is not specified when adding a topic via the Kafka protocol. Analogous to [num.partitions](https://kafka.apache.org/documentation/#brokerconfigs_num.partitions) option in Apache Kafka. |
| `ssl_cerificate` | string | — | The path to the SSL certificate file, which includes both the certificate file and the key file. When this parameter is specified, Kafka Proxy automatically starts processing requests using the specified SSL certificate. |
| `cert` | string | — | The path to the SSL certificate file. When this parameter is specified, Kafka Proxy automatically starts processing requests using the specified SSL certificate. |
| `key` | string | — | The path to the SSL key file. |

## Example of a completed config

```yaml
kafka_proxy_config:
  enable_kafka_proxy: true
  listening_port: 9092
  transaction_timeout_ms: 300000 # 5 minutes
  auto_create_topics_enable: true
  auto_create_consumers_enable: true
  topic_creation_default_partitions: 1
  cert: /path/to/cert.pem
  key: /path/to/key.pem
```
