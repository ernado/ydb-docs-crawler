---
title: "Configuring ydbops"
url: "https://ydb.tech/docs/en/reference/ydbops/configuration?version=v26.1"
doc_path: "en/reference/ydbops/configuration"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/ydbops/configuration.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/ydbops/configuration.md"
description: "Note. The ydbops utility is under active development. Although backward-incompatible changes are unlikely, they may still occur."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Configuring ydbops

> [!NOTE]
> The `ydbops` utility is under active development. Although backward-incompatible changes are unlikely, they may still occur.

`ydbops` can be run by specifying all the necessary command line arguments on the command invocation. However, it has two features that allow to avoid repeating the commonly used arguments:

- [Config file](configuration.md#config-file)
- [Environment variables](configuration.md#environment-variables)

## Config file

The configuration file for `ydbops` is a YAML-formatted file containing multiple profiles. Profiles for `ydbops` work in the same way as profiles in [YDB CLI](../ydb-cli/profile/index.md) do.

Default configuration file location follows the same convention as YDB CLI does, it is located in the same folder in `ydbops` subdirectory. For comparison:

- default configuration file for YDB CLI: `$HOME/.ydb/config/config.yaml`
- default configuration file for `ydbops` CLI, `ydbops` subdirectory: `$HOME/ydb/ydbops/config/config.yaml`

Certain command line options can be written in the configuration file instead of being specified directly in the `ydbops` invocation.

### Examples

Calling the `ydbops restart` command without a profile:

```bash
ydbops restart \
 -e grpc://<hostname>:2135 \
 --kubeconfig ~/.kube/config \
 --k8s-namespace <k8s-namespace> \
 --user admin \
 --password-file ~/<password-file> \
 --tenant --tenant-list=my-tenant
```

Calling the same `ydbops restart` command with profile options enabled makes the command much shorter:

```bash
ydbops restart \
 --config-file ./config.yaml \
 --tenant --tenant-list=<tenant-name>
```

For the invocation above, the following `config.yaml` is assumed to be present:

```yaml
current-profile: my-profile
profiles:
  my-profile:
    endpoint: grpcs://<hostname>:2135
    ca-file: ~/<ca-certificate-file>
    user: <username>
    password-file: ~/<password-file>
    k8s-namespace: <k8s-namespace>
    kubeconfig: ~/.kube/config
```

### Profile management commands

Currently, `ydbops` does not support the creation, modification, and activation of profiles via the CLI commands [the way that YDB CLI does](../ydb-cli/profile/index.md#commands).

The configuration file needs to be created and edited manually.

### Configuration file reference

Here is an example of a configuration file with all possible options that can be specified and example values (most likely, they will not all be needed at the same time):

```yaml
# a special key `current-profile` can be specified to
# be used as the default active profile in the CLI invocation
current-profile: my-profile

# profile definitions are added as subkeys to the `profiles` key
profiles:
  my-profile:
    endpoint: grpcs://your.ydb.cluster.fqdn:2135

    # CA file location if using grpcs to the endpoint
    ca-file: /path/to/custom/ca/file

    # a username and password file if static credentials are used:
    user: your-ydb-user-name
    password-file: /path/to/password-file

    # when using access token
    token-file: /path/to/ydb/token

    # if working with YDB clusters in Kubernetes, kubeconfig path can be specified:
    kubeconfig: /path/to/kube/config
    k8s-namespace: <k8s-namespace>
```

## Environment variables

Alternatively, there is an option to specify several environment variables instead of passing command-line arguments or using [config files](configuration.md#config-file).

For an explanation of which options take precedence, please invoke `ydbops --help`.

- `YDB_TOKEN` can be passed instead of the `--token-file` flag or `token-file` profile option.
- `YDB_PASSWORD` can be passed instead of the `--password-file` flag or `password-file` profile option.
- `YDB_USER` can be passed instead of the `--user` flag or `user` profile option.
