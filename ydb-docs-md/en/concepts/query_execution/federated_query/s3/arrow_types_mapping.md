---
title: "Mapping types when reading and writing Parquet data"
url: "https://ydb.tech/docs/en/concepts/query_execution/federated_query/s3/arrow_types_mapping?version=v26.1"
doc_path: "en/concepts/query_execution/federated_query/s3/arrow_types_mapping"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/query_execution/federated_query/s3/arrow_types_mapping.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/query_execution/federated_query/s3/arrow_types_mapping.md"
description: "When reading and writing data in Parquet format, YDB uses the Apache Arrow logical type system — the standard Parquet uses to describe data semantics. The table"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Mapping types when reading and writing Parquet data

When reading and writing data in Parquet format, YDB uses the Apache Arrow logical type system — the standard Parquet uses to describe data semantics. The table below shows how YQL types map to Arrow logical types written in Parquet files.

| YQL type | Arrow type on export | Arrow type on import | Notes |
| --- | --- | --- | --- |
| `Bool` | `UINT8` | `BOOL`, `UINT8` |  |
| `Int8` | `INT8` | `INT8` |  |
| `Int16` | `INT16` | `INT16` |  |
| `Int32` | `INT32` | `INT32` |  |
| `Int64` | `INT64` | `INT64` |  |
| `Uint8` | `UINT8` | `UINT8` |  |
| `Uint16` | `UINT16` | `UINT16` |  |
| `Uint32` | `UINT32` | `UINT32` |  |
| `Uint64` | `UINT64` | `UINT64` |  |
| `Float` | `FLOAT (32)` | `FLOAT (32)` |  |
| `Double` | `FLOAT (64)` | `FLOAT (64)` |  |
| `Date` | `UINT16` | `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `DATE`, `TIMESTAMP (s, ms, us)` | number of days since the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) |
| `Date32` | `DATE (s)` | `DATE (s)` |  |
| `Datetime` | `UINT32` | `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `DATE`, `TIMESTAMP (s, ms, us)` | number of seconds since the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) |
| `Datetime64` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Timestamp` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Timestamp64` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Decimal(s, p)` | `DECIMAL (128, s, p)` | `DECIMAL (128, s, p)` |  |
| `String` | `BINARY` | `BINARY` |  |
| `Utf8` | `BINARY` | `BINARY` |  |
| `Json` | `BINARY` | `BINARY` |  |
