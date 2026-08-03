---
title: "Saving a consumer offset"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-consumer-offset-commit?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-consumer-offset-commit"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-consumer-offset-commit.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-consumer-offset-commit.md"
description: "Each topic consumer has a consumer offset. You can use the topic consumer offset commit command to save the consumer offset for the consumer that you added."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Saving a consumer offset

Each topic consumer has a [consumer offset](../../concepts/datamodel/topic.md#consumer-offset).

You can use the `topic consumer offset commit` command to save the consumer offset for the consumer that you [added](topic-consumer-add.md).

General format of the command:

```bash
ydb [global options...] topic consumer offset commit [options...] <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](topic-consumer-offset-commit.md#options).
- `topic-path`: Topic path.

Viewing the command description:

```bash
ydb topic consumer offset commit --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--consumer <value>` | Consumer name. |
| `--partition <value>` | Partition number. |
| `--offset <value>` | Offset value that you want to set. |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

For `my-consumer`, set the offset of 123456789 in `my-topic` and partition `1`:

```bash
ydb -p db1 topic consumer offset commit \
  --consumer my-consumer \
  --partition 1 \
  --offset 123456789 \
  my-topic
```
