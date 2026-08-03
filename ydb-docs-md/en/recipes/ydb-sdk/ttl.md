---
title: "Configuring Time to Live (TTL)"
url: "https://ydb.tech/docs/en/recipes/ydb-sdk/ttl?version=v26.1"
doc_path: "en/recipes/ydb-sdk/ttl"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-sdk/ttl.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-sdk/ttl.md"
description: "This section contains recipes for configuration of table's TTL with YDB SDK. Enabling TTL for an existing table."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Configuring Time to Live (TTL)

This section contains recipes for configuration of table's TTL with YDB SDK.

## Enabling TTL for an existing table {#enable-on-existent-table}

In the example below, the items of the `mytable` table will be deleted an hour after the time set in the `created_at` column:

{% list tabs %}

- C++

  ```c++
  session.AlterTable(
    "mytable",
    TAlterTableSettings()
      .BeginAlterTtlSettings()
        .Set("created_at", TDuration::Hours(1))
      .EndAlterTtlSettings()
  );
  ```

- Go

  ```go
  err := session.AlterTable(ctx, "mytable",
    options.WithSetTimeToLiveSettings(
      options.NewTTLSettings().ColumnDateType("created_at").ExpireAfter(time.Hour),
    ),
  )
  ```

- Python

  ```python
  session.alter_table('mytable', set_ttl_settings=ydb.TtlSettings().with_date_type_column('created_at', 3600))
  ```

- JavaScript

  This section is under development.

- Java

  ```java
  AlterTableSettings settings = new AlterTableSettings()
          .setTableTtl(TableTtl.dateTimeColumn("created_at", 3600));

  session.alterTable("mytable", settings).join().expectSuccess();
  ```

{% endlist %}

The example below shows how to use the `modified_at` column with a numeric type (`Uint32`) as a TTL column. The column value is interpreted as the number of seconds since the Unix epoch:

{% list tabs %}

- C++

  ```c++
  session.AlterTable(
    "mytable",
    TAlterTableSettings()
      .BeginAlterTtlSettings()
        .Set("modified_at", TTtlSettings::EUnit::Seconds, TDuration::Hours(1))
      .EndAlterTtlSettings()
  );
  ```

- Go

  ```go
  err := session.AlterTable(ctx, "mytable",
    options.WithSetTimeToLiveSettings(
      options.NewTTLSettings().ColumnSeconds("modified_at").ExpireAfter(time.Hour),
    ),
  )
  ```

- Python

  ```python
  session.alter_table('mytable', set_ttl_settings=ydb.TtlSettings().with_value_since_unix_epoch('modified_at', UNIT_SECONDS, 3600))
  ```

- JavaScript

  This section is under development.

- Java

  ```java
  AlterTableSettings settings = new AlterTableSettings()
          .setTableTtl(TableTtl.valueSinceUnixEpoch(
                  "modified_at",
                  TableTtl.TtlUnit.SECONDS,
                  3600
          ));

  session.alterTable("mytable", settings).join().expectSuccess();
  ```

{% endlist %}

## Enabling data eviction to S3-compatible external storage {#enable-tiering-on-existing-tables}

> [!WARNING]
> Supported only for [column-oriented](../../concepts/datamodel/table.md#column-oriented-tables) tables. Support for [row-oriented](../../concepts/datamodel/table.md#row-oriented-tables) tables is currently under development.

To enable data eviction, an [external data source](../../concepts/datamodel/external_data_source.md) object that describes a connection to the external storage is needed. Refer to [YQL recipe](../../yql/reference/recipes/ttl.md#enable-tiering-on-existing-tables) for examples of creating an external data source.

In the following example, rows of the table `mytable` will be moved to the bucket described in the external data source `/Root/s3_cold_data` one hour after the time recorded in the column `created_at` and will be deleted after 24 hours:

{% list tabs %}

- C++

  ```c++
  session.AlterTable(
      "mytable",
      TAlterTableSettings()
          .BeginAlterTtlSettings()
              .Set("created_at", {
                      TTtlTierSettings(TDuration::Hours(1), TTtlEvictToExternalStorageAction("/Root/s3_cold_data")),
                      TTtlTierSettings(TDuration::Hours(24), TTtlDeleteAction("/Root/s3_cold_data"))
                  })
          .EndAlterTtlSettings()
  );
  ```

- Java

  This functionality is not currently supported.

- Go

  This functionality is not currently supported.

- Python

  This functionality is not currently supported.

- JavaScript

  This section is under development.

{% endlist %}

## Enabling TTL for a newly created table {#enable-for-new-table}

For a newly created table, you can pass TTL settings along with the table description:

{% list tabs %}

- C++

  ```c++
  session.CreateTable(
    "mytable",
    TTableBuilder()
      .AddNullableColumn("id", EPrimitiveType::Uint64)
      .AddNullableColumn("expire_at", EPrimitiveType::Timestamp)
      .SetPrimaryKeyColumn("id")
      .SetTtlSettings("expire_at")
      .Build()
  );
  ```

- Go

  ```go
  err := session.CreateTable(ctx, "mytable",
    options.WithColumn("id", types.Optional(types.TypeUint64)),
    options.WithColumn("expire_at", types.Optional(types.TypeTimestamp)),
    options.WithTimeToLiveSettings(
      options.NewTTLSettings().ColumnDateType("expire_at"),
    ),
  )
  ```

- Python

  ```python
  session.create_table(
    'mytable',
    ydb.TableDescription()
      .with_column(ydb.Column('id', ydb.OptionalType(ydb.DataType.Uint64)))
      .with_column(ydb.Column('expire_at', ydb.OptionalType(ydb.DataType.Timestamp)))
      .with_primary_key('id')
      .with_ttl(ydb.TtlSettings().with_date_type_column('expire_at'))
  )
  ```

- JavaScript

  This section is under development.

- Java

  ```java
  TableDescription description = TableDescription.newBuilder()
          .addNullableColumn("id", PrimitiveType.Uint64)
          .addNullableColumn("expire_at", PrimitiveType.Timestamp)
          .setPrimaryKey("id")
          .setTtlSettings(TableTtl.dateTimeColumn("expire_at", 0))
          .build();

  session.createTable("mytable", description).join().expectSuccess();
  ```

{% endlist %}

## Disabling TTL {#disable}

{% list tabs %}

- C++

  ```c++
  session.AlterTable(
    "mytable",
    TAlterTableSettings()
      .BeginAlterTtlSettings()
        .Drop()
      .EndAlterTtlSettings()
  );
  ```

- Go

  ```go
  err := session.AlterTable(ctx, "mytable",
    options.WithDropTimeToLive(),
  )
  ```

- Python

  ```python
  session.alter_table('mytable', drop_ttl_settings=True)
  ```

- JavaScript

  This section is under development.

- Java

  ```java
  AlterTableSettings settings = new AlterTableSettings()
          .setTableTtl(TableTtl.notSet());

  session.alterTable("mytable", settings).join().expectSuccess();
  ```

{% endlist %}

## Getting TTL settings {#describe}

The current TTL settings can be obtained from the table description:

{% list tabs %}

- C++

  ```c++
  auto desc = session.DescribeTable("mytable").GetValueSync().GetTableDescription();
  auto ttl = desc.GetTtlSettings();
  ```

- Go

  ```go
  desc, err := session.DescribeTable(ctx, "mytable")
  if err != nil {
    // process error
  }
  ttl := desc.TimeToLiveSettings
  ```

- Python

  ```python
  desc = session.describe_table('mytable')
  ttl = desc.ttl_settings
  ```

- JavaScript

  This section is under development.

- Java

  ```java
  TableTtl ttl = session.describeTable("mytable").join().getValue().getTableDescription().getTableTtl();
  ```

{% endlist %}
