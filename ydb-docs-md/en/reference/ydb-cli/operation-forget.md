---
title: "Deleting long running operations from the list"
url: "https://ydb.tech/docs/en/reference/ydb-cli/operation-forget?version=v26.1"
doc_path: "en/reference/ydb-cli/operation-forget"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/operation-forget.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/operation-forget.md"
description: "Use the ydb operation forget subcommand to delete information about the specified long running operation from the list. The operation must be complete."
revision: "15d2b39e9edb57dad2b885fbb65cec1653e2a8f4"
---

# Deleting long running operations from the list

Use the `ydb operation forget` subcommand to delete information about the specified long running operation from the list. The operation must be complete.

General format of the command:

```bash
ydb [global options...] operation forget <id>
```

- `global options`: [Global parameters](commands/global-options.md).
- `id`: The ID of the long running operation. The ID contains characters that can be interpreted by your command shell. If necessary, use shielding, for example, `'<id>'` for bash.

View a description of the command to delete information about the specified long running operation:

```bash
ydb operation forget --help
```

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Delete the long running operation with the `ydb://buildindex/7?id=281489389055514` ID from the list:

```bash
ydb -p db1 operation forget \
  'ydb://buildindex/7?id=281489389055514'
```
