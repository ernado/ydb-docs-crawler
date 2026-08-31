---
title: "admin cluster config fetch"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/cluster/fetch?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/cluster/fetch"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/cluster/fetch.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/cluster/fetch.md"
description: "With the admin cluster config fetch command, you can retrieve the current dynamic configuration of the YDB cluster. General command syntax:"
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# admin cluster config fetch

With the `admin cluster config fetch` command, you can retrieve the current [dynamic](../../../../../devops/configuration-management/configuration-v1/dynamic-config.md) configuration of the YDB cluster.

General command syntax:

```bash
ydb [global options...] admin cluster config fetch
```

- `global options` — Global parameters.

View the description of the dynamic configuration fetch command:

```bash
ydb admin cluster config fetch --help
```

## Examples

Fetch the current dynamic configuration of the cluster:

```bash
ydb --endpoint grpc://localhost:2135 admin cluster config fetch > config.yaml
```
