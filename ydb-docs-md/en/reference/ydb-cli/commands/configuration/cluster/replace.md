---
title: "admin cluster config replace"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/cluster/replace?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/cluster/replace"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/cluster/replace.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/cluster/replace.md"
description: "With the admin cluster config replace command, you can upload a dynamic configuration to the YDB cluster. Alert."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster config replace

With the `admin cluster config replace` command, you can upload a [dynamic configuration](../../../../../maintenance/manual/dynamic-config.md) to the YDB cluster.

> [!CAUTION]
> Commands in this section can harm your cluster if used incorrectly. Due to the potentially dangerous nature of these commands, ALL global parameters must be specified explicitly. Profiles are disabled by default and are only used when explicitly specified (--profile ). Some commands do not require global options that are otherwise mandatory.

General command syntax:

```bash
ydb [global options...] admin cluster config replace [options...]
```

- `global options` — Global parameters.
- `options` — [Subcommand parameters](replace.md#options).

View the description of the dynamic configuration replacement command:

```bash
ydb admin cluster config replace --help
```

## Subcommand Parameters {#options}

|  |  |
| --- | --- |
| Name | Description |
| `-f`, `--filename` | Path to the file containing the configuration. |
| `--allow-unknown-fields` | Allow unknown fields in the configuration.<br>If the flag is not set, unknown fields in the configuration result in an error. |
| `--ignore-local-validation` | Ignore basic client-side configuration validation.<br>If the flag is not set, YDB CLI performs basic client-side configuration validation. |

## Examples

Upload the dynamic configuration file to the cluster:

```bash
ydb admin cluster config replace --filename config.yaml
```

Upload the dynamic configuration file to the cluster, ignoring local applicability checks:

```bash
ydb admin cluster config replace -f config.yaml --ignore-local-validation
```

Upload the dynamic configuration file to the cluster, ignoring the check for unknown fields:

```bash
ydb admin cluster config replace -f config.yaml --allow-unknown-fields
```
