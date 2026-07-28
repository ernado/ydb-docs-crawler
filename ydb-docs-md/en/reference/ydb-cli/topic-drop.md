---
title: "Deleting a topic"
url: "https://ydb.tech/docs/en/reference/ydb-cli/topic-drop?version=v26.1"
doc_path: "en/reference/ydb-cli/topic-drop"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/topic-drop.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/topic-drop.md"
description: "You can use the topic drop subcommand to delete a previously created topic. Note. Deleting a topic also deletes all the consumers added for it."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Deleting a topic

You can use the `topic drop` subcommand to delete a [previously created](topic-create.md) topic.

> [!NOTE]
> Deleting a topic also deletes all the consumers added for it.

General format of the command:

```bash
ydb [global options...] topic drop <topic-path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `topic-path`: Topic path.

View the description of the delete topic command:

```bash
ydb topic drop --help
```

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Delete the [previously created](topic-create.md) topic:

```bash
ydb -p quickstart topic drop my-topic
```
