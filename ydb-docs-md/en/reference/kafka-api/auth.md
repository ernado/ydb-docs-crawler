---
title: "Kafka API authentication"
url: "https://ydb.tech/docs/en/reference/kafka-api/auth?version=v26.1"
doc_path: "en/reference/kafka-api/auth"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/kafka-api/auth.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/kafka-api/auth.md"
description: "Enabling authentication. When you run a single-node local YDB cluster, anonymous authentication is used by default. It doesn't require a username and password."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Kafka API authentication

## Enabling authentication

When you run [a single-node local YDB cluster](../../quickstart.md), [anonymous authentication](../../security/authentication.md#anonymous) is used by default. It doesn't require a username and password.

To require authentication see [Authentication](../../security/authentication.md#static-credentials).

Authentication is always enabled when using the [Kafka API in Yandex Cloud](https://yandex.cloud/en/docs/data-streams/kafkaapi/auth).

## How does authentication work in the Kafka API?

The Kafka API uses the `SASL_PLAINTEXT/PLAIN` or `SASL_SSL/PLAIN` authentication mechanism.

The following variables are required for authentication:

- `<user-name>` — the username. For information about user management, refer to the [Authorization](../../security/authorization.md#user) section.
- `<password>` — the user's password. For information about user management, refer to the [Authorization](../../security/authorization.md#user) section.
- `<database>` — [the database path](../../concepts/connect.md#database).

These parameters form the following variables, which you can use in the `sasl.jaas.config` Kafka client property:

- `<sasl.username> = <user-name>@<database>`
- `<sasl.password> = <password>`

> [!NOTE]
> The `<sasl.username>` and `<sasl.password>` parameters are formed differently. See [examples](examples.md#authentication-in-cloud-examples) for details.

For authentication examples, see [Kafka API usage examples](examples.md).
