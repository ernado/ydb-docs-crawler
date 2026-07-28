---
title: "YDB Model Context Protocol Server"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/mcp/?version=v26.1"
doc_path: "en/reference/languages-and-apis/mcp/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/mcp/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/mcp/index.md"
description: "YDB Model Context Protocol (MCP) server allows you to work with YDB databases from any Large Language Model (LLM) that supports MCP using any of the MCP clients"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# YDB Model Context Protocol Server

[YDB Model Context Protocol (MCP) server](https://github.com/ydb-platform/ydb-mcp) allows you to work with YDB databases from any [Large Language Model (LLM)](https://en.wikipedia.org/wiki/Large_language_model) that supports [MCP](https://modelcontextprotocol.io/introduction) using any of the [MCP clients](https://modelcontextprotocol.io/clients). This integration enables AI-powered database operations and natural language interactions with your YDB instances.

## Getting Started

### Prerequisites

1. Install an [MCP client](https://modelcontextprotocol.io/clients) that supports MCP tools (most do). The configuration examples below use a common format supported by several popular MCP clients (Claude Desktop, Cursor, etc.), but you may need to adjust the format to meet your client's requirements.
2. The YDB MCP server is a Python application that is typically co-hosted with the MCP client. There are several options for installing and running the YDB MCP server [explained below](index.md#server-arguments), but all of them require a pre-installed Python 3.10+ environment.

### Anonymous Authentication

{% list tabs %}

- uvx

  [uvx](https://docs.astral.sh/uv/guides/tools/) allows you to run Python applications without explicitly installing them.

  Configure YDB MCP in your MCP client settings:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "uvx",
        "args": [
          "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

- pipx

  [pipx](https://pipx.pypa.io/stable/installation/) allows you to run applications from PyPI without explicit installation (pipx itself must be installed first).

  Configure YDB MCP in your MCP client settings:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "pipx",
        "args": [
          "run", "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

- pip

  Optionally, create and activate a [Python virtual environment](https://docs.python.org/3/library/venv.html). Install YDB MCP using [pip](https://pypi.org/project/pip/):

  ```bash
  pip install ydb-mcp
  ```

  Configure YDB MCP in your MCP client settings:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "python3",
        "args": [
          "-m", "ydb_mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local"
        ]
      }
    }
  }
  ```

{% endlist %}

## Login-Password Authentication

{% list tabs %}

- uvx

  Configure login/password authentication with `uvx`:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "uvx",
        "args": [
          "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<your-username>",
          "--ydb-password", "<your-password>"
        ]
      }
    }
  }
  ```

- pipx

  Configure login/password authentication with `pipx`:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "pipx",
        "args": [
          "run", "ydb-mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<your-username>",
          "--ydb-password", "<your-password>"
        ]
      }
    }
  }
  ```

- pip

  Configure login/password authentication with `pip`-installed YDB MCP:

  ```json
  {
    "mcpServers": {
      "ydb": {
        "command": "python3",
        "args": [
          "-m", "ydb_mcp",
          "--ydb-endpoint", "grpc://localhost:2136/local",
          "--ydb-auth-mode", "login-password",
          "--ydb-login", "<your-username>",
          "--ydb-password", "<your-password>"
        ]
      }
    }
  }
  ```

{% endlist %}

### Run Queries

Ask your LLM questions regarding the data stored in YDB using the MCP client configured above. The language model will see the tools available to it via MCP and will use them to execute [YQL](../../../yql/reference/index.md) queries and other YDB API calls. An example of how it might look:

![Example usage of YDB MCP server](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/languages-and-apis/mcp/_assets/example-usage.png)

## Available Tools

YDB MCP provides the following tools for interacting with YDB databases:

- `ydb_query`: Run a SQL query against a YDB database

  - Parameters:

    - `sql`: SQL query string to execute

- `ydb_query_with_params`: Run a parameterized SQL query with JSON parameters

  - Parameters:

    - `sql`: SQL query string with parameters
    - `params`: JSON string containing parameter values

- `ydb_list_directory`: List directory contents in YDB

  - Parameters:

    - `path`: YDB directory path to list

- `ydb_describe_path`: Get detailed information about a [scheme object](../../../concepts/glossary.md#scheme-object) (table, directory, etc) located at the specified YDB path

  - Parameters:

    - `path`: YDB path to describe

- `ydb_status`: Get the current status of the YDB connection

## Command-line arguments and environment variables {#server-arguments}

The following table describes the command-line arguments and environment variables for the YDB MCP server:

| Arguments | Environment variable | Default | Description |
| --- | --- | --- | --- |
| `--ydb-endpoint` | `YDB_ENDPOINT` | — | YDB endpoint consisting of protocol, hostname, port, and database name |
| `--ydb-login` | `YDB_LOGIN` | — | YDB login |
| `--ydb-password` | `YDB_PASSWORD` | — | YDB password |
| `--ydb-auth-mode` | `YDB_AUTH_MODE` | `anonymous` | YDB authentication mode. Valid values: `anonymous`, `login-password` |
| `--log-level` | — | `INFO` | Logging level. Valid values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

> [!NOTE]
> Command-line arguments override the corresponding environment variables.

## Learn More

For more information visit the [YDB MCP GitHub repository](https://github.com/ydb-platform/ydb-mcp).
