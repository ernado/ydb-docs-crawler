---
title: "kafka_proxy_config"
url: "https://ydb.tech/docs/ru/reference/configuration/kafka_proxy_config?version=v26.1"
doc_path: "ru/reference/configuration/kafka_proxy_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/kafka_proxy_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/kafka_proxy_config.md"
description: "В разделе kafka_proxy_config файла конфигурации YDB включается и конфигурируется Kafka Proxy, которая дает доступ к работе с YDB Topics по Kafka API."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# kafka_proxy_config

В разделе `kafka_proxy_config` файла конфигурации YDB включается и конфигурируется Kafka Proxy, которая дает доступ к работе с [YDB Topics](../../concepts/datamodel/topic.md) по [Kafka API](../kafka-api/index.md).

## Описание параметров {#opisanie-parametrov}

|  |  |  |  |
| --- | --- | --- | --- |
| Параметр | Тип | Значение по умолчанию | Описание |
| `enable_kafka_proxy` | bool | `false` | Включает или отключает Kafka Proxy. |
| `listening_port` | int32 | `9092` | Порт, на котором будет доступен Kafka API. |
| `transaction_timeout_ms` | uint32 | `300000` (5 минут) | Максимальный таймаут для Kafka транзакций, после которого транзакция будет отменена. |
| `auto_create_topics_enable` | bool | `false` | Включает автоматическое создание топиков при обращении к ним. Аналог [такой же опции](https://kafka.apache.org/documentation/#brokerconfigs_auto.create.topics.enable) в Apache Kafka. |
| `auto_create_consumers_enable` | bool | `true` | Включает автоматическое заведение консьюмеров при обращении к ним. |
| `topic_creation_default_partitions` | uint32 | `1` | Количество партиций, которое будет создано, если при добавлении топика по Kafka протоколу не было указано количество партиций. Аналог опиции [num.partitions](https://kafka.apache.org/documentation/#brokerconfigs_num.partitions) в Apache Kafka. |
| `ssl_cerificate` | string | - | Путь к файлу сертификата для доступа по SSL, включающий в себя сразу и файл сертификата и файл ключа. При указании этого параметра Kafka Proxy автоматически начинает обрабатывать запросы с использованием указанного SSL-сертификата. |
| `cert` | string | - | Путь к файлу сертификата для доступа по SSL. При указании этого параметра Kafka Proxy автоматически начинает обрабатывать запросы с использованием указанного SSL-сертификата. |
| `key` | string | - | Путь к файлу ключа для доступа по SSL. |

## Пример заполненного конфига {#primer-zapolnennogo-konfiga}

```yaml
kafka_proxy_config:
  enable_kafka_proxy: true
  listening_port: 9092
  transaction_timeout_ms: 300000 # 5 минут
  auto_create_topics_enable: true
  auto_create_consumers_enable: true
  topic_creation_default_partitions: 1
  cert: /path/to/cert.pem
  key: /path/to/key.pem
```
