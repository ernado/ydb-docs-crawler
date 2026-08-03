---
title: "Obtaining the status of long-running operations"
url: "https://ydb.tech/docs/en/reference/ydb-cli/operation-get?version=v26.1"
doc_path: "en/reference/ydb-cli/operation-get"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/operation-get.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/operation-get.md"
description: "Use the ydb operation get subcommand to obtain the status of the specified long-running operation. General format of the command:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Obtaining the status of long-running operations

Use the `ydb operation get` subcommand to obtain the status of the specified long-running operation.

General format of the command:

```bash
ydb [global options...] operation get [options...] <id>
```

- `global options`: [Global parameters](commands/global-options.md).
- `options`: [Parameters of the subcommand](operation-get.md#options).
- `id`: The ID of the long-running operation. The ID contains characters that can be interpreted by your command shell. If necessary, use shielding, for example, `'<id>'` for bash.

View a description of the command to obtain the status of a long-running operation:

```bash
ydb operation get --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `--format` | Input format.  <br>Default value: `pretty`.  <br>Acceptable values:<br>- `pretty`: A human-readable format.<br>- `proto-json-base64`: Protobuf result in [JSON](https://en.wikipedia.org/wiki/JSON) format, binary strings are encoded in [Base64](https://en.wikipedia.org/wiki/Base64). |

## Examples {#examples-{examples}}

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Obtain the status of the long-running operation with the `ydb://buildindex/7?id=281489389055514` ID:

```bash
ydb -p quickstart operation get \
  'ydb://buildindex/7?id=281489389055514'
```

Result:

```text
┌───────────────────────────────────────┬───────┬─────────┬───────┬──────────┬─────────────────────┬─────────────┐
| id                                    | ready | status  | state | progress | table               | index       |
├───────────────────────────────────────┼───────┼─────────┼───────┼──────────┼─────────────────────┼─────────────┤
| ydb://buildindex/7?id=281489389055514 | true  | SUCCESS | Done  | 100.00%  | /my-database/series | idx_release |
└───────────────────────────────────────┴───────┴─────────┴───────┴──────────┴─────────────────────┴─────────────┘
```
