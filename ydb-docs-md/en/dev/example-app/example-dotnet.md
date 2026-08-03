---
title: "Example app in C# (.NET)"
url: "https://ydb.tech/docs/en/dev/example-app/example-dotnet?version=v26.1"
doc_path: "en/dev/example-app/example-dotnet"
version: "v26.1"
lang: "en"
source_path: "en/core/dev/example-app/example-dotnet.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/dev/example-app/example-dotnet.md"
description: "Example app in C# (.NET). This page contains a detailed description of the code of a test app that uses the YDB C# (.NET) SDK."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Example app in C# (.NET)

This page contains a detailed description of the code of a [test app](https://github.com/ydb-platform/ydb-dotnet-examples) that uses the YDB [C# (.NET) SDK](https://github.com/ydb-platform/ydb-dotnet-sdk).

## Initializing a database connection {#init}

To interact with YDB, create instances of the driver, client, and session:

- The YDB driver facilitates interaction between the app and YDB nodes at the transport layer. It must be initialized before creating a client or session and must persist throughout the YDB access lifecycle.
- The YDB client operates on top of the YDB driver and enables the handling of entities and transactions.
- The YDB session, which is part of the YDB client context, contains information about executed transactions and prepared queries.

App code snippet for connecting to the database:

```c#
using Ydb.Sdk.Ado;

await using var dataSource = new YdbDataSource("Host=localhost;Port=2136;Database=/local");
await using var connection = await dataSource.OpenConnectionAsync();
```

## Creating tables {#create-table}

Create tables to be used in operations on a test app. This step results in the creation of database tables for the series directory data model:

- `Series`
- `Seasons`
- `Episodes`

After the tables are created, a method for retrieving information about data schema objects is called, and the result of its execution is displayed.

To create tables, use `YdbCommand` with a DDL (Data Definition Language) YQL query:

```c#
await using var command = new YdbCommand(connection)
{
    CommandText = @"
        CREATE TABLE series (
            series_id Uint64 NOT NULL,
            title Utf8,
            series_info Utf8,
            release_date Date,
            PRIMARY KEY (series_id)
        );

        CREATE TABLE seasons (
            series_id Uint64,
            season_id Uint64,
            title Utf8,
            first_aired Date,
            last_aired Date,
            PRIMARY KEY (series_id, season_id)
        );

        CREATE TABLE episodes (
            series_id Uint64,
            season_id Uint64,
            episode_id Uint64,
            title Utf8,
            air_date Date,
            PRIMARY KEY (series_id, season_id, episode_id)
        );"
};
await command.ExecuteNonQueryAsync();
```

## Adding data {#write-queries}

Add data to the created tables using the [`UPSERT`](../../yql/reference/syntax/upsert_into.md) statement in [YQL](../../yql/reference/index.md). A data update request is sent to the server as a single request with transaction auto-commit mode enabled.

Code snippet for data insert/update:

```c#
await using var command = new YdbCommand(@"
    UPSERT INTO series (series_id, title, release_date) VALUES
        ($id, $title, $release_date);
    ", connection);
command.Parameters.Add(new YdbParameter("$id", YdbDbType.Uint64, 1UL));
command.Parameters.Add(new YdbParameter("$title", YdbDbType.Text, "NewTitle"));
command.Parameters.Add(new YdbParameter("$release_date", YdbDbType.Date, DateTime.UtcNow));
await command.ExecuteNonQueryAsync();
```

## Retrieving data {#query-processing}

Retrieve data using a [`SELECT`](../../yql/reference/syntax/select/index.md) statement in [YQL](../../yql/reference/index.md). Handle the retrieved data selection in the app.

To read data with a YQL query, use the `ExecuteReaderAsync` method. Query parameters are passed through the `Parameters` collection of the `YdbCommand` object:

```c#
await using var command = new YdbCommand(@"
    SELECT
        series_id,
        title,
        release_date
    FROM series
    WHERE series_id = $id;
    ", connection);
command.Parameters.Add(new YdbParameter("$id", YdbDbType.Uint64, id));
await using var reader = await command.ExecuteReaderAsync();
```

### Processing execution results {#results-processing}

The query result is processed via `DbDataReader`. Example of processing the result:

```c#
while (await reader.ReadAsync())
{
    Console.WriteLine($"> Series, " +
        $"series_id: {reader.GetUint64(0)}, " +
        $"title: {reader.GetString(1)}, " +
        $"release_date: {reader.GetDateTime(2)}");
}
```

For sequential row reading from another query:

```c#
await using var command = new YdbCommand(
    "SELECT title FROM seasons ORDER BY series_id, season_id;", connection);
await using var reader = await command.ExecuteReaderAsync();
while (await reader.ReadAsync())
{
    Console.WriteLine(reader.GetString(0));
}
```
