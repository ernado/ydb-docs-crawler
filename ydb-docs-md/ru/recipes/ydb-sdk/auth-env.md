---
title: "Аутентификация при помощи переменных окружения"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth-env?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth-env"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth-env.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth-env.md"
description: "При использовании данного метода режим аутентификации и его параметры будут определены окружением, в котором запускается приложение, в описанном здесь порядке."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Аутентификация при помощи переменных окружения

При использовании данного метода режим аутентификации и его параметры будут определены окружением, в котором запускается приложение, в [описанном здесь порядке](../../reference/ydb-sdk/auth.md#env).

Установив одну из следующих переменных окружения, можно управлять способом аутентификации:

- `YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS=<path/to/sa_key_file>` — использовать файл сервисного аккаунта в Яндекс Облаке.
- `YDB_ANONYMOUS_CREDENTIALS="1"` — Использовать анонимную аутентификацию. Актуально для тестирования против докер-контейнера с YDB.
- `YDB_METADATA_CREDENTIALS="1"` — использовать сервис метаданных внутри Яндекс Облака (Яндекс функция или виртуальная машина).
- `YDB_ACCESS_TOKEN_CREDENTIALS=<access_token>` — использовать аутентификацию с токеном.

Ниже приведены примеры кода аутентификации при помощи переменных окружения в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>
    #include <ydb-cpp-sdk/client/helpers/helpers.h>

    NYdb::TDriver CreateDriverFromEnvironment(const std::string& connectionString) {
        return NYdb::TDriver(NYdb::CreateFromEnvironment(connectionString));
    }
    ```

  - userver

    Функциональность на данный момент не поддерживается.

  {% endlist %}

- Native SDK

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>
  #include <ydb-cpp-sdk/client/helpers/helpers.h>

  NYdb::TDriver CreateDriverFromEnvironment(const std::string& connectionString) {
      return NYdb::TDriver(NYdb::CreateFromEnvironment(connectionString));
  }
  ```

- userver

  Функциональность на данный момент не поддерживается.

- Go

  {% list tabs %}

  - Native SDK

    ```go
    package main

    import (
      "context"
      "os"

      environ "github.com/ydb-platform/ydb-go-sdk-auth-environ"
      "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        environ.WithEnvironCredentials(ctx),
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
      "os"

      environ "github.com/ydb-platform/ydb-go-sdk-auth-environ"
      "github.com/ydb-platform/ydb-go-sdk/v3"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        environ.WithEnvironCredentials(ctx),
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
    "os"

    environ "github.com/ydb-platform/ydb-go-sdk-auth-environ"
    "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      environ.WithEnvironCredentials(ctx),
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
    "os"

    environ "github.com/ydb-platform/ydb-go-sdk-auth-environ"
    "github.com/ydb-platform/ydb-go-sdk/v3"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      environ.WithEnvironCredentials(ctx),
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
        AuthProvider authProvider = new EnvironAuthProvider();

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
        // Подключение без явных учётных данных: драйвер читает переменные окружения YDB_* в порядке,
        // описанном в разделе [Аутентификация](../../reference/ydb-sdk/auth.md#env)
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", new Properties())) {
            doWork(connection);
        }
    }
    ```

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения; учётные данные из переменных окружения подхватываются драйвером так же, как в примере выше (например, через `spring.datasource.url`).

  {% endlist %}

- Native SDK

  ```java
  public void work(String connectionString) {
      AuthProvider authProvider = new EnvironAuthProvider();

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
      // Подключение без явных учётных данных: драйвер читает переменные окружения YDB_* в порядке,
      // описанном в разделе [Аутентификация](../../reference/ydb-sdk/auth.md#env)
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", new Properties())) {
          doWork(connection);
      }
  }
  ```

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения; учётные данные из переменных окружения подхватываются драйвером так же, как в примере выше (например, через `spring.datasource.url`).

- JavaScript

  ```typescript
    import { Driver, getCredentialsFromEnv } from 'ydb-sdk';

    export async function connect(endpoint: string, database: string) {
        const authService = getCredentialsFromEnv();
        const driver = new Driver({endpoint, database, authService});
        const timeout = 10000;
        if (!await driver.ready(timeout)) {
            console.log(`Driver has not become ready in ${timeout}ms!`);
            process.exit(1);
        }
        console.log('Driver connected')
        return driver
    }
  ```

- Python

  {% list tabs %}

  - Native SDK

    ```python
    import os
    import ydb

    with ydb.Driver(
        connection_string=os.environ["YDB_CONNECTION_STRING"],
        credentials=ydb.credentials_from_env_variables(),
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
            credentials=ydb.credentials_from_env_variables(),
        ) as driver:
            await driver.wait()
            ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import os
    import sqlalchemy as sa
    import ydb

    engine = sa.create_engine(
        "yql+ydb://localhost:2136/local",
        connect_args={
            "credentials": ydb.credentials_from_env_variables()
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
      credentials=ydb.credentials_from_env_variables(),
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
          credentials=ydb.credentials_from_env_variables(),
      ) as driver:
          await driver.wait()
          ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import os
  import sqlalchemy as sa
  import ydb

  engine = sa.create_engine(
      "yql+ydb://localhost:2136/local",
      connect_args={
          "credentials": ydb.credentials_from_env_variables()
      }
  )
  with engine.connect() as connection:
      result = connection.execute(sa.text("SELECT 1"))
  ```

- C#

  Функциональность на данный момент не поддерживается.

- Rust

  ```rust
  use ydb::{ClientBuilder, FromEnvCredentials, YdbResult};

  let client = ClientBuilder::new_from_connection_string(std::env::var("YDB_CONNECTION_STRING")?)?
      .with_credentials(FromEnvCredentials::new()?)
      .client()?;
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\EnvironCredentials;

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

      'credentials' => new EnvironCredentials()
  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
