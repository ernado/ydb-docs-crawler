---
title: "Getting profile information"
url: "https://ydb.tech/docs/en/reference/ydb-cli/profile/list-and-get?version=v26.1"
doc_path: "en/reference/ydb-cli/profile/list-and-get"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/profile/list-and-get.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/profile/list-and-get.md"
description: "Getting profile information Getting a list of profiles. Getting a list of profiles: ydb config profile list."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Getting profile information

## Getting a list of profiles {#list}

Getting a list of profiles:

```bash
ydb config profile list
```

If there is a currently [activated profile](activate.md), it will be marked as `(active)` in the output list, for example:

```text
prod
test (active)
local
```

## Getting detailed profile information {#get}

Getting parameters saved in the specified profile:

```bash
ydb config profile get <profile_name>
```

For example:

```bash
$ ydb config profile get local1
  endpoint: grpcs://ydb.serverless.yandexcloud.net:2135
  database: /rul1/b1g8skp/etn02099
  sa-key-file: /Users/username/secrets/sa_key_test.json
```

## Getting profiles with content {#get-all}

Full information on all profiles and parameters stored in them:

```bash
ydb config profile list --with-content
```

The output of this command combines the output of the command to get a list of profiles (with the active profile marked) and the parameters of each profile in the lines following its name.
