---
title: "Creating a topic"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-create?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-create"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-create.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-create.md"
description: "You can use the topic create subcommand to create a new topic. General format of the command: ydb [global options...] topic create [options...] <topic-path>."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Creating a topic

You can use the `topic create` subcommand to create a new topic.

General format of the command:

```bash
ydb [global options...] topic create [options...] <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](topic-create.md#options).
- `topic-path`: Topic path.

View the description of the create topic command:

```bash
ydb topic create --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--partitions-count` | The number of topic [partitions](../../concepts/datamodel/topic.md#partitioning).  <br>The default value is `1`. |
| `--retention-period` | Data retention time in a topic. A positive number followed by a unit of time.  <br>The following units are supported:<br>- `s` – seconds;<br>- `m` – minutes;<br>- `h` – hours;<br>- `d` – days.<br>The default value is `18h`. |
| `--partition-write-speed-kbps` | The maximum write speed to a [partition](../../concepts/datamodel/topic.md#partitioning), specified in KB/s.  <br>The default value is `1024`. |
| `--retention-storage-mb` | The maximum storage size, specified in MB. When the limit is reached, the oldest data will be deleted. The consumed space may exceed the set value when autopartitioning is enabled.  <br>The default value is `0` (no limit). |
| `--supported-codecs` | Supported data compression methods. Set with a comma.  <br>The default value is `raw`.  <br>Possible values:<br>- `RAW`: No compression.<br>- `ZSTD`: [zstd](https://en.wikipedia.org/wiki/Zstandard) compression.<br>- `GZIP`: [gzip](https://en.wikipedia.org/wiki/Gzip) compression.<br>- `LZOP`: [lzop](https://en.wikipedia.org/wiki/Lzop) compression. |
| `--metering-mode` | The topic pricing method for a serverless database.  <br>Possible values:<br>- `request-units`: Based on actual usage.<br>- `reserved-capacity`: Based on dedicated resources. |

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Create a topic with 2 partitions, `RAW` and `GZIP` compression methods, message retention time of 2 hours, and the `my-topic` path:

```bash
ydb -p quickstart topic create \
  --partitions-count 2 \
  --supported-codecs raw,gzip \
  --retention-period 2h \
  my-topic
```

View parameters of the created topic:

```bash
ydb -p quickstart scheme describe my-topic
```

Result:

```text
RetentionPeriod: 2h
PartitionsCount: 2
SupportedCodecs: RAW, GZIP
```
