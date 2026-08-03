---
title: "Running a script (with streaming support)"
url: "https://ydb.tech/docs/en/reference/ydb-cli/yql?version=v26.1"
doc_path: "en/reference/ydb-cli/yql"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/yql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/yql.md"
description: "Warning. This command is deprecated. The preferred way to run queries in YDB CLI is to use the ydb sql command."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Running a script (with streaming support)

> [!WARNING]
> This command is deprecated.
>  The preferred way to run queries in YDB CLI is to use the [`ydb sql`](sql.md) command.

You can use the `yql` subcommand to run a YQL script. The script can include queries of different types. Unlike `scripting yql`, the `yql` subcommand establishes a streaming connection and retrieves data through it. With the in-stream query execution, no limit is imposed on the amount of data read.

General format of the command:

```bash
ydb [global options...] yql [options...]
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](yql.md#options).

View the description of the YQL script command:

```bash
ydb yql --help
```

## Parameters of the subcommand {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--timeout` | The time within which the operation should be completed on the server. |
| `--stats` | Statistics mode.<br>Acceptable values:<br>- `none` (default): Do not collect.<br>- `basic`: Collect statistics for basic events.<br>- `full`: Collect statistics for all events. |
| `-s`, `--script` | Text of the YQL query to be executed. |
| `-f`, `--file` | Path to the text of the YQL query to be executed. |
| `--format` | Result format.<br>Possible values:<br>- `pretty` (default): Human-readable format.<br>- `json-unicode`: [JSON](https://en.wikipedia.org/wiki/JSON) output with binary strings [Unicode](https://en.wikipedia.org/wiki/Unicode)-encoded and each JSON string in a separate line.<br>- `json-unicode-array`: JSON output with binary strings Unicode-encoded and the result output as an array of JSON strings with each JSON string in a separate line.<br>- `json-base64`: JSON output with binary strings [Base64](https://en.wikipedia.org/wiki/Base64)-encoded and each JSON string in a separate line.<br>- `json-base64-array`: JSON output with binary strings Base64-encoded and the result output as an array of JSON strings with each JSON string in a separate line;<br>- `parquet`: Output in [Apache Parquet](https://parquet.apache.org/docs/) format.<br>- `csv`: Output in [CSV](https://en.wikipedia.org/wiki/CSV) format.<br>- `tsv`: Output in [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) format. |

### Working with parameterized queries {#parameterized-query}

A brief help is provided below. For a detailed description with examples, see [Running parametrized YQL queries and scripts](parameterized-queries-cli.md).

| Name | Description |
| --- | --- |
| `-p, --param` | The value of a single parameter of a YQL query, in the format: `$name=value`, where `$name` is the parameter name and `value` is its value (a valid [JSON value](https://www.json.org/json-ru.html)). |
| `--param-file` | Name of the file in [JSON](https://en.wikipedia.org/wiki/JSON) format and in [UTF-8](https://en.wikipedia.org/wiki/UTF-8) encoding that specifies values of the parameters matched against the YQL query parameters by key names. |
| `--input-format` | Format of parameter values. Applies to all the methods of parameter transmission (among command parameters, in a file or using `stdin`).  <br>Acceptable values:<br>- `json-unicode` (default):[JSON](https://en.wikipedia.org/wiki/JSON).<br>- `json-base64`: [JSON](https://en.wikipedia.org/wiki/JSON) format in which values of binary string parameters (`DECLARE $par AS String`) are [Base64](https://en.wikipedia.org/wiki/Base64)-encoded. |
| `--stdin-format` | The parameter format and framing for `stdin`. To set both values, specify the parameter twice.  <br>**Format of parameter encoding for `stdin`**  <br>Acceptable values:<br>- `json-unicode`: [JSON](https://en.wikipedia.org/wiki/JSON).<br>- `json-base64`: [JSON](https://en.wikipedia.org/wiki/JSON) format in which values of binary string parameters (`DECLARE $par AS String`) are [Base64](https://en.wikipedia.org/wiki/Base64)-encoded.<br>- `raw` is binary data; the parameter name is set in `--stdin-par`.<br>If the format of parameter encoding for `stdin` isn't specified, the format set in `--input-format` is used.  <br>  <br>**Classification of parameter sets for `stdin` (framing)**  <br>Acceptable values:<br>- `no-framing` (default): Framing isn't used<br>- `newline-delimited`: The newline character is used in `stdin` to end a given parameter set, separating it from the next one. |
| `--stdin-par` | The name of the parameter whose value will be sent over `stdin` is specified without a `$`. |
| `--batch` | The batch mode of transmitting parameter sets received via `stdin`.  <br>Acceptable values:<br>- `iterative` (default): Batch mode is disabled<br>- `full`: Full-scale batch mode is enabled<br>- `adaptive`: Adaptive batching is enabled |
| `--batch-limit` | A maximum number of sets of parameters per batch in the adaptive batch mode. The setting of `0` removes the limit.  <br>  <br>The default value is `1000`. |
| `--batch-max-delay` | The maximum delay related to processing the resulting parameter set in the adaptive batch mode. It's set as a number of `s`, `ms`, `m`.  <br>  <br>Default value: `1s` (1 second). |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

A script to create a table, populate it with data, and select data from the table:

```bash
ydb -p quickstart yql -s '
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
ydb -p quickstart yql -f script1.yql --format json-unicode
```

Command output:

```text
{"release_date":"2023-04-20","series_id":1,"series_info":"Info1","title":"Title1"}
```

You can find examples of passing parameters to scripts in the [article on how to pass parameters to YQL execution commands](parameterized-queries-cli.md).
