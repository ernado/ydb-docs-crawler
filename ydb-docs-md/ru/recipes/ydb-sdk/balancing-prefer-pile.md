---
title: "Предпочитать пайл c конкретным состоянием"
url: "https://ydb.tech/docs/ru/recipes/ydb-sdk/balancing-prefer-pile?version=v26.1"
doc_path: "ru/recipes/ydb-sdk/balancing-prefer-pile"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-sdk/balancing-prefer-pile.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-sdk/balancing-prefer-pile.md"
description: "Ниже приведен пример кода установки опции алгоритма балансировки \"предпочитать пайл c конкретным состоянием \" в YDB SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Предпочитать пайл c конкретным состоянием

Ниже приведен пример кода установки опции алгоритма балансировки "предпочитать [пайл](../../concepts/glossary.md#pile) c конкретным [состоянием](../../concepts/bridge.md#pile-states)" в YDB SDK.

Если при установке опции состояние не задано, SDK предпочитает PRIMARY [пайл](../../concepts/glossary.md#pile).

Данная опция имеет смысл, только если кластер находится в [bridge режиме](../../concepts/bridge.md). Если это неверно, SDK будет использовать [равномерную случайную балансировку](balancing-random-choice.md).

{% list tabs %}

- С++

  {% list tabs %}

  - Native SDK

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

  - userver

    Функциональность на данный момент не поддерживается.

  {% endlist %}

- Native SDK

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

- userver

  Функциональность на данный момент не поддерживается.

- Go

  Функциональность на данный момент не поддерживается.

- Python

  Функциональность на данный момент не поддерживается.

- C#

  Функциональность на данный момент не поддерживается.

- JavaScript

  Функциональность на данный момент не поддерживается.

- Java

  Функциональность на данный момент не поддерживается.

- Rust

  Функциональность на данный момент не поддерживается.

  Отслеживать прогресс или проголосовать за поддержку в Rust SDK: [ydb-rs-sdk#491](https://github.com/ydb-platform/ydb-rs-sdk/issues/491)

- PHP

  Функциональность на данный момент не поддерживается.

{% endlist %}
