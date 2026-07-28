---
title: "List of endpoints"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/discovery-list?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/discovery-list"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/discovery-list.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/discovery-list.md"
description: "List of endpoints."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# List of endpoints

Using the `discovery list` information command, you can get a list of YDB cluster [endponts](../../../concepts/connect.md#endpoint) that you can connect to in order to access your database:

```bash
ydb [connection options] discovery list
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

The output rows in the response contain the following information:

1. Endpoint, including protocol and port
2. Availability zone (in square brackets)
3. The `#` character is used for the list of YDB services available on this endpoint

An endpoint discovery request to the YDB cluster is executed in the YDB SDK at driver initialization so that you can use the `discovery list` CLI command to localize connection issues.

## Example

```bash
$ ydb -p quickstart discovery list
grpcs://vm-etn01q5-ysor.etn01q5k.ydb.mdb.yandexcloud.net:2135 [sas] #table_service #scripting #discovery #rate_limiter #locking #kesus
grpcs://vm-etn01q5-arum.etn01ftr.ydb.mdb.yandexcloud.net:2135 [vla] #table_service #scripting #discovery #rate_limiter #locking #kesus
grpcs://vm-etn01q5beftr.ydb.mdb.yandexcloud.net:2135 [myt] #table_service #scripting #discovery #rate_limiter #locking #kesus
```
