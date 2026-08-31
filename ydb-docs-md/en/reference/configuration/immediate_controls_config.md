---
title: "immediate_controls_config"
url: "https://ydb.tech/docs/en/reference/configuration/immediate_controls_config?version=v26.1"
doc_path: "en/reference/configuration/immediate_controls_config"
version: "v26.1"
lang: "en"
source_path: "en/core/reference/configuration/immediate_controls_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/reference/configuration/immediate_controls_config.md"
description: "The immediate_controls_config section provides a set of dynamic parameters for fine-tuning YDB components, including DataShard, Coordinator, SchemeShard, BlobSt"
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# immediate_controls_config

The `immediate_controls_config` section provides a set of dynamic parameters for fine-tuning YDB components, including [DataShard](../../concepts/glossary.md#data-shard), [Coordinator](../../concepts/glossary.md#coordinator), [SchemeShard](../../concepts/glossary.md#scheme-shard), [BlobStorage](../../concepts/glossary.md#distributed-storage), and others. These settings let you adapt cluster behavior to specific scenarios — for example, by configuring thresholds for automatic shard splitting as data grows or load increases.

## Syntax

```yaml
immediate_controls_config:
  ...
  scheme_shard_controls:
    force_shard_split_data_size: 2147483648
    ...
```

## Parameters

| Parameter | Minimum value | Maximum value | Default value | Description |
| --- | --- | --- | --- | --- |
| `scheme_shard_controls.force_shard_split_data_size` | 10 MiB | 16 GiB | 2 GiB | A table partition is forcibly split when it reaches the specified data size, even if the table's [partition size threshold or maximum partition count](../../concepts/datamodel/table.md#partitioning_row_table) would otherwise prevent the split. Specify the value in bytes. |
