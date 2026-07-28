---
title: "cms_config"
url: "https://ydb.tech/docs/ru/reference/configuration/cms_config?version=v26.1"
doc_path: "ru/reference/configuration/cms_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/cms_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/cms_config.md"
description: "Cluster Management System (CMS) — компонент YDB, с помощью которого можно выполнять безопасное обслуживание кластера YDB, например, обновлять его версию или зам"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# cms_config

[Cluster Management System (CMS)](../../concepts/glossary.md#cms) — компонент YDB, с помощью которого можно выполнять [безопасное обслуживание кластера YDB](../../devops/concepts/maintenance-without-downtime.md), например, обновлять его версию или заменять сломавшиеся диски без потери доступности. Поведение CMS конфигурируется в секции `cms_config` конфигурации YDB.

## Синтаксис {#sintaksis}

```yaml
cms_config:
  tenant_limits:
    disabled_nodes_limit: 2
    disabled_nodes_ratio_limit: 5
  cluster_limits:
    disabled_nodes_limit: 3
    disabled_nodes_ratio_limit: 5
  disable_maintenance: true
```

## Параметры {#parametry}

| Параметр | Значение по умолчанию | Описание |
| --- | --- | --- |
| `tenant_limits.disabled_nodes_limit` | - | Максимальное количество [узлов базы данных](../../concepts/glossary.md#database-node), которые могут быть одновременно недоступны или заблокированы. |
| `tenant_limits.disabled_nodes_ratio_limit` | `13` | Максимальный процент [узлов базы данных](../../concepts/glossary.md#database-node), которые могут быть одновременно недоступны или заблокированы. |
| `cluster_limits.disabled_nodes_limit` | - | Максимальное количество узлов [кластера](../../concepts/glossary.md#cluster), которые могут быть одновременно недоступны или заблокированы. |
| `cluster_limits.disabled_nodes_ratio_limit` | `13` | Максимальный процент узлов [кластера](../../concepts/glossary.md#cluster), которые могут быть одновременно недоступны. |
| `disable_maintenance` | `false` | Флаг [приостанавливает](../../devops/concepts/maintenance-without-downtime.md#disable-maintenance) новые работы по обслуживанию кластера. |
