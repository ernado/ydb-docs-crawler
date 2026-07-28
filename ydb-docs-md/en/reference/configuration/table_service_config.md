---
title: "<code class=\"yfm-clipboard-inline-code\" role=\"button\" tabindex='0' id=\"inline-code-id-hg5gddr3\">table_service_config</code> configuration section"
url: "https://ydb.tech/docs/en/reference/configuration/table_service_config?version=v26.1"
doc_path: "en/reference/configuration/table_service_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/table_service_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/table_service_config.md"
description: "The table_service_config section contains configuration parameters for the table service, including spilling settings. spilling_service_config."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# <code class="yfm-clipboard-inline-code" role="button" tabindex='0' id="inline-code-id-hg5gddr3">table_service_config</code> configuration section

The `table_service_config` section contains configuration parameters for the table service, including spilling settings.

## spilling_service_config {#spilling_service_config}

[Spilling](../../concepts/query_execution/spilling.md) is a memory management mechanism in YDB that temporarily saves data to disk when the system runs out of RAM.

### Primary Configuration Parameters

```yaml
table_service_config:
    spilling_service_config:
        local_file_config:
            root: ""
            max_total_size: 21474836480
            io_thread_pool:
            workers_count: 2
            queue_size: 1000
```

### Directory Configuration

#### local_file_config.root {#local_file_configroot}

**Type:** `string`  
 **Default:** `""` (temporary directory)  
 **Description:** A filesystem directory for saving spilling files.

For each `ydbd` process, a separate directory is created with a unique name. Spilling directories have the following name format:

`node_<node_id>_<spilling_service_id>`

Where:

- `node_id` — [node](../../concepts/glossary.md#node) identifier
- `spilling_service_id` — unique instance identifier that is created when initializing the [Spilling Service](../../contributor/spilling-service.md) one time when the ydbd process starts

Spilling files are stored inside each such directory.

Example of a complete spilling directory path:

```bash
/tmp/spilling-tmp-<username>/node_1_32860791-037c-42b4-b201-82a0a337ac80
```

Where:

- `/tmp` — value of the `root` parameter
- `<username>` — username under which the `ydbd` process is running

**Important notes:**

- At process startup, all existing spilling directories in the specified directory are automatically deleted. Spilling directories have a special name format that includes an instance identifier, which is generated once when the ydbd process starts. When a new process starts, all directories in the spilling directory that match the name format but have a different `spilling_service_id` from the current one are deleted.
- The directory must have sufficient write and read permissions for the user under which ydbd is running

> [!NOTE]
> Spilling is only performed on [database nodes](../../concepts/glossary.md#database-node).

##### Possible errors

- `Permission denied` — insufficient directory access permissions. See [Permission Denied](../../troubleshooting/spilling/permission-denied.md)

#### local_file_config.max_total_size {#local_file_configmax_total_size}

**Type:** `uint64`  
 **Default:** `21474836480` (20 GiB)  
 **Description:** Maximum total size of all spilling files on each [node](../../concepts/glossary.md#node). When the limit is exceeded, spilling operations fail with an error. The total spilling limit across the entire cluster is the sum of `max_total_size` values from all nodes.

##### Recommendations

- Set the value based on available disk space

##### Possible errors {#possible-errors1}

- `Total size limit exceeded: X/YMb` — maximum total size of spilling files exceeded. See [Total Size Limit Exceeded](../../troubleshooting/spilling/total-size-limit-exceeded.md)

### Thread Pool Configuration

> [!NOTE]
> I/O pool threads for spilling are created in addition to threads allocated for the [actor system](../../concepts/glossary.md#actor-system). When planning the number of threads, consider the overall system load.
>
> **Important:** The spilling thread pool is separate from the actor system thread pools.
>
> For information about configuring actor system thread pools and their impact on system performance, see [Actor System Configuration](index.md#actor-system) and [Changing Actor System Configuration](../../devops/configuration-management/configuration-v1/change_actorsystem_configs.md). For Configuration V2, the actor system settings are described in the [Configuration V2 settings](../../devops/configuration-management/configuration-v2/config-settings.md).

#### local_file_config.io_thread_pool.workers_count {#local_file_configio_thread_poolworkers_count}

**Type:** `uint32`  
 **Default:** `2`  
 **Description:** Number of worker threads for processing spilling I/O operations.

##### Recommendations {#recommendations1}

- Increase for high-load systems

##### Possible errors {#possible-errors2}

- `Can not run operation` — I/O thread pool operation queue overflow. See [Can not run operation](../../troubleshooting/spilling/can-not-run-operation.md)

#### local_file_config.io_thread_pool.queue_size {#local_file_configio_thread_poolqueue_size}

**Type:** `uint32`  
 **Default:** `1000`  
 **Description:** Size of the spilling operations queue. Each task sends only one data block to spilling at a time, so large values are usually not required.

##### Possible errors {#possible-errors3}

- `Can not run operation` — I/O thread pool operation queue overflow. See [Can not run operation](../../troubleshooting/spilling/can-not-run-operation.md)

### Memory Management

#### Relationship with memory_controller_config {#relationship-with-memory_controller_config}

Spilling activation is closely related to memory controller settings. Detailed `memory_controller_config` configuration is described in a [separate article](memory_controller_config.md).

The key parameter for spilling is **`activities_limit_percent`**, which determines the amount of memory allocated for query processing activities. This parameter affects the available memory for user queries and, accordingly, the frequency of spilling activation.

#### Impact on spilling

- When increasing `activities_limit_percent`, more memory is available for queries → spilling activates less frequently
- When decreasing `activities_limit_percent`, less memory is available for queries → spilling activates more frequently

> [!WARNING]
> However, it's important to consider that spilling itself requires memory. If you set `activities_limit_percent` too high, memory may still be exhausted despite spilling, as the spilling mechanism itself consumes memory resources.

### File System Requirements

#### File Descriptors

> [!NOTE]
> For information about configuring file descriptor limits during initial deployment, see the [File Descriptor Limits](../../devops/deployment-options/manual/initial-deployment/deployment-preparation.md#file-descriptors) section.

### Configuration Examples

#### High-load System

For maximum performance in high-load systems, it is recommended to increase the spilling size and number of worker threads:

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      root: ""
      max_total_size: 107374182400   # 100 GiB
      io_thread_pool:
        workers_count: 8
        queue_size: 2000
```

#### Limited Resources

For systems with limited resources, it is recommended to use conservative settings:

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      root: ""
      max_total_size: 5368709120     # 5 GiB
      io_thread_pool:
        workers_count: 1
        queue_size: 500
```

### Advanced Configuration

#### Enabling and Disabling Spilling

The following parameters control the enabling and disabling of various spilling types. They should typically only be changed when there are specific system requirements.

##### local_file_config.enable {#local_file_configenable}

**Location:** `table_service_config.spilling_service_config.local_file_config.enable`  
 **Type:** `boolean`  
 **Default:** `true`  
 **Description:** Enables or disables the spilling service. When disabled (`false`), [spilling](../../concepts/query_execution/spilling.md) does not function, which may lead to errors when processing large data volumes.

##### Possible errors {#possible-errors4}

- `Spilling Service not started` / `Service not started` — attempt to use spilling when Spilling Service is disabled. See [Spilling Service Not Started](../../troubleshooting/spilling/service-not-started.md)

```yaml
table_service_config:
  spilling_service_config:
    local_file_config:
      enable: true
```

##### enable_spilling_nodes {#enable_spilling_nodes}

**Location:** `table_service_config.enable_spilling_nodes`  
 **Type:** `bool`  
 **Default:** `true`  
 **Description:** Enables spilling on database nodes. When disabled (`false`), spilling does not function on database nodes.

```yaml
table_service_config:
  enable_spilling_nodes: true
```

##### enable_query_service_spilling {#enable_query_service_spilling}

**Location:** `table_service_config.enable_query_service_spilling`  
 **Type:** `boolean`  
 **Default:** `true`  
 **Description:** Global option that enables transport spilling during data transfer between tasks.

```yaml
table_service_config:
  enable_query_service_spilling: true
```

> [!NOTE]
> This setting works in conjunction with the local spilling service configuration. When disabled (`false`), transport spilling does not function even with enabled `spilling_service_config`.

### Complete Example

```yaml
table_service_config:
  enable_spilling_nodes: true
  enable_query_service_spilling: true
  spilling_service_config:
    local_file_config:
      enable: true
      root: "/var/spilling"
      max_total_size: 53687091200    # 50 GiB
      io_thread_pool:
        workers_count: 4
        queue_size: 1500
```

## See Also

- [Spilling Concept](../../concepts/query_execution/spilling.md)
- [Spilling Service Architecture](../../contributor/spilling-service.md)
- [Spilling Troubleshooting](../../troubleshooting/spilling/index.md)
- [Memory Controller Configuration](memory_controller_config.md)
- [YDB Monitoring](../../devops/observability/monitoring.md)
- [Performance Diagnostics](../../troubleshooting/performance/index.md)
