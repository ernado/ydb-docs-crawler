---
title: "admin cluster config generate"
url: "https://ydb.tech/docs/en/reference/ydb-cli/commands/configuration/cluster/generate?version=v26.1"
doc_path: "en/reference/ydb-cli/commands/configuration/cluster/generate"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydb-cli/commands/configuration/cluster/generate.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydb-cli/commands/configuration/cluster/generate.md"
description: "With the admin cluster config generate command, you can generate a dynamic configuration file based on the static configuration file on the YDB cluster."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# admin cluster config generate

With the `admin cluster config generate` command, you can generate a [dynamic configuration](../../../../../maintenance/manual/dynamic-config.md) file based on the [static configuration](../../../../configuration/index.md) file on the YDB cluster.  
 The dynamic configuration uses the format of an extended static configuration; the command automates the conversion process.

General command syntax:

```bash
ydb [global options...] admin cluster config generate
```

- `global options` — Global parameters.

View the description of the dynamic configuration generation command:

```bash
ydb admin cluster config generate --help
```

## Examples

Generate the dynamic configuration based on the static configuration:

```bash
ydb admin cluster config generate > config.yaml
```

After executing this command, the `config.yaml` file will contain a YAML document in the following format:

```yaml
metadata:
  kind: MainConfig
  cluster: ""
  version: 0
config:
  <static cluster configuration>
```

## Using the Generated Dynamic Configuration

After generating the dynamic configuration, you can perform the following steps:

1. Add configuration parameters to the dynamic configuration file.
2. Apply the dynamic configuration to the cluster using the [`admin cluster config replace`](replace.md) command.
