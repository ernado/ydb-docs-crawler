---
title: "Adding or removing a changefeed"
url: "https://ydb.tech/docs/en/yql/reference/syntax/alter_table/changefeed?version=v26.1"
doc_path: "en/yql/reference/syntax/alter_table/changefeed"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/alter_table/changefeed.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/alter_table/changefeed.md"
description: "Warning. Supported only for row-oriented tables. Support for column-oriented tables is currently under development."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Adding or removing a changefeed

> [!WARNING]
> Supported only for [row-oriented](../../../../concepts/datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](../../../../concepts/datamodel/table.md#column-oriented-tables) tables is currently under development.

`ADD CHANGEFEED <name> WITH (<option> = <value>[, ...])`: Adds a [changefeed](../../../../concepts/cdc.md) with the specified name and options.

## Changefeed options

- `MODE`: Operation mode. Specifies what to write to a changefeed each time table data is altered.

  - `KEYS_ONLY`: Only the primary key components and change flag are written.
  - `UPDATES`: Updated column values that result from updates are written.
  - `NEW_IMAGE`: Any column values resulting from updates are written.
  - `OLD_IMAGE`: Any column values before updates are written.
  - `NEW_AND_OLD_IMAGES`: A combination of `NEW_IMAGE` and `OLD_IMAGE` modes. Any column values *prior to* and *resulting from* updates are written.

- `FORMAT`: Data write format.

  - `JSON`: Write data in [JSON](../../../../concepts/cdc.md#json-record-structure) format.
  - `DEBEZIUM_JSON`: Write data in the [Debezium-like JSON format](../../../../concepts/cdc.md#debezium-json-record-structure).

- `VIRTUAL_TIMESTAMPS`: Enabling/disabling [virtual timestamps](../../../../concepts/cdc.md#virtual-timestamps). Disabled by default.

- `BARRIERS_INTERVAL` — [barrier](../../../../concepts/cdc.md#barriers) emission interval. The value type is `Interval`. Disabled by default.

- `RETENTION_PERIOD`: [Record retention period](../../../../concepts/cdc.md#retention-period). The value type is `Interval` and the default value is 24 hours (`Interval('PT24H')`).

- `TOPIC_AUTO_PARTITIONING`: [Topic autopartitioning mode](../../../../concepts/cdc.md#topic-partitions):

  - `ENABLED` – An [autopartitioned topic](../../../../concepts/datamodel/topic.md#autopartitioning) will be created for this changefeed. The number of partitions in such a topic increases automatically as the table update rate increases. Topic autopartitioning parameters [can be configured](../alter-topic.md#alter-topic).
  - `DISABLED` – A topic without [autopartitioning](../../../../concepts/datamodel/topic.md#autopartitioning) will be created for this changefeed. This is the default value.

- `TOPIC_MIN_ACTIVE_PARTITIONS`: [The initial number of topic partitions](../../../../concepts/cdc.md#topic-partitions). By default, the initial number of topic partitions is equal to the number of table partitions. For autopartitioned topics, the number of partitions increases automatically as the table update rate increases.

- `INITIAL_SCAN`: Enables/disables [initial table scan](../../../../concepts/cdc.md#initial-scan). Disabled by default.

The code below adds a changefeed named `updates_feed`, where the values of updated table columns will be exported in JSON format:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES'
);
```

Records in this changefeed will be stored for 24 hours (default value). The code in the following example will create a changefeed with a record retention period of 12 hours:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    RETENTION_PERIOD = Interval('PT12H')
);
```

The example of creating a changefeed with enabled virtual timestamps:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    VIRTUAL_TIMESTAMPS = TRUE
);
```

The example of creating a changefeed with virtual timestamps and barriers every 10 seconds:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    VIRTUAL_TIMESTAMPS = TRUE,
    BARRIERS_INTERVAL = Interval('PT10S')
);
```

Example of creating a changefeed with initial scan:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    INITIAL_SCAN = TRUE
);
```

Example of creating a changefeed with autopartitioning:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    TOPIC_AUTO_PARTITIONING = 'ENABLED',
    TOPIC_MIN_ACTIVE_PARTITIONS = 2
);
```

`DROP CHANGEFEED`: Deletes the changefeed with the specified name. The code below deletes the `updates_feed` changefeed:

```yql
ALTER TABLE `series` DROP CHANGEFEED `updates_feed`;
```
