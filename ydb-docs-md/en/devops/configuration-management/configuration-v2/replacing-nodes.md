---
title: "Replacing Node FQDN"
url: "https://ydb.tech/docs/en/devops/configuration-management/configuration-v2/replacing-nodes?version=v26.1"
doc_path: "en/devops/configuration-management/configuration-v2/replacing-nodes"
version: "v26.1"
lang: "en"
source_path: "en/core/devops/configuration-management/configuration-v2/replacing-nodes.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/devops/configuration-management/configuration-v2/replacing-nodes.md"
description: "Replacing Node FQDN. This procedure describes how to replace the FQDN (Fully Qualified Domain Name) of a YDB cluster node without downtime. Prerequisites. Note."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Replacing Node FQDN

This procedure describes how to replace the FQDN (Fully Qualified Domain Name) of a YDB cluster node without downtime.

## Prerequisites

> [!NOTE]
> A YDB cluster is fault-tolerant. Temporary node shutdown does not lead to cluster unavailability. For more details, see [YDB Cluster Topology](../../../concepts/topology.md).

> [!WARNING]
> Incorrect sequence of actions or configuration errors can lead to YDB cluster unavailability.

## Procedure Overview

The FQDN replacement process involves:

1. **Preparation**: Verify cluster health and prepare a new node configuration
2. **Node shutdown**: Gracefully stop the node to be replaced
3. **Configuration update**: Update the cluster configuration with a new FQDN
4. **Node restart**: Start the node with new FQDN
5. **Verification**: Confirm successful FQDN change

## Step-by-Step Instructions

### Step 1: Verify Cluster Health

Before starting the replacement, ensure the cluster is healthy:

```bash
ydb monitoring healthcheck
```

### Step 2: Prepare New Node Configuration

1. Update DNS records to point the new FQDN to the same IP address
2. Update TLS certificates if they include hostname verification
3. Prepare updated configuration files with the new FQDN

### Step 3: Stop the Target Node

Gracefully stop the node that needs FQDN replacement:

```bash
# For systemd-managed nodes
sudo systemctl stop ydbd-storage

# For manually started nodes
kill -TERM <ydbd_pid>
```

### Step 4: Update Cluster Configuration

Update the cluster configuration to reflect the new FQDN:

```yaml
# Example configuration update
hosts:
  - host: new-hostname.example.com  # Updated FQDN
    host_config_id: 1
    port: 19001
    location:
      unit: "1"
      data_center: "DC1"
      rack: "1"
```

### Step 5: Apply Configuration Changes

Apply the updated configuration to the cluster:

```bash
ydb admin config replace --config-file updated-config.yaml
```

### Step 6: Start Node with New FQDN

Start the node using the new FQDN:

```bash
# Update hostname if necessary
sudo hostnamectl set-hostname new-hostname.example.com

# Start the node
sudo systemctl start ydbd-storage
```

### Step 7: Verify the Change

Confirm the FQDN change was successful:

```bash
# Check node status
ydb monitoring healthcheck

# Verify node registration
ydb admin config fetch | grep new-hostname
```

## Troubleshooting

### Common Issues

1. **DNS resolution problems**: Ensure new FQDN resolves correctly
2. **Certificate validation errors**: Update certificates if they include hostname verification
3. **Node registration failures**: Check network connectivity and firewall rules

### Recovery Procedures

If the FQDN replacement fails:

1. Revert DNS changes to the original FQDN
2. Restore the original configuration
3. Restart the node with the original settings
4. Investigate and resolve the underlying issue

## Best Practices

1. **Test in staging**: Always test FQDN replacement in a non-production environment first
2. **Backup configurations**: Keep backups of working configurations before making changes
3. **Monitor during change**: Watch cluster health metrics during the replacement process
4. **Document changes**: Maintain records of FQDN changes for future reference
5. **Coordinate with the team**: Ensure all team members are aware of the planned change
