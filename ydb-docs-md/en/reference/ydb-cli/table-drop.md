---
title: "Deleting a table"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-drop?version=v26.1"
doc_path: "en/reference/ydb-cli/table-drop"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-drop.md"
description: "Using the table drop subcommand, you can delete a specified table. General format of the command: ydb [global options...] table drop [options...] <table path>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Deleting a table

Using the `table drop` subcommand, you can delete a specified table.

General format of the command:

```bash
ydb [global options...] table drop [options...] <table path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](table-drop.md#options).
- `table path`: The table path.

To view a description of the table delete command:

```bash
ydb table drop --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--timeout` | The time within which the operation should be completed on the server. |

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

To delete the table `series`:

```bash
ydb -p quickstart table drop series
```
