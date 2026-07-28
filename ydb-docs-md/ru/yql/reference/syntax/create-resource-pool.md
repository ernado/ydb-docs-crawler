---
title: "CREATE RESOURCE POOL"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-resource-pool?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-resource-pool"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-resource-pool.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-resource-pool.md"
description: "CREATE RESOURCE POOL создаёт пул ресурсов. Синтаксис. CREATE RESOURCE POOL <name> WITH ( <parameter_name> [= <parameter_value>] [,... ] )."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE RESOURCE POOL

`CREATE RESOURCE POOL` создаёт [пул ресурсов](../../../concepts/glossary.md#resource-pool.md).

## Синтаксис {#sintaksis}

```yql
CREATE RESOURCE POOL <name>
WITH ( <parameter_name> [= <parameter_value>] [, ... ] )
```

- `name` - имя создаваемого пула ресурсов. Должно быть уникально. Не допускается запись в виде пути (т.е. не должно содержать `/`).
- `WITH ( <parameter_name> [= <parameter_value>] [, ... ] )` позволяет задать значения параметров, определяющих поведение пула ресурсов.

### Параметры {#parameters}

- `CONCURRENT_QUERY_LIMIT` (Int32) — опциональное поле, задающее количество параллельно выполняющихся запросов в пуле ресурсов. Если значение `-1`, то ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `QUEUE_SIZE` (Int32) — опциональное поле, определяющее размер очереди ожидания. Всего в системе может находиться не более чем CONCURRENT_QUERY_LIMIT+QUEUE_SIZECONCURRENT\\_QUERY\\_LIMIT + QUEUE\\_SIZECONCURRENT_QUERY_LIMIT+QUEUE_SIZE запросов одновременно. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].
- `DATABASE_LOAD_CPU_THRESHOLD` (Int32) — опциональное поле, задающее порог загрузки CPU всей базы данных, после которого запросы не отправляются на выполнение и остаются в очереди. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_MEMORY_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, определяющее процент доступной памяти на узле, который может использовать запрос в данном пуле ресурсов. Если значение `-1`, действует ограничение на общую доступную память между всеми запросами. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `TOTAL_CPU_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, задающее процент доступного CPU, который могут использовать все запросы на узле в данном пуле ресурсов. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `QUERY_CPU_LIMIT_PERCENT_PER_NODE` (Double) — опциональное поле, определяющее процент доступного CPU на узле для одного запроса в пуле ресурсов. Если значение `-1`, ограничений нет. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,100\]-1, \[0, 100\]−1,\[0,100\].
- `RESOURCE_WEIGHT` (Int32) — опциональное поле, задающее веса для распределения ресурсов между пулами. Если значение `-1`, веса не используются. Значение по умолчанию: `-1`. Допустимые значения: −1,\[0,231−1\]-1, \[0, 2^{31}-1\]−1,\[0,231−1\].

## Замечания {#remark}

Запросы всегда выполняются в каком-либо пуле ресурсов. По умолчанию все запросы отправляются в пул ресурсов `default`, который создаётся автоматически и не может быть удалён — он всегда присутствует в системе.

Если для параметра `CONCURRENT_QUERY_LIMIT` установить значение 0, то все запросы, отправленные в этот пул, будут немедленно завершены со статусом `PRECONDITION_FAILED`.

## Разрешения {#razresheniya}

Требуется [разрешение](grant.md#permissions-list) `CREATE TABLE` на директорию `.metadata/workload_manager/pools`, пример выдачи такого разрешения:

```yql
GRANT 'CREATE TABLE' ON `.metadata/workload_manager/pools` TO `user1@domain`;
```

## Примеры {#examples}

```yql
CREATE RESOURCE POOL olap WITH (
    CONCURRENT_QUERY_LIMIT=20,
    QUEUE_SIZE=1000,
    DATABASE_LOAD_CPU_THRESHOLD=80,
    RESOURCE_WEIGHT=100,
    QUERY_MEMORY_LIMIT_PERCENT_PER_NODE=80,
    TOTAL_CPU_LIMIT_PERCENT_PER_NODE=70
)
```

В примере выше создаётся пул ресурсов со следующими ограничениями:

- Максимальное число параллельных запросов — 20.
- Максимальный размер очереди ожидания — 1000.
- При достижении загрузки базы данных в 80%, запросы перестают запускаться параллельно.
- Каждый запрос в пуле может потребить не более 80% доступной памяти на узле. Если запрос превысит этот лимит, он будет завершён со статусом `OVERLOADED`.
- Общее ограничение на доступный CPU для всех запросов в пуле на узле составляет 70%.
- Пул ресурсов имеет вес 100, который начинает работать только в случае переподписки.

## См. также {#sm-takzhe}

- [Workload Manager — управление потреблением ресурсов](../../../dev/resource-consumption-management.md)
- [ALTER RESOURCE POOL](alter-resource-pool.md)
- [DROP RESOURCE POOL](drop-resource-pool.md)
