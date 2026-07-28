---
title: "Installing ydbops"
url: "https://ydb.tech/docs/en/reference/ydbops/install?version=v26.1"
doc_path: "en/reference/ydbops/install"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydbops/install.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydbops/install.md"
description: "Note. The ydbops utility is under active development. Although backward-incompatible changes are unlikely, they may still occur."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Installing ydbops

> [!NOTE]
> The `ydbops` utility is under active development. Although backward-incompatible changes are unlikely, they may still occur.

## Download the binary from the releases page

You can download binary releases from [Download YDB Ops](../../downloads/ydb-ops.md).

## Building from source

1. Clone the `ydbops` repository from GitHub:

   ```bash
   git clone https://github.com/ydb-platform/ydbops.git
   ```

2. There are two ways to build `ydbops`:

   1. [Directly with Go](install.md#go)
   2. [Inside a Docker container](install.md#docker)

The second approach requires a prepared [Docker](<https://en.wikipedia.org/wiki/Docker_(software)>) environment and uses the official Docker image for [Golang](<https://en.wikipedia.org/wiki/Go_(programming_language)>) [v1.22](https://hub.docker.com/_/golang/tags?name=1.22), guaranteeing a successful build. The Docker container operates using the `Dockerfile` from the repository. The build process in Docker also performs additional tasks: running linter checks and substituting the version for the `ydbops` assembly to register it in the executable file.

### Building directly with Go {#go}

#### Prerequsites

[Install Go](https://go.dev/doc/install). The recommended version is 1.22.

#### Compiling

Invoke `go build` in the repository root folder:

```bash
go build
```

The `ydbops` executable will be available in the repository root folder.

#### Installing

You can copy the executable file manually or use `make`:

```bash
make install INSTALL_DIR=install_folder BUILD_DIR=.
```

### Inside a Docker container {#docker}

#### Prerequsites {#prerequsites1}

- make
- [Install docker engine](https://docs.docker.com/engine/install/)

#### Compiling {#compiling1}

Invoke this command in the repository root folder:

```bash
make build-in-docker
```

The `ydbops` executables will be available in the `bin` folder. Binary files are generated for Linux and macOS (arm64, amd64).

| Binary name | Platform |
| --- | --- |
| ydbops | Linux (amd64) |
| ydbops_darwin_amd64 | macOS (amd64) |
| ydbops_darwin_arm64 | macOS (arm64) |

#### Installing {#installing1}

To install the binary file, execute the command `make`.

Optional parameters:

- `INSTALL_DIR`: The folder where the executable file will be installed. Default value: `~/ydb/bin`.
- `BUILD_DIR`: The folder that contains the generated executable file. Use this parameter if you created the executable file manually. For example, use `BUILD_DIR=.` if the executable file is in the current working directory.

```bash
make install [INSTALL_DIR=<path_to_install_folder>] [BUILD_DIR=<path_to_build_folder>]
```

Sample command to install into `install_folder` from the current folder:

```bash
make install INSTALL_DIR=install_folder BUILD_DIR=.
```
