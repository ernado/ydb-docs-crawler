---
title: "Authentication using the metadata service"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/auth-metadata?version=v26.1"
doc_path: "en/recipes/ydb-sdk/auth-metadata"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/auth-metadata.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/auth-metadata.md"
description: "Below are examples of authentication with the metadata service in different YDB SDKs. Go. Java. JavaScript. Python. C# (.NET). PHP. Native SDK. database/sql."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Authentication using the metadata service

Below are examples of authentication with the metadata service in different YDB SDKs.

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
      yc "github.com/ydb-platform/ydb-go-yc-metadata"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        yc.WithCredentials(),
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
      yc "github.com/ydb-platform/ydb-go-yc-metadata"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        yc.WithCredentials(),
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
    yc "github.com/ydb-platform/ydb-go-yc-metadata"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      yc.WithCredentials(),
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
    yc "github.com/ydb-platform/ydb-go-yc-metadata"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      yc.WithCredentials(),
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
    public void work(String connectionString) {
        AuthProvider authProvider = CloudAuthHelper.getMetadataAuthProvider();

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
        props.setProperty("useMetadata", "true");
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
            doWork(connection);
        }

        // You can also set useMetadata in the JDBC URL
        try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local?useMetadata=true")) {
            doWork(connection);
        }
    }
    ```

    In Spring Boot, ORMs, and other JDBC wrappers, pass the same JDBC URLs and parameters (`useMetadata` in the URL or in the data source properties) as in the example above.

  {% endlist %}

- Native SDK

  ```java
  public void work(String connectionString) {
      AuthProvider authProvider = CloudAuthHelper.getMetadataAuthProvider();

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
      props.setProperty("useMetadata", "true");
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local", props)) {
          doWork(connection);
      }

      // You can also set useMetadata in the JDBC URL
      try (Connection connection = DriverManager.getConnection("jdbc:ydb:grpc://localhost:2136/local?useMetadata=true")) {
          doWork(connection);
      }
  }
  ```

  In Spring Boot, ORMs, and other JDBC wrappers, pass the same JDBC URLs and parameters (`useMetadata` in the URL or in the data source properties) as in the example above.

- JavaScript

  ```typescript
  import { Driver } from "@ydbjs/core";
  import { MetadataCredentialsProvider } from "@ydbjs/auth/metadata";

  const driver = new Driver("grpc://localhost:2136/local", {
    credentialsProvider: new MetadataCredentialsProvider(),
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
        credentials=ydb.iam.MetadataUrlCredentials(),
    ) as driver:
        driver.wait(timeout=5)
        ...
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import ydb
    import ydb.iam
    import asyncio

    async def ydb_init():
        async with ydb.aio.Driver(
            endpoint=os.environ["YDB_ENDPOINT"],
            database=os.environ["YDB_DATABASE"],
            credentials=ydb.iam.MetadataUrlCredentials(),
        ) as driver:
            await driver.wait()
            ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import sqlalchemy as sa
    import ydb.iam

    engine = sa.create_engine(
        "yql+ydb://localhost:2136/local",
        connect_args={
            "credentials": ydb.iam.MetadataUrlCredentials()
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
      credentials=ydb.iam.MetadataUrlCredentials(),
  ) as driver:
      driver.wait(timeout=5)
      ...
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import ydb
  import ydb.iam
  import asyncio

  async def ydb_init():
      async with ydb.aio.Driver(
          endpoint=os.environ["YDB_ENDPOINT"],
          database=os.environ["YDB_DATABASE"],
          credentials=ydb.iam.MetadataUrlCredentials(),
      ) as driver:
          await driver.wait()
          ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import sqlalchemy as sa
  import ydb.iam

  engine = sa.create_engine(
      "yql+ydb://localhost:2136/local",
      connect_args={
          "credentials": ydb.iam.MetadataUrlCredentials()
      }
  )
  with engine.connect() as connection:
      result = connection.execute(sa.text("SELECT 1"))
  ```

- C# (.NET)

  ```C#
  using Ydb.Sdk;
  using Ydb.Sdk.Yc;

  var metadataProvider = new MetadataProvider();

  // Await initial IAM token.
  await metadataProvider.Initialize();

  var config = new DriverConfig(
      endpoint: endpoint, // Database endpoint, "grpcs://host:port"
      database: database, // Full database path
      credentials: metadataProvider
  );

  await using var driver = await Driver.CreateInitialized(config);
  ```

- PHP

  ```php
  <?php

  use YdbPlatform\Ydb\Ydb;
  use YdbPlatform\Ydb\Auth\Implement\MetadataAuthentication;

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

      'credentials' => new MetadataAuthentication()
  ];

  $ydb = new Ydb($config);
  ```

{% endlist %}
