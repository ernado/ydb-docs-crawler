---
title: "Configuration Management"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/index.md"
description: "The YDB CLI provides commands for managing the dynamic configuration at different levels of the system. General command syntax:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Configuration Management

The YDB CLI provides commands for managing the [dynamic configuration](../../../../maintenance/manual/dynamic-config.md) at different levels of the system.

General command syntax:

```bash
ydb [global options...] admin [scope] config [subcommands...]
```

- `global options` — [Global parameters](../global-options.md).
- `scope` — Configuration scope (`cluster`, `node`).
- `subcommands` — Subcommands for managing configuration.

View the command description:

```bash
ydb admin --help
```

## Available Configuration Scopes {#scopes}

### Cluster Configuration {#cluster}

Managing cluster-level configuration:

```bash
ydb admin cluster config [subcommands...]
```

Available subcommands:

- [fetch](cluster/fetch.md) - Fetches the current dynamic cluster configuration.
- [generate](cluster/generate.md) - Generates dynamic configuration based on the static configuration on the cluster.
- [replace](cluster/replace.md) - Replaces the dynamic configuration.
- version - Show configuration version on nodes (V1/V2).

### Node Configuration {#node}

Managing node-level configuration:

```bash
ydb admin node config [subcommands...]
```

Available subcommands:

- [init](node/init.md) - Initializes the directory for node configuration.
