---
title: "admin node config init"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/node/init?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/node/init"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/node/init.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/node/init.md"
description: "When deploying a new YDB cluster or adding nodes to an existing one (scaling out), each node requires a directory to store its configuration. The admin node con"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin node config init

When deploying a new YDB cluster or adding nodes to an existing one (scaling out), each node requires a directory to store its configuration. The `admin node config init` command creates and prepares this directory by placing a specified configuration file in it or retrieving the configuration from another cluster node (seed node).

General command syntax:

```bash
ydb [global options...] admin node config init [options...]
```

- `global options` — Global parameters.
- `options` — [Subcommand parameters](init.md#options).

View the description of the node configuration initialization command:

```bash
ydb admin node config init --help
```

## Subcommand Parameters {#options}

| Name | Description |
| --- | --- |
| `-d`, `--config-dir` | **Required**. Path to the directory for storing the configuration file. |
| `-f`, `--from-config` | Path to the initial configuration file. Required for initial cluster deployment. Can also be used for scaling out if a file with the current cluster configuration has been delivered to the node beforehand. |
| `-s`, `--seed-node` | Endpoint of the source node (seed node) from which the configuration will be retrieved. Used for scaling out the cluster. |

## Examples

Initialize the node's configuration directory using the specified configuration file:

```bash
ydb admin node config init --config-dir /opt/ydb/cfg-dir --from-config config.yaml
```

Initialize the node's configuration by retrieving it from a source node:

```bash
ydb admin node config init --config-dir /opt/ydb/cfg-dir --seed-node <node.ydb.tech>:2135
```

## Usage

After successfully initializing the node's configuration directory, you can start the `ydbd` process on this node by adding the `--config-dir` parameter specifying the path to the directory. From this point on, when the cluster configuration is updated, the system automatically saves the updated config to the specified directory, eliminating the need to manually update the configuration file on the node.

When the node restarts, it automatically loads the current configuration from this directory.
