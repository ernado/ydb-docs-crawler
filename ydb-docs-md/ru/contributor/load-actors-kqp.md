---
title: "KqpLoad"
url: "https://ydb.tech/docs/ru/contributor/load-actors-kqp?version=v26.1"
doc_path: "ru/contributor/load-actors-kqp"
version: "v26.1"
lang: "ru"
source_path: "ru/core/contributor/load-actors-kqp.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/contributor/load-actors-kqp.md"
description: "Тестирует производительности кластера YDB в целом, нагружая все компоненты через слой Query Processor. Нагрузка, аналогична нагрузке от подкоманды workload YDB"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# KqpLoad

Тестирует производительности кластера YDB в целом, нагружая все компоненты через слой Query Processor. Нагрузка, аналогична нагрузке от подкоманды [workload](../reference/ydb-cli/commands/workload/index.md) YDB CLI, но запускается изнутри кластера.

Вы можете запустить два вида нагрузки:

- **Stock** — симулирует работу склада интернет-магазина: создает заказы из нескольких товаров, получает список заказов по клиенту.
- **Key-value** — использует БД как key-value хранилище.

Перед началом работы создаются необходимые таблицы, после завершения они удаляются.

## Параметры актора {#options}

Ниже описаны основные параметры актора. Полный список параметров смотрите в файле [load_test.proto](https://github.com/ydb-platform/ydb/blob/main/ydb/core/protos/load_test.proto) Git-репозитория YDB.

| Параметр | Описание |
| --- | --- |
| `DurationSeconds` | Продолжительность нагрузки в секундах. |
| `WindowDuration` | Размер окна для агрегации статистики. |
| `WorkingDir` | Путь директории, в которой будут созданы тестовые таблицы. |
| `NumOfSessions` | Количество параллельных потоков, подающих нагрузку. Каждый поток пишет в свою сессию. |
| `DeleteTableOnFinish` | Если `False`, то созданные таблицы не удаляются после завершения работы нагрузки. Может быть полезно в случае, когда при первом запуске актора создается большая таблица, а при последующих выполняются запросы к ней. |
| `UniformPartitionsCount` | Количество партиций, создаваемых в тестовых таблицах. |
| `WorkloadType` | Тип нагрузки.  <br>В случае Stoсk:<br>- `0` — InsertRandomOrder;<br>- `1` — SubmitRandomOrder;<br>- `2` — SubmitSameOrder;<br>- `3` — GetRandomCustomerHistory;<br>- `4` — GetCustomerHistory.<br>В случае Key-Value:<br>- `0` — UpsertRandom;<br>- `1` — InsertRandom;<br>- `2` — SelectRandom. |
| `Workload` | Вид нагрузки.  <br>`Stock`:<br>- `ProductCount` — количество видов товаров.<br>- `Quantity` — количество товаров каждого вида на складе.<br>- `OrderCount` — первоначальное количество заказов в БД.<br>- `Limit` — минимальное количество шардов для таблиц.<br>`Kv`:<br>- `InitRowCount` — до начала нагрузки нагружающий актор запишет в таблицу указанное количество строк.<br>- `StringLen` — длина строки `value`.<br>- `ColumnsCnt` — сколько столбцов использовать в таблице.<br>- `RowsCnt` — сколько строк вставлять или читать в одном SQL запросе. |

## Примеры {#example}

Следующий актор запускает stock-нагрузку БД `/slice/db`, выполняя простые UPSERT-запросы в `64` потока в течение `30` секунд.

```proto
KqpLoad: {
    DurationSeconds: 30
    WindowDuration: 1
    WorkingDir: "/slice/db"
    NumOfSessions: 64
    UniformPartitionsCount: 1000
    DeleteTableOnFinish: 1
    WorkloadType: 0
    Stock: {
        ProductCount: 100
        Quantity: 1000
        OrderCount: 100
        Limit: 10
    }
}
```

Результатом теста является количество успешных транзакций в секунду, количество повторных попыток исполнения транзакций и количество ошибок.

> [!TIP]
> **Хотите присоединиться к команде разработки YDB?**
>
> Ознакомьтесь с разделами о [команде YDB и открытых вакансиях](https://ydb.tech/ru/careers/), а также о [возможностях для студентов](https://ydb.tech/ru/students/).
