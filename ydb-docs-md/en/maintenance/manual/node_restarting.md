---
title: "Safe restart and shutdown of nodes"
url: "https://ydb.tech/docs/en/maintenance/manual/node_restarting?version=v26.1"
doc_path: "en/maintenance/manual/node_restarting"
version: "v26.1"
lang: "en"
source_path: "en/core/maintenance/manual/node_restarting.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/maintenance/manual/node_restarting.md"
description: "Stopping/restarting a YDB process on a node. To make sure that the process is stoppable, follow these steps. Access the node via SSH. Execute the command."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Safe restart and shutdown of nodes

## Stopping/restarting a YDB process on a node {#restart_process}

To make sure that the process is stoppable, follow these steps.

1. Access the node via SSH.

2. Execute the command

   ```bash
   ydbd cms request restart host {node_id} --user {user} --duration 60 --dry --reason 'some-reason'
   ```

   If the process is stoppable, you'll see `ALLOW`.

3. Stop the process

   ```bash
   sudo service ydbd stop
   ```

4. Restart the process if needed

   ```bash
    sudo service ydbd start
   ```

## Replacing equipment {#replace-hardware}

Before replacing equipment, make sure that the YDB process is [stoppable](node_restarting.md#restart_process).  
 If the replacement is going to take a long time, first move all the VDisks from this node and wait until replication is complete.  
 After replication is complete, you can safely shut down the node.

To make sure that disabling the dynamic node doesn't affect query handling, drain the tablets from this node first.

Go to the [Hive web-viewer](../../reference/embedded-ui/hive.md) page.  
 Click "View Nodes" to see a list of all nodes.

Before disabling the node, first disable the transfer of tablets through the Active button, then click Drain, and wait for all the tablets to be moved away.
