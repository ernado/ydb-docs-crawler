---
title: "ClickBench load"
url: "https://ydb.tech/docs/en/reference/ydb-cli/workload-click-bench?version=v26.1"
doc_path: "en/reference/ydb-cli/workload-click-bench"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/workload-click-bench.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/workload-click-bench.md"
description: "The load is based on data and queries from the https://github.com/ClickHouse/ClickBench repository, and the queries and table layout are adapted to YDB."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ClickBench load

The load is based on data and queries from the [https://github.com/ClickHouse/ClickBench](https://github.com/ClickHouse/ClickBench) repository, and the queries and table layout are adapted to YDB.

The benchmark generates typical workload in the following areas: clickstream and traffic analysis, web analytics, machine-generated data, structured logs, and event data. It covers typical queries in analytics and real-time dashboards.

The dataset for this benchmark was obtained from an actual traffic recording of one of the world's largest web analytics platforms. It has been anonymized while keeping all the essential data distributions. The query set was improvised to reflect realistic workloads, while the queries are not directly from production.

## Common command options

All commands support the common option `--path`, which specifies the path to a table in the database:

```bash
ydb workload clickbench --path clickbench/hits ...
```

### Available options {#common_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--path` or `-p` | Specifies the table path. | `clickbench/hits` |

## Initializing a load test {#init}

Before running the benchmark, create a table:

```bash
ydb workload clickbench --path clickbench/hits init
```

See the description of the command to init the data load:

```bash
ydb workload clickbench init --help
```

### Available parameters {#init_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--store <value>` | Table storage type. Possible values: `row`, `column`, `external-s3`. | `column`. |
| `--external-s3-prefix <value>` | Only relevant for external tables. Root path to the dataset in S3 storage. |  |
| `--external-s3-endpoint <value>` or `-e <value>` | Only relevant for external tables. Link to S3 Bucket with data. |  |
| `--string` | Use `String` type for text fields. `Utf8` is used by default. |  |
| `--datetime` | Use `Date`, `Datetime` and `Timestamp` type for time-related fields. | `Date32`, `Datetime64` and `Timestamp64` |
| `--partition-size` | Maximum partition size in megabytes (AUTO_PARTITIONING_PARTITION_SIZE_MB) for row tables. | 2000 |
| `--clear` | If the table at the specified path has already been created, it will be deleted. |  |
| `--dry-run` | Do not execute initialization queries, but only display their text. |  |

## Loading data into a table {#load}

Download the data archive, then load the data into the table:

```bash
wget https://datasets.clickhouse.com/hits_compatible/hits.csv.gz
ydb workload clickbench --path clickbench/hits import files --input hits.csv.gz
```

For source files, you can use CSV and TSV files, as well as directories containing such files. They can be either compressed or not.

### Available parameters {#load_files_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--input <path>` or `-i <path>` | Path to the source data files. Both unpacked and packed CSV and TSV files, as well as directories containing such files, are supported. Data can be downloaded from the official ClickBench website: [csv.gz](https://datasets.clickhouse.com/hits_compatible/hits.csv.gz), [tsv.gz](https://datasets.clickhouse.com/hits_compatible/hits.tsv.gz). To speed up the process, these files can be split into smaller parts, allowing parallel downloads. |  |
| `--state <path>` | Path to the download state file. If the download is interrupted, it will resume from the same point when restarted. |  |
| `--clear-state` | Relevant if the `--state` parameter is specified. Clears the state file and restarts the download from the beginning. |  |
| `--dry-run` | Do not execute loading queries, but only display their text. |  |

### Common parameters of the import command {#load_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--upload-threads <value>` or `-t <value>` | The number of execution threads for data preparation. | The number of available cores on the client. |
| `--bulk-size <value>` | The size of the chunk for sending data, in rows. | 10000 |
| `--max-in-flight <value>` | The maximum number of data chunks that can be processed simultaneously. | 128 |
| `--file-output-path <value>` or `-f <path>` | If this option is set, the data will not be loaded into the database, but will be saved to the directory<br>. |  |

## Run a load test {#run}

Run the load:

```bash
ydb workload clickbench --path clickbench/hits run
```

During the test, load statistics are displayed for each request.

See the command description to run the load:

```bash
ydb workload clickbench run --help
```

### Common parameters for all load types {#run_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--dry-run` | Do not execute initialization queries, but only display their text. |  |
| `--check-canonical` or `-c` | Use special version of queries (they have deterministic answers) and compare results with canonical ones. |  |
| `--output <value>` | The name of the file where the query execution results will be saved. | `results.out` |
| `--iterations <value>` | The number of times each load query will be executed. | `1` |
| `--json <name>` | The name of the file where query execution statistics will be saved in `json` format. | Not saved by default |
| `--ministat <name>` | The name of the file where query execution statistics will be saved in `ministat` format. | Not saved by default |
| `--csv <name>` | The name of the file to save the CSV version of the result table. | Not saved by default |
| `--plan <name>` | The name of the file to save the query plan. Files like `<name>.<query number>.explain` and `<name>.<query number>.<iteration number>` will be saved in formats: `ast`, `json`, `svg`, and `table`. | Not saved by default |
| `--query-prefix <setting>` | Query prefix. Every prefix is a line that will be added to the beginning of each query. For multiple prefix lines use this option several times. | Not specified by default |
| `--retries` | Max retry count for every request. | `0` |
| `--include` | Names, numbers or ranges of query numbers to be executed as part of the load. Specified as a comma-separated list, e.g.: `1,2,4-6`. | All queries executed |
| `--exclude` | Names, numbers or ranges of query numbers to be excluded from the load. Specified as a comma-separated list, e.g.: `1,2,4-6`. | None excluded by default |
| `--verbose` or `-v` | Print additional information to the screen during query execution. |  |
| `--global-timeout <value>` | Global timeout for all queries. Supports time units (e.g., '5s', '1m'). Plain number interpreted as milliseconds. | Not specified by default. The time is unlimited. |
| `--request-timeout <value>` | Timeout for each iteration of each query. Supports time units (e.g., '5s', '1m'). Plain number interpreted as milliseconds. | Not specified by default. The time is unlimited. |
| `--threads <value>` or `-t <value>` | The number of parallel threads generating the load. Zero means that queries will be executed in the main thread; otherwise, queries will be mixed. | `0` |

### ClickBench-specific options {#run_clickbench_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--syntax <value>` | Syntax of the queries to use. Available values: `yql`. For more information about working with YQL syntax, see [here](../../yql/reference/index.md). | `yql` |

## Cleanup test data {#cleanup}

Run cleanup:

```bash
ydb workload clickbench --path clickbench/hits clean
```

The command has no parameters.
