---
title: "table attribute add"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-attribute-add?version=v26.1"
doc_path: "en/reference/ydb-cli/table-attribute-add"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-attribute-add.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-attribute-add.md"
description: "With the table attribute add command, you can add a custom attribute to your table. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# table attribute add

With the `table attribute add` command, you can add a [custom attribute](../../concepts/datamodel/table.md#users-attr) to your table.

General format of the command:

```bash
ydb [global options...] table attribute add [options...] <table path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](table-attribute-add.md#options).
- `table path`: The table path.

Look up the description of the command to add a custom attribute:

```bash
ydb table attribute add --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--attribute` | The custom attribute in the `<key>=<value>` format. You can use `--attribute` many times to add multiple attributes by a single command. |

## Examples {#examples-{examples}}

Add the custom attributes with the keys `attr_key1`, `attr_key2` and the respective values `attr_value1`, `attr_value2` to the `my-table` table:

```bash
ydb table attribute add --attribute attr_key1=attr_value1 --attribute attr_key2=attr_value2 my-table
```
