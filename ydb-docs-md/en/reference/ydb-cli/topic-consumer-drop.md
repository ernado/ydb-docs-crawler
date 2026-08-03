---
title: "Deleting a topic consumer"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-consumer-drop?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-consumer-drop"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-consumer-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-consumer-drop.md"
description: "You can use the topic consumer drop command to delete a previously added consumer. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Deleting a topic consumer

You can use the `topic consumer drop` command to delete a [previously added](topic-consumer-add.md) consumer.

General format of the command:

```bash
ydb [global options...] topic consumer drop <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `topic-path`: Topic path.

View the description of the delete consumer command:

```bash
ydb topic consumer drop --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--consumer VAL` | Name of the consumer to be deleted. |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Delete the [previously created](topic-consumer-add.md) consumer with the `my-consumer` name for the `my-topic` topic:

```bash
ydb -p quickstart topic consumer drop \
  --consumer my-consumer \
  my-topic
```
