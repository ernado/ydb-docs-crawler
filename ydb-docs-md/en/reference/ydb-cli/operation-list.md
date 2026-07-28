---
title: "Getting a list of long-running operations"
url: "https://ydb.tech/docs/en/reference/ydb-cli/operation-list?version=v26.1"
doc_path: "en/reference/ydb-cli/operation-list"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/operation-list.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/operation-list.md"
description: "Use the ydb operation list subcommand to get a list of long-running operations of the specified type. General format of the command:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Getting a list of long-running operations

Use the `ydb operation list` subcommand to get a list of long-running operations of the specified type.

General format of the command:

```bash
ydb [global options...] operation list [options...] <kind>
```

- `global options`: [Global parameters](commands/global-options.md).

- `options`: [Parameters of the subcommand](operation-list.md#options).

- `kind`: The type of operation. Possible values:

  - `buildindex`: The build index operations.
  - `compaction`: The table compaction operations.
  - `export/s3`: The export to S3 operations.
  - `export/nfs`: The export to NFS operations.
  - `import/s3`: The import from S3 operations.
  - `import/nfs`: The import from NFS operations.
  - `scriptexec`: The script execution operations.
  - `incbackup`: The incremental backup operations.
  - `restore`: The backup collection restore operations.

View a description of the command to get a list of long-running operations:

```bash
ydb operation list --help
```

## Parameters of the subcommand {#options}

| Name | Description |
| --- | --- |
| `-s`, `--page-size` | Number of operations on one page. If the list of operations contains more strings than specified in the `--page-size` parameter, the result will be split into several pages. To get the next page, specify the `--page-token` parameter. |
| `-t`, `--page-token` | Page token. |
| `--format` | Output format.  <br>Default value: `pretty`.  <br>Acceptable values:<br>- `pretty`: A human-readable format.<br>- `proto-json-base64`: Protobuf result in [JSON](https://en.wikipedia.org/wiki/JSON) format, binary strings are encoded in [Base64](https://en.wikipedia.org/wiki/Base64). |

## Examples

> [!NOTE]
> The examples use the `quickstart` profile. To learn more, see [Creating a profile to connect to a test database](profile/create.md#quickstart).

Get a list of long-running build index operations for the `series` table:

```bash
ydb -p quickstart operation list \
  buildindex
```

Result:

```text
┌───────────────────────────────────────┬───────┬─────────┬───────┬──────────┬─────────────────────┬─────────────┐
| id                                    | ready | status  | state | progress | table               | index       |
├───────────────────────────────────────┼───────┼─────────┼───────┼──────────┼─────────────────────┼─────────────┤
| ydb://buildindex/7?id=281489389055514 | true  | SUCCESS | Done  | 100.00%  | /my-database/series | idx_release |
└───────────────────────────────────────┴───────┴─────────┴───────┴──────────┴─────────────────────┴─────────────┘

Next page token: 0
```
