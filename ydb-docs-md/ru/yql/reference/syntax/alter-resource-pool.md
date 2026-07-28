---
title: "ALTER RESOURCE POOL"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-resource-pool?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-resource-pool"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-resource-pool.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-resource-pool.md"
description: "ALTER RESOURCE POOL изменяет определение пула ресурсов. Синтаксис Изменение параметров."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER RESOURCE POOL

`ALTER RESOURCE POOL` изменяет определение [пула ресурсов](../../../concepts/glossary.md#resource-pool.md).

## Синтаксис {#sintaksis}

### Изменение параметров {#izmenenie-parametrov}

Синтаксис для изменения любого параметра пула ресурсов выглядит следующим образом:

```yql
ALTER RESOURCE POOL <name> SET (<key> = <value>);
```

`<key>` — имя параметра, `<value>` — его новое значение.

Например, такая команда включит ограничение на число параллельных запросов, равное 100:

```yql
ALTER RESOURCE POOL olap SET (CONCURRENT_QUERY_LIMIT = "100");
```

### Сброс параметров {#sbros-parametrov}

Команда для сброса параметра пула ресурсов выглядит следующим образом:

```yql
ALTER RESOURCE POOL <name> RESET (<key>);
```

`<key>` — имя параметра.

Например, такая команда сбросит настройки `TOTAL_CPU_LIMIT_PERCENT_PER_NODE` для пула ресурсов:

```yql
ALTER RESOURCE POOL olap RESET (TOTAL_CPU_LIMIT_PERCENT_PER_NODE);
```

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `ALTER SCHEMA` на пул ресурсов в директории `.metadata/workload_manager/pools`, пример выдачи такого разрешения:

```yql
GRANT 'ALTER SCHEMA' ON `.metadata/workload_manager/pools/olap_pool` TO `user1@domain`;
```

## Параметры {#parametry}

- `CONCURRENT_QUERY_LIMIT` (Int32) — опциональное поле, задающее количество параллельно выполняющихся запросов в пуле ресурсов. Если значение `-1`, то ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `QUEUE_SIZE` (Int32) — опциональное поле, определяющее размер очереди ожидания. Всего в системе может находиться не более чем CONCURRENT_QUERY_LIMIT+QUEUE_SIZECONCURRENT\\_QUERY\\_LIMIT + QUEUE\\_SIZECONCURRENT_QUERY_LIMIT+QUEUE_SIZE запросов одновременно. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `DATABASE_LOAD_CPU_THRESHOLD` (Int32) — опциональное поле, задающее порог загрузки CPU всей базы данных, после которого запросы не отправляются на выполнение и остаются в очереди. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_MEMORY_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, определяющее процент доступной памяти на узле, который может использовать запрос в данном пуле ресурсов. Если значение `-1`, действует ограничение на общую доступную память между всеми запросами. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `TOTAL_CPU_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, задающее процент доступного CPU, который могут использовать все запросы на узле в данном пуле ресурсов. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_CPU_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, определяющее процент доступного CPU на узле для одного запроса в пуле ресурсов. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `RESOURCE_WEIGHT` (Int32) — опциональное поле, задающее веса для распределения ресурсов между пулами. Если значение `-1`, веса не используются. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [CREATE RESOURCE POOL](create-resource-pool.md)
- [DROP RESOURCE POOL](drop-resource-pool.md)
