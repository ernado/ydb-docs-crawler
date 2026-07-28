---
title: "admin cluster bridge takedown"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/takedown?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/takedown"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/takedown.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/takedown.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# admin cluster bridge takedown

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Use the `admin cluster bridge takedown` command to perform [planned disable](../../../../concepts/bridge.md#takedown) of a pile. If you are disabling the current `PRIMARY`, you must specify the new `PRIMARY`.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, **ALL** global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (`--profile <profile-name>`). Some commands do not require global options that are otherwise mandatory.

General command syntax:

```bash
ydb [global options...] admin cluster bridge takedown [options...]
```

- `global options` — global parameters.
- `options` — [subcommand parameters](takedown.md#options).

View command help:

```bash
ydb admin cluster bridge takedown --help
```

## Subcommand parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--pile <pile>` | Name of the pile to take out of the cluster. |
| `--new-primary <pile>` | Name of the pile that should become the new `PRIMARY` if the current `PRIMARY` is being disabled. |

## Requirements

- If you are disabling the current `PRIMARY`, you must specify `--new-primary` and choose a pile in the `SYNCHRONIZED` state.

## Examples

Take `SYNCHRONIZED` pile `pile-b` out of the cluster:

```bash
ydb admin cluster bridge takedown --pile pile-b
```

Take `PRIMARY` pile `pile-a` out of the cluster and transition `pile-b` from `SYNCHRONIZED` to `PRIMARY`:

```bash
ydb admin cluster bridge takedown --pile pile-a --new-primary pile-b
```

### Verifying the result {#verify}

Verify the resulting pile states with the [list](list.md) command:

```bash
ydb admin cluster bridge list

pile-a: PRIMARY
pile-b: DISCONNECTED
```

If you disabled the current `PRIMARY` with `--new-primary`, verify that the chosen pile has become `PRIMARY`:

```bash
ydb admin cluster bridge list

pile-a: DISCONNECTED
pile-b: PRIMARY
```
