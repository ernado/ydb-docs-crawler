---
title: "admin cluster bridge list"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/bridge/list?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/bridge/list"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/bridge/list.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/bridge/list.md"
description: "Feature of Yandex Enterprise Database. This functionality is available only in the Yandex Enterprise Database. In the open-source version of YDB it is absent."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster bridge list

> [!NOTE]
> **Feature of Yandex Enterprise Database**
>
> This functionality is available only in the [Yandex Enterprise Database](../../../../downloads/yandex-enterprise-database.md). In the open-source version of YDB it is absent.

Use the `admin cluster bridge list` command to list the state of each pile in [bridge mode](../../../../concepts/bridge.md).

General command syntax:

```bash
ydb [global options...] admin cluster bridge list [options...]
```

- `global options` — [global parameters](../global-options.md) for the CLI.
- `options` — [subcommand parameters](list.md#options).

View command help:

```bash
ydb admin cluster bridge list --help
```

## Subcommand parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--format <pretty, json, csv>` | Output format. Valid values: `pretty`, `json`, `csv`. Default: `pretty`. |

## Examples

List piles in human-readable format:

```bash
ydb admin cluster bridge list

pile-a: PRIMARY
pile-b: SYNCHRONIZED
```

Output state in JSON format:

```bash
ydb admin cluster bridge list --format json

{
  "pile-a": "PRIMARY",
  "pile-b": "SYNCHRONIZED"
}
```

Output state in CSV format:

```bash
ydb admin cluster bridge list --format csv

pile,state
pile-a,PRIMARY
pile-b,SYNCHRONIZED
```
