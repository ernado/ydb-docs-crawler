---
title: "Ограничения Kafka API"
url: "https://ydb.tech/docs/ru/reference/kafka-api/constraints?version=v26.1"
doc_path: "ru/reference/kafka-api/constraints"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/kafka-api/constraints.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/kafka-api/constraints.md"
description: "Поддержка протокола Kafka версии 3.4.0 осуществляется в ограниченном объеме: Поддержаны только SASL/PLAIN и SASL/SCRAM-SHA-256 механизмы аутентификации."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Ограничения Kafka API

Поддержка протокола Kafka версии 3.4.0 осуществляется в ограниченном объеме:

1. Поддержаны только SASL/PLAIN и SASL/SCRAM-SHA-256 [механизмы аутентификации](https://kafka.apache.org/documentation/#security_sasl).
2. Не поддержано [сжатие сообщений](https://www.confluent.io/blog/apache-kafka-message-compression/).
3. Не поддержана [операция удаления топика](https://kafka.apache.org/protocol#The_Messages_DeleteTopics). Для удаления топика используйте [YQL](../../yql/reference/syntax/drop-topic.md) или [YDB CLI](../ydb-cli/topic-drop.md).
4. Не поддержана [проверка crc](https://kafka.apache.org/documentation/#consumerconfigs_check.crcs).
5. Не поддержана [работа с ACL](https://kafka.apache.org/documentation/#security_authz). Для управления доступом к топикам используйте [YQL](../../yql/reference/syntax/grant.md).
6. Если на топике включено [автопартиционирование](../../concepts/datamodel/topic.md#autopartitioning), то в такой топик нельзя писать или читать из него по протоколу Kafka API.
