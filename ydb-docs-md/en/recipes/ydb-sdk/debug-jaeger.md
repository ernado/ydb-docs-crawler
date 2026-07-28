---
title: "Enabling tracing in Jaeger"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/debug-jaeger?version=v26.1"
doc_path: "en/recipes/ydb-sdk/debug-jaeger"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/debug-jaeger.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/debug-jaeger.md"
description: "Below are examples of code for enabling tracing in Jaeger in different YDB SDKs. C++. Go. Java. Python. C#. JavaScript. Rust. PHP. Python."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Enabling tracing in Jaeger

Below are examples of code for enabling tracing in Jaeger in different YDB SDKs.

{% list tabs %}

- C++

  The functionality is not supported at the moment.

- Go

  {% list tabs %}

  - Native SDK

    ```go
    package main

    import (
        "context"
        "time"

        "github.com/opentracing/opentracing-go"
        jaegerConfig "github.com/uber/jaeger-client-go/config"

        "github.com/ydb-platform/ydb-go-sdk/v3"
        "github.com/ydb-platform/ydb-go-sdk/v3/trace"

        tracing "github.com/ydb-platform/ydb-go-sdk-opentracing"
    )

    const (
        tracerURL   = "localhost:5775"
        serviceName = "ydb-go-sdk"
    )

    func main() {
        tracer, closer, err := jaegerConfig.Configuration{
            ServiceName: serviceName,
            Sampler: &jaegerConfig.SamplerConfig{
                Type:  "const",
                Param: 1,
            },
            Reporter: &jaegerConfig.ReporterConfig{
                LogSpans:            true,
                BufferFlushInterval: 1 * time.Second,
                LocalAgentHostPort:  tracerURL,
            },
        }.NewTracer()
        if err != nil {
            panic(err)
        }

        defer closer.Close()

        // set global tracer of this application
        opentracing.SetGlobalTracer(tracer)

        span, ctx := opentracing.StartSpanFromContext(context.Background(), "client")
        defer span.Finish()

        db, err := ydb.Open(ctx,
            os.Getenv("YDB_CONNECTION_STRING"),
            tracing.WithTraces(tracing.WithDetails(trace.DetailsAll)),
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
        "time"

        "github.com/opentracing/opentracing-go"
        jaegerConfig "github.com/uber/jaeger-client-go/config"

        "github.com/ydb-platform/ydb-go-sdk/v3"
        "github.com/ydb-platform/ydb-go-sdk/v3/trace"

        tracing "github.com/ydb-platform/ydb-go-sdk-opentracing"
    )

    const (
        tracerURL   = "localhost:5775"
        serviceName = "ydb-go-sdk"
    )

    func main() {
        tracer, closer, err := jaegerConfig.Configuration{
            ServiceName: serviceName,
                Sampler: &jaegerConfig.SamplerConfig{
                Type:  "const",
                Param: 1,
            },
            Reporter: &jaegerConfig.ReporterConfig{
                LogSpans:            true,
                BufferFlushInterval: 1 * time.Second,
                LocalAgentHostPort:  tracerURL,
            },
        }.NewTracer()
        if err != nil {
            panic(err)
        }

        defer closer.Close()

        // set global tracer of this application
        opentracing.SetGlobalTracer(tracer)

        span, ctx := opentracing.StartSpanFromContext(context.Background(), "client")
        defer span.Finish()

        nativeDriver, err := ydb.Open(ctx,
            os.Getenv("YDB_CONNECTION_STRING"),
            tracing.WithTraces(tracing.WithDetails(trace.DetailsAll)),
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
      "time"

      "github.com/opentracing/opentracing-go"
      jaegerConfig "github.com/uber/jaeger-client-go/config"

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"

      tracing "github.com/ydb-platform/ydb-go-sdk-opentracing"
  )

  const (
      tracerURL   = "localhost:5775"
      serviceName = "ydb-go-sdk"
  )

  func main() {
      tracer, closer, err := jaegerConfig.Configuration{
          ServiceName: serviceName,
          Sampler: &jaegerConfig.SamplerConfig{
              Type:  "const",
              Param: 1,
          },
          Reporter: &jaegerConfig.ReporterConfig{
              LogSpans:            true,
              BufferFlushInterval: 1 * time.Second,
              LocalAgentHostPort:  tracerURL,
          },
      }.NewTracer()
      if err != nil {
          panic(err)
      }

      defer closer.Close()

      // set global tracer of this application
      opentracing.SetGlobalTracer(tracer)

      span, ctx := opentracing.StartSpanFromContext(context.Background(), "client")
      defer span.Finish()

      db, err := ydb.Open(ctx,
          os.Getenv("YDB_CONNECTION_STRING"),
          tracing.WithTraces(tracing.WithDetails(trace.DetailsAll)),
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
      "time"

      "github.com/opentracing/opentracing-go"
      jaegerConfig "github.com/uber/jaeger-client-go/config"

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"

      tracing "github.com/ydb-platform/ydb-go-sdk-opentracing"
  )

  const (
      tracerURL   = "localhost:5775"
      serviceName = "ydb-go-sdk"
  )

  func main() {
      tracer, closer, err := jaegerConfig.Configuration{
          ServiceName: serviceName,
              Sampler: &jaegerConfig.SamplerConfig{
              Type:  "const",
              Param: 1,
          },
          Reporter: &jaegerConfig.ReporterConfig{
              LogSpans:            true,
              BufferFlushInterval: 1 * time.Second,
              LocalAgentHostPort:  tracerURL,
          },
      }.NewTracer()
      if err != nil {
          panic(err)
      }

      defer closer.Close()

      // set global tracer of this application
      opentracing.SetGlobalTracer(tracer)

      span, ctx := opentracing.StartSpanFromContext(context.Background(), "client")
      defer span.Finish()

      nativeDriver, err := ydb.Open(ctx,
          os.Getenv("YDB_CONNECTION_STRING"),
          tracing.WithTraces(tracing.WithDetails(trace.DetailsAll)),
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

  Feature not supported

- Python

  Feature not supported

- C#

  Feature not supported

- JavaScript

  Feature not supported

- Rust

  Feature not supported

  Use the [`tracing`](https://docs.rs/tracing) ecosystem and OpenTelemetry export ([#268](https://github.com/ydb-platform/ydb-rs-sdk/issues/268)).

- PHP

  Feature not supported

- Python

  This functionality is not currently supported.

{% endlist %}
