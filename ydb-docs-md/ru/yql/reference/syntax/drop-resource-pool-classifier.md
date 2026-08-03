---
title: "DROP RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-resource-pool-classifier?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-resource-pool-classifier"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-resource-pool-classifier.md"
description: "DROP RESOURCE POOL CLASSIFIER удаляет классификатор пулов ресурсов. Синтаксис. DROP RESOURCE POOL CLASSIFIER <name>. Параметры."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# DROP RESOURCE POOL CLASSIFIER

`DROP RESOURCE POOL CLASSIFIER` удаляет [классификатор пулов ресурсов](../../../concepts/glossary.md#resource-pool-classifier).

## Синтаксис {#sintaksis}

```yql
DROP RESOURCE POOL CLASSIFIER <name>
```

### Параметры {#parametry}

- `name` - имя классификатора пула ресурсов, подлежащего удалению.

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `ALL` на базу данных, пример выдачи такого разрешения:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Примеры {#primery}

Следующая команда удалит классификатор пула ресурсов с именем "olap_classifier":

```yql
DROP RESOURCE POOL CLASSIFIER olap_classifier;
```

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL CLASSIFIER](create-resource-pool-classifier.md)
- [ALTER RESOURCE POOL CLASSIFIER](alter-resource-pool-classifier.md)
