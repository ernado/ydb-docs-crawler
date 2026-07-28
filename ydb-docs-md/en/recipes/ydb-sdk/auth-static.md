---
title: "Username and password based authentication"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/auth-static?version=v26.1"
doc_path: "en/recipes/ydb-sdk/auth-static"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/auth-static.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/auth-static.md"
description: "Username and password based authentication. Below are examples of authentication with a username and password in different YDB SDKs. C++. Go. Java. JavaScript."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Username and password based authentication

Below are examples of authentication with a username and password in different YDB SDKs.

{% list tabs %}

- C++

  ```c++
  auto driverConfig = NYdb::TDriverConfig()
    .SetEndpoint(endpoint)
    .SetDatabase(database)
    .SetCredentialsProviderFactory(NYdb::CreateLoginCredentialsProviderFactory({
        .User = "user",
        .Password = "password",
    }));

  NYdb::TDriver driver(driverConfig);
  ```

- Go

  {% list tabs %}

  - Native SDK

    You can pass the username and password in the connection string. For example:

    ```shell
    "grpcs://login:password@localhost:2135/local"
    ```

    You can also pass them explicitly using the `ydb.WithStaticCredentials` option:

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
          ydb.WithStaticCredentials("user", "password"),
      )
      if err != nil {
          panic(err)
      }
      defer db.Close(ctx)
      ...
    }
    ```

  - database/sql

    You can pass the username and password in the connection string. For example:

    ```go
    package main

    import (
      "context"

      _ "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      db, err := sql.Open("ydb", "grpcs://login:password@localohost:2135/local")
      if err != nil {
          panic(err)
      }
      defer db.Close()
      ...
    }
    ```

    You can also pass them explicitly when initializing the driver via a connector using the `ydb.WithStaticCredentials` option:

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
      nativeDriver, err := ydb.Open(ctx,
          os.Getenv("YDB_CONNECTION_STRING"),
          ydb.WithStaticCredentials("user", "password"),
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

  You can pass the username and password in the connection string. For example:

  ```shell
  "grpcs://login:password@localhost:2135/local"
  ```

  You can also pass them explicitly using the `ydb.WithStaticCredentials` option:

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
        ydb.WithStaticCredentials("user", "password"),
    )
    if err != nil {
        panic(err)
    }
    defer db.Close(ctx)
    ...
  }
  ```

- database/sql

  You can pass the username and password in the connection string. For example:

  ```go
  package main

  import (
    "context"

    _ "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    db, err := sql.Open("ydb", "grpcs://login:password@localohost:2135/local")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    ...
  }
  ```

  You can also pass them explicitly when initializing the driver via a connector using the `ydb.WithStaticCredentials` option:

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
    nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithStaticCredentials("user", "password"),
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
    public void work(String connectionString, String username, String password) {
        StaticCredentials authProvider = new StaticCredentials(username, password);

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
    public void work(String username, String password) throws SQLException {
        Properties props = new Properties();
        props.setProperty("username", username);
        props.setProperty("password", password);
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
            doWork(connection);
        }

        // Username and password can be passed directly
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", username, password)) {
            doWork(connection);
        }
    }
    ```

    In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL, username, and password as above (for example `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password`, or the pool’s equivalent settings).

  {% endlist %}

- Native SDK

  ```java
  public void work(String connectionString, String username, String password) {
      StaticCredentials authProvider = new StaticCredentials(username, password);

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
  public void work(String username, String password) throws SQLException {
      Properties props = new Properties();
      props.setProperty("username", username);
      props.setProperty("password", password);
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
          doWork(connection);
      }

      // Username and password can be passed directly
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", username, password)) {
          doWork(connection);
      }
  }
  ```

  In Spring Boot, ORMs, and other JDBC wrappers, use the same JDBC URL, username, and password as above (for example `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password`, or the pool’s equivalent settings).

- JavaScript

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { StaticCredentialsProvider } from "@ydbjs/auth/static";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: new StaticCredentialsProvider(
      { username: user, password: password },
      "grpc://localhost:2136",
    ),
  });

  await driver.ready();
  ```

- Python

  {% list tabs %}

  - Native SDK

    ```python
    import os
    import ydb

    config = ydb.DriverConfig(
        endpoint=os.environ["YDB_ENDPOINT"],
        database=os.environ["YDB_DATABASE"],
    )

    credentials = ydb.StaticCredentials(
        driver_config=config,
        user=os.environ["YDB_USER"],
        password=os.environ["YDB_PASSWORD"]
    )

    with ydb.Driver(driver_config=config, credentials=credentials) as driver:
        driver.wait(timeout=5)
        ...
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import ydb
    import asyncio

    config = ydb.DriverConfig(
        endpoint=os.environ["YDB_ENDPOINT"],
        database=os.environ["YDB_DATABASE"],
    )

    credentials = ydb.StaticCredentials(
        driver_config=config,
        user=os.environ["YDB_USER"],
        password=os.environ["YDB_PASSWORD"],
    )

    async def ydb_init():
        async with ydb.aio.Driver(driver_config=config, credentials=credentials) as driver:
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
            "credentials": {
                "username": os.environ["YDB_USER"],
                "password": os.environ["YDB_PASSWORD"]
            }
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

  config = ydb.DriverConfig(
      endpoint=os.environ["YDB_ENDPOINT"],
      database=os.environ["YDB_DATABASE"],
  )

  credentials = ydb.StaticCredentials(
      driver_config=config,
      user=os.environ["YDB_USER"],
      password=os.environ["YDB_PASSWORD"]
  )

  with ydb.Driver(driver_config=config, credentials=credentials) as driver:
      driver.wait(timeout=5)
      ...
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import ydb
  import asyncio

  config = ydb.DriverConfig(
      endpoint=os.environ["YDB_ENDPOINT"],
      database=os.environ["YDB_DATABASE"],
  )

  credentials = ydb.StaticCredentials(
      driver_config=config,
      user=os.environ["YDB_USER"],
      password=os.environ["YDB_PASSWORD"],
  )

  async def ydb_init():
      async with ydb.aio.Driver(driver_config=config, credentials=credentials) as driver:
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
          "credentials": {
              "username": os.environ["YDB_USER"],
              "password": os.environ["YDB_PASSWORD"]
          }
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

  var config = new DriverConfig(
      endpoint: endpoint, // Database endpoint, "grpcs://host:port"
      database: database, // Full database path
      credentials: new StaticCredentialsProvider(user, password)
  );

  await using var driver = await Driver.CreateInitialized(config);
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\Implement\StaticAuthentication;

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

      'credentials' => new StaticAuthentication($user, $password)
  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
