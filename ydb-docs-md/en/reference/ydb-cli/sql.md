---
title: "Query execution"
url: "https://ydb.tech/docs/en/reference/ydb-cli/sql?version=v26.1"
doc_path: "en/reference/ydb-cli/sql"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/sql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/sql.md"
description: "You can use the ydb sql subcommand to execute an SQL query. The query can be of any type (DDL, DML, etc.) and can consist of several subqueries. The ydb sql sub"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Query execution

You can use the `ydb sql` subcommand to execute an SQL query. The query can be of any type (DDL, DML, etc.) and can consist of several subqueries. The `ydb sql` subcommand establishes a streaming connection and retrieves data through it. With in-stream query execution, no limit is imposed on the amount of data read. Data can also be written using this command, which is more efficient when executing repeated queries with data passed through parameters.

General format of the command:

```bash
ydb [global options...] sql [options...]
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Subcommand parameters](sql.md#options).

View the description of this command by calling it with `--help` option:

```bash
ydb sql --help
```

## Parameters of the subcommand {#options}

|  |  |
| --- | --- |
| Name | Description |
| `-h`, `--help` | Print general usage help. |
| `-hh` | Print complete usage help, including specific options not shown with `--help`. |
| `-s`, `--script` | Script (query) text to execute. |
| `-f`, `--file` | Path to a file with query text to execute. Path `-` means reading query text from `stdin` which disables passing parameters via `stdin`. |
| `--stats` | Statistics mode.  <br>Available options:<br>- `none` (default): Do not collect statistics.<br>- `basic`: Collect aggregated statistics for updates and deletes per table.<br>- `full`: Include execution statistics and plan in addition to `basic`.<br>- `profile`: Collect detailed execution statistics, including statistics for individual tasks and channels. |
| `--explain` | Execute an explain request for the query. Displays the query's logical plan. The query is not actually executed and does not affect database data. |
| `--explain-ast` | Same as `--explain`, but in addition to the query's logical plan, an [abstract syntax tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) is printed. The AST section contains a representation in the internal [miniKQL](../../concepts/glossary.md#minikql) language. |
| `--explain-analyze` | Execute the query in `EXPLAIN ANALYZE` mode. Displays the query execution plan. Query results are ignored.  <br>**Important note: The query is actually executed, so any changes will be applied to the database**. |
| `--format` | Output format.  <br>Available options:<br>- `pretty` (default): Human-readable format.<br>- `json-unicode`: [JSON](https://en.wikipedia.org/wiki/JSON) output with binary strings [Unicode](https://en.wikipedia.org/wiki/Unicode)-encoded and each JSON string in a separate line.<br>- `json-unicode-array`: JSON output with binary strings Unicode-encoded and the result output as an array of JSON strings with each JSON string in a separate line.<br>- `json-base64`: JSON output with binary strings [Base64](https://en.wikipedia.org/wiki/Base64)-encoded and each JSON string in a separate line.<br>- `json-base64-array`: JSON output with binary strings Base64-encoded and the result output as an array of JSON strings with each JSON string in a separate line;<br>- `parquet`: Output in [Apache Parquet](https://parquet.apache.org/docs/) format.<br>- `csv`: Output in [CSV](https://en.wikipedia.org/wiki/CSV) format.<br>- `tsv`: Output in [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) format. |

### Working with parameterized queries {#parameterized-query}

For a detailed description with examples on how to use parameterized queries, see [Running parameterized queries](parameterized-query-execution.md).

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

A script to create a table, populate it with data, and select data from the table:

```bash
ydb -p quickstart sql -s '
    CREATE TABLE series (series_id Uint64, title Utf8, series_info Utf8, release_date Date, PRIMARY KEY (series_id));
    COMMIT;
    UPSERT INTO series (series_id, title, series_info, release_date) values (1, "Title1", "Info1", Cast("2023-04-20" as Date));
    COMMIT;
    SELECT * from series;
  '
```

Command output:

```text
┌──────────────┬───────────┬─────────────┬──────────┐
| release_date | series_id | series_info | title    |
├──────────────┼───────────┼─────────────┼──────────┤
| "2023-04-20" | 1         | "Info1"     | "Title1" |
└──────────────┴───────────┴─────────────┴──────────┘
```

Running a script from the example above saved as the `script1.yql` file, with results output in `JSON` format:

```bash
ydb -p quickstart sql -f script1.yql --format json
```

Command output:

```text
{"release_date":"2023-04-20","series_id":1,"series_info":"Info1","title":"Title1"}
```

You can find examples of passing parameters to queries in the [article on how to pass parameters to `ydb sql`](parameterized-query-execution.md).
