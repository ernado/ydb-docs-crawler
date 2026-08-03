---
title: "Anonymous authentication"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/auth-anonymous?version=v26.1"
doc_path: "en/recipes/ydb-sdk/auth-anonymous"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/auth-anonymous.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/auth-anonymous.md"
description: "Below are examples of anonymous authentication in different YDB SDKs. Go. Java. JavaScript. Python. C# (.NET). PHP. Native SDK. database/sql."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Anonymous authentication

Below are examples of anonymous authentication in different YDB SDKs.

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

    Anonymous authentication is the default.
     You can enable it explicitly as follows:

    ```go
    package main

    import (
      "context"
      "os"

      "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithAnonymousCredentials(),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

  - database/sql

    Anonymous authentication is the default.
     You can enable it explicitly as follows:

    ```go
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
        ydb.WithAnonymousCredentials(),
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

  Anonymous authentication is the default.
   You can enable it explicitly as follows:

  ```go
  package main

  import (
    "context"
    "os"

    "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydb.WithAnonymousCredentials(),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

- database/sql

  Anonymous authentication is the default.
   You can enable it explicitly as follows:

  ```go
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
      ydb.WithAnonymousCredentials(),
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

  {% list tabs %}

  - Native SDK

    ```java
    public void work(String connectionString) {
        AuthProvider authProvider = NopAuthProvider.INSTANCE;

        try (GrpcTransport transport = GrpcTransport.forConnectionString(connectionString)
                .withAuthProvider(authProvider)
                .build();
             QueryClient queryClient = QueryClient.newClient(transport).build()) {

            doWork(queryClient);
        }
    }
    ```

  - JDBC

    ```java
    public void work() throws SQLException {
        // Connection with no extra options — anonymous authentication
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
            doWork(connection);
        }
    }
    ```

    In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL as above (for example `spring.datasource.url`).

  {% endlist %}

- Native SDK

  ```java
  public void work(String connectionString) {
      AuthProvider authProvider = NopAuthProvider.INSTANCE;

      try (GrpcTransport transport = GrpcTransport.forConnectionString(connectionString)
              .withAuthProvider(authProvider)
              .build();
           QueryClient queryClient = QueryClient.newClient(transport).build()) {

          doWork(queryClient);
      }
  }
  ```

- JDBC

  ```java
  public void work() throws SQLException {
      // Connection with no extra options — anonymous authentication
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
          doWork(connection);
      }
  }
  ```

  In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL as above (for example `spring.datasource.url`).

- JavaScript

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { AnonymousCredentialsProvider } from "@ydbjs/auth/anonymous";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: new AnonymousCredentialsProvider(),
  });

  await driver.ready();
  ```

- Python

  {% list tabs %}

  - Native SDK

    ```python
    import os
    import ydb

    with ydb.Driver(
        connection_string=os.environ["YDB_CONNECTION_STRING"],
        credentials=ydb.credentials.AnonymousCredentials(),
    ) as driver:
        driver.wait(timeout=5)
        ...
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import ydb
    import asyncio

    async def ydb_init():
        async with ydb.aio.Driver(
            endpoint=os.environ["YDB_ENDPOINT"],
            database=os.environ["YDB_DATABASE"],
            credentials=ydb.credentials.AnonymousCredentials(),
        ) as driver:
            await driver.wait()
            ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import sqlalchemy as sa

    engine = sa.create_engine("yql+ydb://localhost:2136/local")
    with engine.connect() as connection:
        result = connection.execute(sa.text("SELECT 1"))
    ```

  {% endlist %}

- Native SDK

  ```python
  import os
  import ydb

  with ydb.Driver(
      connection_string=os.environ["YDB_CONNECTION_STRING"],
      credentials=ydb.credentials.AnonymousCredentials(),
  ) as driver:
      driver.wait(timeout=5)
      ...
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import ydb
  import asyncio

  async def ydb_init():
      async with ydb.aio.Driver(
          endpoint=os.environ["YDB_ENDPOINT"],
          database=os.environ["YDB_DATABASE"],
          credentials=ydb.credentials.AnonymousCredentials(),
      ) as driver:
          await driver.wait()
          ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import sqlalchemy as sa

  engine = sa.create_engine("yql+ydb://localhost:2136/local")
  with engine.connect() as connection:
      result = connection.execute(sa.text("SELECT 1"))
  ```

- C# (.NET)

  ```C#
  using Ydb.Sdk;
  using Ydb.Sdk.Auth;

  const string endpoint = "grpc://localhost:2136";
  const string database = "/local";

  var config = new DriverConfig(
      endpoint: endpoint,
      database: database,
      credentials: new AnonymousProvider()
  );

  await using var driver = await Driver.CreateInitialized(config);
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\Implement\AnonymousAuthentication;

  $config = [

      // Database path
      'database'    => '/local',

      // Database endpoint
      'endpoint'    => 'localhost:2136',

      // Auto discovery (dedicated server only)
      'discovery'   => false,

      // IAM config
      'iam_config'  => [
          'insecure' => true,
          // 'root_cert_file' => './CA.pem', // Root CA file (uncomment for dedicated server)
      ],

      'credentials' => new AnonymousAuthentication()
  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
