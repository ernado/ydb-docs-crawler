---
title: "Authentication"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/discovery-whoami?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/discovery-whoami"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/discovery-whoami.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/discovery-whoami.md"
description: "Authentication. The discovery whoami information command lets you check the account on behalf of which the server actually accepts requests:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Authentication

The `discovery whoami` information command lets you check the account on behalf of which the server actually accepts requests:

```bash
ydb [connection options] discovery whoami [-g]
```

where \[connection options\] are [database connection options](../connect.md#command-line-pars)

The response includes the account name (User SID) and, if the `-g` option is specified, the information whether the account belongs to groups.

If authentication is not enabled on the YDB server (for example, in the case of an independent local deployment), the command will fail with an error.

Support for the `-g` option depends on the server configuration. If disabled, you'll receive `User has no groups` in response, regardless of the actual inclusion of your account in any groups.

## Example

```bash
$ ydb -p quickstart discovery whoami -g
User SID: aje5kkjdgs0puc18976co@as

User has no groups
```
