---
title: "Updating a topic"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-alter?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-alter"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-alter.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-alter.md"
description: "You can use the topic alter subcommand to update a previously created topic. General format of the command:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Updating a topic

You can use the `topic alter` subcommand to update a [previously created](topic-create.md) topic.

General format of the command:

```bash
ydb [global options...] topic alter [options...] <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](topic-alter.md#options).
- `topic-path`: Topic path.

View the description of the update topic command:

```bash
ydb topic alter --help
```

## Parameters of the subcommand {#options}

The command changes the values of parameters specified in the command line. The other parameter values remain unchanged.

| Name | Description |
| --- | --- |
| `--partitions-count` | The number of topic [partitions](../../concepts/datamodel/topic.md#partitioning). You can only increase the number of partitions. |
| `--retention-period` | Data retention time in a topic. A positive number followed by a unit of time.  <br>The following units are supported:<br>- `s` – seconds;<br>- `m` – minutes;<br>- `h` – hours;<br>- `d` – days. |
| `--partition-write-speed-kbps` | The maximum write speed to a [partition](../../concepts/datamodel/topic.md#partitioning), specified in KB/s.  <br>The default value is `1024`. |
| `--retention-storage-mb` | The maximum storage size, specified in MB. When the limit is reached, the oldest data will be deleted. The consumed space may exceed the set value when autopartitioning is enabled.  <br>The default value is `0` (no limit). |
| `--supported-codecs` | Supported data compression methods.  <br>Possible values:<br>- `RAW`: No compression.<br>- `ZSTD`: [zstd](https://en.wikipedia.org/wiki/Zstandard) compression.<br>- `GZIP`: [gzip](https://en.wikipedia.org/wiki/Gzip) compression.<br>- `LZOP`: [lzop](https://en.wikipedia.org/wiki/Lzop) compression. |
| `--metering-mode` | The topic pricing method for a serverless database.  <br>Possible values:<br>- `request-units`: Based on actual usage.<br>- `reserved-capacity`: Based on dedicated resources. |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Add a partition and the `lzop` compression method to the [previously created](topic-create.md) topic:

```bash
ydb -p quickstart topic alter \
  --partitions-count 3 \
  --supported-codecs raw,gzip,lzop \
  my-topic
```

Make sure that the topic parameters have been updated:

```bash
ydb -p quickstart scheme describe my-topic
```

Result:

```text
RetentionPeriod: 2h
PartitionsCount: 3
SupportedCodecs: RAW, GZIP, LZOP
```
