---
title: "en/devops/deployment-options/manual/maintenance"
url: "https://ydb.tech/docs/en/devops/deployment-options/manual/maintenance?version=v26.1"
doc_path: "en/devops/deployment-options/manual/maintenance"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/deployment-options/manual/maintenance.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/deployment-options/manual/maintenance.md"
description: "Cluster maintenance. The ydbops utility uses CMS to perform cluster maintenance without losing availability. You can also use CMS directly through the gRPC API."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# en/devops/deployment-options/manual/maintenance

## Cluster maintenance

The [ydbops](../../../reference/ydbops/index.md) utility uses CMS to perform cluster maintenance without losing availability. You can also use CMS directly through the [gRPC API](https://github.com/ydb-platform/ydb/blob/main/ydb/public/api/grpc/draft/ydb_maintenance_v1.proto).

### Rolling restart

To perform a rolling restart of the entire cluster, you can use the command:

```bash
$ ydbops restart
```

By default, the `strong` availability mode will be used, minimizing the risk of losing availability. You can override it using the `--availability-mode` parameter.

The `ydbops` utility will automatically create a maintenance task to restart the entire cluster using the specified availability mode. As it progresses, `ydbops` will update the maintenance task and obtain exclusive locks on nodes in CMS until all nodes are restarted.

### Take a host out for maintenance {#host-maintenance}

To take a host out for maintenance, follow these steps:

1. Create a maintenance task using the command:

   ```bash
   $ ydbops maintenance create --hosts=<fqdn> --duration=<seconds>
   ```

   This command will create a maintenance task that will take an exclusive lock on the host with the fully qualified domain name `<fqdn>` for `<seconds>` seconds.

2. After creating the task, you need to update its state until the lock is taken, using the command:

   ```bash
   $ ydbops maintenance refresh --task-id=<id>
   ```

   This command will update the task with identifier `<id>` and attempt to take the required lock. When you receive a `PERFORMED` response, you can proceed to the next step.

3. Perform host maintenance while the lock is held.

4. After completing the work, you need to release the lock on the host using the command:

   ```bash
   $ ydbops maintenance complete --task-id=<id> --hosts=<fqdn>
   ```
