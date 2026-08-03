---
title: "Cluster Configuration Management Commands"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/cluster/?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/cluster/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/cluster/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/cluster/index.md"
description: "Cluster configuration management commands are designed for working with the configuration at the level of the entire YDB cluster. These commands allow cluster a"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Cluster Configuration Management Commands

Cluster configuration management commands are designed for working with the configuration at the level of the entire YDB cluster. These commands allow cluster administrators to view, modify, and manage [settings](../../../../configuration/index.md) that apply to all cluster nodes.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, ALL global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (--profile ). Some commands do not require global options that are otherwise mandatory.

General syntax for calling cluster configuration management commands:

```bash
ydb [global options] admin cluster config [command options] <subcommand>
```

Where:

- `ydb` – The command to run the YDB CLI from the operating system command line.
- `[global options]` – Global options, common to all YDB CLI commands.
- `admin cluster config` – The command for managing cluster configuration.
- `[command options]` – Command options specific to each command and subcommand.
- `<subcommand>` – The subcommand.

## Commands {#list}

The following is a list of available subcommands for managing cluster configuration. Any command can be called from the command line with the `--help` option to get help for it.

| Command / Subcommand | Brief Description |
| --- | --- |
| [admin cluster config fetch](fetch.md) | Fetch the current dynamic configuration (aliases: `get`, `dump`) |
| [admin cluster config generate](generate.md) | Generate dynamic configuration from the static startup configuration |
| [admin cluster config replace](replace.md) | Replace the dynamic configuration |
| admin cluster config vesion | Show configuration version on nodes (V1/V2) |
