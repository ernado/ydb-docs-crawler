---
title: "Example app in Rust"
url: "https://ydb.tech/docs/en/dev/example-app/rust/?version=v26.1"
doc_path: "en/dev/example-app/rust/"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/example-app/rust/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/example-app/rust/index.md"
description: "This page provides a detailed description of the code for a test app that uses the YDB Rust SDK. Downloading and starting."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Example app in Rust

This page provides a detailed description of the code for a [test app](https://github.com/ydb-platform/ydb-rs-sdk/tree/master/ydb/examples/basic) that uses the YDB [Rust SDK](https://github.com/ydb-platform/ydb-rs-sdk).

## Downloading and starting {#download}

[Git](https://git-scm.com/downloads) and [Rust](https://www.rust-lang.org/tools/install) 1.85+ are required. For SDK installation, see [Installing the YDB SDK](../../../reference/ydb-sdk/install.md).

Clone the repository:

```bash
git clone https://github.com/ydb-platform/ydb-rs-sdk.git
```

Start the example:

{% list tabs %}

- Local Docker

  To connect to a locally deployed YDB database according to the [Docker](../../../quickstart.md) use case, run the following command in the default configuration:

  ```bash
  export YDB_CONNECTION_STRING=grpc://localhost:2136/local
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

- Any database

  To run the example against any available YDB database, provide the [endpoint](../../../concepts/connect.md#endpoint) and the [database path](../../../concepts/connect.md#database).

  If authentication is enabled, choose an [authentication mode](../../../security/authentication.md) and set the corresponding environment variables.

  ```bash
  export <auth_mode_var>="<auth_mode_value>"
  export YDB_CONNECTION_STRING="<endpoint>/<database>"
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

  where

  - `<endpoint>`: The [endpoint](../../../concepts/connect.md#endpoint).
  - `<database>`: The [database path](../../../concepts/connect.md#database).
  - `<auth_mode_var>`: The [environment variable](../../../reference/ydb-sdk/auth.md#env) for the authentication mode.
  - `<auth_mode_value>`: The credential value for the selected mode.

  For example:

  ```bash
  export YDB_ACCESS_TOKEN_CREDENTIALS="t1.9euelZqOnJuJlc..."
  export YDB_CONNECTION_STRING="grpcs://ydb.example.com:2135/somepath/somelocation"
  cd ydb-rs-sdk/ydb
  cargo run --example basic
  ```

{% endlist %}

## Initializing a database connection {#init}

To interact with YDB, create instances of the driver, client, and session:

- The YDB driver facilitates interaction between the app and YDB nodes at the transport layer. It must be initialized before creating a client or session and must persist throughout the YDB access lifecycle.
- The YDB client operates on top of the YDB driver and enables the handling of entities and transactions.
- The YDB session, which is part of the YDB client context, contains information about executed transactions and prepared queries.

Import the crate and open a client:

```rust
use ydb::{ClientBuilder, YdbResult};

#[tokio::main]
async fn main() -> YdbResult<()> {
    let connection_string = std::env::var("YDB_CONNECTION_STRING")
        .unwrap_or_else(|_| "grpc://localhost:2136/local".to_string());

    let client = ClientBuilder::new_from_connection_string(connection_string)?.client()?;
    client.wait().await?;

    let mut qc = client.query_client().clone_with_idempotent_operations(true);
    // ...
    Ok(())
}
```

`ClientBuilder::new_from_connection_string` accepts a YDB connection string (`grpc://host:port/database`). `client.wait()` waits until the driver discovers cluster endpoints. `query_client()` is the entry point for the Query Service API.

By default, anonymous authentication is used for local Docker. For token auth, use [`ClientBuilder::with_credentials`](https://docs.rs/ydb/latest/ydb/struct.ClientBuilder.html) — see [authentication recipes](../../../recipes/ydb-sdk/auth.md).

## Query Service client {#query-client}

To run a single transactional SQL statement, use awaitable builders on [`QueryClient`](https://docs.rs/ydb/latest/ydb/struct.QueryClient.html):

- `qc.exec(yql)` — statement with no result set (DDL, DML).
- `qc.query_row(yql)` — exactly one row.
- `qc.query(yql).await?` — streaming [`QueryStream`](https://docs.rs/ydb/latest/ydb/struct.QueryStream.html) for large results.

Automatic retries are enabled via `clone_with_idempotent_operations(true)` for idempotent reads and DDL.

## Creating tables {#create-table}

Create tables to be used in operations on a test app. This step results in the creation of database tables for the series directory data model:

- `Series`
- `Seasons`
- `Episodes`

After the tables are created, a method for retrieving information about data schema objects is called, and the result of its execution is displayed.

Table creation (no explicit transaction control — implicit session, server-side DDL):

```rust
qc.exec(format!(
    "CREATE TABLE IF NOT EXISTS `{}` (
        series_id Bytes,
        title Text,
        series_info Text,
        release_date Date,
        comment Text,
        PRIMARY KEY(series_id)
    )",
    "native/query/series"
))
.await?;
```

## Adding data {#write-queries}

Add data to the created tables using the [`UPSERT`](../../../yql/reference/syntax/upsert_into.md) statement in [YQL](../../../yql/reference/index.md). A data update request is sent to the server as a single request with transaction auto-commit mode enabled.

Bulk load with `AS_TABLE` and typed parameters:

```rust
use ydb::{Value, ydb_struct};

let rows: Vec<Value> = /* ... */;
let list = Value::list_from(example_row, rows)?;
qc.exec("UPSERT INTO ... FROM AS_TABLE($seriesData);")
    .param("$seriesData", list)
    .await?;
```

## Retrieving data {#query-processing}

Retrieve data using a [`SELECT`](../../../yql/reference/syntax/select/index.md) statement in [YQL](../../../yql/reference/index.md). Handle the retrieved data selection in the app.

Read materialized result with snapshot read-only isolation:

```rust
use ydb::QueryTxMode;

let mut result = qc
    .query("SELECT series_id, title, release_date FROM `native/query/series`")
    .with_tx_mode(QueryTxMode::SnapshotReadOnly)
    .idempotent(true)
    .await?;

while let Some(result_set) = result.next_result_set().await? {
    for mut row in result_set {
        // extract columns from row
    }
}
result.close().await?;
```

## Parameterized queries {#param-queries}

Query data using parameters. This query execution method is preferable because it allows the server to reuse the query execution plan for subsequent calls and protects against vulnerabilities such as [SQL injection](https://en.wikipedia.org/wiki/SQL_injection).

Per-call parameters use `.param(name, value)` or the `ydb_params!` macro:

```rust
use ydb::ydb_params;

// one parameter at a time
qc.exec("UPSERT INTO `native/query/series` (series_id, title) VALUES ($id, $title)")
    .param("$id", b"series-1".to_vec())
    .param("$title", "Example title")
    .await?;

// several parameters via macro
qc.exec("UPSERT INTO `native/query/series` (series_id, title) VALUES ($id, $title)")
    .params(ydb_params!(
        "$id" => b"series-2".to_vec(),
        "$title" => "Another title",
    ))
    .await?;
```

## Managing transactions {#tcl}

Transactions are managed through [TCL](../../../concepts/transactions.md) `Begin` and `Commit` calls.

In most cases, instead of explicitly using `Begin` and `Commit` calls, it's better to use transaction control parameters in execute calls. This allows to avoid additional requests to YDB server and thus run queries more efficiently.

The Rust SDK does not expose explicit `Begin` / `Commit` to application code. Use `retry_transaction` with [`QueryTransactionOptions`](https://docs.rs/ydb/latest/ydb/struct.QueryTransactionOptions.html) for interactive transactions. For a single SQL statement, set isolation with `.with_tx_mode(...)`.

Single statement in snapshot read-only mode:

```rust
use ydb::QueryTxMode;

let mut row = qc
    .query_row("SELECT title FROM `native/query/series` WHERE series_id = $id")
    .param("$id", b"series-1".to_vec())
    .with_tx_mode(QueryTxMode::SnapshotReadOnly)
    .idempotent(true)
    .await?;
```

Interactive transaction with multiple operations:

```rust
use ydb::{QueryTransactionOptions, QueryTxMode};

let mut qc = qc.clone_with_transaction_options(
    QueryTransactionOptions::new().with_mode(QueryTxMode::SerializableReadWrite),
);

let title: String = qc
    .retry_transaction(async |tx| {
        let mut row = tx
            .query_row("SELECT title FROM `native/query/series` WHERE series_id = $id")
            .param("$id", b"series-1".to_vec())
            .await?;
        Ok(row.remove_field_by_name("title")?.try_into()?)
    })
    .await?;
```

By default, such calls use implicit transaction control — the server infers isolation from the SQL statement.
