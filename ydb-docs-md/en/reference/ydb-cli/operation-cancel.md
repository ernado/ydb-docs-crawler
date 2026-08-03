---
title: "Canceling long-running operations"
url: "https://ydb.tech/docs/en/reference/ydb-cli/operation-cancel?version=v26.1"
doc_path: "en/reference/ydb-cli/operation-cancel"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/operation-cancel.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/operation-cancel.md"
description: "Use the ydb operation cancel subcommand to cancel the specified long-running operation. Only an incomplete operation can be canceled."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Canceling long-running operations

Use the `ydb operation cancel` subcommand to cancel the specified long-running operation. Only an incomplete operation can be canceled.

General format of the command:

```bash
ydb [global options...] operation cancel <id>
```

- `global options`: [Global parameters](commands/global-options.md).
- `id`: The ID of the long-running operation. The ID contains characters that can be interpreted by your command shell. If necessary, use shielding, for example, `'<id>'` for bash.

View a description of the command to obtain the status of a long-running operation:

```bash
ydb operation cancel --help
```

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).
