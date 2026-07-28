---
title: "Node Configuration Management Commands"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/node/?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/node/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/node/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/node/index.md"
description: "Node configuration management commands are designed for working with the configuration at the level of individual YDB cluster nodes. These commands allow cluste"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Node Configuration Management Commands

Node configuration management commands are designed for working with the configuration at the level of individual YDB cluster nodes. These commands allow cluster administrators to initialize, update, and manage the settings of individual nodes.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, ALL global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (--profile ). Some commands do not require global options that are otherwise mandatory.

General syntax for calling node configuration management commands:

```bash
ydb [global options] admin node config [command options] <subcommand>
```

- `ydb` – The command to run the YDB CLI from the operating system command line.
- `[global options]` – Global options, common to all YDB CLI commands.
- `admin node config` – The command for managing node configuration.
- `[command options]` – Command options specific to each command and subcommand.
- `<subcommand>` – The subcommand.

## Commands {#list}

The following is a list of available subcommands for managing node configuration. Any command can be called from the command line with the `--help` option to get help for it.

| Command / Subcommand | Brief Description |
| --- | --- |
| [admin node config init](init.md) | Initialize the directory for node configuration |
