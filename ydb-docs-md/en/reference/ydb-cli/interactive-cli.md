---
title: "Interactive query execution mode"
url: "https://ydb.tech/docs/en/reference/ydb-cli/interactive-cli?version=v26.1"
doc_path: "en/reference/ydb-cli/interactive-cli"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/interactive-cli.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/interactive-cli.md"
description: "Overview."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Interactive query execution mode

## Overview

Executing the `ydb` command without subcommands launches the interactive query execution mode. After that, you can enter queries directly into the console or terminal. When you enter a newline character, the query text is considered complete, and query execution begins. The query text can be either a [YQL query](../../yql/reference/index.md) or a [special command](interactive-cli.md#spec-commands).

General format of the command:

```bash
ydb [global options...]
```

- `global options` — [global parameters](commands/global-options.md).

> [!NOTE]
> Note that the command still requires [connection parameters](connect.md) to be set. You can supply them by having the default profile, via an explicitly specified profile, or by passing a set of connection parameters.

Example usage:

![Example](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/general-example.gif)

The interactive query execution mode in YDB CLI offers the following features:

- [Syntax highlighting](interactive-cli.md#syntax-highlighting)
- [Hotkeys](interactive-cli.md#hotkeys)
- [Query history](interactive-cli.md#query-history)
- [Auto completion](interactive-cli.md#auto-completion)
- [Special commands](interactive-cli.md#spec-commands)

## Syntax highlighting

![Syntax highlighting](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/highlighting.jpg)

Interactive mode supports YQL syntax highlighting, which helps to better understand the query structure. Different colors are used for the following groups of elements:

- YQL keywords (`SELECT`, `FROM`, `WHERE`, `INSERT`, `UPDATE`, and others)
- Table and column names
- String literals (text in quotes)
- Numeric literals
- Operators (`=`, `<`, `>`, `+`, `-`, and others)
- Special characters (brackets, commas, dots)
- Comments

## Hotkeys

You can use these hotkeys while working in the interactive mode:

| Hotkey | Description |
| --- | --- |
| `Up arrow` | Shows the previous query from history. |
| `Down arrow` | Shows the next query from history. |
| `TAB` | Completes the current word based on YQL syntax. |
| `CTRL + R` | Searches for a query in history containing a specified substring. |
| `CTRL + D` | Exits interactive mode. |

## Query history

You can navigate through the query history using the up and down arrow keys:

![History](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/history.gif)

History is stored locally and persists between CLI launches.

A query search function (`CTRL + R`) is also supported:

![Search](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/history-search.gif)

## Auto completion

Auto completion helps you write queries more efficiently. While typing, it suggests possible completions for the current word based on YQL syntax.

It also searches for schema object names in the database where possible.

There are two types of suggestions: auto completion by pressing the `TAB` key and interactive hints.

### Auto completion by pressing the `TAB`key {#auto-completion-tab}

While in interactive mode, pressing the `TAB` key shows a list of suggestions for completing the current word according to the YQL syntax.

![Auto completion](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/candidates.gif)

Continue typing to narrow down the list of suitable candidates.

If there is only one available option, pressing `TAB` will automatically complete the current word.

If all available options share a common prefix, pressing `TAB` will automatically insert it.

### Interactive hints

While typing in interactive mode, a list of hints appears under the cursor, showing the first four suggestions for completing the current word according to the YQL grammar.

![Interactive hints](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/reference/ydb-cli/_assets/hints.gif)

This feature provides quick guidance without overwhelming you with all possible options, helping you stay on track while writing queries.

## Special commands {#spec-commands}

Special commands are CLI-specific commands and are not part of the YQL syntax. Their purpose is to perform various functions that cannot be accomplished through a YQL query.

| Command | Description |
| --- | --- |
| `SET param = value` | Sets the value of the [internal variable](interactive-cli.md#internal-vars) `param` to `value`. |
| `EXPLAIN query-text` | Outputs the query plan for `query-text`. Equivalent to the command [ydb table query explain](commands/explain-plan.md#explain-plan). |
| `EXPLAIN AST query-text` | Outputs the query plan for `query-text` along with the [AST](commands/explain-plan.md). Equivalent to the command [ydb table query explain --ast](commands/explain-plan.md#ast). |

### List of internal variables {#internal-vars}

Internal variables determine the behavior of commands and are set using the [special command](interactive-cli.md#spec-commands) `SET`.

| Variable | Description |
| --- | --- |
| `stats` | The statistics collection mode for subsequent queries.  <br>Acceptable values:<br>- `none` (default): Do not collect.<br>- `basic`: Collect statistics.<br>- `full`: Collect statistics and query plan. |

### Example {#examples}

Executing a query in the `full` statistics collection mode:

```bash
$ ydb
ydb> SET stats = full
ydb> select * from table1 limit 1
┌────┬─────┬───────┐
│ id │ key │ value │
├────┼─────┼───────┤
│ 10 │ 0   │ ""    │
└────┴─────┴───────┘

Statistics:
query_phases {
  duration_us: 14987
  table_access {
    name: "/ru-central1/a1v7bqj3vtf10qjleyow/laebarufb61tguph3g22/table1"
    reads {
      rows: 9937
      bytes: 248426
    }
  }
  cpu_time_us: 2925
  affected_shards: 1
}
process_cpu_time_us: 3816
total_duration_us: 79530
total_cpu_time_us: 6741

Full statistics:
Query 0:
ResultSet
└──Limit (Limit: 1)
   TotalCpuTimeUs: 175
   TotalTasks: 1
   TotalInputBytes: 6
   TotalInputRows: 1
   TotalOutputBytes: 16
   TotalDurationMs: 0
   TotalOutputRows: 1
   └──<UnionAll>
      └──Limit (Limit: 1)
      └──TableFullScan (ReadColumns: ["id","key","value"], ReadRanges: ["key (-∞, +∞)"], Table: impex_table)
         Tables: ["table1"]
         TotalCpuTimeUs: 154
         TotalTasks: 1
         TotalInputBytes: 0
         TotalInputRows: 0
         TotalOutputBytes: 16
         TotalDurationMs: 0
         TotalOutputRows: 1
```
