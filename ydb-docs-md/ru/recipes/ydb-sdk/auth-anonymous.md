---
title: "Анонимная аутентификация"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth-anonymous?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth-anonymous"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth-anonymous.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth-anonymous.md"
description: "Ниже приведены примеры кода анонимной аутентификации в разных YDB SDK. C++. Go. Java. JavaScript. Python. C#. Rust. PHP. Native SDK. userver."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Анонимная аутентификация

Ниже приведены примеры кода анонимной аутентификации в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    Анонимная аутентификация является аутентификацией по умолчанию.
     Явным образом анонимную аутентификацию можно включить так:

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>
    #include <ydb-cpp-sdk/client/types/credentials/credentials.h>

    NYdb::TDriver CreateDriverAnonymous() {
        auto config = NYdb::TDriverConfig("grpc://localhost:2136/local")
            .SetCredentialsProviderFactory(NYdb::CreateInsecureCredentialsProviderFactory());

        return NYdb::TDriver(config);
    }
    ```

  - userver

    Если в статическом конфиге не задавать `credentials-provider`, не указывать `databases.*.credentials` и не класть в secdist для этой базы `token`, `iam_jwt_params` и пару `user`/`password`, драйвер будет использовать анонимный режим по умолчанию.

    Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

  {% endlist %}

- Native SDK

  Анонимная аутентификация является аутентификацией по умолчанию.
   Явным образом анонимную аутентификацию можно включить так:

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>
  #include <ydb-cpp-sdk/client/types/credentials/credentials.h>

  NYdb::TDriver CreateDriverAnonymous() {
      auto config = NYdb::TDriverConfig("grpc://localhost:2136/local")
          .SetCredentialsProviderFactory(NYdb::CreateInsecureCredentialsProviderFactory());

      return NYdb::TDriver(config);
  }
  ```

- userver

  Если в статическом конфиге не задавать `credentials-provider`, не указывать `databases.*.credentials` и не класть в secdist для этой базы `token`, `iam_jwt_params` и пару `user`/`password`, драйвер будет использовать анонимный режим по умолчанию.

  Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

- Go

  {% list tabs %}

  - Native SDK

    Анонимная аутентификация является аутентификацией по умолчанию.
     Явным образом анонимную аутентификацию можно включить так:

    ```go
    package main

    import (
      "context"

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

    Анонимная аутентификация является аутентификацией по умолчанию.
     Явным образом анонимную аутентификацию можно включить так:

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

  Анонимная аутентификация является аутентификацией по умолчанию.
   Явным образом анонимную аутентификацию можно включить так:

  ```go
  package main

  import (
    "context"

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

  Анонимная аутентификация является аутентификацией по умолчанию.
   Явным образом анонимную аутентификацию можно включить так:

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
        // Подключение без дополнительных опций — с анонимной аутентификацией
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
            doWork(connection);
        }
    }
    ```

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC подключение задаётся той же JDBC-строкой подключения, что и выше (например, `spring.datasource.url`).

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
      // Подключение без дополнительных опций — с анонимной аутентификацией
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local")) {
          doWork(connection);
      }
  }
  ```

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC подключение задаётся той же JDBC-строкой подключения, что и выше (например, `spring.datasource.url`).

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

- C#

  ```C#
  using Ydb.Sdk.Ado;

  await using var dataSource = new YdbDataSource("Host=localhost;Port=2136;Database=/local");
  await using var connection = await dataSource.OpenConnectionAsync();
  ```

  Для Entity Framework и linq2db используйте тот же connectionString.

- Rust

  ```rust
  use ydb::{AnonymousCredentials, ClientBuilder, YdbResult};

  let client = ClientBuilder::new_from_connection_string("grpc://localhost:2136?database=local")?
      .with_credentials(AnonymousCredentials::new())
      .client()?;
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
