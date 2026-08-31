---
title: "Resetting TTL parameters"
url: "https://ydb.tech/docs/en/reference/ydb-cli/table-ttl-reset?version=v26.1"
doc_path: "en/reference/ydb-cli/table-ttl-reset"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/table-ttl-reset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/table-ttl-reset.md"
description: "Use the table ttl reset subcommand to reset TTL for the specified table. General format of the command: ydb [global options...] table ttl reset <table path>."
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# Resetting TTL parameters

Use the `table ttl reset` subcommand to reset [TTL](../../concepts/ttl.md) for the specified table.

General format of the command:

```bash
ydb [global options...] table ttl reset <table path>
```

- `global options`: [Global parameters](commands/global-options.md).
- `table path`: The table path.

View the description of the TTL reset command:

```bash
ydb table ttl reset --help
```

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Reset TTL for the `series` table:

```bash
ydb -p quickstart table ttl reset \
  series
```
