---
title: "Отображение типов при чтении и записи данных в формате Parquet"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/s3/arrow_types_mapping?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/s3/arrow_types_mapping"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/s3/arrow_types_mapping.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/s3/arrow_types_mapping.md"
description: "При чтении и записи данных в формате Parquet YDB использует логическую схему типов Apache Arrow — стандарт, применяемый в Parquet для описания семантики данных."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Отображение типов при чтении и записи данных в формате Parquet

При чтении и записи данных в формате Parquet YDB использует логическую схему типов Apache Arrow — стандарт, применяемый в Parquet для описания семантики данных. Ниже приведено соответствие между типами YQL и логическими типами Arrow, которые записываются в Parquet-файл.

| Тип YQL | Тип Arrow при экспорте | Тип Arrow при импорте | Комментарий |
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
| `Date` | `UINT16` | `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `DATE`, `TIMESTAMP (s, ms, us)` | количество дней, прошедших с начала [Unix-эпохи](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F) |
| `Date32` | `DATE (s)` | `DATE (s)` |  |
| `Datetime` | `UINT32` | `UINT16`, `INT32`, `UINT32`, `INT64`, `UINT64`, `DATE`, `TIMESTAMP (s, ms, us)` | количество секунд, прошедших с начала [Unix-эпохи](https://ru.wikipedia.org/wiki/Unix-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F) |
| `Datetime64` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Timestamp` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Timestamp64` | `TIMESTAMP (us)` | `TIMESTAMP (s, ms, us)` |  |
| `Decimal(s, p)` | `DECIMAL (128, s, p)` | `DECIMAL (128, s, p)` |  |
| `String` | `BINARY` | `BINARY` |  |
| `Utf8` | `BINARY` | `BINARY` |  |
| `Json` | `BINARY` | `BINARY` |  |
