---
title: "Kafka API constraints"
url: "https://ydb.tech/docs/en/reference/kafka-api/constraints?version=v26.1"
doc_path: "en/reference/kafka-api/constraints"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/kafka-api/constraints.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/kafka-api/constraints.md"
description: "YDB supports Apache Kafka protocol version 3.4.0 with the following constraints: Only SASL/PLAIN authentication is supported."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Kafka API constraints

YDB supports [Apache Kafka protocol](https://kafka.apache.org/protocol.html) version 3.4.0 with the following constraints:

1. Only [SASL/PLAIN authentication](https://kafka.apache.org/documentation/#security_sasl) is supported.
2. [Message compression](https://www.confluent.io/blog/apache-kafka-message-compression) is not supported.
3. [The topic deletion operation](https://kafka.apache.org/protocol#The_Messages_DeleteTopics) is not supported. To delete a topic, use [YQL](../../yql/reference/syntax/drop-topic.md) or [YDB CLI](../ydb-cli/topic-drop.md).
4. [CRC checks](https://kafka.apache.org/documentation/#consumerconfigs_check.crcs) are not supported.
5. [Support for ACL](https://kafka.apache.org/documentation/#security_authz) is not provided. Use [YQL](../../yql/reference/syntax/grant.md) to manage access to topics.
6. If [auto-partitioning](../../concepts/datamodel/topic.md#autopartitioning) is enabled on a topic, you cannot write to or read from such a topic using the Kafka API.
