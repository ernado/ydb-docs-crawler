---
title: "ALTER RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-resource-pool-classifier?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-resource-pool-classifier"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-resource-pool-classifier.md"
description: "ALTER RESOURCE POOL CLASSIFIER изменяет определение классификатора пула ресурсов. Синтаксис Изменение параметров."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ALTER RESOURCE POOL CLASSIFIER

`ALTER RESOURCE POOL CLASSIFIER` изменяет определение [классификатора пула ресурсов](../../../concepts/glossary.md#resource-pool-classifier.md).

## Синтаксис {#sintaksis}

### Изменение параметров {#izmenenie-parametrov}

Синтаксис для изменения любого параметра классификатора пула ресурсов выглядит следующим образом:

```yql
ALTER RESOURCE POOL CLASSIFIER <name> SET (<key> = <value>);
```

`<key>` — имя параметра, `<value>` — его новое значение.

Например, такая команда изменит пользователя, для которого применяется правило:

```yql
ALTER RESOURCE POOL CLASSIFIER olap_classifier SET (MEMBER_NAME = "user2@domain");
```

### Сброс параметров {#sbros-parametrov}

Команда для сброса параметра классификатора пула ресурсов выглядит следующим образом:

```yql
ALTER RESOURCE POOL CLASSIFIER <name> RESET (<key>);
```

`<key>` — имя параметра.

Например, такая команда сбросит настройку `MEMBER_NAME`:

```yql
ALTER RESOURCE POOL CLASSIFIER olap_classifier RESET (MEMBER_NAME);
```

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `ALL` на базу данных, пример выдачи такого разрешения:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Параметры {#parametry}

- `RANK` (Int64) — опциональное поле, задающее порядок выбора классификатора пула ресурсов. Если значение не указано, берётся максимальный существующий `RANK` и к нему прибавляется 1000. Допустимые значения: уникальное число в диапазоне \[0,263−1\]\[0, 2^{63}-1\]\[0,263−1\].
- `RESOURCE_POOL` (String) — обязательное поле, задающее имя пула ресурсов, в который будут отправлены запросы, удовлетворяющие критериям классификатора.
- `MEMBER_NAME` (String) — опциональное поле, определяющее, какой пользователь или группа пользователей будут отправлены в указанный пул ресурсов. Если поле не указано, классификатор игнорирует `MEMBER_NAME`, и классификация осуществляется по другим признакам.

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL CLASSIFIER](create-resource-pool-classifier.md)
- [DROP RESOURCE POOL CLASSIFIER](drop-resource-pool-classifier.md)
