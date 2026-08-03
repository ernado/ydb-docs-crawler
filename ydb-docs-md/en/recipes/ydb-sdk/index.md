---
title: "Code recipes using YDB SDK and frameworks"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/?version=v26.1"
doc_path: "en/recipes/ydb-sdk/"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/index.md"
description: "This section contains code recipes in various programming languages for solving common practical tasks using YDB SDK. Contents: Driver initialization."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Code recipes using YDB SDK and frameworks

This section contains code recipes in various programming languages for solving common practical tasks using YDB SDK.

Contents:

- [Driver initialization](init.md)

- [Authentication](auth.md)

  - [Using a token](auth-access-token.md)
  - [Anonymous](auth-anonymous.md)
  - [Service account file](auth-service-account.md)
  - [Metadata service](auth-metadata.md)
  - [Using environment variables](auth-env.md)
  - [Using login and password](auth-static.md)

- [Load balancing](balancing.md)

  - [Uniform random selection](balancing-random-choice.md)
  - [Prefer the nearest data center](balancing-prefer-local.md)
  - [Prefer the availability zone](balancing-prefer-location.md)

- [Retrying requests](retry.md)

- [Setting the session pool size](session-pool-limit.md)

- [Inserting data](upsert.md)

- [Batch data insertion](bulk-upsert.md)

- [Setting the transaction execution mode](tx-control.md)

- [Configuring table row time-to-live (TTL)](ttl.md)

- [Vector search](vector-search.md)

- Coordination

  - [Distributed locking](distributed-lock.md)
  - [Service discovery](service-discovery.md)
  - [Configuration publication](config-publication.md)
  - [Leader election](leader-election.md)

- [Troubleshooting](debug.md)

  - [Enable logging](debug-logs.md)
  - [Connect metrics to Prometheus](debug-prometheus.md)
  - [Tracing with OpenTelemetry](debug-otel.md)

See also:

- [YDB for Application Developers / Software Engineers](../../dev/index.md)
- [Example applications working with YDB](../../dev/example-app/index.md)
- [Reference for YDB SDK](../../reference/ydb-sdk/index.md)
