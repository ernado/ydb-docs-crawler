---
title: "Data formats"
url: "https://ydb.tech/docs/en/reference/ydb-sdk/data-formats/?version=v26.1"
doc_path: "en/reference/ydb-sdk/data-formats/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-sdk/data-formats/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-sdk/data-formats/index.md"
description: "YDB supports several data representation formats and schema return modes for queries executed through QueryService. The format and schema return mode are set wh"
revision: "6a967ac39a5eac92f33ed9e017b7e5e4482fb785"
---

# Data formats

YDB supports several data representation formats and schema return modes for queries executed through QueryService. The format and schema return mode are set when the query runs and apply to every statement that returns data (for example, a [SELECT](../../../yql/reference/syntax/select/index.md) statement or the `RETURNING` clause). How you configure these settings may differ across SDKs.

## Data representation formats {#data-formats-list}

The following sections describe the available data representation formats:

- [Protobuf (Value)](format-protobuf.md) — the default format; rows are returned one by one with automatic conversion to native types in your programming language.
- [Apache Arrow](format-arrow.md) — a columnar format for analytics workloads and high-throughput transfer of large result sets.

## Schema return modes {#schema-inclusion-mode}

When a query runs as a stream, results arrive in parts. The schema return mode controls which parts of the stream include schema information.

- **Always (default)** — the data schema is included in every part of the result stream. Convenient when each part is processed independently.
- **First only** — the data schema is included only in the first part of the stream for each result set; later parts omit it. Reduces metadata volume when you stream large results.

The exact schema payload depends on the data format; each format’s section describes what is returned.
