---
title: "Установка SDK"
url: "https://ydb.tech/docs/ru/reference/ydb-sdk/install?version=v26.1"
doc_path: "ru/reference/ydb-sdk/install"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-sdk/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-sdk/install.md"
description: "Установка SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Установка SDK

Ниже приведены инструкции по быстрой установке SDK. На рабочей станции должны быть предварительно установлены и сконфигурированы инструменты по работе с выбранным языком программирования, а также пакетные менеджеры.

Описание порядка сборки из исходного кода размещено в репозиториях исходного кода на GitHub, ссылки на которые приведены на странице [YDB SDK - Обзор](index.md).

{% list tabs %}

- Go

  Выполните команду из командной строки:

  ```bash
  go get -u github.com/ydb-platform/ydb-go-sdk/v3
  ```

  Для успешной установки в вашем окружении должен быть установлен [Go](https://go.dev/doc/install) версии не ниже 1.17.

- Java

  Добавьте зависимости в Maven-проект, как описано в пункте ["Install the SDK"](https://github.com/ydb-platform/ydb-java-sdk#install-the-sdk) файла `readme.md` в репозитории исходного кода.

- Python

  Выполните команду из командной строки:

  ```bash
  python3 -m pip install ydb
  ```

  Если команда не выполнилась успешно, убедитесь, что в вашем окружении установлен [Python3](https://www.python.org/downloads/) версии 3.8 или более новой, со включенным пакетным менеджером [pip](https://pypi.org/project/pip/).

- С#

  ```bash
  dotnet add package Ydb.Sdk
  ```

- JavaScript

  ```bash
  npm install @ydbjs/core @ydbjs/query
  ```

  Минимальная поддерживаемая версия [Node.js®](https://nodejs.org/en/download) не ниже 20.19.

- Rust

  ```bash
  cargo add ydb
  ```

- C++

  ### Пакеты Debian (Ubuntu 24.04) {#pakety-debian-ubuntu-2404}

  Готовые `.deb`-пакеты для Ubuntu 24.04 (Noble), amd64 прикреплены к каждому [релизу на GitHub](https://github.com/ydb-platform/ydb-cpp-sdk/releases). Скачайте и установите их локально:

  ```bash
  # Замените <TAG> на тег релиза со страницы GitHub releases
  TAG=<TAG>
  BASE="https://github.com/ydb-platform/ydb-cpp-sdk/releases/download/${TAG}"

  wget "${BASE}/yandex-googleapis-api-common-protos-1.0.0-Linux.deb"
  wget "${BASE}/libydb-cpp-dev_${TAG#v}_amd64.deb"
  # Дополнительные плагины:
  wget "${BASE}/libydb-cpp-iam-dev_${TAG#v}_amd64.deb"
  wget "${BASE}/libydb-cpp-otel-metrics-dev_${TAG#v}_amd64.deb"
  wget "${BASE}/libydb-cpp-otel-tracing-dev_${TAG#v}_amd64.deb"

  sudo apt-get update
  sudo apt-get install -y \
      ./yandex-googleapis-api-common-protos-*.deb \
      ./libydb-cpp-dev_*.deb ./libydb-cpp-iam-dev_*.deb \
      ./libydb-cpp-otel-metrics-dev_*.deb ./libydb-cpp-otel-tracing-dev_*.deb
  ```

  Доступные пакеты:

  - `yandex-googleapis-api-common-protos` — обязательная зависимость protobuf;
  - `libydb-cpp-dev` — основной SDK: статическая библиотека, публичные заголовки и файлы CMake-пакета;
  - `libydb-cpp-iam-dev` — плагин IAM-аутентификации (опционально);
  - `libydb-cpp-otel-metrics-dev` — плагин метрик OpenTelemetry (опционально);
  - `libydb-cpp-otel-tracing-dev` — плагин трассировки OpenTelemetry (опционально; для заголовков и библиотек OTel требуется `libydb-cpp-otel-metrics-dev`).

  > [!NOTE]
  > - Поддерживаемая платформа: Ubuntu 24.04 (Noble), amd64.
  > - Пакеты собраны без apt-зависимостей; установите `yandex-googleapis-api-common-protos` вместе с основным пакетом SDK.
  > - Для других платформ используйте инструкции по сборке из исходного кода ниже.

  ### Использование SDK в CMake {#ispolzovanie-sdk-v-cmake}

  После установки пакетов подключите SDK в CMake-проекте:

  ```cmake
  find_package(ydb-cpp-sdk REQUIRED COMPONENTS Driver Table Topic)
  target_link_libraries(myapp PRIVATE YDB-CPP-SDK::Driver YDB-CPP-SDK::Table)
  ```

  При конфигурации проекта передайте `-DCMAKE_PREFIX_PATH=/usr/share/yandex`, так как пакеты устанавливаются в префикс Yandex.

  ### Сборка из исходного кода {#sborka-iz-ishodnogo-koda}

  Склонируйте репозиторий [ydb-cpp-sdk](https://github.com/ydb-platform/ydb-cpp-sdk) и выполните команду из командной строки:

  ```bash
  cmake --preset release-${compiler} -D YDB_SDK_INSTALL=On
  cmake --build --preset default
  cmake --install build --prefix ${ydb_install_dir}
  ```

  - `compiler` — ваш компилятор (`clang` или `gcc`);
  - `ydb_install_dir` — путь, по которому вы хотите установить SDK.

  Перед выполнением команды убедитесь, что все зависимости установлены. Полный список зависимостей для сборки и инструкции см. в [README](https://github.com/ydb-platform/ydb-cpp-sdk/blob/main/README.md) репозитория.

- PHP

  ```bash
  composer require ydb-platform/ydb-php-sdk
  ```

{% endlist %}
