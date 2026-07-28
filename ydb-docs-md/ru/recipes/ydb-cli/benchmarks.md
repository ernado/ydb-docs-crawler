---
title: "Проведение нагрузочного тестирования"
url: "https://ydb.tech/docs/ru/recipes/ydb-cli/benchmarks?version=v26.1"
doc_path: "ru/recipes/ydb-cli/benchmarks"
version: "v26.1"
lang: "ru"
source_path: "ru/core/recipes/ydb-cli/benchmarks.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/recipes/ydb-cli/benchmarks.md"
description: "В YDB интегрирован инструментарий для проведения нагрузочных тестов с использованием стандартных бенчмарков: Бенчмарк Справка. TPC-C. tpcc. TPC-H. tpch. TPC-DS."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Проведение нагрузочного тестирования

В YDB интегрирован инструментарий для проведения нагрузочных тестов с использованием стандартных бенчмарков:

| Бенчмарк | Справка |
| --- | --- |
| [TPC-C](https://tpc.org/tpcc/) | [tpcc](../../reference/ydb-cli/workload-tpcc.md) |
| [TPC-H](https://tpc.org/tpch/) | [tpch](../../reference/ydb-cli/workload-tpch.md) |
| [TPC-DS](https://tpc.org/tpcds/) | [tpcds](../../reference/ydb-cli/workload-tpcds.md) |
| [ClickBench](https://benchmark.clickhouse.com/) | [clickbench](../../reference/ydb-cli/workload-click-bench.md) |

Помимо стандартных бенчмарков есть еще несколько внутренних:

| Бенчмарк | Справка |
| --- | --- |
| `Key Value` | [kv](../../reference/ydb-cli/workload-kv.md) |
| `Stock` | [stock](../../reference/ydb-cli/commands/workload/stock.md) |
| `Topic` | [topic](../../reference/ydb-cli/workload-topic.md) |
| `Transfer` | [topic](../../reference/ydb-cli/workload-transfer.md) |

Также предусмотрена возможность запуска пользовательских сценариев тестирования, которые инициируются посредством команды `ydb workload query`, см. [описание](../../reference/ydb-cli/workload-query.md). Подробности приведены в соответствующем разделе.

Все указанные методы эмулируют пользовательскую нагрузку на базу данных в рамках заданных сценариев. Детальное описание каждого метода представлено в соответствующих разделах, ссылки на которые приведены выше.

Все команды для работы с бенчмарками сгруппированы в соответствующие категории:

```bash
ydb workload tpcc --path path/in/database ...
ydb workload clickbench --path path/in/database ...
ydb workload tpch --path path/in/database ...
ydb workload tpcds --path path/in/database ...
ydb workload query --path path/in/database ...
ydb workload kv --path path/in/database ...
ydb workload stock --path path/in/database ...
ydb workload topic ...
ydb workload transfer ...
```

Нагрузочное тестирование состоит из трёх этапов:

1. [Подготовка данных](benchmarks.md#data-preparation)
2. [Тестирование](benchmarks.md#testing)
3. [Очистка](benchmarks.md#cleanup)

## Подготовка данных {#data-preparation}

Состоит из двух этапов, это инициализация таблиц и наполнение их данными.

### Инициализация {#inicializaciya}

Инициализация производится командой `init`:

```bash
ydb workload tpcc --path tpcc/10wh init
ydb workload clickbench --path clickbench/hits init --store=row
ydb workload tpch --path tpch/s1 init --store=column
ydb workload tpcds --path tpcds/s1 init --store=external-s3
ydb workload query --path user/suite1 init --suite-path /home/user/user_suite
ydb workload kv --path kv init --store=column
ydb workload stock --path stock init --store=row
ydb workload topic init --topic some_topic
ydb workload transfer topic-to-table init --topic some_topic --table /db/table
```

На этапе создания таблиц, если вы запускаете `tpch`, `tpcds` или `clickbench`, возможно дополнительно настроить создаваемые таблицы:

- Выбрать тип используемых таблиц: строковые, колоночные, внешние и тд. (параметр `--store`);
- Выбрать типы используемых колонок: строк (параметр `--string`), дат и времени (`--datetime`) и тип вещественных чисел (`--float-mode`).

Также можно указать, что перед созданием таблицы должны быть удалены, если они уже созданы (параметр `--clear`).

Подробнее см. описание команд для каждого бенчмарка:

- [tpcc init](../../reference/ydb-cli/workload-tpcc.md#init)
- [clickbench init](../../reference/ydb-cli/workload-click-bench.md#init)
- [tpch init](../../reference/ydb-cli/workload-tpch.md#init)
- [tpcds init](../../reference/ydb-cli/workload-tpcds.md#init)
- [query init](../../reference/ydb-cli/workload-query.md#init)
- [kv init](../../reference/ydb-cli/workload-kv.md#init)
- [stock init](../../reference/ydb-cli/commands/workload/stock.md#init)
- [topic init](../../reference/ydb-cli/workload-topic.md#init)
- [transfer init](../../reference/ydb-cli/workload-transfer.md#init)

### Наполнение данными {#napolnenie-dannymi}

Наполнение созданных таблиц данными выполняется с помощью команды `import`. Эта команда специфична для каждого бенчмарка, и её поведение зависит от дополнительных опций.

Подробное описание см. в соответствующих разделах:

- [tpcc import](../../reference/ydb-cli/workload-tpcc.md#load)
- [clickbench import](../../reference/ydb-cli/workload-click-bench.md#load)
- [tpch import](../../reference/ydb-cli/workload-tpch.md#load)
- [tpcds import](../../reference/ydb-cli/workload-tpcds.md#load)
- [query import](../../reference/ydb-cli/workload-query.md#load)

Примеры:

```bash
ydb workload tpcc --path tpcc/10wh import
ydb workload clickbench --path clickbench/hits import files --input hits.csv.gz
ydb workload tpch --path tpch/s1 import generator --scale 1
ydb workload tpcds --path tpcds/s1 import generator --scale 1
ydb workload query --path user/suite1 import --suite-path /home/user/user_suite
```

## Тестирование {#testing}

Непосредственный запуск нагрузочного тестирования выполняется командой `run`. Её поведение практически одинаково для разных бенчмарков, хотя некоторые различия всё-таки присутствуют.

Примеры:

```bash
ydb workload tpcc --path tpcc/10wh run
ydb workload clickbench --path clickbench/hits run --include 1-5,8
ydb workload tpch --path tpch/s1 run --exсlude 3,4 --iterations 3
ydb workload tpcds --path tpcds/s1 run --plan ~/query_plan --include 2 --iterations 5
ydb workload query --path user/suite1 run --plan ~/query_plan --include first_query_set.1.sql,second_query_set.2.sql --iterations 5
ydb workload kv --path kv run mixed
ydb workload stock --path stock run add-rand-order
ydb workload topic run full --topic some_topic
ydb workload transfer topic-to-table run --topic some_topic --table /db/table
```

Команда `run` для каждого из бенчмарков имеет ряд дополнительных параметров для настройки видов генерируемых отчётов, сбора статистики и прочих результатов нагрузочного тестирования.

Подробное описание см. в соответствующих разделах:

- [tpcc run](../../reference/ydb-cli/workload-tpcc.md#run)
- [clickbench run](../../reference/ydb-cli/workload-click-bench.md#run)
- [tpch run](../../reference/ydb-cli/workload-tpch.md#run)
- [tpcds run](../../reference/ydb-cli/workload-tpcds.md#run)
- [query run](../../reference/ydb-cli/workload-query.md#run)
- [kv run](../../reference/ydb-cli/workload-kv.md#run)
- [stock run](../../reference/ydb-cli/commands/workload/stock.md#run)
- [topic run](../../reference/ydb-cli/workload-topic.md#run)
- [transfer run](../../reference/ydb-cli/workload-transfer.md#run)

## Очистка {#cleanup}

При завершении работ по нагрузочному тестированию тестовые данные и таблицы можно удалить командой `clean`:

```bash
ydb workload tpcc --path tpcc/10wh clean
ydb workload clickbench --path clickbench/hits clean
ydb workload tpch --path tpch/s1 clean
ydb workload tpcds --path tpcds/s1 clean
ydb workload query --path user/suite1 clean
ydb workload kv --path kv clean
ydb workload stock --path stock clean
ydb workload topic clean --topic some_topic
ydb workload transfer topic-to-table clean --topic some_topic --table /db/table
```

Подробное описание см. в соответствующих разделах:

- [tpcc clean](../../reference/ydb-cli/workload-tpcc.md#cleanup)
- [clickbench clean](../../reference/ydb-cli/workload-click-bench.md#cleanup)
- [tpch clean](../../reference/ydb-cli/workload-tpch.md#cleanup)
- [tpcds clean](../../reference/ydb-cli/workload-tpcds.md#cleanup)
- [query clean](../../reference/ydb-cli/workload-query.md#cleanup)
- [kv clean](../../reference/ydb-cli/workload-kv.md#cleanup)
- [stock clean](../../reference/ydb-cli/commands/workload/stock.md#cleanup)
- [topic clean](../../reference/ydb-cli/workload-topic.md#cleanup)
- [transfer clean](../../reference/ydb-cli/workload-transfer.md#cleanup)
