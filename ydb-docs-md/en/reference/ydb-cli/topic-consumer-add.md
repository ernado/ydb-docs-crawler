---
title: "Adding a topic consumer"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-consumer-add?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-consumer-add"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-consumer-add.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-consumer-add.md"
description: "You can use the topic consumer add command to add a consumer for a previously created topic. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Adding a topic consumer

You can use the `topic consumer add` command to add a consumer for a [previously created](topic-create.md) topic.

General format of the command:

```bash
ydb [global options...] topic consumer add [options...] <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](topic-consumer-add.md#options).
- `topic-path`: Topic path.

View the description of the add consumer command:

```bash
ydb topic consumer add --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--consumer VAL` | Name of the consumer to be added. |
| `--starting-message-timestamp VAL` | Time in [UNIX timestamp](https://en.wikipedia.org/wiki/Unix_time) format. Consumption starts as soon as the first [message](../../concepts/datamodel/topic.md#message) is received after the specified time. If the time is not specified, consumption will start from the oldest message in the topic. |
| `--supported-codecs` | Supported data compression methods.  <br>The default value is `raw`.  <br>Possible values:<br>- `RAW`: No compression.<br>- `ZSTD`: [zstd](https://en.wikipedia.org/wiki/Zstandard) compression.<br>- `GZIP`: [gzip](https://en.wikipedia.org/wiki/Gzip) compression.<br>- `LZOP`: [lzop](https://en.wikipedia.org/wiki/Lzop) compression. |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Create a consumer with the `my-consumer` name for the [previously created](topic-create.md) `my-topic` topic. Consumption will start as soon as the first message is received after August 15, 2022 13:00:00 GMT:

```bash
ydb -p quickstart topic consumer add \
  --consumer my-consumer \
  --starting-message-timestamp 1660568400 \
  my-topic
```

Make sure the consumer was created:

```bash
ydb -p quickstart scheme describe my-topic
```

Result:

```text
RetentionPeriod: 2h
PartitionsCount: 2
SupportedCodecs: RAW, GZIP

Consumers:
┌──────────────┬─────────────────┬───────────────────────────────┬───────────┐
| ConsumerName | SupportedCodecs | ReadFrom                      | Important |
├──────────────┼─────────────────┼───────────────────────────────┼───────────┤
| my-consumer  | RAW, GZIP       | Mon, 15 Aug 2022 16:00:00 MSK | 0         |
└──────────────┴─────────────────┴───────────────────────────────┴───────────┘
```
