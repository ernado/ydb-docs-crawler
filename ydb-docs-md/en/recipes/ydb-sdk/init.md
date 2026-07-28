---
title: "Initialize the driver"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/init?version=v26.1"
doc_path: "en/recipes/ydb-sdk/init"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/init.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/init.md"
description: "To connect to YDB, you must specify the required parameters (see Connecting to a YDB server ) and optional parameters that control driver behavior."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Initialize the driver

To connect to YDB, you must specify the required parameters (see [Connecting to a YDB server](../../concepts/connect.md)) and optional parameters that control driver behavior.

Below are examples of connecting to YDB (creating a driver) in different YDB SDKs.

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

    ```golang
    package main

    import (
      "context"

      "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()

      db, err := ydb.Open(ctx, "grpc://localhost:2136/local")
      if err != nil {
          panic(err)
      }
      defer db.Close()

      // ...
    }
    ```

  - database/sql

    <details>
    <summary>Using a connector (recommended)</summary>

    ```golang
    package main

    import (
      "context"
      "database/sql"
      "os"

      "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()

      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
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

      // ...
    }
    ```

    </details>

    <details>
    <summary>Using a connection string</summary>

    The `database/sql` driver is registered when you import the driver package with a blank import:

    ```golang
    package main

    import (
      "database/sql"

      _ "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      db, err := sql.Open("ydb", "grpc://localhost:2136/local")
      if err != nil {
        panic(err)
      }
      defer db.Close()

      // ...
    }
    ```

    </details>

  {% endlist %}

- Native SDK

  ```golang
  package main

  import (
    "context"

    "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    db, err := ydb.Open(ctx, "grpc://localhost:2136/local")
    if err != nil {
        panic(err)
    }
    defer db.Close()

    // ...
  }
  ```

- database/sql

  <details>
  <summary>Using a connector (recommended)</summary>

  ```golang
  package main

  import (
    "context"
    "database/sql"
    "os"

    "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
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

    // ...
  }
  ```

  </details>

  <details>
  <summary>Using a connection string</summary>

  The `database/sql` driver is registered when you import the driver package with a blank import:

  ```golang
  package main

  import (
    "database/sql"

    _ "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    db, err := sql.Open("ydb", "grpc://localhost:2136/local")
    if err != nil {
      panic(err)
    }
    defer db.Close()

    // ...
  }
  ```

  </details>

- Java

  {% list tabs %}

  - Native SDK

    ```java
    public void work() {
        try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
                .build()) {
            // Work with transport
            doWork(transport);
        }
    }
    ```

  - JDBC

    ```java
    public void work() throws SQLException {
        // tech.ydb.jdbc.YdbDriver must be on the classpath for DriverManager auto-loading
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
            // Work with connection
            doWork(connection);
        }
    }
    ```

    For Spring Boot, set the URL and driver class in `application.properties` or `application.yml` (`spring.datasource.url`, `spring.datasource.driver-class-name`).

    Spring Boot, ORMs, and other JDBC stacks (Hibernate, JOOQ, MyBatis, and so on) talk to YDB like any JDBC source: add the YDB JDBC dependency and configure the URL — you do not need to configure native `GrpcTransport` separately.

  {% endlist %}

- Native SDK

  ```java
  public void work() {
      try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
              .build()) {
          // Work with transport
          doWork(transport);
      }
  }
  ```

- JDBC

  ```java
  public void work() throws SQLException {
      // tech.ydb.jdbc.YdbDriver must be on the classpath for DriverManager auto-loading
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
          // Work with connection
          doWork(connection);
      }
  }
  ```

  For Spring Boot, set the URL and driver class in `application.properties` or `application.yml` (`spring.datasource.url`, `spring.datasource.driver-class-name`).

  Spring Boot, ORMs, and other JDBC stacks (Hibernate, JOOQ, MyBatis, and so on) talk to YDB like any JDBC source: add the YDB JDBC dependency and configure the URL — you do not need to configure native `GrpcTransport` separately.

- Python

  {% list tabs %}

  - Native SDK

    ```python
    import ydb

    with ydb.Driver(connection_string="grpc://localhost:2136?database=/local") as driver:
      driver.wait(timeout=5)
      ...
    ```

  - Native SDK (Asyncio)

    ```python
    import ydb
    import asyncio

    async def ydb_init():
      async with ydb.aio.Driver(endpoint="grpc://localhost:2136", database="/local") as driver:
        await driver.wait()
        ...

    asyncio.run(ydb_init())
    ```

  {% endlist %}

- Native SDK

  ```python
  import ydb

  with ydb.Driver(connection_string="grpc://localhost:2136?database=/local") as driver:
    driver.wait(timeout=5)
    ...
  ```

- Native SDK (Asyncio)

  ```python
  import ydb
  import asyncio

  async def ydb_init():
    async with ydb.aio.Driver(endpoint="grpc://localhost:2136", database="/local") as driver:
      await driver.wait()
      ...

  asyncio.run(ydb_init())
  ```

- C# (.NET)

  ```C#
  using Ydb.Sdk;

  var config = new DriverConfig(
      endpoint: "grpc://localhost:2136",
      database: "/local"
  );

  await using var driver = await Driver.CreateInitialized(config);
  ```

- JavaScript

  ```javascript
  import { Driver } from '@ydbjs/core'

  const driver = new Driver('grpc://localhost:2136/local')
  await driver.ready()
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;

  $config = [
      // Database path
      'database'    => '/ru-central1/b1glxxxxxxxxxxxxxxxx/etn0xxxxxxxxxxxxxxxx',

      // Database endpoint
      'endpoint'    => 'ydb.serverless.yandexcloud.net:2135',

      // Auto discovery (dedicated server only)
      'discovery'   => false,

      // IAM config
      'iam_config'  => [
          // 'root_cert_file' => './CA.pem', // Root CA file (uncomment for dedicated server)
      ],

      'credentials' => new \YdbPlatform\Ydb\Auth\Implement\AccessTokenAuthentication('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA') // use from reference/ydb-sdk/auth
  ];

  $ydb = new Ydb($config);
  ```

- Rust

  ```rust
  use ydb::{AccessTokenCredentials, ClientBuilder, YdbResult};

  #[tokio::main]
  async fn main() -> YdbResult<()> {
      let client = ClientBuilder::new_from_connection_string("grpc://localhost:2136/local")?
          .with_credentials(AccessTokenCredentials::from("..."))
          .client()?;
      client.wait().await?;
      Ok(())
  }
  ```

{% endlist %}
