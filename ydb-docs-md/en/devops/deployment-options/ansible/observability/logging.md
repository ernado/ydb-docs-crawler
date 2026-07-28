---
title: "Logging on Clusters Deployed with Ansible"
url: "https://ydb.tech/docs/en/devops/deployment-options/ansible/observability/logging?version=v26.1"
doc_path: "en/devops/deployment-options/ansible/observability/logging"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/ansible/observability/logging.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/ansible/observability/logging.md"
description: "During initial deployment, the Ansible playbook sets up several systemd units that run YDB nodes. Typically, there are multiple YDB nodes per physical server or"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Logging on Clusters Deployed with Ansible

During [initial deployment](../initial-deployment/index.md), the Ansible playbook sets up several [systemd](https://systemd.io/) units that run YDB nodes. Typically, there are multiple YDB nodes per physical server or virtual machine, each having its own log. There are two main ways to view logs of such cluster: via an Ansible playbook or via `ssh`.

## View Logs via Ansible Playbook

[ydb-ansible](https://github.com/ydb-platform/ydb-ansible) repository contains a playbook called `ydb_platform.ydb.logs` that can be used to show logs of all YDB nodes in a cluster. The playbook gathers logs from nodes and outputs them to `stdout`, which allows to pipe them for further processing, for example with commands like `grep` or `awk`.

### All Logs of All Nodes

By default, the `ydb_platform.ydb.logs` playbook fetches logs of all YDB nodes. The command to do it:

```bash
ansible-playbook ydb_platform.ydb.logs
```

### Filter by Node Type

There are two main node types in a YDB cluster:

- Storage (also known as static)
- Database (also known as dynamic)

Tasks in the `ydb_platform.ydb.logs` playbook are tagged with node types, so you can use Ansible's tags functionality to filter logs by node type.

These two commands are equivalent and will output the storage node logs:

```bash
ansible-playbook ydb_platform.ydb.logs --tags storage
ansible-playbook ydb_platform.ydb.logs --tags static
```

These two commands are equivalent, too, and will output the database node logs:

```bash
ansible-playbook ydb_platform.ydb.logs --tags database
ansible-playbook ydb_platform.ydb.logs --tags dynamic
```

### Filter by hostname

To show logs of a specific host or subset of hosts, use the `--limit` argument:

```bash
ansible-playbook ydb_platform.ydb.logs --limit='<hostname>'
ansible-playbook ydb_platform.ydb.logs --limit='<hostname-1,hosntname-2>'
```

It can be used together with tags, too:

```bash
ansible-playbook ydb_platform.ydb.logs --tags database --limit='<hostname>'
```

## View Logs via SSH

To manually access YDB cluster logs via `ssh`, perform the following steps:

1. Construct a `ssh` command to access the server that runs a YDB node you need logs for. The basic version would look like `ssh -i <path-to-ssh-key> <username>@<hostname>`. Take values for these placeholders from the `inventory/50-inventory.yaml` you used for deployment:

   - `<path-to-ssh-key>` is `children.ydb.ansible_ssh_private_key_file`
   - `<username>` is `children.ydb.ansible_user`
   - `<hostname>` is one of `children.ydb.hosts`

2. Choose which systemd unit's logs you need. You can skip this step if you already know the unit name. After logging in to the server using the `ssh` command constructed in the previous step, obtain the list of YDB-related systemd units using `systemctl list-units | grep ydb`. There'll likely be one storage node and multiple database nodes.

   <details>
   <summary>Example output</summary>

   ```bash
   $ systemctl list-units | grep ydb
   ydb-transparent-hugepages.service                                              loaded active     exited    Configure Transparent Huge Pages (THP)
   ydbd-database-a.service                                                        loaded active     running   YDB dynamic node / database / a
   ydbd-database-b.service                                                        loaded active     running   YDB dynamic node / database / b
   ydbd-storage.service                                                           loaded active     running   YDB storage node
   ```

   </details>

3. Take the systemd unit name from the previous step and use it in the following command `journalctl -u <systemd-unit>` to actually show logs. You can specify `-u` multiple times to show logs of multiple units or use any other arguments from `man journalctl` to adjust the output.
