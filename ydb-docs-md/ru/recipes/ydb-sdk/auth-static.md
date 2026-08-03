---
title: "Аутентификация при помощи логина и пароля"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth-static?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth-static"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth-static.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth-static.md"
description: "Аутентификация при помощи логина и пароля. Ниже приведены примеры кода аутентификации при помощи логина и пароля в разных YDB SDK. C++. Go. Java. JavaScript."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Аутентификация при помощи логина и пароля

Ниже приведены примеры кода аутентификации при помощи логина и пароля в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>
    #include <ydb-cpp-sdk/client/types/credentials/credentials.h>

    NYdb::TDriver CreateDriverWithStaticCredentials(
        const std::string& connectionString,
        const std::string& user,
        const std::string& password)
    {
        auto config = NYdb::TDriverConfig(connectionString)
            .SetCredentialsProviderFactory(NYdb::CreateLoginCredentialsProviderFactory({
                .User = user,
                .Password = password,
            }));

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
          "user": "user",
          "password": "password"
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
  #include <ydb-cpp-sdk/client/types/credentials/credentials.h>

  NYdb::TDriver CreateDriverWithStaticCredentials(
      const std::string& connectionString,
      const std::string& user,
      const std::string& password)
  {
      auto config = NYdb::TDriverConfig(connectionString)
          .SetCredentialsProviderFactory(NYdb::CreateLoginCredentialsProviderFactory({
              .User = user,
              .Password = password,
          }));

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
        "user": "user",
        "password": "password"
      }
    }
  }
  ```

  </details>

  Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

- Go

  {% list tabs %}

  - Native SDK

    Передать логин и пароль можно в составе строки подключения. Например, так:

    ```shell
    "grpcs://login:password@localhost:2135/local"
    ```

    Также можно передать логин и пароль явно через опцию `ydb.WithStaticCredentials`:

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

    Передать логин и пароль можно в составе строки подключения. Например, так:

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

    Также можно передать логин и пароль явно при инициализации драйвера через коннектор с помощью специальной опции `ydb.WithStaticCredentials`:

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

  Передать логин и пароль можно в составе строки подключения. Например, так:

  ```shell
  "grpcs://login:password@localhost:2135/local"
  ```

  Также можно передать логин и пароль явно через опцию `ydb.WithStaticCredentials`:

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

  Передать логин и пароль можно в составе строки подключения. Например, так:

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

  Также можно передать логин и пароль явно при инициализации драйвера через коннектор с помощью специальной опции `ydb.WithStaticCredentials`:

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

        // Логин и пароль могут быть указаны напрямую
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", username, password)) {
            doWork(connection);
        }
    }
    ```

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC задайте те же JDBC URL, логин и пароль, что и в примере выше (например, `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password` или эквивалент в конфигурации пула).

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

      // Логин и пароль могут быть указаны напрямую
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", username, password)) {
          doWork(connection);
      }
  }
  ```

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC задайте те же JDBC URL, логин и пароль, что и в примере выше (например, `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password` или эквивалент в конфигурации пула).

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

- C#

  ```C#
  using Ydb.Sdk.Ado;

  await using var dataSource = new YdbDataSource(
      "Host=localhost;Port=2136;Database=/local;User=user;Password=password");
  await using var connection = await dataSource.OpenConnectionAsync();
  ```

- Rust

  ```rust
  use ydb::{ClientBuilder, StaticCredentials, YdbResult};

  let client = ClientBuilder::new_from_connection_string("grpc://localhost:2136?database=local")?
      .with_credentials(StaticCredentials::new(
          std::env::var("YDB_USER")?,
          std::env::var("YDB_PASSWORD")?,
          http::Uri::from_static("grpc://localhost:2136"),
          "local".into(),
      ))
      .client()?;
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
