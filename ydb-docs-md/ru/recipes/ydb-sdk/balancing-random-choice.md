---
title: "Равномерный случайный выбор"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/balancing-random-choice?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/balancing-random-choice"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/balancing-random-choice.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/balancing-random-choice.md"
description: "YDB SDK использует алгоритм random_choice (равномерную случайную балансировку) по умолчанию, кроме С++ SDK, который использует алгоритм \"предпочитать ближайший"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Равномерный случайный выбор

YDB SDK использует алгоритм `random_choice` (равномерную случайную балансировку) по умолчанию, кроме С++ SDK, который использует алгоритм ["предпочитать ближайший дата-центр"](balancing-prefer-local.md) по умолчанию.

Ниже приведены примеры кода принудительной установки алгоритма балансировки "равномерный случайный выбор" в разных YDB SDK.

{% list tabs %}

- C++

  {% list tabs %}

  - Native SDK

    ```cpp
    #include <ydb-cpp-sdk/client/driver/driver.h>

    int main() {
      auto connectionString = std::string(std::getenv("YDB_CONNECTION_STRING"));

      auto driverConfig = NYdb::TDriverConfig(connectionString)
        .SetBalancingPolicy(NYdb::TBalancingPolicy::UseAllNodes());

      NYdb::TDriver driver(driverConfig);
      // ...
      driver.Stop(true);
      return 0;
    }
    ```

  - userver

    <details>
    <summary>static config</summary>

    ```yaml
    ydb:
        databases:
            db:
                endpoint: grpc://localhost:2136
                database: /local
                prefer_local_dc: false
    ```

    </details>

    Код инициализации `ydb::YdbComponent`, получения `ydb::TableClient` и запуска `components::MinimalServerComponentList` — как в примере из [init.md](init.md).

  {% endlist %}

- Native SDK

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>

  int main() {
    auto connectionString = std::string(std::getenv("YDB_CONNECTION_STRING"));

    auto driverConfig = NYdb::TDriverConfig(connectionString)
      .SetBalancingPolicy(NYdb::TBalancingPolicy::UseAllNodes());

    NYdb::TDriver driver(driverConfig);
    // ...
    driver.Stop(true);
    return 0;
  }
  ```

- userver

  <details>
  <summary>static config</summary>

  ```yaml
  ydb:
      databases:
          db:
              endpoint: grpc://localhost:2136
              database: /local
              prefer_local_dc: false
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
      "github.com/ydb-platform/ydb-go-sdk/v3/balancers"
    )

    func main() {
      ctx, cancel := context.WithCancel(context.Background())
      defer cancel()
      db, err := ydb.Open(ctx,
        os.Getenv("YDB_CONNECTION_STRING"),
        ydb.WithBalancer(
          balancers.RandomChoice(),
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

    Пример кода установки алгоритма балансировки "равномерный случайный выбор":

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
          balancers.RandomChoice(),
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
        balancers.RandomChoice(),
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

  Пример кода установки алгоритма балансировки "равномерный случайный выбор":

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
        balancers.RandomChoice(),
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

  {% list tabs %}

  - Native SDK

    ```python
    import os
    import ydb

    driver_config = ydb.DriverConfig(
        endpoint=os.environ["YDB_ENDPOINT"],
        database=os.environ["YDB_DATABASE"],
        credentials=ydb.credentials_from_env_variables(),
        use_all_nodes=True,  # равномерный случайный выбор
    )

    with ydb.Driver(driver_config) as driver:
        driver.wait(timeout=5)
        # ...
    ```

  - Native SDK (Asyncio)

    ```python
    import os
    import ydb
    import asyncio

    async def ydb_init():
        driver_config = ydb.DriverConfig(
            endpoint=os.environ["YDB_ENDPOINT"],
            database=os.environ["YDB_DATABASE"],
            credentials=ydb.credentials_from_env_variables(),
            use_all_nodes=True,  # равномерный случайный выбор
        )
        async with ydb.aio.Driver(driver_config) as driver:
            await driver.wait()
            # ...

    asyncio.run(ydb_init())
    ```

  - SQLAlchemy

    ```python
    import os
    import sqlalchemy as sa

    engine = sa.create_engine(
        os.environ["YDB_SQLALCHEMY_URL"],
        connect_args={
            "driver_config_kwargs": {
                "use_all_nodes": True,  # равномерный случайный выбор
            }
        },
    )
    ```

  {% endlist %}

- Native SDK

  ```python
  import os
  import ydb

  driver_config = ydb.DriverConfig(
      endpoint=os.environ["YDB_ENDPOINT"],
      database=os.environ["YDB_DATABASE"],
      credentials=ydb.credentials_from_env_variables(),
      use_all_nodes=True,  # равномерный случайный выбор
  )

  with ydb.Driver(driver_config) as driver:
      driver.wait(timeout=5)
      # ...
  ```

- Native SDK (Asyncio)

  ```python
  import os
  import ydb
  import asyncio

  async def ydb_init():
      driver_config = ydb.DriverConfig(
          endpoint=os.environ["YDB_ENDPOINT"],
          database=os.environ["YDB_DATABASE"],
          credentials=ydb.credentials_from_env_variables(),
          use_all_nodes=True,  # равномерный случайный выбор
      )
      async with ydb.aio.Driver(driver_config) as driver:
          await driver.wait()
          # ...

  asyncio.run(ydb_init())
  ```

- SQLAlchemy

  ```python
  import os
  import sqlalchemy as sa

  engine = sa.create_engine(
      os.environ["YDB_SQLALCHEMY_URL"],
      connect_args={
          "driver_config_kwargs": {
              "use_all_nodes": True,  # равномерный случайный выбор
          }
      },
  )
  ```

- C#

  Этот алгоритм используется по умолчанию.

- JavaScript

  Функциональность на данный момент не поддерживается.

- Java

  {% list tabs %}

  - Native SDK

    Алгоритм «равномерный случайный выбор» в Java SDK задаётся политикой `USE_ALL_NODES` в `BalancingSettings` (это поведение по умолчанию, если настройки не переопределять).

    ```java
    import tech.ydb.core.grpc.BalancingSettings;
    import tech.ydb.core.grpc.GrpcTransport;

    try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
            .withBalancingSettings(BalancingSettings.fromPolicy(BalancingSettings.Policy.USE_ALL_NODES))
            .build()) {
        // ...
    }
    ```

  - JDBC

    Балансировка при выборе новой сессии задаётся на стороне нативного транспорта внутри драйвера; при необходимости используйте те же параметры, что и в нативном SDK, через [настройки подключения JDBC](../../reference/languages-and-apis/jdbc-driver/properties.md).

    В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения и параметры балансировки, что и при прямом использовании драйвера (например, `spring.datasource.url` с нужными query-параметрами или свойства `DataSource`).

  {% endlist %}

- Native SDK

  Алгоритм «равномерный случайный выбор» в Java SDK задаётся политикой `USE_ALL_NODES` в `BalancingSettings` (это поведение по умолчанию, если настройки не переопределять).

  ```java
  import tech.ydb.core.grpc.BalancingSettings;
  import tech.ydb.core.grpc.GrpcTransport;

  try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
          .withBalancingSettings(BalancingSettings.fromPolicy(BalancingSettings.Policy.USE_ALL_NODES))
          .build()) {
      // ...
  }
  ```

- JDBC

  Балансировка при выборе новой сессии задаётся на стороне нативного транспорта внутри драйвера; при необходимости используйте те же параметры, что и в нативном SDK, через [настройки подключения JDBC](../../reference/languages-and-apis/jdbc-driver/properties.md).

  В Spring Boot, ORM и прочих сторонних фреймворках вокруг JDBC укажите ту же JDBC-строку подключения и параметры балансировки, что и при прямом использовании драйвера (например, `spring.datasource.url` с нужными query-параметрами или свойства `DataSource`).

- Rust

  Политика RandomChoice (случайный выбор endpoint среди нод discovery) используется **по умолчанию** — дополнительная настройка не требуется.

- PHP

  Функциональность на данный момент не поддерживается.

{% endlist %}
