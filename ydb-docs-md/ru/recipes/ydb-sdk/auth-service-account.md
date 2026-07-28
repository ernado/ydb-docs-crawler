---
title: "Аутентификация при помощи файла сервисного аккаунта"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/auth-service-account?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/auth-service-account"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/auth-service-account.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/auth-service-account.md"
description: "Ниже приведены примеры кода аутентификации при помощи файла сервисного аккаунта в разных YDB SDK. C++. Go. Java. JavaScript. Python. C#. Rust. PHP. Native SDK."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Аутентификация при помощи файла сервисного аккаунта

Ниже приведены примеры кода аутентификации при помощи файла сервисного аккаунта в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>
    #include <ydb-cpp-sdk/client/iam/iam.h>

    NYdb::TDriver CreateDriverWithServiceAccountKeyFile(
        const std::string& connectionString,
        const std::string& saKeyFilePath,
        const std::string& internalCA)
    {
        auto config = NYdb::TDriverConfig(connectionString)
            .UseSecureConnection(internalCA)
            .SetCredentialsProviderFactory(NYdb::CreateIamJwtFileCredentialsProviderFactory({
                .JwtFilename = saKeyFilePath,
            }));

        return NYdb::TDriver(config);
    }
    ```

  - userver

    <details>
    <summary>secdist</summary>

    `<PEM>` - сертификаты Yandex Cloud.

    ```json
    {
      "ydb_settings": {
        "db": {
          "iam_jwt_params": {
            "id": "...",
            "service_account_id": "...",
            "private_key": "..."
          },
          "secure_connection_cert": "<PEM>"
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
  #include <ydb-cpp-sdk/client/iam/iam.h>

  NYdb::TDriver CreateDriverWithServiceAccountKeyFile(
      const std::string& connectionString,
      const std::string& saKeyFilePath,
      const std::string& internalCA)
  {
      auto config = NYdb::TDriverConfig(connectionString)
          .UseSecureConnection(internalCA)
          .SetCredentialsProviderFactory(NYdb::CreateIamJwtFileCredentialsProviderFactory({
              .JwtFilename = saKeyFilePath,
          }));

      return NYdb::TDriver(config);
  }
  ```

- userver

  <details>
  <summary>secdist</summary>

  `<PEM>` - сертификаты Yandex Cloud.

  ```json
  {
    "ydb_settings": {
      "db": {
        "iam_jwt_params": {
          "id": "...",
          "service_account_id": "...",
          "private_key": "..."
        },
        "secure_connection_cert": "<PEM>"
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
      yc "github.com/ydb-platform/ydb-go-yc"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        yc.WithServiceAccountKeyFileCredentials(
          os.Getenv("YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"),
        ),
        yc.WithInternalCA(), // append Yandex Cloud certificates
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

      "github.com/ydb-platform/ydb-go-sdk/v3"
      yc "github.com/ydb-platform/ydb-go-yc"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        yc.WithServiceAccountKeyFileCredentials(
          os.Getenv("YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"),
        ),
        yc.WithInternalCA(), // append Yandex Cloud certificates
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

    "github.com/ydb-platform/ydb-go-sdk/v3"
    yc "github.com/ydb-platform/ydb-go-yc"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      yc.WithServiceAccountKeyFileCredentials(
        os.Getenv("YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"),
      ),
      yc.WithInternalCA(), // append Yandex Cloud certificates
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

    "github.com/ydb-platform/ydb-go-sdk/v3"
    yc "github.com/ydb-platform/ydb-go-yc"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      yc.WithServiceAccountKeyFileCredentials(
        os.Getenv("YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"),
      ),
      yc.WithInternalCA(), // append Yandex Cloud certificates
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
    public void work(String connectionString, String saKeyPath) {
        AuthProvider authProvider = CloudAuthHelper.getServiceAccountFileAuthProvider(saKeyPath);

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
        Properties props = new Properties();
        props.setProperty("saKeyFile", "~/keys/sa_key.json");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
            doWork(connection);
        }

        // Опцию saKeyFile также можно указать прямо в JDBC URL
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local?saKeyFile=~/keys/sa_key.json")) {
            doWork(connection);
        }
    }
    ```

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения и параметр `saKeyFile` (в URL или в свойствах `DataSource`), что и в примере выше.

  {% endlist %}

- Native SDK

  ```java
  public void work(String connectionString, String saKeyPath) {
      AuthProvider authProvider = CloudAuthHelper.getServiceAccountFileAuthProvider(saKeyPath);

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
      Properties props = new Properties();
      props.setProperty("saKeyFile", "~/keys/sa_key.json");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
          doWork(connection);
      }

      // Опцию saKeyFile также можно указать прямо в JDBC URL
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local?saKeyFile=~/keys/sa_key.json")) {
          doWork(connection);
      }
  }
  ```

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения и параметр `saKeyFile` (в URL или в свойствах `DataSource`), что и в примере выше.

- JavaScript

  Загрузка данных сервисного аккаунта из файла:

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { ServiceAccountCredentialsProvider } from "@ydbjs/auth-yandex-cloud";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: ServiceAccountCredentialsProvider.fromFile("./authorized_key.json"),
  });

  await driver.ready();
  ```

  Загрузка данных сервисного аккаунта из стороннего источника (например, из хранилища секретов):

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { ServiceAccountCredentialsProvider } from "@ydbjs/auth-yandex-cloud";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: new ServiceAccountCredentialsProvider({
      id: "serviceAccountId",
      keyId: "accessKeyId",
      privateKey: "-----BEGIN PRIVATE KEY-----\n...",
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
    import ydb.iam

    with ydb.Driver(
        connection_string=os.environ["YDB_CONNECTION_STRING"],
        # service account key should be in the local file,
        # and SA_KEY_FILE environment variable should point to it
        credentials=ydb.iam.ServiceAccountCredentials.from_file(os.environ["SA_KEY_FILE"]),
    ) as driver:
        driver.wait(timeout=5)
        ...
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import asyncio
    import ydb
    import ydb.iam

    async def ydb_init():
        async with ydb.aio.Driver(
            endpoint=os.environ["YDB_ENDPOINT"],
            database=os.environ["YDB_DATABASE"],
            # service account key should be in the local file,
            # and SA_KEY_FILE environment variable should point to it
            credentials=ydb.iam.ServiceAccountCredentials.from_file(os.environ["SA_KEY_FILE"]),
        ) as driver:
            await driver.wait()
            ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import os
    import sqlalchemy as sa
    import ydb.iam

    engine = sa.create_engine(
        "yql+ydb://localhost:2136/local",
        connect_args={
            "credentials": ydb.iam.ServiceAccountCredentials.from_file(
                os.environ["YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"]
            )
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
  import ydb.iam

  with ydb.Driver(
      connection_string=os.environ["YDB_CONNECTION_STRING"],
      # service account key should be in the local file,
      # and SA_KEY_FILE environment variable should point to it
      credentials=ydb.iam.ServiceAccountCredentials.from_file(os.environ["SA_KEY_FILE"]),
  ) as driver:
      driver.wait(timeout=5)
      ...
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import asyncio
  import ydb
  import ydb.iam

  async def ydb_init():
      async with ydb.aio.Driver(
          endpoint=os.environ["YDB_ENDPOINT"],
          database=os.environ["YDB_DATABASE"],
          # service account key should be in the local file,
          # and SA_KEY_FILE environment variable should point to it
          credentials=ydb.iam.ServiceAccountCredentials.from_file(os.environ["SA_KEY_FILE"]),
      ) as driver:
          await driver.wait()
          ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import os
  import sqlalchemy as sa
  import ydb.iam

  engine = sa.create_engine(
      "yql+ydb://localhost:2136/local",
      connect_args={
          "credentials": ydb.iam.ServiceAccountCredentials.from_file(
              os.environ["YDB_SERVICE_ACCOUNT_KEY_FILE_CREDENTIALS"]
          )
      }
  )
  with engine.connect() as connection:
      result = connection.execute(sa.text("SELECT 1"))
  ```

- C#

  ```C#
  using Ydb.Sdk.Ado;

  await using var dataSource = new YdbDataSource(
      "Host=ydb.serverless.yandexcloud.net;Port=2135;Database=/ru-central1/<folder-id>/<database-id>;ServiceAccountKeyFilePath=path/to/sa_file.json");
  await using var connection = await dataSource.OpenConnectionAsync();
  ```

  Для Entity Framework и linq2db используйте тот же connectionString.

- Rust

  ```rust
  use ydb::{ClientBuilder, ServiceAccountCredentials, YdbResult};

  let client = ClientBuilder::new_from_connection_string(std::env::var("YDB_CONNECTION_STRING")?)?
      .with_credentials(ServiceAccountCredentials::from_env()?)
      .client()?;
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\JwtWithJsonAuthentication;

  $config = [
      'database'    => '/ru-central1/b1glxxxxxxxxxxxxxxxx/etn0xxxxxxxxxxxxxxxx',
      'endpoint'    => 'ydb.serverless.yandexcloud.net:2135',
      'discovery'   => false,
      'iam_config'  => [
          'temp_dir'       => './tmp', // Temp directory
          // 'root_cert_file' => './CA.pem', // Root CA file (uncomment for dedicated server)ы
      ],

      'credentials' => new JwtWithJsonAuthentication('./jwtjson.json')
  ];

  $ydb = new Ydb($config);
  ```

  или

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\JwtWithPrivateKeyAuthentication;

  $config = [
      'database'    => '/ru-central1/b1glxxxxxxxxxxxxxxxx/etn0xxxxxxxxxxxxxxxx',
      'endpoint'    => 'ydb.serverless.yandexcloud.net:2135',
      'discovery'   => false,
      'iam_config'  => [
          'temp_dir'           => './tmp', // Temp directory
          // 'root_cert_file' => './CA.pem', // Root CA file (uncomment for dedicated server)

      ],

      'credentials' => new JwtWithPrivateKeyAuthentication(
          "ajexxxxxxxxx","ajeyyyyyyyyy",'./private.key')

  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
