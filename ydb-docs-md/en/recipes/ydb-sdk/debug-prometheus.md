---
title: "Enabling metrics in Prometheus"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/debug-prometheus?version=v26.1"
doc_path: "en/recipes/ydb-sdk/debug-prometheus"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/debug-prometheus.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/debug-prometheus.md"
description: "Below are examples of the code for enabling metrics in Prometheus in different YDB SDKs. Go. Java. Python. JavaScript. Rust. Native SDK. database/sql."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Enabling metrics in Prometheus

Below are examples of the code for enabling metrics in Prometheus in different YDB SDKs.

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

    ```go
    package main

    import (
        "context"

        "github.com/prometheus/client_golang/prometheus"
        metrics "github.com/ydb-platform/ydb-go-sdk-prometheus/v2"
        "github.com/ydb-platform/ydb-go-sdk/v3"
        "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
        ctx := context.Background()
        registry := prometheus.NewRegistry()
        db, err := ydb.Open(ctx,
            os.Getenv("YDB_CONNECTION_STRING"),
            metrics.WithTraces(
                registry,
                metrics.WithDetails(trace.DetailsAll),
                metrics.WithSeparator("_"),
            ),
        )
        if err != nil {
            panic(err)
        }
        defer db.Close(ctx)
        ...
    }
    ```

  - database/sql

    ```go
    package main

    import (
        "context"
        "database/sql"

        "github.com/prometheus/client_golang/prometheus"
        metrics "github.com/ydb-platform/ydb-go-sdk-prometheus/v2"
        "github.com/ydb-platform/ydb-go-sdk/v3"
        "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
        ctx := context.Background()
        registry := prometheus.NewRegistry()
        nativeDriver, err := ydb.Open(ctx,
            os.Getenv("YDB_CONNECTION_STRING"),
            metrics.WithTraces(
                registry,
                metrics.WithDetails(trace.DetailsAll),
                metrics.WithSeparator("_"),
            ),
        )
        if err != nil {
            panic(err)
        }
        defer nativeDriver.Close(ctx)

        connector, err := ydb.Connector(nativeDriver)
        if err != nil {
            panic(err)
        }

        db := sql.OpenDB(connector)
        defer db.Close()
        ...
    }
    ```

  {% endlist %}

- Native SDK

  ```go
  package main

  import (
      "context"

      "github.com/prometheus/client_golang/prometheus"
      metrics "github.com/ydb-platform/ydb-go-sdk-prometheus/v2"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
      ctx := context.Background()
      registry := prometheus.NewRegistry()
      db, err := ydb.Open(ctx,
          os.Getenv("YDB_CONNECTION_STRING"),
          metrics.WithTraces(
              registry,
              metrics.WithDetails(trace.DetailsAll),
              metrics.WithSeparator("_"),
          ),
      )
      if err != nil {
          panic(err)
      }
      defer db.Close(ctx)
      ...
  }
  ```

- database/sql

  ```go
  package main

  import (
      "context"
      "database/sql"

      "github.com/prometheus/client_golang/prometheus"
      metrics "github.com/ydb-platform/ydb-go-sdk-prometheus/v2"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
      ctx := context.Background()
      registry := prometheus.NewRegistry()
      nativeDriver, err := ydb.Open(ctx,
          os.Getenv("YDB_CONNECTION_STRING"),
          metrics.WithTraces(
              registry,
              metrics.WithDetails(trace.DetailsAll),
              metrics.WithSeparator("_"),
          ),
      )
      if err != nil {
          panic(err)
      }
      defer nativeDriver.Close(ctx)

      connector, err := ydb.Connector(nativeDriver)
      if err != nil {
          panic(err)
      }

      db := sql.OpenDB(connector)
      defer db.Close()
      ...
  }
  ```

- Java

  This functionality is not currently supported.

- Python

  This functionality is not currently supported.

- JavaScript

  This section is under development.

- Rust

  This functionality is not currently supported.

  Track progress or vote for Rust SDK support: [ydb-rs-sdk#267](https://github.com/ydb-platform/ydb-rs-sdk/issues/267)

{% endlist %}
