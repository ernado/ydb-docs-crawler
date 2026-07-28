---
title: "admin cluster bridge failover"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/failover?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/failover"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/failover.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/failover.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster bridge failover

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Use the `admin cluster bridge failover` command to perform [emergency disable](../../../../concepts/bridge.md#failover) of a pile when it is unavailable. You can optionally specify the pile that will become the new `PRIMARY`.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, **ALL** global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (`--profile <profile-name>`). Some commands do not require global options that are otherwise mandatory.

General command syntax:

```bash
ydb [global options...] admin cluster bridge failover [options...]
```

- `global options` — [global parameters](../global-options.md) for the CLI.
- `options` — [subcommand parameters](failover.md#options).

View command help:

```bash
ydb admin cluster bridge failover --help
```

## Subcommand parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--pile <pile>` | Name of the unavailable pile. |
| `--new-primary <pile>` | Name of the pile that should become the new `PRIMARY`. Specify if the unavailable pile was `PRIMARY`. |

## Requirements

- If the current `PRIMARY` is unavailable, you must specify `--new-primary` and choose a pile in the `SYNCHRONIZED` state. If `--new-primary` is missing or the chosen pile is not in `SYNCHRONIZED` state, the command returns an error without making any changes.
- The cluster will not enter an invalid state: if requirements are violated, the command makes no changes and reports an error.
- If the pile has not failed but you need to disable it, use [planned disable](../../../../concepts/bridge.md#takedown) — the [`takedown`](takedown.md) command.

## Examples

Perform emergency disable for an unavailable pile named `pile-a`:

```bash
ydb admin cluster bridge failover --pile pile-a
```

Perform emergency disable for an unavailable `PRIMARY` pile and designate a synchronized pile as the new `PRIMARY`:

```bash
ydb admin cluster bridge failover --pile pile-a --new-primary pile-b
```

### Verifying the result {#verify}

Use the [list](list.md) command to verify that the unavailable pile has been moved to `DISCONNECTED` and (if `--new-primary` was specified) a new `PRIMARY` has been selected:

```bash
ydb admin cluster bridge list

pile-a: DISCONNECTED
pile-b: PRIMARY
```
