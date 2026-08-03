---
title: "table attribute drop"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-attribute-drop?version=v26.1"
doc_path: "en/reference/ydb-cli/table-attribute-drop"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-attribute-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-attribute-drop.md"
description: "With the table attribute drop command, you can drop a custom attribute from your table. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# table attribute drop

With the `table attribute drop` command, you can drop a [custom attribute](../../concepts/datamodel/table.md#users-attr) from your table.

General format of the command:

```bash
ydb [global options...] table attribute drop [options...] <table path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](table-attribute-drop.md#options).
- `table path`: The table path.

Look up the description of the command to add a custom attribute:

```bash
ydb table attribute drop --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--attributes` | The key of the custom attribute to be dropped. You can list multiple keys separated by a comma (`,`). |

## Examples {#examples-{examples}}

Drop the custom attributes with the keys `attr_key1` and `attr_key2` from the `my-table` table:

```bash
ydb table attribute drop --attributes attr_key1,attr_key2 my-table
```
