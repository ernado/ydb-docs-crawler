---
title: "Deploying a cluster using configuration V2"
url: "https://ydb.tech/docs/en/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2?version=v26.1"
doc_path: "en/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/ansible/initial-deployment/deployment-configuration-v2.md"
description: "Alert."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Deploying a cluster using configuration V2

> [!CAUTION]
> This article is about YDB clusters that use **configuration V2**. This configuration method is still experimental and is only available for YDB versions starting with v25.1. For production we recommend [configuration V1](deployment-configuration-v1.md), which is the main, officially supported configuration for all YDB clusters.

## Prepare the environment {#deployment-preparation}

Before deploying the system, complete the preparation steps. See the [Deployment preparation](deployment-preparation.md) document.

## Create a working directory {#prepare-directory}

```bash
mkdir deployment
cd deployment
mkdir -p inventory/group_vars/ydb
mkdir files
```

## Create the Ansible configuration file {#ansible-creat-config}

Create `ansible.cfg` with Ansible configuration suitable for your target deployment environment. See the [Ansible configuration reference](https://docs.ansible.com/ansible/latest/reference_appendices/config.html) for details. This guide assumes the `./inventory` subdirectory of the working directory is set up for inventory files.

<details>
<summary>Example starter ansible.cfg</summary>

> [!NOTE]
> Using the `StrictHostKeyChecking=no` parameter in `ssh_args` makes automation easier but reduces SSH connection security (disables host key verification). For production environments, we recommend omitting this argument and configuring trusted keys manually. Use this parameter only for test and temporary installations.

```ini
[defaults]
conditional_bare_variables = False
force_handlers = True
forks = 300
gathering = explicit
host_key_checking = False
interpreter_python = /usr/bin/python3
inventory = ./inventory
module_name = shell
pipelining = True
private_role_vars = True
retry_files_enabled = False
timeout = 5
vault_password_file = ./ansible_vault_password_file
verbosity = 1
log_path = ./ydb.log

[ssh_connection]
retries = 5
ssh_args = -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o ControlMaster=auto -o ControlPersist=60s -o ControlPath=/tmp/ssh-%h-%p-%r -o ServerAliveCountMax=3 -o ServerAliveInterval=10 
```

</details>

## Create the main inventory file {#inventory-create}

Create the file `inventory/group_vars/ydb/all.yaml` and fill it.

{% list tabs %}

- mirror-3-dc-3nodes

  ```yaml
  # Ansible
  ansible_user: username
  ansible_ssh_private_key_file: "/path/to/your/id_rsa"

  # System
  system_timezone: UTC
  system_ntp_servers: [time.cloudflare.com, time.google.com, ntp.ripe.net, pool.ntp.org]

  # Database
  ydb_user: root
  ydb_dbname: db

  # Storage
  ydb_disks:
    - name: /dev/vdb
      label: ydb_disk_1
    - name: /dev/vdc
      label: ydb_disk_2
    - name: /dev/vdd
      label: ydb_disk_3
  ydb_pool_kind: ssd
  ydbops_local: true
  ydb_cores_dynamic: 2
  ydb_dynnodes:
    - {"instance": "a", offset: 1}
  ydb_cores_static:  2

  # YDB
  ydb_version: "system_version"
  ydb_archive: "{{ ansible_config_file | dirname }}/files/ydbd.tar.gz"

  # Additional parameters
  ydb_allow_format_drives: true
  ydb_skip_data_loss_confirmation_prompt: false
  ```

{% endlist %}

Required settings to adapt for your environment in the chosen template:

1. **SSH access configuration.** Specify the `ansible_user` and the path to the private key `ansible_ssh_private_key_file` that Ansible will use to connect to your servers.
2. **Filesystem paths to block devices.** In the `ydb_disks` section, the template assumes `/dev/vda` is for the operating system and the following disks, such as `/dev/vdb`, are for the YDB storage layer. Disk labels are created by the playbooks automatically, and their names can be arbitrary.
3. **System version.** In the `ydb_version` parameter, specify the YDB version to install. The list of available versions is on the [downloads](../../../../downloads/ydb-open-source-database.md) page.

Recommended settings to adapt for your environment:

- `ydb_domain`. This will be the first path component for all [scheme objects](../../../../concepts/glossary.md#scheme-object) in the cluster. For example, you can put your company name, cluster region, and so on there.
- `ydb_dbname`. This will be the second path component for all [scheme objects](../../../../concepts/glossary.md#scheme-object) in the database. For example, you can put the use case or project name there.

<details>
<summary>Additional settings</summary>

There are several options to specify which YDB executables you want to use for the cluster:

- `ydb_version`: automatically download one of the [official YDB releases](../../../../downloads/index.md#ydb-server) by version number. For example, `23.4.11`.
- `ydb_archive`: a local filesystem path to a YDB distribution archive [downloaded](../../../../downloads/index.md#ydb-server) or otherwise prepared in advance.

Installing a [connector](../../../../concepts/query_execution/federated_query/architecture.md#connectors) may be required for using [federated queries](../../../../concepts/query_execution/federated_query/index.md). The playbook can deploy [fq-connector-go](../../manual/federated-queries/connector-deployment.md#fq-connector-go) on hosts with dynamic nodes. Use the following settings:

- `ydb_install_fq_connector` — set to `true` to install the connector.

- Choose one of the available options for deploying fq-connector-go executables:

  - `ydb_fq_connector_version`: automatically download one of the [fq-connector-go official releases](https://github.com/ydb-platform/fq-connector-go/releases) by version number. For example, `v0.7.1`.
  - `ydb_fq_connector_git_version`: automatically compile the fq-connector-go executable from source code downloaded from the [official GitHub repository](https://github.com/ydb-platform/fq-connector-go). The setting value is a branch, tag, or commit name. For example, `main`.
  - `ydb_fq_connector_archive`: a local filesystem path to a fq-connector-go distribution archive [downloaded](https://github.com/ydb-platform/fq-connector-go/releases) or otherwise prepared in advance.
  - `ydb_fq_connector_binary`: local filesystem paths to the fq-connector-go executable, [downloaded](https://github.com/ydb-platform/fq-connector-go/releases) or otherwise prepared in advance.

- `ydb_tls_dir` — specify a local path to a folder with TLS certificates prepared in advance. It must contain the `ca.crt` file and subdirectories whose names match the node hostnames, each containing certificates for that node. If not specified, self-signed TLS certificates will be generated automatically for the entire YDB cluster.

- `ydb_brokers` — list the FQDNs of the broker nodes. For example:

  ```yaml
  ydb_brokers:
      - static-node-1.ydb-cluster.com
      - static-node-2.ydb-cluster.com
      - static-node-3.ydb-cluster.com
  ```

The optimal value for the `ydb_database_groups` setting in the `vars` section depends on the available disks. Assuming only one database in the cluster, use the following logic:

- For production deployments, use disks with capacity over 800 GB and high IOPS, then choose the value for this setting based on cluster topology:

  - For `block-4-2`, set `ydb_database_groups` to 95% of the total number of disks, rounded down.
  - For `mirror-3-dc`, set `ydb_database_groups` to 84% of the total number of disks, rounded down.

- For testing YDB on small disks, set `ydb_database_groups` to 1 regardless of cluster topology.

The values of the `system_timezone` and `system_ntp_servers` variables depend on the infrastructure where the YDB cluster is deployed. By default, `system_ntp_servers` includes a set of NTP servers without regard to the geographic location of the infrastructure. We strongly recommend using a local NTP server for on-premise infrastructure and the following NTP servers for cloud providers:

{% list tabs %}

- AWS

  - `system_timezone`: USA/\<region_name>
  - `system_ntp_servers`: \[169.254.169.123, time.aws.com\] [Learn more](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html#configure-time-sync) about AWS NTP server settings.

- Azure

  - You can read about how time synchronization is configured on Azure virtual machines in [this](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/time-sync) article.

- Alibaba

  - The specifics of connecting to NTP servers in Alibaba are described in [this article](https://www.alibabacloud.com/help/en/ecs/user-guide/alibaba-cloud-ntp-server).

- Yandex Cloud

  - `system_timezone`: Europe/Moscow
  - `system_ntp_servers`: \[0.ru.pool.ntp.org, 1.ru.pool.ntp.org, ntp0.NL.net, ntp2.vniiftri.ru, ntp.ix.ru, ntps1-1.cs.tu-berlin.de\] [Learn more](https://yandex.cloud/en/docs/tutorials/infrastructure-management/ntp) about Yandex Cloud NTP server settings.

{% endlist %}

</details>

## Change the root user password {#change-password}

Create the file `ansible_vault_password_file` with the following content:

```bash
password
```

This file contains the password that Ansible will use to encrypt and decrypt sensitive data automatically, for example user password files. This way passwords are not stored in plain text in the repository. For more on how Ansible Vault works, see the [official documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html).

Next, set the password for the initial user specified in the `ydb_user` setting (default `root`). This user will have full access rights in the cluster initially; you can change this later if needed. Create `inventory/group_vars/ydb/vault.yaml` with the following content (replace `<password>` with the actual password):

```yaml
ydb_password: <password>
```

Encrypt this file with the command `ansible-vault encrypt inventory/group_vars/ydb/vault.yaml`.

## Prepare the YDB configuration file {#ydb-config-prepare}

Create the file `files/config.yaml` and fill it.

{% list tabs %}

- mirror-3-dc-3nodes

  ```yaml
  metadata:
    kind: MainConfig
    cluster: ""
    version: 0
  config:
    yaml_config_enabled: true
    erasure: mirror-3-dc
    fail_domain_type: disk
    self_management_config:
      enabled: true
    default_disk_type: SSD
    host_configs:
    - host_config_id: 1
      drive:
      - path: /dev/disk/by-partlabel/ydb_disk_1
        type: SSD
      - path: /dev/disk/by-partlabel/ydb_disk_2
        type: SSD
      - path: /dev/disk/by-partlabel/ydb_disk_3
        type: SSD
    hosts:
    - host: ydb-node-zone-a.local
      host_config_id: 1
      location:
        body: 1
        data_center: 'zone-a'
        rack: '1'
    - host: ydb-node-zone-b.local
      host_config_id: 1
      location:
        body: 2
        data_center: 'zone-b'
        rack: '1'
    - host: ydb-node-zone-c.local
      host_config_id: 1
      location:
        body: 3
        data_center: 'zone-c'
        rack: '1'
    actor_system_config:
      use_auto_config: true
      cpu_count: 1
    interconnect_config:
      start_tcp: true
      encryption_mode: OPTIONAL
      path_to_certificate_file: "/opt/ydb/certs/node.crt"
      path_to_private_key_file: "/opt/ydb/certs/node.key"
      path_to_ca_file: "/opt/ydb/certs/ca.crt"
    grpc_config:
      cert: "/opt/ydb/certs/node.crt"
      key: "/opt/ydb/certs/node.key"
      ca: "/opt/ydb/certs/ca.crt"
      services_enabled:
      - legacy
    security_config:
      enforce_user_token_requirement: true
    client_certificate_authorization:
      request_client_certificate: true
      client_certificate_definitions:
      - member_groups: ["databaseNodes@cert"]
        subject_terms:
        - short_name: "O"
          values: ["YDB"]
    domains_config:
      security_config:
        monitoring_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        administration_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        viewer_allowed_sids:
        - "root"
        - "ADMINS"
        - "DATABASE-ADMINS"
        register_dynamic_node_allowed_sids:
        - databaseNodes@cert
        - root@builtin
  ```

{% endlist %}

To speed up and simplify the initial YDB deployment, the configuration file already contains most of the cluster setup. You only need to replace the placeholder host FQDNs in the `hosts` section and the disk paths in the `host_configs` section with the actual values.

- The `hosts` section:

  ```yaml
  ...
  hosts:
    - host: ydb-node-zone-a.local
    host_config_id: 1
    location:
      body: 1
      data_center: 'zone-a'
      rack: '1'
  ...
  ```

- The `host_configs` section:

  ```yaml
  ...
  host_configs:
  - host_config_id: 1
    drive:
    - path: /dev/disk/by-partlabel/ydb_disk_1
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_2
      type: SSD
    - path: /dev/disk/by-partlabel/ydb_disk_3
      type: SSD
  ...
  ```

Leave the rest of the configuration file sections and settings unchanged.

Create the file `inventory/ydb_inventory.yaml` with the following content:

```yaml
plugin: ydb_platform.ydb.ydb_inventory
ydb_config: "files/config.yaml"
```

## Deploy the YDB cluster {#cluster-deployment}

After completing all the preparation steps above, the actual initial cluster deployment is running the following command from the working directory:

```bash
ansible-playbook ydb_platform.ydb.initial_setup
```

Shortly after it starts, you will need to confirm full wipe of the configured disks. Completion can then take tens of minutes depending on the environment and settings. This playbook performs roughly the same steps as in the [manual YDB cluster deployment](../../manual/initial-deployment/index.md) instructions.

### Check cluster state {#cluster-state}

On the last step, the playbook runs several test queries using real temporary tables to verify correct operation. On success, you will see status ok, failed=0, and test query results (3 and 6) for each server when the playbook output is verbose enough.

<details>
<summary>Example output</summary>

```txt
...

TASK [ydb_platform.ydb.ydbd_dynamic : run test queries] *******************************************************************************************************************************************************
ok: [static-node-1.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-1.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-2.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-2.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-3.ydb-cluster.com] => (item={'instance': 'a'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "a"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
ok: [static-node-3.ydb-cluster.com] => (item={'instance': 'b'}) => {"ansible_loop_var": "item", "changed": false, "item": {"instance": "b"}, "msg": "all test queries were successful, details: {\"count\":3,\"sum\":6}\n"}
PLAY RECAP ****************************************************************************************************************************************************************************************************
static-node-1.ydb-cluster.com : ok=167  changed=80   unreachable=0    failed=0    skipped=167  rescued=0    ignored=0
static-node-2.ydb-cluster.com : ok=136  changed=69   unreachable=0    failed=0    skipped=113  rescued=0    ignored=0
static-node-3.ydb-cluster.com : ok=136  changed=69   unreachable=0    failed=0    skipped=113  rescued=0    ignored=0
```

</details>

Running the `ydb_platform.ydb.initial_setup` playbook creates a YDB cluster. It will contain a [domain](../../../../concepts/glossary.md#domain) named from the `ydb_domain` setting (default `Root`), a [database](../../../../concepts/glossary.md#database) named from the `ydb_dbname` setting (default `db`), and an initial [user](../../../../concepts/glossary.md#access-user) named from the `ydb_user` setting (default `root`).

## Additional steps

The easiest way to explore the newly deployed cluster is [Embedded UI](../../../../reference/embedded-ui/index.md), which runs on port 8765 on each server. If you do not have direct browser access to that port, set up SSH tunneling by running `ssh -L 8765:localhost:8765 -i <private-key> <user>@<any-ydb-server-hostname>` on your local machine (add more options if needed). After the connection is established, open [localhost:8765](http://localhost:8765) in your browser. The browser may ask you to accept a security exception. Example:

![ydb-web-ui](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/_assets/ydb-web-console.png)

After the YDB cluster is created, check its state on this Embedded UI page: [http://localhost:8765/monitoring/cluster/tenants](http://localhost:8765/monitoring/cluster/tenants). It might look like this:

![ydb-cluster-check](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/_assets/ydb-cluster-check.png)

This section shows the following YDB cluster parameters:

- `Tablets` — list of running [tablets](../../../../concepts/glossary.md#tablet). All tablet state indicators should be green.
- `Nodes` — number and state of storage and database nodes running in the cluster. The node state indicator should be green, and the number of created and running nodes should match (e.g., 18/18 for a nine-node cluster with one database node per server).

The `Load` (RAM used) and `Storage` (disk space used) indicators should also be green.

You can check the storage group state in the `storage` section — [http://localhost:8765/monitoring/cluster/storage](http://localhost:8765/monitoring/cluster/storage):

![ydb-storage-gr-check](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/en/core/_assets/ydb-storage-gr-check.png)

The `VDisks` indicators should be green, and the `state` status (in the tooltip when hovering over the Vdisk indicator) should be `Ok`. For more on cluster state indicators and monitoring, see [YDB Monitoring](../../../../reference/embedded-ui/ydb-monitoring.md).

### Cluster testing {#testing}

You can test the cluster using the built-in load tests in YDB CLI. [Install YDB CLI](../../../../reference/ydb-cli/install.md) and create a profile with connection parameters, replacing the placeholders:

```shell
ydb \
  config profile create <profile-name> \
  -d /<ydb-domain>/<ydb-database> \
  -e grpcs://<any-ydb-cluster-hostname>:2135 \
  --ca-file $(pwd)/files/TLS/certs/ca.crt \
  --user root \
  --password-file <path-to-a-file-with-password>
```

Command parameters and their meaning:

- `config profile create` — creates a connection profile. Specify the profile name. For more on creating and changing profiles, see [Creating and updating profiles](../../../../reference/ydb-cli/profile/create.md).
- `-e` — endpoint, a string in the form `protocol://host:port`. You can specify the FQDN of any cluster node and omit the port. Port 2135 is used by default.
- `--ca-file` — path to the root certificate for database connections over `grpcs`.
- `--user` — user for database connection.
- `--password-file` — path to the password file. Omit to enter the password manually.

To verify the profile was created, use `ydb config profile list`. Activate the profile with `ydb config profile activate <profile-name>`. To confirm it is active, run `ydb config profile list` again — the active profile will show `(active)`.

To run a [YQL](../../../../yql/reference/index.md) query, use `ydb sql -s 'SELECT 1;'`, which returns the result of `SELECT 1` in table form in the terminal. After checking the connection, create a test table with:  
 `ydb workload kv init --init-upserts 1000 --cols 4`. This creates the test table `kv_test` with 4 columns and 1000 rows. To verify the table and data, run `ydb sql -s 'select * from kv_test limit 10;'`.

The terminal will show a table of 10 rows. You can then run cluster performance tests. [Key-Value load](../../../../reference/ydb-cli/workload-kv.md) describes workload types (`upsert`, `insert`, `select`, `read-rows`, `mixed`) and their parameters. Example for the `upsert` workload with `--print-timestamp` and default parameters: `ydb workload kv run upsert --print-timestamp`:

```text
Window Txs/Sec Retries Errors  p50(ms) p95(ms) p99(ms) pMax(ms)        Timestamp
1          727 0       0       11      27      71      116     2024-02-14T12:56:39Z
2          882 0       0       10      21      29      38      2024-02-14T12:56:40Z
3          848 0       0       10      22      30      105     2024-02-14T12:56:41Z
4          901 0       0       9       20      27      42      2024-02-14T12:56:42Z
5          879 0       0       10      22      31      59      2024-02-14T12:56:43Z
...
```

When you are done, remove the `kv_test` table with `ydb workload kv clean`. For more on test table options and tests, see [Key-Value load](../../../../reference/ydb-cli/workload-kv.md).

## See also

- [Additional Ansible configuration examples](https://github.com/ydb-platform/ydb-ansible-examples)
- [Restarting YDB Clusters deployed with Ansible](../restart.md)
- [Updating Configuration of YDB Clusters Deployed with Ansible](../update-config.md)
- [Updating YDB Version on Clusters Deployed with Ansible](../update-executable.md)
