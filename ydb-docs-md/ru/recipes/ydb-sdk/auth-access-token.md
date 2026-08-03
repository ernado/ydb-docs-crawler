---
title: "Аутентификация при помощи токена"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth-access-token?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth-access-token"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth-access-token.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth-access-token.md"
description: "Ниже приведены примеры кода аутентификации при помощи токена в разных YDB SDK. C++. Go. Java. JavaScript. Python. C#. Rust. PHP. Native SDK. userver."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Аутентификация при помощи токена

Ниже приведены примеры кода аутентификации при помощи токена в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>

    NYdb::TDriver CreateDriverWithAccessToken(const std::string& accessToken) {
        auto config = NYdb::TDriverConfig("grpcs://localhost:2135/?database=/local")
            .SetAuthToken(accessToken);

        return NYdb::TDriver(config);
    }
    ```

  - userver

    <details>
    <summary>secdist</summary>

    ```json
    {
      "ydb_settings": {
        "db": {
          "token": "<access token>"
        }
      }
    }
    ```

    </details>

    Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

  {% endlist %}

- Native SDK

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>

  NYdb::TDriver CreateDriverWithAccessToken(const std::string& accessToken) {
      auto config = NYdb::TDriverConfig("grpcs://localhost:2135/?database=/local")
          .SetAuthToken(accessToken);

      return NYdb::TDriver(config);
  }
  ```

- userver

  <details>
  <summary>secdist</summary>

  ```json
  {
    "ydb_settings": {
      "db": {
        "token": "<access token>"
      }
    }
  }
  ```

  </details>

  Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

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
    <summary>Если используется коннектор для создания подключения к YDB</summary>

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
    <summary>Если используется строка подключения</summary>

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
  <summary>Если используется коннектор для создания подключения к YDB</summary>

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
  <summary>Если используется строка подключения</summary>

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
        // Подключение с указанием значения токена аутентификации
        Properties props1 = new Properties();
        props1.setProperty("token", "AQAD-XXXXXXXXXXXXXXXXXXXX");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props1)) {
            doWork(connection);
        }

        // Подключение с чтением токена аутентификации из указанного файла
        Properties props2 = new Properties();
        props2.setProperty("tokenFile", "~/.ydb_token");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props2)) {
            doWork(connection);
        }
    }
    ```

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC используйте ту же JDBC-строку подключения и те же параметры аутентификации, что и выше (например, `spring.datasource.url` с query-параметрами или `spring.datasource.*` для токена и файла токена).

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
      // Подключение с указанием значения токена аутентификации
      Properties props1 = new Properties();
      props1.setProperty("token", "AQAD-XXXXXXXXXXXXXXXXXXXX");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props1)) {
          doWork(connection);
      }

      // Подключение с чтением токена аутентификации из указанного файла
      Properties props2 = new Properties();
      props2.setProperty("tokenFile", "~/.ydb_token");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props2)) {
          doWork(connection);
      }
  }
  ```

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC используйте ту же JDBC-строку подключения и те же параметры аутентификации, что и выше (например, `spring.datasource.url` с query-параметрами или `spring.datasource.*` для токена и файла токена).

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

- C#

  ```C#
  using Ydb.Sdk.Ado;
  using Ydb.Sdk.Auth;

  var builder = new YdbConnectionStringBuilder("Host=localhost;Port=2136;Database=/local")
  {
      CredentialsProvider = new TokenProvider("MY_VERY_SECURE_TOKEN")
  };

  await using var dataSource = new YdbDataSource(builder);
  await using var connection = await dataSource.OpenConnectionAsync();
  ```

  Для Entity Framework и linq2db не поддерживается.

- Rust

  ```rust
  use ydb::{AccessTokenCredentials, ClientBuilder, YdbResult};

  let client = ClientBuilder::new_from_connection_string("grpc://localhost:2136?database=local")?
      .with_credentials(AccessTokenCredentials::from(std::env::var("YDB_TOKEN")?))
      .client()?;
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
