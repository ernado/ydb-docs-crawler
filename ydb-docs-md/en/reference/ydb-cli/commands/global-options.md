---
title: "Global parameters"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/global-options?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/global-options"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/global-options.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/global-options.md"
description: "Global parameters DB connection options. DB connection options are described in Connecting to and authenticating with a database. Service options."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Global parameters

## DB connection options {#connection-options}

DB connection options are described in [Connecting to and authenticating with a database](../connect.md#command-line-pars).

## Service options

- `--profile <name>`: Indicates the use of the DB connection profile with the specified name when executing a YDB CLI command. Most connection parameters can be stored in the profile.
- `-v, --verbose`: Prints detailed information about all operations being executed. Specifying this option is helpful when locating DB connection issues.
- `--profile-file`: Use profiles from the specified file. By default, profiles from the `~/.ydb/config/config.yaml` file are used.
