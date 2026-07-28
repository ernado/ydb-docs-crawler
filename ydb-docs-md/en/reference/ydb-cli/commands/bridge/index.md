---
title: "Bridge cluster management commands"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/index.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Bridge cluster management commands

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Commands for managing the cluster in [bridge mode](../../../../concepts/bridge.md) let you view [pile](../../../../concepts/glossary.md#pile) state, perform planned and emergency PRIMARY change, temporarily take a pile out for maintenance, and return it to the cluster.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, **ALL** global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (`--profile <profile-name>`). Some commands do not require global options that are otherwise mandatory.

General syntax for bridge cluster management commands:

```bash
ydb [global options...] admin cluster bridge [command options...] <subcommand>
```

where:

- `ydb` — command to launch YDB CLI from the operating system command line;
- `[global options]` — global parameters common to all YDB CLI commands;
- `admin cluster bridge` — cluster configuration management command;
- `[command options]` — parameters specific to each command and subcommand;
- `<subcommand>` — subcommand.

## Commands {#list}

Below is the list of available subcommands for bridge cluster management. You can run any command with the `--help` option for help.

| Command / subcommand | Brief description |
| --- | --- |
| [admin cluster bridge list](list.md) | List pile state |
| [admin cluster bridge switchover](switchover.md) | Planned PRIMARY change |
| [admin cluster bridge failover](failover.md) | Emergency failover |
| [admin cluster bridge takedown](takedown.md) | Take pile out of cluster |
| [admin cluster bridge rejoin](rejoin.md) | Return pile to cluster |
