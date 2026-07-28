---
title: "Running a query"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-query-execute?version=v26.1"
doc_path: "en/reference/ydb-cli/table-query-execute"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-query-execute.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-query-execute.md"
description: "Warning. This command is deprecated. The preferred way to run queries in YDB CLI is to use the ydb sql command."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Running a query

> [!WARNING]
> This command is deprecated.
>  The preferred way to run queries in YDB CLI is to use the [`ydb sql`](sql.md) command.

The `table query execute` subcommand is designed for reliable execution of YQL queries. With this sub-command, you can successfully execute your query when certain table partitions are unavailable for a short time (for example, due to being [split or merged](../../concepts/datamodel/table.md#partitioning)) by using built-in retry policies.

General format of the command:

```bash
ydb [global options...] table query execute [options...]
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](table-query-execute.md#options).

View the description of the YQL query command:

```bash
ydb table query execute --help
```

## Parameters of the subcommand {#options}

|  |  |
| --- | --- |
| Name | Description |
| `--timeout` | The time within which the operation should be completed on the server. |
| `-t`, `--type` | Query type.  <br> Acceptable values:<br>- `data`: A YQL query that includes [DML](https://en.wikipedia.org/wiki/Data_Manipulation_Language) operations; it can be used both to update data in the database and fetch several selections limited to 1,000 rows per selection.<br><br>- `scan`: A [scan](../../concepts/query_execution/scan_query.md) YQL query; it allows read-only access to the database and can return only one result set, but without a limit on the number of rows in it. The server-side execution algorithm for `scan` queries is more complex than for `data`, so if you do not need to return more than 1,000 rows, it is more efficient to use the `data` query type.<br><br>- `scheme`: A YQL query that includes [DDL](https://en.wikipedia.org/wiki/Data_Definition_Language) operations.<br>   The default value is `data`. |
| `--stats` | Statistics mode.  <br> Acceptable values:<br>- `none`: Do not collect statistics.<br><br>- `basic`: Collect statistics for basic events.<br><br>- `full`: Collect statistics for all events.<br><br>  Defaults to `none`. |
| `-s` | Enable statistics collection in the `basic` mode. |
| `--tx-mode` | [Transaction mode](../../concepts/transactions.md#modes) (for `data` queries).  <br> Acceptable values:<br>`serializable-rw`: The result of parallel transactions is equivalent to their serial execution.<br>`online-ro`: Each of the reads in the transaction reads data that is most recent at the time of its execution.<br>`stale-ro`: Data reads in a transaction return results with a possible delay (fractions of a second).Default value: `serializable-rw`. |
| `-q`, `--query` | Text of the YQL query to be executed. |
| `-f,` `--file` | Path to the text of the YQL query to be executed. |
| `--format` | Result format.  <br> Possible values:<br>- `pretty` (default): Human-readable format.<br>- `json-unicode`: [JSON](https://en.wikipedia.org/wiki/JSON) output with binary strings [Unicode](https://en.wikipedia.org/wiki/Unicode)-encoded and each JSON string in a separate line.<br>- `json-unicode-array`: JSON output with binary strings Unicode-encoded and the result output as an array of JSON strings with each JSON string in a separate line.<br>- `json-base64`: JSON output with binary strings [Base64](https://en.wikipedia.org/wiki/Base64)-encoded and each JSON string in a separate line.<br>- `json-base64-array`: JSON output with binary strings Base64-encoded and the result output as an array of JSON strings with each JSON string in a separate line;<br>- `parquet`: Output in [Apache Parquet](https://parquet.apache.org/docs/) format.<br>- `csv`: Output in [CSV](https://en.wikipedia.org/wiki/CSV) format.<br>- `tsv`: Output in [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) format. |

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

### Creating tables {#examples-create-tables}

```bash
ydb -p quickstart table query execute \
  --type scheme \
  -q '
  CREATE TABLE series (series_id Uint64 NOT NULL, title Utf8, series_info Utf8, release_date Date, PRIMARY KEY (series_id));
  CREATE TABLE seasons (series_id Uint64, season_id Uint64, title Utf8, first_aired Date, last_aired Date, PRIMARY KEY (series_id, season_id));
  CREATE TABLE episodes (series_id Uint64, season_id Uint64, episode_id Uint64, title Utf8, air_date Date, PRIMARY KEY (series_id, season_id, episode_id));
  '
```

### Populating the table with data {#examples-upsert}

```bash
ydb -p quickstart table query execute \
  -q '
UPSERT INTO series (series_id, title, release_date, series_info) VALUES
  (1, "IT Crowd", Date("2006-02-03"), "The IT Crowd is a British sitcom produced by Channel 4, written by Graham Linehan, produced by Ash Atalla and starring Chris O'"'"'Dowd, Richard Ayoade, Katherine Parkinson, and Matt Berry."),
  (2, "Silicon Valley", Date("2014-04-06"), "Silicon Valley is an American comedy television series created by Mike Judge, John Altschuler and Dave Krinsky. The series focuses on five young men who founded a startup company in Silicon Valley.");

UPSERT INTO seasons (series_id, season_id, title, first_aired, last_aired) VALUES
    (1, 1, "Season 1", Date("2006-02-03"), Date("2006-03-03")),
    (1, 2, "Season 2", Date("2007-08-24"), Date("2007-09-28")),
    (2, 1, "Season 1", Date("2014-04-06"), Date("2014-06-01")),
    (2, 2, "Season 2", Date("2015-04-12"), Date("2015-06-14"));

UPSERT INTO episodes (series_id, season_id, episode_id, title, air_date) VALUES
    (1, 1, 1, "Yesterday'"'"'s Jam", Date("2006-02-03")),
    (1, 1, 2, "Calamity Jen", Date("2006-02-03")),
    (2, 1, 1, "Minimum Viable Product", Date("2014-04-06")),
    (2, 1, 2, "The Cap Table", Date("2014-04-13"));
'
```

### Simple data selection {#examples-simple-query}

```bash
ydb -p quickstart table query execute -q '
  SELECT season_id, episode_id, title
  FROM episodes
  WHERE series_id = 1
'
```

Result:

```text
┌───────────┬────────────┬───────────────────┐
| season_id | episode_id | title             |
├───────────┼────────────┼───────────────────┤
| 1         | 1          | "Yesterday's Jam" |
├───────────┼────────────┼───────────────────┤
| 1         | 2          | "Calamity Jen"    |
└───────────┴────────────┴───────────────────┘
```

### Unlimited selection for automated processing {#examples-query-stream}

Selecting data by a query whose text is saved to a file, without a limit on the number of rows in the selection and data output in the format: [Newline-delimited JSON stream](https://en.wikipedia.org/wiki/JSON_streaming).

Let's write the query text to the `request1.yql` file.

```bash
echo 'SELECT season_id, episode_id, title FROM episodes' > request1.yql
```

Now, run the query:

```bash
ydb -p quickstart table query execute -f request1.yql --type scan --format json-unicode
```

Result:

```text
{"season_id":1,"episode_id":1,"title":"Yesterday's Jam"}
{"season_id":1,"episode_id":2,"title":"Calamity Jen"}
{"season_id":1,"episode_id":1,"title":"Minimum Viable Product"}
{"season_id":1,"episode_id":2,"title":"The Cap Table"}
```

### Passing parameters {#examples-params}

You can find examples of executing parameterized queries, including streamed processing, in the [Passing parameters to YQL execution commands](parameterized-queries-cli.md) article.
