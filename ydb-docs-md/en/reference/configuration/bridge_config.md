---
title: "bridge_config"
url: "https://ydb.tech/docs/en/reference/configuration/bridge_config?version=v26.1"
doc_path: "en/reference/configuration/bridge_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/bridge_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/bridge_config.md"
description: "This section describes the cluster piles for bridge mode. Specify the list of pile names used for binding hosts and other entities. In bridge mode, you must als"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# bridge_config

This section describes the cluster piles for bridge mode. Specify the list of pile names used for binding hosts and other entities. In bridge mode, you must also specify the name of the corresponding pile for each host in the `hosts` section (the `bridge_pile_name` field), see [hosts](hosts.md#hosts-bridge).

## Syntax

```yaml
bridge_config:
  piles:
  - name: <pile_name_1>
  - name: <pile_name_2>
  ...
  - name: <pile_name_n>
```
