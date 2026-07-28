---
title: "Service commands"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/service?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/service"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/service.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/service.md"
description: "Service commands."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Service commands

These commands have to do with the YDB CLI client itself and do not involve establishing a DB connection. They can be expressed either as a parameter or as an option.

| Name | Description |
| --- | --- |
| `-?`, `-h`, `--help` | Output the YDB CLI syntax help |
| `version` | Output the YDB CLI version (for public builds) |
| `update` | Update the YDB CLI to the latest version (for public builds) |
| `config info` | Displaying [connection parameters](../connect.md) |
| `--license` | Show the license (for public builds) |
| `--credits` | Show third-party product licenses (for public builds) |

If it is not known whether the used YDB CLI build is public, you can find out if a particular service command is supported through help output.
