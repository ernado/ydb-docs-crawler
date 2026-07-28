---
title: "Updating Configuration of YDB Clusters Deployed with Ansible"
url: "https://ydb.tech/docs/en/devops/deployment-options/ansible/update-config?version=v26.1"
doc_path: "en/devops/deployment-options/ansible/update-config"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/ansible/update-config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/ansible/update-config.md"
description: "During initial deployment, the Ansible playbook used the provided config file to create the initial cluster configuration. Technically, it generates two variant"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Updating Configuration of YDB Clusters Deployed with Ansible

During [initial deployment](initial-deployment/index.md), the Ansible playbook used the provided config file to create the initial cluster configuration. Technically, it generates two variants of the original config file and deploys them to all hosts via Ansible's mechanism for cross-server file copy. This article explains which options are available to change the cluster's configuration after the initial deployment.

## Update Configuration via Ansible Playbook

[ydb-ansible](https://github.com/ydb-platform/ydb-ansible) repository contains a playbook called `ydb_platform.ydb.update_config` that can be used to update YDB cluster's configuration. Go to the same directory used for the [initial deployment](initial-deployment/index.md), edit `files/config.yaml` as needed, and then run this playbook:

```bash
ansible-playbook ydb_platform.ydb.update_config
```

The playbook deploys the new version of the config files and then performs a [rolling restart](restart.md).

### Filter by Node Type

Tasks in the `ydb_platform.ydb.update_config` playbook are tagged with node types, so you can use Ansible's tags functionality to filter nodes by their kind.

These two commands are equivalent and will change the configuration of all [storage nodes](../../../concepts/glossary.md#storage-node):

```bash
ansible-playbook ydb_platform.ydb.update_config --tags storage
ansible-playbook ydb_platform.ydb.update_config --tags static
```

These two commands are equivalent and will change the configuration of all [database nodes](../../../concepts/glossary.md#database-node):

```bash
ansible-playbook ydb_platform.ydb.update_config --tags database
ansible-playbook ydb_platform.ydb.update_config --tags dynamic
```

### Skip Restart

There's a `no_restart` tag to only deploy the config files and skip the cluster restart. This might be useful if the cluster will be [restarted](restart.md) later manually or as part of some other maintenance tasks. Example:

```bash
ansible-playbook ydb_platform.ydb.update_config --tags no_restart
```
