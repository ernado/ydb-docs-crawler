---
title: "CREATE RESOURCE POOL CLASSIFIER"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-resource-pool-classifier?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-resource-pool-classifier"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-resource-pool-classifier.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-resource-pool-classifier.md"
description: "CREATE RESOURCE POOL CLASSIFIER создаёт пул классификаторов ресурсов. Синтаксис."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE RESOURCE POOL CLASSIFIER

`CREATE RESOURCE POOL CLASSIFIER` создаёт [пул классификаторов ресурсов](../../../concepts/glossary.md#resource-pool-classifier.md).

## Синтаксис {#sintaksis}

```yql
CREATE RESOURCE POOL CLASSIFIER <name>
WITH ( <parameter_name> [= <parameter_value>] [, ... ] )
```

- `name` — имя создаваемого классификатора пула ресурсов. Должно быть уникальным. Имя не должно содержать символы, запрещённые для схемных объектов.
- `WITH ( <parameter_name> [= <parameter_value>] [, ... ] )` — позволяет задавать значения параметров, определяющих поведение классификатора пула ресурсов.

### Параметры {#parametry}

- `RANK` (Int64) — опциональное поле, задающее порядок выбора классификатора пула ресурсов. Если значение не указано, берётся максимальный существующий `RANK` и к нему прибавляется 1000. Допустимые значения: уникальное число в диапазоне \[0,263−1\]\[0, 2^{63}-1\]\[0,263−1\].
- `RESOURCE_POOL` (String) — обязательное поле, задающее имя пула ресурсов, в который будут отправлены запросы, удовлетворяющие критериям классификатора.
- `MEMBER_NAME` (String) — опциональное поле, определяющее, какой пользователь или группа пользователей будут отправлены в указанный пул ресурсов. Если поле не указано, классификатор игнорирует `MEMBER_NAME`, и классификация осуществляется по другим признакам.

## Замечания {#remarks}

Если в DDL для создания классификатора пула ресурсов не указан `RANK`, то по умолчанию ему будет присвоено значение RANK=MAX(existing_ranks)+1000RANK = MAX(existing\\_ranks) + 1000RANK=MAX(existing_ranks)+1000. Все значения `RANK` должны быть уникальными, чтобы обеспечить строго детерминированный порядок выбора пула ресурсов в случае конфликтующих условий. Такое поведение выбрано для возможности добавлять новые классификаторы пулов ресурсов между уже существующими.

Также возможно наличие классификатора, который ссылается на несуществующий пул ресурсов или к которому у пользователя нет доступа. В таком случае такие классификаторы будут пропускаться.

С ограничениями на число классификаторов можно ознакомиться на странице [ограничений](../../../concepts/limits-ydb.md#resource_pool).

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `ALL` на базу данных

Пример выдачи такого разрешения:

```yql
GRANT 'ALL' ON `/my_db` TO `user1@domain`;
```

## Примеры {#examples}

```yql
CREATE RESOURCE POOL CLASSIFIER olap_classifier WITH (
    RANK=1000,
    RESOURCE_POOL="olap",
    MEMBER_NAME="user1@domain"
)
```

В примере выше создаётся классификатор пула ресурсов с именем `olap_classifier`, который направляет запросы от пользователя `user1@domain` в пул ресурсов с именем `olap`. Запросы от всех остальных пользователей будут отправляться в пул ресурсов `default`, при условии, что других классификаторов пулов ресурсов не существует.

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [ALTER RESOURCE POOL CLASSIFIER](alter-resource-pool-classifier.md)
- [DROP RESOURCE POOL CLASSIFIER](drop-resource-pool-classifier.md)
