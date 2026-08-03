---
title: "admin cluster bridge switchover"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/switchover?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/switchover"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/switchover.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/switchover.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster bridge switchover

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Use the `admin cluster bridge switchover` command to perform a smooth, planned transition of the specified pile to `PRIMARY` via the intermediate `PROMOTED` state. For details, see the [scenario description](../../../../concepts/bridge.md#switchover).

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, **ALL** global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (`--profile <profile-name>`). Some commands do not require global options that are otherwise mandatory.

General command syntax:

```bash
ydb [global options...] admin cluster bridge switchover [options...]
```

- `global options` — [global parameters](../global-options.md) for the CLI.
- `options` — [subcommand parameters](switchover.md#options).

View command help:

```bash
ydb admin cluster bridge switchover --help
```

## Subcommand parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--new-primary <pile>` | Name of the pile that should become the new PRIMARY. |

## Requirements

- The target pile must be in the `SYNCHRONIZED` state.

## Examples

Transition pile `pile-b` from `SYNCHRONIZED` to `PRIMARY` via the intermediate `PROMOTED` state:

```bash
ydb admin cluster bridge switchover --new-primary pile-b
```

### Verifying the result {#verify}

After a short time (a few minutes), verify that pile states have changed correctly using the [list](list.md) command:

```bash
ydb admin cluster bridge list

pile-a: SYNCHRONIZED
pile-b: PRIMARY
```
