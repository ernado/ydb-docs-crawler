---
title: "node_broker_config"
url: "https://ydb.tech/docs/en/reference/configuration/node_broker_config?version=v26.1"
doc_path: "en/reference/configuration/node_broker_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/node_broker_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/node_broker_config.md"
description: "The node_broker_config section configures stable node names for dynamic nodes in YDB clusters. Node names are assigned through the Node Broker, which is a syste"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# node_broker_config

The `node_broker_config` section configures stable node names for dynamic nodes in YDB clusters. Node names are assigned through the Node Broker, which is a system tablet that registers dynamic nodes in the cluster.

Node Broker assigns names to dynamic nodes when they register in the cluster. By default, a node name consists of the hostname and the port on which the node is running.

In a dynamic environment where hostnames often change, such as in Kubernetes, using hostname and port leads to an uncontrollable increase in the number of unique node names. This is true even for a database with a handful of dynamic nodes. Such behavior may be undesirable for a time series monitoring system as the number of metrics grows uncontrollably. To solve this problem, the system administrator can set up *stable* node names.

A stable name identifies a node within the tenant. It consists of a prefix and a node's sequential number within its tenant. If a dynamic node has been shut down, after a timeout, its stable name can be taken by a new dynamic node serving the same tenant.

To enable stable node names, you need to add the following to the cluster configuration:

```yaml
feature_flags:
  enable_stable_node_names: true
```

By default, the prefix is `slot-`. To override the prefix, add the following to the cluster configuration:

```yaml
node_broker_config:
  stable_node_name_prefix: <new prefix>
```
