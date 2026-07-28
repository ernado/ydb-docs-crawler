---
title: "Нагрузочное тестирование"
url: "https://ydb.tech/docs/ru/reference/ydb-cli/commands/workload/?version=v26.1"
doc_path: "ru/reference/ydb-cli/commands/workload/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/ydb-cli/commands/workload/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/ydb-cli/commands/workload/index.md"
description: "Нагрузочное тестирование. С помощью команды workload вы можете запустить различные виды нагрузки для вашей БД. Общий вид команды:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Нагрузочное тестирование

С помощью команды `workload` вы можете запустить различные виды нагрузки для вашей БД.

Общий вид команды:

```bash
ydb [global options...] workload [subcommands...]
```

- `global options` — [глобальные параметры](../global-options.md).
- `subcommands` — [подкоманды](index.md#subcommands).

Посмотрите описание команды для запуска нагрузки:

```bash
ydb workload --help
```

## Доступные подкоманды {#subcommands}

В данный момент поддерживаются следующие виды нагрузочных тестов:

- [Stock](stock.md) - симулятор склада интернет-магазина.
- [Key-value](../../workload-kv.md) - Key-Value нагрузка.
- [ClickBench](../../workload-click-bench.md) - [аналитический бенчмарк ClickBench](https://github.com/ClickHouse/ClickBench).
- [TPC-C](../../workload-tpcc.md): [TPC-C benchmark](https://www.tpc.org/tpcc/).
- [TPC-H](../../workload-tpch.md) - [TPC-H бенчмарк](https://www.tpc.org/tpch/).
- [TPC-DS](../../workload-tpcds.md) - [TPC-DS бенчмарк](https://www.tpc.org/tpcds/).
- [Topic](../../workload-topic.md) - Topic нагрузка.
- [Transfer](../../workload-transfer.md) - Transfer нагрузка.
- [Query](../../workload-query.md) - Пользовательская нагрузка.
