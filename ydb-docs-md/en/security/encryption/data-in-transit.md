---
title: "Data in transit encryption"
url: "https://ydb.tech/docs/en/security/encryption/data-in-transit?version=v26.1"
doc_path: "en/security/encryption/data-in-transit"
version: "v26.1"
lang: "en"
source_path: "en/core/security/encryption/data-in-transit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/security/encryption/data-in-transit.md"
description: "As YDB is a distributed system typically running on a cluster, often spanning multiple datacenters or availability zones, user data is routinely transferred ove"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Data in transit encryption

As YDB is a distributed system typically running on a cluster, often spanning multiple datacenters or availability zones, user data is routinely transferred over the network. Various protocols can be involved, and each can be configured to run over [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security). Below is a list of protocols supported by YDB:

- [Interconnect](../../concepts/glossary.md#actor-system-interconnect), a specialized protocol for all communication between YDB nodes.

- YDB as a server:

  - [gRPC](../../reference/ydb-sdk/overview-grpc-api.md) for external communication with client applications designed to work natively with YDB via the [SDK](../../reference/ydb-sdk/index.md) or [CLI](../../reference/ydb-cli/index.md).
  - [Kafka wire protocol](../../reference/kafka-api/index.md) for external communication with client applications initially designed to work with [Apache Kafka](https://kafka.apache.org/).
  - HTTP for running the [Embedded UI](../../reference/embedded-ui/index.md), exposing [metrics](../../devops/observability/monitoring.md), and other miscellaneous endpoints.

- YDB as a client:

  - [LDAP](../authentication.md#ldap) for user authentication.
  - [Federated queries](../../concepts/query_execution/federated_query/index.md), a feature that allows YDB to query various external data sources. Some sources are queried directly from the `ydbd` process, while others are proxied via a separate connector process.
  - [Tracing](../../reference/observability/tracing/setup.md) data sent to an external collector via gRPC.

- In [asynchronous replication](../../concepts/async-replication.md) between two YDB databases, one serves as a client to the other.

By default, data in transit encryption is disabled and must be enabled separately for each protocol. They can either share the same set of TLS certificates or use dedicated ones. For instructions on how to enable TLS, refer to the [tls](../../reference/configuration/tls.md) section.
