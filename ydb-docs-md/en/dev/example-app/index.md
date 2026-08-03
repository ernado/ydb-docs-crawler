---
title: "Example applications working with YDB"
url: "https://ydb.tech/docs/en/dev/example-app/?version=v26.1"
doc_path: "en/dev/example-app/"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/example-app/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/example-app/index.md"
description: "Example applications working with YDB."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Example applications working with YDB

This section outlines the implementation of example applications, all designed to perform similar functions, using the YDB SDKs across various programming languages. Each app is developed to demonstrate how a respective SDK can be utilized in a specific language.

- [C++](example-cpp.md)
- [C# (.NET)](example-dotnet.md)
- [Go](go/index.md)
- [Java](java/index.md)
- [JavaScript](example-js.md)
- [Python](python/index.md)
- [Rust](rust/index.md)

Refer to [YDB SDK reference documentation](../../reference/ydb-sdk/index.md) for more details.

A test app performs the following steps:

## Initializing a database connection {#init}

To interact with YDB, create instances of the driver, client, and session:

- The YDB driver facilitates interaction between the app and YDB nodes at the transport layer. It must be initialized before creating a client or session and must persist throughout the YDB access lifecycle.
- The YDB client operates on top of the YDB driver and enables the handling of entities and transactions.
- The YDB session, which is part of the YDB client context, contains information about executed transactions and prepared queries.

[C++](example-cpp.md#init) | [C# (.NET)](example-dotnet.md#init) | [Go](go/index.md#init) | [Java](java/index.md#init) | JavaScript | [PHP](example-php.md#init) | [Python](python/index.md#init) | [Rust](rust/index.md#download)

## Creating tables {#create-table}

Create tables to be used in operations on a test app. This step results in the creation of database tables for the series directory data model:

- `Series`
- `Seasons`
- `Episodes`

After the tables are created, a method for retrieving information about data schema objects is called, and the result of its execution is displayed.

[C++](example-cpp.md#create-table) | [C# (.NET)](example-dotnet.md#create-table) | [Go](go/index.md#create-table) | [Java](java/index.md#create-table) | JavaScript | [PHP](example-php.md#create-table) | [Python](python/index.md#create-table) | [Rust](rust/index.md#query-client)

## Adding data {#write-queries}

Add data to the created tables using the [`UPSERT`](../../yql/reference/syntax/upsert_into.md) statement in [YQL](../../yql/reference/index.md). A data update request is sent to the server as a single request with transaction auto-commit mode enabled.

[C++](example-cpp.md#write-queries) | [C# (.NET)](example-dotnet.md#write-queries) | Go | [Java](java/index.md#write-queries) | JavaScript | [PHP](example-php.md#write-queries) | [Python](python/index.md#write-queries) | [Rust](rust/index.md#query-client)

## Retrieving data {#query-processing}

Retrieve data using a [`SELECT`](../../yql/reference/syntax/select/index.md) statement in [YQL](../../yql/reference/index.md). Handle the retrieved data selection in the app.

[C++](example-cpp.md#query-processing) | [C# (.NET)](example-dotnet.md#query-processing) | [Go](go/index.md#query-processing) | [Java](java/index.md#query-processing) | JavaScript | [PHP](example-php.md#query-processing) | [Python](python/index.md#query-processing) | [Rust](rust/index.md#query-client)

## Parameterized queries {#param-queries}

Query data using parameters. This query execution method is preferable because it allows the server to reuse the query execution plan for subsequent calls and protects against vulnerabilities such as [SQL injection](https://en.wikipedia.org/wiki/SQL_injection).

[C++](example-cpp.md#param-queries) | [C# (.NET)](example-dotnet.md#param-queries) | [Go](go/index.md#param-queries) | [Java](java/index.md#param-queries) | JavaScript | [PHP](example-php.md#param-queries) | [Python](python/index.md#param-queries) | [Rust](rust/index.md#query-client)

## Multistep transactions

Multiple statements can be executed within a single multistep transaction. Client-side code can run between query steps. Using a transaction ensures that queries executed in its context are consistent with each other.

[C++](example-cpp.md#multistep-transactions) | C# (.NET) | Go | [Java](java/index.md#multistep-transactions) | JavaScript | PHP | Python

## Managing transactions {#tcl}

Transactions are managed through [TCL](../../concepts/transactions.md) `Begin` and `Commit` calls.

In most cases, instead of explicitly using `Begin` and `Commit` calls, it's better to use transaction control parameters in execute calls. This allows to avoid additional requests to YDB server and thus run queries more efficiently.

[C++](example-cpp.md#tcl) | C# (.NET) | Go | [Java](java/index.md#tcl) | JavaScript | PHP | [Python](python/index.md#tcl) | [Rust](rust/index.md#query-client)

## Error handling

For more information about error handling, see [Error handling in the API](../../reference/ydb-sdk/error_handling.md).
