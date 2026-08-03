---
title: "Installing the YDB SDK"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/install?version=v26.1"
doc_path: "en/reference/ydb-sdk/install"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/install.md"
description: "Installing the YDB SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Installing the YDB SDK

Follow the instructions below to quickly install the OpenSource SDK. Make sure to preinstall and configure tools for working with the selected programming language and package managers on your workstation.

The build process using the source code is described in the source code repositories on GitHub. Follow the links given on the [YDB SDK - Overview](index.md) page.

{% list tabs %}

- Go

  Run the command from the command line:

  ```bash
  go get -u github.com/ydb-platform/ydb-go-sdk/v3
  ```

  To ensure that the installation is successful, make sure that your environment is running [Go](https://go.dev/doc/install) 1.17 or higher.

- Java

  Add dependencies to the Maven project as described in the ["Install the SDK"](https://github.com/ydb-platform/ydb-java-sdk#install-the-sdk) step of the `readme.md` file in the source code repository.

- Python

  Run the command from the command line:

  ```bash
  python3 -m pip install ydb
  ```

  If the command fails, make sure your environment has [Python](https://www.python.org/downloads/) 3.8 or newer installed with the [pip](https://pypi.org/project/pip/) package manager enabled.

- C# (.NET)

  ```bash
  dotnet add package Ydb.Sdk
  ```

- JavaScript

  ```bash
  npm install @ydbjs/core @ydbjs/query
  ```

  The minimum supported [Node.js®](https://nodejs.org/en/download) version is 20.19.

- Rust

  Add to Cargo.toml last version of [ydb](https://crates.io/crates/ydb) crate.

- C++

  ### Debian packages (Ubuntu 24.04)

  Pre-built `.deb` packages for Ubuntu 24.04 (Noble), amd64 are attached to each [GitHub release](https://github.com/ydb-platform/ydb-cpp-sdk/releases). Download and install them locally:

  ```bash
  # Replace <TAG> with a release tag from GitHub releases
  TAG=<TAG>
  BASE="https://github.com/ydb-platform/ydb-cpp-sdk/releases/download/${TAG}"

  wget "${BASE}/yandex-googleapis-api-common-protos-1.0.0-Linux.deb"
  wget "${BASE}/libydb-cpp-dev_${TAG#v}_amd64.deb"
  # Optional plugins:
  wget "${BASE}/libydb-cpp-iam-dev_${TAG#v}_amd64.deb"
  wget "${BASE}/libydb-cpp-otel-metrics-dev_${TAG#v}_amd64.deb"
  wget "${BASE}/libydb-cpp-otel-tracing-dev_${TAG#v}_amd64.deb"

  sudo apt-get update
  sudo apt-get install -y \
      ./yandex-googleapis-api-common-protos-*.deb \
      ./libydb-cpp-dev_*.deb ./libydb-cpp-iam-dev_*.deb \
      ./libydb-cpp-otel-metrics-dev_*.deb ./libydb-cpp-otel-tracing-dev_*.deb
  ```

  Available packages:

  - `yandex-googleapis-api-common-protos` — required protobuf dependency;
  - `libydb-cpp-dev` — core SDK: static library, public headers, and CMake package files;
  - `libydb-cpp-iam-dev` — IAM credentials plugin (optional);
  - `libydb-cpp-otel-metrics-dev` — OpenTelemetry metrics plugin (optional);
  - `libydb-cpp-otel-tracing-dev` — OpenTelemetry tracing plugin (optional; requires `libydb-cpp-otel-metrics-dev` for OTel headers and libraries).

  > [!NOTE]
  > - Supported platform: Ubuntu 24.04 (Noble), amd64.
  > - The `.deb` packages do not declare apt dependencies on each other; install `yandex-googleapis-api-common-protos` together with the core SDK package.
  > - For other platforms, use the build-from-source instructions below.

  ### Using the SDK in CMake

  After installing the packages, use the SDK in your CMake project:

  ```cmake
  find_package(ydb-cpp-sdk REQUIRED COMPONENTS Driver Table Topic)
  target_link_libraries(myapp PRIVATE YDB-CPP-SDK::Driver YDB-CPP-SDK::Table)
  ```

  Pass `-DCMAKE_PREFIX_PATH=/usr/share/yandex` when configuring your project, since the packages install under the Yandex prefix.

  ### Build from source

  Clone the [ydb-cpp-sdk](https://github.com/ydb-platform/ydb-cpp-sdk) repository and run the following commands from the command line:

  ```bash
  cmake --preset release-${compiler} -D YDB_SDK_INSTALL=On
  cmake --build --preset default
  cmake --install build --prefix ${ydb_install_dir}
  ```

  - `compiler` — your compiler (`clang` or `gcc`);
  - `ydb_install_dir` — the path where you want to install the SDK.

  Make sure all dependencies are installed before running the commands. See the [README](https://github.com/ydb-platform/ydb-cpp-sdk/blob/main/README.md) in the source repository for the full list of build dependencies and instructions.

- PHP

  ```bash
  composer require ydb-platform/ydb-php-sdk
  ```

{% endlist %}
