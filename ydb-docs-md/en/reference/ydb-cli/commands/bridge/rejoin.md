---
title: "admin cluster bridge rejoin"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/rejoin?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/rejoin"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/rejoin.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/rejoin.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster bridge rejoin

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Use the `admin cluster bridge rejoin` command to [return](../../../../concepts/bridge.md#rejoin) the specified pile to the cluster after maintenance or recovery. After the command runs, the pile is expected to transition from `DISCONNECTED` to `NOT_SYNCHRONIZED`, then sync automatically and transition to `SYNCHRONIZED`.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, **ALL** global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (`--profile <profile-name>`). Some commands do not require global options that are otherwise mandatory.

General command syntax:

```bash
ydb [global options...] admin cluster bridge rejoin [options...]
```

- `global options` — global parameters.
- `options` — [subcommand parameters](rejoin.md#options).

View command help:

```bash
ydb admin cluster bridge rejoin --help
```

## Subcommand parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--pile <pile>` | Name of the pile to return to the cluster. |

## Requirements

- The pile must be in the `DISCONNECTED` state before it can be returned.

## Examples

Return pile `pile-a` from `DISCONNECTED` state:

```bash
ydb admin cluster bridge rejoin --pile pile-a
```

### Verifying the result {#verify}

Right after the command runs, the pile is expected to transition to `NOT_SYNCHRONIZED`. Verify with the [list](list.md) command:

```bash
ydb admin cluster bridge list

pile-a: NOT_SYNCHRONIZED
pile-b: PRIMARY
```

After synchronization completes, the pile transitions to `SYNCHRONIZED`:

```bash
ydb admin cluster bridge list

pile-a: SYNCHRONIZED
pile-b: PRIMARY
```
