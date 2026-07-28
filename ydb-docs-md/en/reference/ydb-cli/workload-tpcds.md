---
title: "TPC-DS workload"
url: "https://ydb.tech/docs/en/reference/ydb-cli/workload-tpcds?version=v26.1"
doc_path: "en/reference/ydb-cli/workload-tpcds"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/workload-tpcds.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/workload-tpcds.md"
description: "The workload is based on the TPC-DS specification, with the queries and table schemas adapted for YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# TPC-DS workload

The workload is based on the TPC-DS [specification](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v3.2.0.pdf), with the queries and table schemas adapted for YDB.

This benchmark generates a workload typical for decision support systems.

## Common command options

All commands support the common option `--path`, which specifies the path to the directory containing benchmark tables in the database:

```bash
ydb workload tpcds --path tpcds/s1 ...
```

### Available options {#common_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--path` or `-p` | Path to the directory with tables. | `/` |

## Initializing the load test {#init}

Before running the benchmark, create a table:

```bash
ydb workload tpcds --path tpcds/s1 init
```

See the command description to run the load:

```bash
ydb workload tpcds init --help
```

### Available parameters {#init_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--store <value>` | Table storage type. Possible values: `row`, `column`, `external-s3`. | `column` |
| `--external-s3-prefix <value>` | Relevant only for external tables. Root path to the dataset in S3 storage. |  |
| `--external-s3-endpoint <value>` or `-e <value>` | Relevant only for external tables. Link to the S3 bucket with data. |  |
| `--string` | Use the `String` type for text fields. | `Utf8` |
| `--datetime` | Use for time-related fields of type `Date`, `Datetime`, and `Timestamp`. | `Date32`, `Datetime64`, `Timestamp64` |
| `--partition-size` | Maximum partition size in megabytes (AUTO_PARTITIONING_PARTITION_SIZE_MB) for row tables. | 2000 |
| `--float-mode <value>` | Specifies the data type to use for fractional fields. Possible values are `double` and `decimal`. `double` uses the `Double` type, `decimal` uses `Decimal` with dimensions specified by the test standard. | `double` |
| `--scale` | Sets the percentage of the benchmark's data size and workload to use, relative to full scale. | 1 |
| `--clear` | If the table at the specified path already exists, it will be deleted. |  |

## Loading data into the table {#load}

The data will be generated and loaded into the table directly by YDB CLI:

```bash
ydb workload tpcds --path tpcds/s1 import generator --scale 1
```

See the command description:

```bash
ydb workload tpcds import --help
```

### Available options {#load_files_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--scale <value>` | Data scale. Typically, powers of ten are used. Also supports fractional scale, which is not described in the TPC-DS specification. It can be useful for quickly testing small YDB databases. Examples: `0.1`, `0.3`. |  |
| `--tables <value>` | Comma-separated list of tables to generate. Available tables: `customer`, `nation`, `order_line`, `part_psupp`, `region`, `supplier`. | All tables |
| `--process-count <value>` or `-C <value>` | Specifies the number of processes for parallel data generation. | `1` |
| `--process-index <value>` or `-i <value>` | Specifies the process number when data generation is split into multiple processes. | `0` |
| `--state <path>` | Path to the state file for resuming generation. If the generation is interrupted, it will resume from the same point when restarted. |  |
| `--clear-state` | Relevant if the `--state` parameter is specified. Clears the state file and restarts the download from the beginning. |  |
| `--dry-run` | Do not execute loading queries, but only display their text. |  |

### Common parameters of the import command {#load_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--upload-threads <value>` or `-t <value>` | The number of execution threads for data preparation. | The number of available cores on the client. |
| `--bulk-size <value>` | The size of the chunk for sending data, in rows. | 10000 |
| `--max-in-flight <value>` | The maximum number of data chunks that can be processed simultaneously. | 128 |
| `--file-output-path <value>` or `-f <path>` | If this option is set, the data will not be loaded into the database, but will be saved to the directory<br>. |  |

## Run the load test {#run}

Run the load:

```bash
ydb workload tpcds --path tpcds/s1 run
```

During the benchmark, load statistics are displayed for each request.

See the command description:

```bash
ydb workload tpcds run --help
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

### TPC-DS-specific options {#run_tpcds_options}

| Name | Description | Default value |
| --- | --- | --- |
| `--syntax <value>` | Syntax of the queries to use. Available values: `yql`. For more information about working with YQL syntax, see [here](../../yql/reference/index.md). | `yql` |
| `--float-mode <value>` | Float mode. Can be `float`, `decimal` or `decimal_ydb`. If the value is `float` - float will be used, `decimal` means that decimal with canonical size specified in the TPC-DS specification (`Decimal(12, 2)`) will be used, and `decimal_ydb` means that all float will be converted to `Decimal(22, 9)`. For more information about the Decimal type, see [documentation](../../yql/reference/types/primitive.md#numeric). | `float` |
| `--scale <value>` | Scale factor. See the TPC-DS specification, chapter 3. Used in TPC-DS queries. Also supports fractional scale, which is not described in the TPC-DS specification. It can be useful for quickly testing small YDB databases. Examples: `0.1`, `0.3`. For scale factors `1`, `10`, `100`, `1000` canonical answers are specified (see the `--check-canonical` option description). | 1 |

## Test data cleanup {#cleanup}

Run cleanup:

```bash
ydb workload tpcds --path tpcds/s1 clean
```

The command has no parameters.
