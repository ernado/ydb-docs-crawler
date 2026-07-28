---
title: "Configuring Time to Live (TTL)"
url: "https://ydb.tech/docs/en/recipes/ydb-cli/ttl?version=v26.1"
doc_path: "en/recipes/ydb-cli/ttl"
version: "v26.1"
lang: "en"
source_path: "en/core/recipes/ydb-cli/ttl.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/recipes/ydb-cli/ttl.md"
description: "This section contains recipes for configuration of table's TTL with YDB CLI. Enabling TTL for an existing table."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Configuring Time to Live (TTL)

This section contains recipes for configuration of table's TTL with YDB CLI.

## Enabling TTL for an existing table {#enable-on-existent-table}

In the example below, the items of the `mytable` table will be deleted an hour after the time set in the `created_at` column:

```bash
$ ydb -e <endpoint> -d <database> table ttl set --column created_at --expire-after 3600 mytable
```

The example below shows how to use the `modified_at` column with a numeric type (`Uint32`) as a TTL column. The column value is interpreted as the number of seconds since the Unix epoch:

```bash
$ ydb -e <endpoint> -d <database> table ttl set --column modified_at --expire-after 3600 --unit seconds mytable
```

## Enabling data eviction to S3-compatible external storage

> [!WARNING]
> Supported only for [column-oriented](../../concepts/datamodel/table.md#column-oriented-tables) tables. Support for [row-oriented](../../concepts/datamodel/table.md#row-oriented-tables) tables is currently under development.

To enable data eviction, an [external data source](../../concepts/datamodel/external_data_source.md) object that describes a connection to the external storage is needed. Refer to [YQL recipe](../../yql/reference/recipes/ttl.md#enable-tiering-on-existing-tables) for examples of creating an external data source.

The example below shows how to enable data eviction by executing a YQL-query from YDB CLI. Rows of the table `mytable` will be moved to the bucket described in the external data source `/Root/s3_cold_data` one hour after the time recorded in the column `created_at` and will be deleted after 24 hours.

```bash
$ ydb -e <endpoint> -d <database> sql -s '
    ALTER TABLE `mytable` SET (
        TTL =
            Interval("PT1H") TO EXTERNAL DATA SOURCE `/Root/s3_cold_data`,
            Interval("PT24H") DELETE
        ON modified_at AS SECONDS
    );
'
```

## Disabling TTL {#disable}

```bash
$ ydb -e <endpoint> -d <database> table ttl reset mytable
```

## Getting TTL settings {#describe}

The current TTL settings can be obtained from the table description:

```bash
$ ydb -e <endpoint> -d <database> scheme describe mytable
```
