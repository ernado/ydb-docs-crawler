---
title: "Предпочитать конкретную зону доступности"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/balancing-prefer-location?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/balancing-prefer-location"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/balancing-prefer-location.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/balancing-prefer-location.md"
description: "Ниже приведены примеры кода установки опции алгоритма балансировки \"предпочитать зону доступности\" в разных YDB SDK. С++. Go. Python. C#. JavaScript. Java."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Предпочитать конкретную зону доступности

Ниже приведены примеры кода установки опции алгоритма балансировки "предпочитать зону доступности" в разных YDB SDK.

{% list tabs %}

- С++

  {% list tabs %}

  - Native SDK

    В C++ SDK можно выбрать только одну зону доступности в качестве предпочитаемой.

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>

    int main() {
      auto connectionString = std::string(std::getenv("YDB_CONNECTION_STRING"));

      auto driverConfig = NYdb::TDriverConfig(connectionString)
        .SetBalancingPolicy(NYdb::TBalancingPolicy::UsePreferableLocation("datacenter1"));

      NYdb::TDriver driver(driverConfig);
      // ...
      driver.Stop(true);
      return 0;
    }
    ```

  - userver

    Функциональность на данный момент не поддерживается.

  {% endlist %}

- Native SDK

  В C++ SDK можно выбрать только одну зону доступности в качестве предпочитаемой.

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>

  int main() {
    auto connectionString = std::string(std::getenv("YDB_CONNECTION_STRING"));

    auto driverConfig = NYdb::TDriverConfig(connectionString)
      .SetBalancingPolicy(NYdb::TBalancingPolicy::UsePreferableLocation("datacenter1"));

    NYdb::TDriver driver(driverConfig);
    // ...
    driver.Stop(true);
    return 0;
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

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/balancers"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithBalancer(
          balancers.PreferLocations(
            balancers.RandomChoice(),
            "a",
            "b",
          ),
        ),
      )
      if err != nil {
        panic(err)
      }
      defer db.Close(ctx)
      // ...
    }
    ```

  - database/sql

    Клиентская балансировка в `database/sql` драйвере для YDB осуществляется только в момент установления нового соединения (в терминах `database/sql`), которое представляет собой сессию YDB на конкретной ноде. После того, как сессия создана, все запросы на этой сессии направляются на ту ноду, на которой была создана сессия. Балансировка запросов на одной и той же сессии YDB между разными нодами YDB не происходит.

    Пример кода установки алгоритма балансировки "предпочитать зону доступности":

    ```go
    package main

    import (
      "context"
      "database/sql"
      "os"

      "github.com/ydb-platform/ydb-go-sdk/v3"
      "github.com/ydb-platform/ydb-go-sdk/v3/balancers"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      nativeDriver, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithBalancer(
          balancers.PreferLocations(
            balancers.RandomChoice(),
            "a",
            "b",
          ),
        ),
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
      // ...
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
    "github.com/ydb-platform/ydb-go-sdk/v3/balancers"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    db, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydb.WithBalancer(
        balancers.PreferLocations(
          balancers.RandomChoice(),
          "a",
          "b",
        ),
      ),
    )
    if err != nil {
      panic(err)
    }
    defer db.Close(ctx)
    // ...
  }
  ```

- database/sql

  Клиентская балансировка в `database/sql` драйвере для YDB осуществляется только в момент установления нового соединения (в терминах `database/sql`), которое представляет собой сессию YDB на конкретной ноде. После того, как сессия создана, все запросы на этой сессии направляются на ту ноду, на которой была создана сессия. Балансировка запросов на одной и той же сессии YDB между разными нодами YDB не происходит.

  Пример кода установки алгоритма балансировки "предпочитать зону доступности":

  ```go
  package main

  import (
    "context"
    "database/sql"
    "os"

    "github.com/ydb-platform/ydb-go-sdk/v3"
    "github.com/ydb-platform/ydb-go-sdk/v3/balancers"
  )

  func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    nativeDriver, err := ydb.Open(ctx,
      os.Getenv("YDB_CONNECTION_STRING"),
      ydb.WithBalancer(
        balancers.PreferLocations(
          balancers.RandomChoice(),
          "a",
          "b",
        ),
      ),
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
    // ...
  }
  ```

- Python

  Функциональность на данный момент не поддерживается.

- C#

  Функциональность на данный момент не поддерживается.

- JavaScript

  Функциональность на данный момент не поддерживается.

- Java

  В **Java SDK** предпочтение зоны доступности задаётся в настройках gRPC-транспорта.

  {% list tabs %}

  - Native SDK

    ```java
    import tech.ydb.core.grpc.BalancingSettings;
    import tech.ydb.core.grpc.GrpcTransport;

    try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
            .withBalancingSettings(BalancingSettings.fromLocation("a")) // предпочитаемая зона доступности
            .build()) {
        // ...
    }
    ```

  - JDBC

    Уточните поддерживаемые параметры зоны доступности в [свойствах JDBC-драйвера](../../reference/languages-and-apis/jdbc-driver/properties.md) или задайте балансировку через нативный API при встраивании драйвера.

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC передайте те же JDBC URL и параметры зоны доступности, что и при прямом подключении (например, в `spring.datasource.url` или свойствах пула).

  {% endlist %}

- Native SDK

  ```java
  import tech.ydb.core.grpc.BalancingSettings;
  import tech.ydb.core.grpc.GrpcTransport;

  try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
          .withBalancingSettings(BalancingSettings.fromLocation("a")) // предпочитаемая зона доступности
          .build()) {
      // ...
  }
  ```

- JDBC

  Уточните поддерживаемые параметры зоны доступности в [свойствах JDBC-драйвера](../../reference/languages-and-apis/jdbc-driver/properties.md) или задайте балансировку через нативный API при встраивании драйвера.

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC передайте те же JDBC URL и параметры зоны доступности, что и при прямом подключении (например, в `spring.datasource.url` или свойствах пула).

- Rust

  Функциональность на данный момент не поддерживается.

  Отслеживать прогресс или проголосовать за поддержку в Rust SDK: [ydb-rs-sdk#238](https://github.com/ydb-platform/ydb-rs-sdk/issues/238)

- PHP

  Функциональность на данный момент не поддерживается.

{% endlist %}
