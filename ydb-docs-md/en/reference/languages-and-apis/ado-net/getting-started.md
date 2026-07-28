---
title: "Getting Started with ADO.NET"
url: "https://ydb.tech/docs/en/reference/languages-and-apis/ado-net/getting-started?version=v26.1"
doc_path: "en/reference/languages-and-apis/ado-net/getting-started"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/languages-and-apis/ado-net/getting-started.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/languages-and-apis/ado-net/getting-started.md"
description: "The best way to use Ydb.Sdk is to install its NuGet package."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Getting Started with ADO.NET

The best way to use `Ydb.Sdk` is to install its [NuGet package](https://www.nuget.org/packages/Ydb.Sdk).

`Ydb.Sdk.Ado` aims to be fully ADO.NET-compatible; its API should feel almost identical to other .NET database drivers.

Here's a basic code snippet to get you started:

```c#
await using var ydbDataSource = new YdbDataSource("Host=localhost;Port=2136;Database=/local;MaxSessionPool=50");
await using var ydbConnection = await ydbDataSource.OpenConnectionAsync();

var ydbCommand = ydbConnection.CreateCommand();
ydbCommand.CommandText = """
                         SELECT series_id, season_id, episode_id, air_date, title
                         FROM episodes
                         WHERE series_id = @series_id AND season_id > @season_id
                         ORDER BY series_id, season_id, episode_id
                         LIMIT @limit_size;
                         """;
ydbCommand.Parameters.Add(new YdbParameter("series_id", DbType.UInt64, 1U));
ydbCommand.Parameters.Add(new YdbParameter("season_id", DbType.UInt64, 1U));
ydbCommand.Parameters.Add(new YdbParameter("limit_size", DbType.UInt64, 3U));

var ydbDataReader = await ydbCommand.ExecuteReaderAsync();

_logger.LogInformation("Selected rows:");
while (await ydbDataReader.ReadAsync())
{
    _logger.LogInformation(
        "series_id: {series_id}, season_id: {season_id}, episode_id: {episode_id}, air_date: {air_date}, title: {title}",
        ydbDataReader.GetUint64(0), ydbDataReader.GetUint64(1), ydbDataReader.GetUint64(2),
        ydbDataReader.GetDateTime(3), ydbDataReader.GetString(4));
}
```

You can find more info about the ADO.NET API in the [MSDN](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/ado-net-overview?redirectedfrom=MSDN) docs or in many tutorials on the Internet.
