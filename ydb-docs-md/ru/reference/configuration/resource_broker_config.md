---
title: "resource_broker_config"
url: "https://ydb.tech/docs/ru/reference/configuration/resource_broker_config?version=v26.1"
doc_path: "ru/reference/configuration/resource_broker_config"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/resource_broker_config.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/resource_broker_config.md"
description: "Секция resource_broker_config настраивает брокер ресурсов — акторный сервис, контролирующий потребление ресурсов узла YDB, таких как: CPU — количество потоков;"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# resource_broker_config

Секция `resource_broker_config` настраивает брокер ресурсов — [акторный сервис](../../concepts/glossary.md#actor-service), контролирующий потребление ресурсов [узла](../../concepts/glossary.md#node) YDB, таких как:

- `CPU` — количество потоков;
- `Memory` — оперативная память.

Разные виды активностей (фоновые операции, удаление данных по [TTL](../../concepts/ttl.md) и т.д.) запускаются в разных *очередях* брокера ресурсов. Каждая такая очередь имеет лимитированное число ресурсов:

| Название очереди | CPU | Memory | Описание |
| --- | --- | --- | --- |
| `queue_ttl` | 2 | — | Операции удаления данных по [TTL](../../concepts/ttl.md). |
| `queue_backup` | 2 | — | Операции [резервного копирования](../../devops/backup-and-recovery/index.md#s3). |
| `queue_restore` | 2 | — | Операции [восстановления из резервной копии](../../devops/backup-and-recovery/index.md#s3). |
| `queue_build_index` | 10 | — | Операции [онлайн-создания вторичного индекса](../../concepts/query_execution/secondary_indexes.md#index-add). |
| `queue_cdc_initial_scan` | 4 | — | [Первоначальное сканирование таблицы](../../concepts/cdc.md#initial-scan). |

> [!NOTE]
> Рекомендуется **дополнять** конфигурацию брокера ресурсов, используя [теги](../../devops/configuration-management/configuration-v2/dynamic-config-selectors.md#dopolnitelnye-tegi-v-yaml) `!inherit` и `!append`.

Пример дополнения конфигурации брокера ресурсов пользовательским лимитом для очереди `queue_ttl`:

```yaml
resource_broker_config: !inherit
  queues: !append
  - name: queue_ttl
    limit:
      cpu: 4
```
