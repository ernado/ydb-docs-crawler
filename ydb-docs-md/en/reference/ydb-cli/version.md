---
title: "Getting YDB CLI version"
url: "https://ydb.tech/docs/en/reference/ydb-cli/version?version=v26.1"
doc_path: "en/reference/ydb-cli/version"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/version.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/version.md"
description: "Use the version subcommand to find out the version of the YDB CLI installed and manage new version availability auto checks."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Getting YDB CLI version

Use the `version` subcommand to find out the version of the YDB CLI installed and manage new version availability auto checks.

New version availability auto checks are made when you run any YDB CLI command, except `ydb version --enable-checks` and `ydb version --disable-checks`, but only once in 24 hours. The result and time of the last check are saved to the YDB CLI configuration file.

General format of the command:

```bash
ydb [global options...] version [options...]
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](version.md#options).

View a description of the command:

```bash
ydb version --help
```

## Parameters of the subcommand {#options}

| Parameter | Description |
| --- | --- |
| `--semantic` | Get only the version number. |
| `--check` | Check if a new version is available. |
| `--disable-checks` | Disable new version availability checks. |
| `--enable-checks` | Enable new version availability checks. |

## Examples

### Disable new version availability checks {#disable-checks}

When running YDB CLI commands, the system automatically checks if a new version is available. If the host where the command is run doesn't have internet access, this causes a delay and the corresponding warning appears during command execution. To disable auto checks for updates, run:

```bash
ydb version --disable-checks
```

Result:

```text
Latest version checks disabled
```

### Getting only the version number {#semantic}

To facilitate data handling in scripts, you can limit result to the YDB CLI version number:

```bash
ydb version --semantic
```

Result:

```text
1.9.1
```
