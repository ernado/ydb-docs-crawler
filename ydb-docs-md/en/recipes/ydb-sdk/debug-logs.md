---
title: "en/recipes/ydb-sdk/debug-logs"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/debug-logs?version=v26.1"
doc_path: "en/recipes/ydb-sdk/debug-logs"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/debug-logs.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/debug-logs.md"
description: "# Enabling logging. Below are examples of code that enables logging in different YDB SDKs. Go. Java. PHP. Python. Native SDK. database/sql."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# en/recipes/ydb-sdk/debug-logs

\# Enabling logging

Below are examples of code that enables logging in different YDB SDKs.

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

    There are several ways to enable logs in an application that uses `ydb-go-sdk`:

    <details>
    <summary>Using the `YDB_LOG_SEVERITY_LEVEL` environment variable</summary>

    This environment variable enables the built-in `ydb-go-sdk` logger (synchronous, non-block) and prints to the standard output stream.
     You can set the environment variable as follows:

    ```shell
    export YDB_LOG_SEVERITY_LEVEL=info
    ```

    (possible values: `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `quiet`, defaults to `quiet`).

    </details>

    <details>
    <summary>Enable a third-party logger `go.uber.org/zap`</summary>

    ```go
    package main

    import (
      "context"
      "os"

      "go.uber.org/zap"

      ydbZap "github.com/ydb-platform/ydb-go-sdk-zap"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var log *zap.Logger // zap-logger with init out of this scope
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydbZap.WithTraces(
          log,
          trace.DetailsAll,
        ),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

    </details>

    <details>
    <summary>Enable a third-party logger `github.com/rs/zerolog`</summary>

    ```go
    package main

    import (
      "context"
      "os"

      "github.com/rs/zerolog"

      ydbZerolog "github.com/ydb-platform/ydb-go-sdk-zerolog"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var log zerolog.Logger // zap-logger with init out of this scope
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydbZerolog.WithTraces(
          &log,
          trace.DetailsAll,
        ),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

    </details>

    <details>
    <summary>Enable a custom logger implementation `github.com/ydb-platform/ydb-go-sdk/v3/log.Logger`</summary>

    ```go
    package main

    import (
      "context"
      "os"

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/log"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var logger log.Logger // logger implementation with init out of this scope
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithLogger(
          logger,
          trace.DetailsAll,
        ),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

    </details>

    <details>
    <summary>Implement your own logging package</summary>

    You can implement your own logging package based on the driver events in the `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package. The `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package describes all logged driver events.

    </details>

    <details>
    <summary>Iterate over server errors with `IterateByIssues`</summary>

    When using YDB through the Go SDK, you can enable logging of requests and responses and also obtain detailed information about server errors (issues) — extra messages YDB returns in the response when operations fail. To iterate over issues in the server response, use [IterateByIssues](https://pkg.go.dev/github.com/ydb-platform/ydb-go-sdk/v3#IterateByIssues).

    </details>

  - database/sql

    There are several ways to enable logs in an application that uses `ydb-go-sdk`:

    <details>
    <summary>Using the `YDB_LOG_SEVERITY_LEVEL` environment variable</summary>

    This environment variable enables the built-in `ydb-go-sdk` logger (synchronous, non-block) and prints to the standard output stream.
     You can set the environment variable as follows:

    ```shell
    export YDB_LOG_SEVERITY_LEVEL=info
    ```

    (possible values: `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `quiet`, defaults to `quiet`).

    </details>

    <details>
    <summary>Enable a third-party logger `go.uber.org/zap`</summary>

    ```go
    package main

    import (
      "context"
      "database/sql"
      "os"

      "go.uber.org/zap"

      ydbZap "github.com/ydb-platform/ydb-go-sdk-zap"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var log *zap.Logger // zap-logger with init out of this scope
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydbZap.WithTraces(
          log,
          trace.DetailsAll,
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
      defer connector.Close()

      db := sql.OpenDB(connector)
      defer db.Close()
      ...
    }
    ```

    </details>

    <details>
    <summary>Enable a third-party logger `github.com/rs/zerolog`</summary>

    ```go
    package main

    import (
      "context"
      "database/sql"
      "os"

      "github.com/rs/zerolog"

      ydbZerolog "github.com/ydb-platform/ydb-go-sdk-zerolog"
      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var log zerolog.Logger // zap-logger with init out of this scope
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydbZerolog.WithTraces(
          &log,
          trace.DetailsAll,
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
      defer connector.Close()

      db := sql.OpenDB(connector)
      defer db.Close()
      ...
    }
    ```

    </details>

    <details>
    <summary>Enable a custom logger implementation `github.com/ydb-platform/ydb-go-sdk/v3/log.Logger`</summary>

    ```go
    package main

    import (
      "context"
      "database/sql"
      "os"

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/log"
      "github.com/ydb-platform/ydb-go-sdk/v3/trace"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      var logger log.Logger // logger implementation with init out of this scope
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithLogger(
          logger,
          trace.DetailsAll,
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
      defer connector.Close()

      db := sql.OpenDB(connector)
      defer db.Close()
      ...
    }
    ```

    </details>

    <details>
    <summary>Implement your own logging package</summary>

    You can implement your own logging package based on the driver events in the `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package. The `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package describes all logged driver events.

    </details>

  {% endlist %}

- Native SDK

  There are several ways to enable logs in an application that uses `ydb-go-sdk`:

  <details>
  <summary>Using the `YDB_LOG_SEVERITY_LEVEL` environment variable</summary>

  This environment variable enables the built-in `ydb-go-sdk` logger (synchronous, non-block) and prints to the standard output stream.
   You can set the environment variable as follows:

  ```shell
  export YDB_LOG_SEVERITY_LEVEL=info
  ```

  (possible values: `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `quiet`, defaults to `quiet`).

  </details>

  <details>
  <summary>Enable a third-party logger `go.uber.org/zap`</summary>

  ```go
  package main

  import (
    "context"
    "os"

    "go.uber.org/zap"

    ydbZap "github.com/ydb-platform/ydb-go-sdk-zap"
    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var log *zap.Logger // zap-logger with init out of this scope
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydbZap.WithTraces(
        log,
        trace.DetailsAll,
      ),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

  </details>

  <details>
  <summary>Enable a third-party logger `github.com/rs/zerolog`</summary>

  ```go
  package main

  import (
    "context"
    "os"

    "github.com/rs/zerolog"

    ydbZerolog "github.com/ydb-platform/ydb-go-sdk-zerolog"
    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var log zerolog.Logger // zap-logger with init out of this scope
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydbZerolog.WithTraces(
        &log,
        trace.DetailsAll,
      ),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

  </details>

  <details>
  <summary>Enable a custom logger implementation `github.com/ydb-platform/ydb-go-sdk/v3/log.Logger`</summary>

  ```go
  package main

  import (
    "context"
    "os"

    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/log"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var logger log.Logger // logger implementation with init out of this scope
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydb.WithLogger(
        logger,
        trace.DetailsAll,
      ),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

  </details>

  <details>
  <summary>Implement your own logging package</summary>

  You can implement your own logging package based on the driver events in the `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package. The `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package describes all logged driver events.

  </details>

  <details>
  <summary>Iterate over server errors with `IterateByIssues`</summary>

  When using YDB through the Go SDK, you can enable logging of requests and responses and also obtain detailed information about server errors (issues) — extra messages YDB returns in the response when operations fail. To iterate over issues in the server response, use [IterateByIssues](https://pkg.go.dev/github.com/ydb-platform/ydb-go-sdk/v3#IterateByIssues).

  </details>

- database/sql

  There are several ways to enable logs in an application that uses `ydb-go-sdk`:

  <details>
  <summary>Using the `YDB_LOG_SEVERITY_LEVEL` environment variable</summary>

  This environment variable enables the built-in `ydb-go-sdk` logger (synchronous, non-block) and prints to the standard output stream.
   You can set the environment variable as follows:

  ```shell
  export YDB_LOG_SEVERITY_LEVEL=info
  ```

  (possible values: `trace`, `debug`, `info`, `warn`, `error`, `fatal`, and `quiet`, defaults to `quiet`).

  </details>

  <details>
  <summary>Enable a third-party logger `go.uber.org/zap`</summary>

  ```go
  package main

  import (
    "context"
    "database/sql"
    "os"

    "go.uber.org/zap"

    ydbZap "github.com/ydb-platform/ydb-go-sdk-zap"
    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var log *zap.Logger // zap-logger with init out of this scope
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydbZap.WithTraces(
        log,
        trace.DetailsAll,
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
    defer connector.Close()

    db := sql.OpenDB(connector)
    defer db.Close()
    ...
  }
  ```

  </details>

  <details>
  <summary>Enable a third-party logger `github.com/rs/zerolog`</summary>

  ```go
  package main

  import (
    "context"
    "database/sql"
    "os"

    "github.com/rs/zerolog"

    ydbZerolog "github.com/ydb-platform/ydb-go-sdk-zerolog"
    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var log zerolog.Logger // zap-logger with init out of this scope
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydbZerolog.WithTraces(
        &log,
        trace.DetailsAll,
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
    defer connector.Close()

    db := sql.OpenDB(connector)
    defer db.Close()
    ...
  }
  ```

  </details>

  <details>
  <summary>Enable a custom logger implementation `github.com/ydb-platform/ydb-go-sdk/v3/log.Logger`</summary>

  ```go
  package main

  import (
    "context"
    "database/sql"
    "os"

    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/log"
    "github.com/ydb-platform/ydb-go-sdk/v3/trace"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    var logger log.Logger // logger implementation with init out of this scope
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydb.WithLogger(
        logger,
        trace.DetailsAll,
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
    defer connector.Close()

    db := sql.OpenDB(connector)
    defer db.Close()
    ...
  }
  ```

  </details>

  <details>
  <summary>Implement your own logging package</summary>

  You can implement your own logging package based on the driver events in the `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package. The `github.com/ydb-platform/ydb-go-sdk/v3/trace` tracing package describes all logged driver events.

  </details>

- Java

  {% list tabs %}

  - Native SDK

    For logging purposes, the YDB Java SDK uses the slf4j library, which supports multiple logging levels (`error`, `warn`, `info`, `debug`, `trace`) for one or many loggers. The current implementation supports the following loggers:

    - The `tech.ydb.core.grpc` logger provides information about the internal gRPC implementation
    - The `debug` level logs all gRPC operations; use it only for debugging
    - The `info` level is recommended by default
    - On the `debug` level, the `tech.ydb.table.impl` logger lets you track the internal state of the YDB driver, including the session pool
    - On the `debug` level, the `tech.ydb.table.SessionRetryContext` logger reports the number of retries, query results, per-retry duration, and total operation time
    - On the `debug` level, the `tech.ydb.table.Session` logger provides the query text, response status, and execution time for session operations

    Enabling and configuring the Java SDK loggers depends on the `slf4j-api` implementation you use.
     Here is an example `log4j2` configuration for the `log4j-slf4j-impl` library:

    ```xml
    <Configuration status="WARN">
      <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
          <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
        </Console>
      </Appenders>

      <Loggers>
        <Logger name="io.netty" level="warn" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="io.grpc.netty" level="warn" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="tech.ydb.core.grpc" level="info" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="tech.ydb.table.impl" level="info" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="tech.ydb.table.SessionRetryContext" level="debug" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="tech.ydb.table.Session" level="debug" additivity="false">
          <AppenderRef ref="Console"/>
        </Logger>

        <Root level="debug" >
          <AppenderRef ref="Console"/>
        </Root>
      </Loggers>
    </Configuration>
    ```

  - JDBC

    The JDBC driver uses the same logging stack via `slf4j`; configure the `tech.ydb.*` loggers the same way as in the native SDK.

    The same debug logs are available in other stacks built on JDBC (Spring Boot, ORMs, connection pools, and so on): they reach YDB through this driver, so it is enough to attach the same `slf4j` / log4j2 / logback configuration in the application.

  {% endlist %}

- Native SDK

  For logging purposes, the YDB Java SDK uses the slf4j library, which supports multiple logging levels (`error`, `warn`, `info`, `debug`, `trace`) for one or many loggers. The current implementation supports the following loggers:

  - The `tech.ydb.core.grpc` logger provides information about the internal gRPC implementation
  - The `debug` level logs all gRPC operations; use it only for debugging
  - The `info` level is recommended by default
  - On the `debug` level, the `tech.ydb.table.impl` logger lets you track the internal state of the YDB driver, including the session pool
  - On the `debug` level, the `tech.ydb.table.SessionRetryContext` logger reports the number of retries, query results, per-retry duration, and total operation time
  - On the `debug` level, the `tech.ydb.table.Session` logger provides the query text, response status, and execution time for session operations

  Enabling and configuring the Java SDK loggers depends on the `slf4j-api` implementation you use.
   Here is an example `log4j2` configuration for the `log4j-slf4j-impl` library:

  ```xml
  <Configuration status="WARN">
    <Appenders>
      <Console name="Console" target="SYSTEM_OUT">
        <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
      </Console>
    </Appenders>

    <Loggers>
      <Logger name="io.netty" level="warn" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>
      <Logger name="io.grpc.netty" level="warn" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>
      <Logger name="tech.ydb.core.grpc" level="info" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>
      <Logger name="tech.ydb.table.impl" level="info" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>
      <Logger name="tech.ydb.table.SessionRetryContext" level="debug" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>
      <Logger name="tech.ydb.table.Session" level="debug" additivity="false">
        <AppenderRef ref="Console"/>
      </Logger>

      <Root level="debug" >
        <AppenderRef ref="Console"/>
      </Root>
    </Loggers>
  </Configuration>
  ```

- JDBC

  The JDBC driver uses the same logging stack via `slf4j`; configure the `tech.ydb.*` loggers the same way as in the native SDK.

  The same debug logs are available in other stacks built on JDBC (Spring Boot, ORMs, connection pools, and so on): they reach YDB through this driver, so it is enough to attach the same `slf4j` / log4j2 / logback configuration in the application.

- PHP

  For logging purposes, you need to use a class, that implements `\Psr\Log\LoggerInterface`.
   `ydb-php-sdk` has build-in loggers in `YdbPlatform\Ydb\Logger` namespace:

  - `NullLogger` - default logger, which writes nothing
  - `SimpleStdLogger($level)` - logger, which writes to logs in stderr.

  Usage example:

  ```php
  $config = [
    'logger' => new \YdbPlatform\Ydb\Logger\SimpleStdLogger(\YdbPlatform\Ydb\Logger\SimpleStdLogger::INFO)
  ]
  $ydb = new \YdbPlatform\Ydb\Ydb($config);
  ```

- Python

  The Python SDK uses the standard `logging` library. To enable a specific logging level:

  ```python
  import logging

  logging.getLogger('ydb').setLevel(logging.DEBUG)
  ```

{% endlist %}
