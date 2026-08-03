---
title: "resource_broker_config"
url: "https://ydb.tech/docs/en/reference/configuration/resource_broker_config?version=v26.1"
doc_path: "en/reference/configuration/resource_broker_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/resource_broker_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/resource_broker_config.md"
description: "The resource broker is an actor service that controls resource consumption on YDB nodes, such as: CPU — number of threads. Memory — RAM."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# resource_broker_config

The resource broker is an [actor service](../../concepts/glossary.md#actor-service) that controls resource consumption on YDB [nodes](../../concepts/glossary.md#node), such as:

- `CPU` — number of threads
- `Memory` — RAM

Different types of activities (background operations, [TTL](../../concepts/ttl.md) data deletion, etc.) run in different resource broker *queues*. Each queue has a limited number of resources:

| Queue name | CPU | Memory | Description |
| --- | --- | --- | --- |
| `queue_ttl` | 2 | — | [TTL](../../concepts/ttl.md) data deletion operations. |
| `queue_backup` | 2 | — | [Backup](../../devops/backup-and-recovery.md#s3) operations. |
| `queue_restore` | 2 | — | [Restore from backup](../../devops/backup-and-recovery.md#s3) operations. |
| `queue_build_index` | 10 | — | [Online secondary index creation](../../concepts/query_execution/secondary_indexes.md#index-add) operations. |
| `queue_cdc_initial_scan` | 4 | — | [Initial table scan](../../concepts/cdc.md#initial-scan) operations. |

> [!NOTE]
> It is recommended to **extend** the resource broker configuration using [tags](../../devops/configuration-management/configuration-v2/dynamic-config-selectors.md#additional-yaml-tags) `!inherit` and `!append`.

Example of extending the resource broker configuration with a custom limit for the `queue_ttl` queue:

```yaml
resource_broker_config: !inherit
  queues: !append
  - name: queue_ttl
    limit:
      cpu: 4
```
