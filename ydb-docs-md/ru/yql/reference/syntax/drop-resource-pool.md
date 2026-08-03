---
title: "DROP RESOURCE POOL"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-resource-pool?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-resource-pool"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-resource-pool.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-resource-pool.md"
description: "DROP RESOURCE POOL удаляет пул ресурсов. Синтаксис. DROP RESOURCE POOL <name>. Параметры. name - имя пула ресурсов, подлежащего удалению. Разрешения."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP RESOURCE POOL

`DROP RESOURCE POOL` удаляет [пул ресурсов](../../../concepts/glossary.md#resource-pool).

## Синтаксис {#sintaksis}

```yql
DROP RESOURCE POOL <name>
```

### Параметры {#parametry}

- `name` - имя пула ресурсов, подлежащего удалению.

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `REMOVE SCHEMA` до пула в директории `.metadata/workload_manager/pools`, пример выдачи такого разрешения:

```yql
GRANT 'REMOVE SCHEMA`' ON `.metadata/workload_manager/pools` TO `user1@domain`;
```

## Примеры {#primery}

Следующая команда удалит пул ресурсов с именем "olap":

```yql
DROP RESOURCE POOL olap;
```

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL](create-resource-pool.md)
- [ALTER RESOURCE POOL](alter-resource-pool.md)
