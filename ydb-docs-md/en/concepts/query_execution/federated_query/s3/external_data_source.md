---
title: "Working with S3 Buckets (Yandex Object Storage)"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/s3/external_data_source?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/s3/external_data_source"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/s3/external_data_source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/s3/external_data_source.md"
description: "To work with S3, you need to set up a data storage connection. There is a DDL for configuring such connections. Next, let's look at the SQL syntax and the manag"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Working with S3 Buckets (Yandex Object Storage)

To work with S3, you need to set up a data storage connection. There is a DDL for configuring such connections. Next, let's look at the SQL syntax and the management of these settings.

There are two types of buckets in S3: public and private. To connect to a public bucket, use `AUTH_METHOD="NONE"`. To connect to a private bucket, use `AUTH_METHOD="AWS"`. A detailed description of `AWS` can be found [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-authentication-methods.html). `AUTH_METHOD="NONE"` means that no authentication is used. If `AUTH_METHOD="AWS"` is specified, several additional parameters are required:

- `AWS_ACCESS_KEY_ID_SECRET_PATH` — the [secret](../../../datamodel/secrets.md) where `AWS_ACCESS_KEY_ID` is stored.
- `AWS_SECRET_ACCESS_KEY_SECRET_PATH` — the [secret](../../../datamodel/secrets.md) where `AWS_SECRET_ACCESS_KEY` is stored.
- `AWS_REGION` – region from which reading is performed, for example, `ru-central-1`.

To set up a connection to a public bucket, execute the following SQL query. The query creates an external connection named `object_storage`, which points to a specific S3 bucket named `bucket`.

```yql
CREATE EXTERNAL DATA SOURCE object_storage WITH (
  SOURCE_TYPE="ObjectStorage",
  LOCATION="https://object_storage_domain/bucket/",
  AUTH_METHOD="NONE"
);
```

To set up a connection to a private bucket, you need to run a few SQL queries. First, create [secrets](../../../datamodel/secrets.md) containing `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

```yql
CREATE SECRET aws_access_id WITH (value='<id>');
CREATE SECRET aws_access_key WITH (value='<key>');
```

The next step is to create an external connection named `object_storage`, which points to a specific S3 bucket named `bucket` and uses `AUTH_METHOD="AWS"`. The parameters `AWS_ACCESS_KEY_ID_SECRET_PATH`, `AWS_SECRET_ACCESS_KEY_SECRET_PATH`, and `AWS_REGION` are filled in for `AWS`. The values of these parameters are described above.

```yql
CREATE EXTERNAL DATA SOURCE object_storage WITH (
  SOURCE_TYPE="ObjectStorage",
  LOCATION="https://object_storage_domain/bucket/",
  AUTH_METHOD="AWS",
  AWS_ACCESS_KEY_ID_SECRET_PATH="aws_access_id",
  AWS_SECRET_ACCESS_KEY_SECRET_PATH="aws_access_key",
  AWS_REGION="ru-central-1"
);
```

## Using an External Connection to an S3 Bucket {#external-data-source-settings}

When working with Yandex Object Storage using [external data sources](../../../datamodel/external_data_source.md), it is convenient to perform prototyping and initial data connection setup.

An example query to read data:

```yql
SELECT
  *
FROM
 object_storage.`*.tsv`
WITH
(
  FORMAT = "tsv_with_names",
  SCHEMA =
  (
    ts Uint32,
    action Utf8
  )
);
```

The list of supported formats and data compression algorithms for reading data in S3 (Yandex Object Storage) is provided in the section [Data Formats and Compression Algorithms](formats.md).

## Data Model {#data_model}

In Yandex Object Storage, data is stored in files. To read data, you need to specify the data format in the files, compression, and lists of fields. This is done using the following SQL expression:

```yql
SELECT
  <expression>
FROM
  <object_storage_connection_name>.`<file_path>`
WITH(
  FORMAT = "<file_format>",
  COMPRESSION = "<compression>",
  SCHEMA = (<schema_definition>),
  <format_settings>)
WHERE
  <filter>;
```

Where:

- `object_storage_connection_name` — the name of the external data source leading to the S3 bucket (Yandex Object Storage).
- `file_path` — the path to the file or files inside the bucket. Wildcards `*` are supported; more details [in the section](external_data_source.md#path_format).
- `file_format` — the [data format](formats.md#formats) in the files.
- `compression` — the [compression format](formats.md#compression_formats) of the files.
- `schema_definition` — the [schema definition](external_data_source.md#schema) of the data stored in the files.
- `format_settings` — optional [format settings](external_data_source.md#format_settings)

### Data Schema Description {#schema}

The data schema description consists of a set of fields:

- Field name.
- Field type.
- Required data flag.

For example, the data schema below describes a schema field named `Year` of type `Int32` with the requirement that this field must be present in the data:

```text
Year Int32 NOT NULL
```

If a data field is marked as required (`NOT NULL`) but is missing in the processed file, processing such a file will result in an error. If a field is marked as optional (`NULL`), no error will occur if the field is absent in the processed file, but the field will take the value `NULL`. The keyword `NULL` is optional in this context.

### Schema Inference {#inference}

YDB can determine the data schema of the files inside the bucket so that you do not have to specify these fields manually.

> [!NOTE]
> Schema inference is available for all [data formats](formats.md#formats) except `raw` and `json_as_string`. For these formats you must [describe the schema manually](external_data_source.md#schema).

To enable schema inference, use the `WITH_INFER` parameter:

```yql
SELECT
  <expression>
FROM
  <object_storage_connection_name>.`<file_path>`
WITH(
  FORMAT = "<file_format>",
  COMPRESSION = "<compression>",
  WITH_INFER = "true")
WHERE
  <filter>;
```

Where:

- `object_storage_connection_name` — the name of the external data source leading to the S3 bucket (Yandex Object Storage).
- `file_path` — the path to the file or files inside the bucket. Wildcards `*` are supported. For more information, see [Data Path Formats Specified in `file_path`](external_data_source.md#path_format).
- `file_format` — the [data format](formats.md#formats) in the files. All formats except `raw` and `json_as_string` are supported.
- `compression` — the [compression format](formats.md#compression_formats) of the files.

As a result of executing such a query, the names and types of fields will be inferred.

### Data Path Formats Specified in `file_path` {#path_format}

In YDB, the followingdata paths are supported:

| Path Format | Description | Example |
| --- | --- | --- |
| Path ends with a `/` | Path to a directory | The path `/a/` addresses all contents of the directory:  <br>`/a/b/c/d/1.txt`  <br>`/a/b/2.csv` |
| Path contains a wildcard character `*` | Any files nested in the path | The path `/a/*.csv` addresses files in directories:  <br>`/a/b/c/1.csv`  <br>`/a/2.csv`  <br>`/a/b/c/d/e/f/g/2.csv` |
| Path does not end with `/` and does not contain wildcard characters | Path to a single file | The path `/a/b.csv` addresses the specific file `/a/b.csv` |

### Format Settings {#format_settings}

In YDB, the following format settings are supported:

| Setting name | Description | Possible values |
| --- | --- | --- |
| `file_pattern` | File name template | File name template string. Wildcards `*` are supported. |
| `data.interval.unit` | Unit for parsing `Interval` type | `MICROSECONDS`, `MILLISECONDS`, `SECONDS`, `MINUTES`, `HOURS`, `DAYS`, `WEEKS` |
| `data.datetime.format_name` | Predefined format in which `Datetime` data is stored | `POSIX`, `ISO` |
| `data.datetime.format` | Strftime-like template which defines how `Datetime` data is stored | Formatting string, for example: `%Y-%m-%dT%H-%M` |
| `date.timestamp.format_name` | Predefined format in which `Timestamp` data is stored | `POSIX`, `ISO`, `UNIX_TIME_SECONDS`, `UNIX_TIME_MILLISECONDS`, `UNIX_TIME_MICROSECONDS` |
| `data.timestamp.format` | Strftime-like template which defines how `Timestamp` data is stored | Formatting string, for example: `%Y-%m-%dT%H-%M-%S` |
| `data.date.format` | The format in which `Date` data is stored | Formatting string, for example: `%Y-%m-%d` |
| `csv_delimiter` | Delimeter for `csv_with_names` format | Any character (UTF-8) |

You can only specify `file_pattern` setting if `file_path` is a path to a directory. Any conversion specifiers supported by [`strftime`(C99)](https://en.cppreference.com/w/c/chrono/strftime) function can be used in formatting strings. In YDB, the following `Datetime` and `Timestamp` formats are supported:

| Name | Description | Example |
| --- | --- | --- |
| `POSIX` | String in `%Y-%m-%d %H:%M:%S` format | 2001-03-26 16:10:00 |
| `ISO` | Format, corresponding to the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard | 2001-03-26 16:10:00Z |
| `UNIX_TIME_SECONDS` | Number of seconds that have elapsed since the 1st of january 1970 (00:00:00 UTC) | 985623000 |
| `UNIX_TIME_MILLISECONDS` | Number of milliseconds that have elapsed since the 1st of january 1970 (00:00:00 UTC) | 985623000000 |
| `UNIX_TIME_MICROSECONDS` | Number of microseconds that have elapsed since the 1st of january 1970 (00:00:00 UTC) | 985623000000000 |

## Example {#read_example}

Example query to read data from S3 (Yandex Object Storage):

```yql
SELECT
  *
FROM
  connection.`folder/`
WITH(
  FORMAT = "csv_with_names",
  COMPRESSION="gzip"
  SCHEMA =
  (
    Id Int32 NOT NULL,
    UserId Int32 NOT NULL,
    TripDate Date NOT NULL,
    TripDistance Double NOT NULL,
    UserComment Utf8
  ),
  FILE_PATTERN="*.csv.gz",
  `DATA.DATE.FORMAT`="%Y-%m-%d",
  CSV_DELIMITER='/'
);
```

Where:

- `connection` — the name of the external data source leading to the S3 bucket (Yandex Object Storage).
- `folder/filename.csv` — the path to the directory in the S3 bucket (Yandex Object Storage).
- `SCHEMA` — the data schema description in the file.
- `*.csv.gz` — file name template.
- `%Y-%m-%d` — format in which `Date` type is stored in S3.
