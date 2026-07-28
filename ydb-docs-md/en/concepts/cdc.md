---
title: "Change Data Capture (CDC)"
url: "https://ydb.tech/docs/en/concepts/cdc?version=v26.1"
doc_path: "en/concepts/cdc"
version: "v26.1"
lang: "en"
source_path: "en/core/concepts/cdc.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/concepts/cdc.md"
description: "Warning. Supported only for row-oriented tables. Support for column-oriented tables is currently under development."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Change Data Capture (CDC)

> [!WARNING]
> Supported only for [row-oriented](datamodel/table.md#row-oriented-tables) tables. Support for [column-oriented](datamodel/table.md#column-oriented-tables) tables is currently under development.

Change Data Capture (CDC) captures changes to YDB table rows, uses these changes to generate a *changefeed*, writes them to distributed storage, and provides access to these records for further processing. It uses a [topic](datamodel/topic.md) as distributed storage to efficiently store the table change log.

When adding, updating, or deleting a table row, CDC generates a change record by specifying the [primary key](datamodel/table.md) of the row and writes it to the topic partition corresponding to this key.

## Guarantees

- Change records are sharded across topic partitions by primary key.
- Each change is only delivered once (exactly-once delivery).
- Changes by the same primary key are delivered to the same topic partition in the order they took place in the table.
- Change records are delivered to the topic partition only after the corresponding transaction in the table has been committed.

## Limitations {#restrictions}

- Changefeeds support records of the following types of operations:

  - Updates: overwriting the values of the specified columns. Query example: [UPDATE](../yql/reference/syntax/update.md).
  - Replacements: overwriting the values of the specified columns, the values of the unspecified columns are replaced by their default values. Query example: [REPLACE INTO](../yql/reference/syntax/replace_into.md).
  - Erases. Query example: [DELETE FROM](../yql/reference/syntax/delete.md).

Adding rows is a special update or replace case, and a record of adding a row in a changefeed will look similar to an update or replace record, depending on the original request that led to the change.

## Virtual Timestamps

All changes in YDB tables are arranged according to the order in which transactions are performed. Each change is marked with a virtual timestamp which consists of two elements:

1. Global coordinator time.
2. Unique transaction ID.

Using these timestamps, you can arrange records from different partitions of the topic relative to each other or use them for filtering (for example, to exclude old change records).

> [!NOTE]
> By default, virtual timestamps are not emitted to the changefeed. To enable them, use the [appropriate parameter](../yql/reference/syntax/alter_table/changefeed.md) when creating a changefeed.

## Barriers

Barriers are service records without data about modification or deletion with [virtual timestamps](cdc.md#virtual-timestamps) that appear in each partition of a topic at a specified interval. A barrier guarantees that any change with a virtual timestamp earlier than the barrier's has been written to this topic partition.

Barriers can be used to ensure strict ordering and global data consistency by buffering data between them.

> [!NOTE]
> By default, barriers are not emitted to the changefeed. To set the frequency at which barriers are emitted, use the [appropriate parameter](../yql/reference/syntax/alter_table/changefeed.md) when creating a changefeed.

## Initial Table Scan {#initial-scan}

By default, a changefeed only includes records about those table rows that changed after the changefeed was created. Initial table scan enables you to export, to the changefeed, the values of all the rows that existed at the time of changefeed creation.

The scan runs in the background mode on top of the table snapshot. The following situations are possible:

- A non-scanned row changes in the table. The changefeed will receive, one after another: a record with the source value and a record about the update. When the same record is changed again, only the update record is exported.
- A changed row is found during scanning. Nothing is exported to the changefeed because the source value has already been exported at the time of change (see the previous paragraph).
- A scanned row changes in the table. Only an update record exports to the changefeed.

This ensures that, for the same row (the same primary key), the source value is exported first, and then the updated value is exported.

> [!NOTE]
> The record with the source row value is labeled as an [update](cdc.md#restrictions) record. When using [virtual timestamps](cdc.md#virtual-timestamps), records are marked by the snapshot's timestamp.

During the scanning process, depending on the table update frequency, you might see too many `OVERLOADED` errors. This is because, besides the update records, you also need to deliver records with the source row values. When the scan is complete, the changefeed switches to normal operation.

> [!WARNING]
> [Automatic partitioning](datamodel/table.md#partitioning) processes are suspended in the table and [barriers](cdc.md#barriers) are not emitted to the changefeed during the initial scan.

## Record Structure

Depending on the [changefeed parameters](../yql/reference/syntax/alter_table/changefeed.md), the structure of a record may differ.

### JSON Format {#json-record-structure}

A [JSON](https://en.wikipedia.org/wiki/JSON) record has the following structure:

```json
{
    "key": [<key components>],
    "update": {<columns>},
    "reset": {<columns>},
    "erase": {},
    "newImage": {<columns>},
    "oldImage": {<columns>},
    "ts": [<step>, <txId>]
}
```

- `key`: An array of primary key component values. Always present. The order of elements matches the order of the columns listed in the primary key of the table.
- `update`: Update flag. Present if a record matches the update operation. In `UPDATES` mode, it also contains the names and values of updated columns.
- `reset`: Replacement flag. Present if a record matches the replacement operation. In `UPDATES` mode, it also contains the names and values of the columns for which a value is set.
- `erase`: Erase flag. Present if a record matches the erase operation.
- `newImage`: Row snapshot that results from its being changed. Present in `NEW_IMAGE` and `NEW_AND_OLD_IMAGES` modes. Contains column names and values.
- `oldImage`: Row snapshot before the change. Present in `OLD_IMAGE` and `NEW_AND_OLD_IMAGES` modes. Contains column names and values.
- `ts`: [Virtual timestamp](cdc.md#virtual-timestamps). Present if the `VIRTUAL_TIMESTAMPS` setting is enabled. Contains the value of the global coordinator time (`step`) and the unique transaction ID (`txId`).

Sample record of an update in `UPDATES` mode:

```json
{
   "key": [1, "one"],
   "update": {
       "payload": "lorem ipsum",
       "date": "2022-02-22"
   }
}
```

Record of an erase:

```json
{
   "key": [2, "two"],
   "erase": {}
}
```

Record with row snapshots:

```json
{
   "key": [1, 2, 3],
   "update": {},
   "newImage": {
       "textColumn": "value1",
       "intColumn": 101,
       "boolColumn": true
   },
   "oldImage": {
       "textColumn": null,
       "intColumn": 100,
       "boolColumn": false
   }
}
```

Record with virtual timestamps:

```json
{
   "key": [1],
   "update": {
       "created": "2022-12-12T00:00:00.000000Z",
       "customer": "Name123"
   },
   "ts": [1670792400890, 562949953607163]
}
```

A barrier record contains a single field `resolved` with a virtual timestamp:

```json
{
    "resolved": [1670792500000, 0]
}
```

> [!NOTE]
> - The same record may not contain the `update`, `reset` and `erase` fields simultaneously, since these fields are operation flags (you can't update and erase a table row at the same time). However, each record contains one of these fields (any operation is either an update, a replacement, or an erase).
> - In `UPDATES` mode, the `update` or `reset` field for update or replacement operations is an operation flag and contains the names and values of updated columns.
> - JSON object fields containing column names and values (`newImage`, `oldImage`, and `update` & `reset` in `UPDATES` mode), *do not include* the columns that are primary key components.
> - If a record contains the `erase` field (indicating that the record matches the erase operation), this is always an empty JSON object (`{}`).

### Debezium-Compatible JSON Format {#debezium-json-record-structure}

A [Debezium](https://debezium.io)-compatible JSON record structure has the following format:

```json
{
    "payload": {
        "op": <op>,
        "before": {<columns>},
        "after": {<columns>},
        "source": {
            "connector": <connector>,
            "version": <version>,
            "ts_ms": <ts_ms>,
            "step": <step>,
            "txId": <txId>,
            "snapshot": <bool>
        }
    }
}
```

- `op`: Operation that was performed on a row:

  - `c` — create. Applicable only in `NEW_AND_OLD_IMAGES` mode.
  - `u` — update.
  - `d` — delete.
  - `r` — read from [snapshot](cdc.md#initial-scan).

- `before`: Row snapshot before the change. Present in `OLD_IMAGE` and `NEW_AND_OLD_IMAGES` modes. Contains column names and values.

- `after`: Row snapshot after the change. Present in `NEW_IMAGE` and `NEW_AND_OLD_IMAGES` modes. Contains column names and values.

- `source`: Source metadata for the event.

  - `connector`: Connector name. Current name is `ydb`.
  - `version`: Connector version that was used to generate the record. Current version is `1.0.0`.
  - `ts_ms`: Approximate time when the change was applied, in milliseconds.
  - `step`: Global coordinator time. Part of the [virtual timestamp](cdc.md#virtual-timestamps).
  - `txId`: Unique transaction ID. Part of the [virtual timestamp](cdc.md#virtual-timestamps).
  - `snapshot`: Whether the event is part of a snapshot.

When reading using Kafka API, the Debezium-compatible primary key of the modified row is specified as the message key:

```json
{
    "payload": {<columns>}
}
```

- `payload`: Key of a row that was changed. Contains names and values of the columns that are components of the primary key.

## Record Retention Period {#retention-period}

By default, records are stored in the changefeed for 24 hours from the time they are sent. Depending on usage scenarios, the retention period can be reduced or increased up to 30 days.

> [!WARNING]
> Records whose retention time has expired are deleted, regardless of whether they were processed (read) or not.

Deleting records before they are processed by the client will cause [offset](datamodel/topic.md#offset) skips, which means that the offsets of the last record read from the partition and the earliest available record will differ by more than one.

To set up the record retention period, specify the [RETENTION_PERIOD](../yql/reference/syntax/alter_table/changefeed.md) parameter when creating a changefeed.

## Topic Partitions

By default, the initial number of [topic partitions](datamodel/topic.md#partitioning) is equal to the number of table partitions. You can redefine the initial number of topic partitions by specifying the [TOPIC_MIN_ACTIVE_PARTITIONS](../yql/reference/syntax/alter_table/changefeed.md) parameter when creating a changefeed. To create a changefeed with a dynamically changing number of partitions, set the [TOPIC_AUTO_PARTITIONING](../yql/reference/syntax/alter_table/changefeed.md) parameter when creating the changefeed.

> [!NOTE]
> Currently, the ability to explicitly specify the number of topic partitions is available only for tables whose first primary key component is of type `Uint64` or `Uint32`.

## Creating and Deleting a Changefeed {#ddl}

You can add a changefeed to an existing table or erase it using the [ADD CHANGEFEED and DROP CHANGEFEED](../yql/reference/syntax/alter_table/changefeed.md) directives of the YQL `ALTER TABLE` statement. When erasing a table, the changefeed added to it is also deleted.

## Getting and Updating Topic Settings {#topic-settings}

You can get the settings using an [SDK](../reference/ydb-sdk/topic.md#describe-topic) or the [YDB CLI](../reference/ydb-cli/commands/scheme-describe.md) by passing the path to the changefeed in the arguments, which has the following format:

```txt
path/to/table/changefeed_name
```

For example, if a table named `table` contains a changefeed named `updates_feed` in the `my` directory, its path looks as follows:

```text
my/table/updates_feed
```

The topic settings can be updated using the expression [ALTER TOPIC](../yql/reference/syntax/alter-topic.md). Supported actions:

- [updating settings](../yql/reference/syntax/alter-topic.md#updating-topic-settings):

  - `retention_period`;
  - `retention_storage_mb`;

- [updating consumers](../yql/reference/syntax/alter-topic.md#updating-a-set-of-consumers).

## CDC Purpose and Use {#best_practices}

For information about using CDC when developing apps, see [best practices](../dev/cdc.md).
