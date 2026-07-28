---
title: "Prefer a specific availability zone"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/balancing-prefer-location?version=v26.1"
doc_path: "en/recipes/ydb-sdk/balancing-prefer-location"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/balancing-prefer-location.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/balancing-prefer-location.md"
description: "Below are examples of setting the \"prefer availability zone\" balancing algorithm in different YDB SDKs. Go. C++. Python. JavaScript. Java. Rust. Native SDK."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Prefer a specific availability zone

Below are examples of setting the "prefer availability zone" balancing algorithm in different YDB SDKs.

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

    Client-side balancing in the YDB `database/sql` driver happens only when opening a new connection (in `database/sql` terms), which maps to a YDB session on a specific node. After the session is created, all queries on that session go to that node. Queries on the same YDB session are not balanced across nodes.

    Example for "prefer availability zone" balancing:

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

  Client-side balancing in the YDB `database/sql` driver happens only when opening a new connection (in `database/sql` terms), which maps to a YDB session on a specific node. After the session is created, all queries on that session go to that node. Queries on the same YDB session are not balanced across nodes.

  Example for "prefer availability zone" balancing:

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

- C++

  The C++ SDK lets you pick only one availability zone as preferred.

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

- Python

  This functionality is not currently supported.

- JavaScript

  This section is under development.

- Java

  In the **Java SDK**, availability zone preference is set on the gRPC transport.

  {% list tabs %}

  - Native SDK

    ```java
    import tech.ydb.core.grpc.BalancingSettings;
    import tech.ydb.core.grpc.GrpcTransport;

    try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
            .withBalancingSettings(BalancingSettings.fromLocation("a")) // preferred availability zone
            .build()) {
        // ...
    }
    ```

  - JDBC

    See supported availability-zone parameters in [JDBC driver properties](../../reference/languages-and-apis/jdbc-driver/properties.md), or configure balancing through the native API when embedding the driver.

    In Spring Boot, ORMs, and other JDBC wrappers, pass the same JDBC URL and zone parameters as for a direct connection (for example in `spring.datasource.url` or pool properties).

  {% endlist %}

- Native SDK

  ```java
  import tech.ydb.core.grpc.BalancingSettings;
  import tech.ydb.core.grpc.GrpcTransport;

  try (GrpcTransport transport = GrpcTransport.forConnectionString("grpc://localhost:2136/local")
          .withBalancingSettings(BalancingSettings.fromLocation("a")) // preferred availability zone
          .build()) {
      // ...
  }
  ```

- JDBC

  See supported availability-zone parameters in [JDBC driver properties](../../reference/languages-and-apis/jdbc-driver/properties.md), or configure balancing through the native API when embedding the driver.

  In Spring Boot, ORMs, and other JDBC wrappers, pass the same JDBC URL and zone parameters as for a direct connection (for example in `spring.datasource.url` or pool properties).

- Rust

  This functionality is not currently supported.

  Track progress or vote for Rust SDK support: [ydb-rs-sdk#238](https://github.com/ydb-platform/ydb-rs-sdk/issues/238)

{% endlist %}
