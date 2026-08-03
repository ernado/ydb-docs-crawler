---
title: "Authentication using a token"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/auth-access-token?version=v26.1"
doc_path: "en/recipes/ydb-sdk/auth-access-token"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/auth-access-token.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/auth-access-token.md"
description: "Below are examples of authentication with a token in different YDB SDKs. Go. Java. JavaScript. Python. C# (.NET). PHP. Native SDK. database/sql."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Authentication using a token

Below are examples of authentication with a token in different YDB SDKs.

{% list tabs %}

- Go

  {% list tabs %}

  - Native SDK

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
        ydb.WithAccessTokenCredentials(os.Getenv("YDB_TOKEN")),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

  - database/sql

    <details>
    <summary>If you use a connector to create a connection to YDB</summary>

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
        ydb.WithAccessTokenCredentials(os.Getenv("YDB_TOKEN")),
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

    </details>

    <details>
    <summary>If you use a connection string</summary>

    ```go
    package main

    import (
      "context"
      "database/sql"
      "os"

      _ "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      db, err := sql.Open("ydb", "grpcs://localhost:2135/local?token="+os.Getenv("YDB_TOKEN"))
      if err != nil {
        panic(err)
      }
      defer db.Close()
      ...
    }
    ```

    </details>

  {% endlist %}

- Native SDK

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
      ydb.WithAccessTokenCredentials(os.Getenv("YDB_TOKEN")),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

- database/sql

  <details>
  <summary>If you use a connector to create a connection to YDB</summary>

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
      ydb.WithAccessTokenCredentials(os.Getenv("YDB_TOKEN")),
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

  </details>

  <details>
  <summary>If you use a connection string</summary>

  ```go
  package main

  import (
    "context"
    "database/sql"
    "os"

    _ "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    db, err := sql.Open("ydb", "grpcs://localhost:2135/local?token="+os.Getenv("YDB_TOKEN"))
    if err != nil {
      panic(err)
    }
    defer db.Close()
    ...
  }
  ```

  </details>

- Java

  {% list tabs %}

  - Native SDK

    ```java
    public void work(String accessToken) {
        AuthProvider authProvider = new TokenAuthProvider(accessToken);

        try (GrpcTransport transport = GrpcTransport.forConnectionString("grpcs://localhost:2135/local")
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
        // Connection with an explicit authentication token value
        Properties props1 = new Properties();
        props1.setProperty("token", "AQAD-XXXXXXXXXXXXXXXXXXXX");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props1)) {
            doWork(connection);
        }

        // Connection with the token read from the specified file
        Properties props2 = new Properties();
        props2.setProperty("tokenFile", "~/.ydb_token");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props2)) {
            doWork(connection);
        }
    }
    ```

    In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL and authentication parameters as above (for example `spring.datasource.url` with query parameters or `spring.datasource.*` for the token and token file).

  {% endlist %}

- Native SDK

  ```java
  public void work(String accessToken) {
      AuthProvider authProvider = new TokenAuthProvider(accessToken);

      try (GrpcTransport transport = GrpcTransport.forConnectionString("grpcs://localhost:2135/local")
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
      // Connection with an explicit authentication token value
      Properties props1 = new Properties();
      props1.setProperty("token", "AQAD-XXXXXXXXXXXXXXXXXXXX");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props1)) {
          doWork(connection);
      }

      // Connection with the token read from the specified file
      Properties props2 = new Properties();
      props2.setProperty("tokenFile", "~/.ydb_token");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props2)) {
          doWork(connection);
      }
  }
  ```

  In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL and authentication parameters as above (for example `spring.datasource.url` with query parameters or `spring.datasource.*` for the token and token file).

- JavaScript

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { AccessTokenCredentialsProvider } from "@ydbjs/auth/access-token";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: new AccessTokenCredentialsProvider({
      token: "accessToken",
    }),
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
        credentials=ydb.credentials.AccessTokenCredentials(os.environ["YDB_TOKEN"]),
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
            credentials=ydb.credentials.AccessTokenCredentials(os.environ["YDB_TOKEN"]),
        ) as driver:
            await driver.wait()
            ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import os
    import sqlalchemy as sa

    engine = sa.create_engine(
        "yql+ydb://localhost:2136/local",
        connect_args={
            "credentials": {"token": os.environ["YDB_TOKEN"]}
        }
    )
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
      credentials=ydb.credentials.AccessTokenCredentials(os.environ["YDB_TOKEN"]),
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
          credentials=ydb.credentials.AccessTokenCredentials(os.environ["YDB_TOKEN"]),
      ) as driver:
          await driver.wait()
          ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import os
  import sqlalchemy as sa

  engine = sa.create_engine(
      "yql+ydb://localhost:2136/local",
      connect_args={
          "credentials": {"token": os.environ["YDB_TOKEN"]}
      }
  )
  with engine.connect() as connection:
      result = connection.execute(sa.text("SELECT 1"))
  ```

- C# (.NET)

  ```C#
  using Ydb.Sdk;
  using Ydb.Sdk.Auth;

  const string endpoint = "grpc://localhost:2136";
  const string database = "/local";
  const string token = "MY_VERY_SECURE_TOKEN";

  var config = new DriverConfig(
      endpoint: endpoint,
      database: database,
      credentials: new TokenProvider(token)
  );

  await using var driver = await Driver.CreateInitialized(config);
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\Implement\AccessTokenAuthentication;

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

      'credentials' => new AccessTokenAuthentication('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
