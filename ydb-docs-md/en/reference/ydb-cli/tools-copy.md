---
title: "Copying tables"
url: "https://ydb.tech/docs/en/reference/ydb-cli/tools-copy?version=v26.1"
doc_path: "en/reference/ydb-cli/tools-copy"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/tools-copy.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/tools-copy.md"
description: "Using the tools copy subcommand, you can create a copy of one or more DB tables. The copy operation leaves the source table unchanged while the copy contains al"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Copying tables

Using the `tools copy` subcommand, you can create a copy of one or more DB tables. The copy operation leaves the source table unchanged while the copy contains all the source table data.

General format of the command:

```bash
ydb [global options...] tools copy [options...]
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](tools-copy.md#options).

View a description of the command to copy a table:

```bash
ydb tools copy --help
```

## Parameters of the subcommand {#options}

| Parameter name | Parameter description |
| --- | --- |
| `--timeout` | The time within which the operation should be completed on the server. |
| `--item <property>=<value>,...` | Operation properties. You can specify the parameter more than once to copy several tables in a single transaction.  <br>Required properties:<br>- `destination`, `dst`, `d`: Path to target table. If the destination path contains folders, they must be created in advance. No table with the destination name should exist.<br>- `source`, `src`, `s`: Path to source table.<br>Optional properties:<br>- `omit-indexes`: If `true`, indexes are not copied (default: `false`). |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Create the `backup` folder in the DB:

```bash
ydb -p quickstart scheme mkdir backup
```

Copy the `series` table to a table called `series-v1`, the `seasons` table to a table called `seasons-v1`, and `episodes` to `episodes-v1` in the `backup` folder:

```bash
ydb -p quickstart tools copy --item destination=backup/series-v1,source=series --item destination=backup/seasons-v1,source=seasons --item destination=backup/episodes-v1,source=episodes
```

View the listing of objects in the `backup` folder:

```bash
ydb -p quickstart scheme ls backup
```

Result:

```text
episodes-v1  seasons-v1  series-v1
```
