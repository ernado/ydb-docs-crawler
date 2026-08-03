---
title: "Prefer a pile with a specific state"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/balancing-prefer-pile?version=v26.1"
doc_path: "en/recipes/ydb-sdk/balancing-prefer-pile"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/balancing-prefer-pile.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/balancing-prefer-pile.md"
description: "Below is example of the code for setting the \"prefer pile with a specific state\" balancing algorithm in YDB SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Prefer a pile with a specific state

Below is example of the code for setting the "prefer pile with a specific state" balancing algorithm in YDB SDK.

If no state is specified when setting the option, the SDK prefers the PRIMARY pile.

This option only makes sense if the cluster is operating in bridge mode. If it is not, the SDK will use [random choice balancing algorithm](balancing-random-choice.md).

{% list tabs %}

- Go

  This functionality is not currently supported.

- C++

  ```cpp
  #include <ydb-cpp-sdk/client/driver/driver.h>

  int main() {
    auto connectionString = std::string(std::getenv("YDB_CONNECTION_STRING"));

    auto driverConfig = NYdb::TDriverConfig(connectionString)
      .SetBalancingPolicy(NYdb::TBalancingPolicy::UsePreferablePileState(NYdb::EPileState::PRIMARY));

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

  This functionality is not currently supported.

- Rust

  This functionality is not currently supported.

  Track progress or vote for Rust SDK support: [ydb-rs-sdk#491](https://github.com/ydb-platform/ydb-rs-sdk/issues/491)

{% endlist %}
