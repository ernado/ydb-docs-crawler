---
title: "Пример диагностики перегруженных шардов"
url: "https://ydb.tech/docs/ru/troubleshooting/examples/schemas/overloaded-shard-simple-case?version=v26.1"
doc_path: "ru/troubleshooting/examples/schemas/overloaded-shard-simple-case"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/examples/schemas/overloaded-shard-simple-case.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/examples/schemas/overloaded-shard-simple-case.md"
description: "В этой статье рассматривается пример диагностики перегруженных шардов и решения этой проблемы."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Пример диагностики перегруженных шардов

В этой статье рассматривается пример диагностики перегруженных шардов и решения этой проблемы.

Дополнительную информацию о перегруженных шардах и причинах их перегрузки см. в статье [Перегруженные таблетки data shard](../../performance/schemas/overloaded-shards.md).

Статья начинается с [описания возникшей проблемы](overloaded-shard-simple-case.md#initial-issue). Затем мы проанализируем графики в Grafana и информацию на вкладке **Diagnostics** в [Embedded UI](../../../reference/embedded-ui/index.md), чтобы [найти решение](overloaded-shard-simple-case.md#solution), и проверим [его эффективность](overloaded-shard-simple-case.md#aftermath).

В конце статьи приводятся шаги по [воспроизведению проблемы](overloaded-shard-simple-case.md#testbed).

## Описание проблемы {#initial-issue}

Вас уведомили о задержках при обработке пользовательских запросов в вашей системе.

> [!NOTE]
> Речь идёт о запросах к [строковой таблице](../../../concepts/datamodel/table.md#row-oriented-tables), управляемой [data shard](../../../concepts/glossary.md#data-shard)'ом.

Рассмотрим графики **Latency** на панели мониторинга Grafana [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview) и определим, имеет ли отношение наша проблема к кластеру YDB:

![DB Overview > Latencies > R tx server latency percentiles](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-latency-percentiles.png)

<details>
<summary>См. описание графика</summary>

График отображает процентили задержек транзакций. Примерно в `10:19:30` эти значения выросли в два-три раза.

</details>

![DB Overview > Latencies > Read only tx server latency](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-latencies.png)

<details>
<summary>См. описание графика</summary>

График отображает тепловую карту (heatmap) задержек транзакций. Транзакции группируются на основании их задержек, каждая группа (bucket) окрашивается в свой цвет. Таким образом, этот график показывает как количество транзакций, обрабатываемых YDB в секунду (по вертикальной оси), так и распределение задержек среди транзакций (цветовая дифференциация).

К `10:20:30` доля транзакций с минимальными задержками (`Группа 1`, тёмно-зелёный) упала в четыре-пять раз. `Группа 4` выросла примерно в пять раз, а также выделилась новая группа транзакций с ещё более высокими задержками — `Группа 8`.

</details>

Таким образом, мы видим, что задержки действительно выросли. Теперь нам необходимо локализовать проблему.

## Диагностика {#diagnostics}

Давайте определим причину роста задержек. Могли ли они увеличиться из-за возросшей нагрузки? Посмотрим на график **Requests** в секции **API details** панели мониторинга Grafana [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview):

![API details](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-api-section-requests.png)

Количество пользовательских запросов выросло приблизительно с 27 000 до 35 000 в `10:20:00`. Но может ли YDB справиться с увеличившейся нагрузкой без дополнительных аппаратных ресурсов?

Загрузка CPU увеличилась, что видно на графике **CPU by execution pool**.

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-by-execution-pool.png)

<details>
<summary>См. графики на панели мониторинга Grafana **CPU**</summary>

Графики на панели мониторинга Grafana **CPU** показывают рост нагрузки на CPU [в пуле ресурсов пользователей и интерконнекта](../../../concepts/glossary.md#actor-system-pool):

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-user-pool-by-actors.png)

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-ic-pool.png)

![CPU](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-cpu-dashboard-ic-pool-by-host.png)

</details>

Мы также можем взглянуть на общее использование CPU на вкладке **Diagnostics** в [Embedded UI](../../../reference/embedded-ui/index.md):

![CPU diagnostics](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-cpu-usage.png)

Кластер YDB не использует все ресурсы CPU.

Взглянув на секции **DataShard** и **DataShard details** на панели мониторинга Grafana [DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview), мы увидим, что после роста нагрузки на кластер один из data shard'ов был перегружен.

![Throughput](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-throughput-rows.png)

<details>
<summary>См. описание графика</summary>

Этот график показывает, что количество читаемых строк в базе данных YDB увеличилось с ~26 000 до ~33 500 строк в секунду.

</details>

![Shard distribution by load](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-shard-distribution-by-workload.png)

<details>
<summary>См. описание графика</summary>

Этот график отображает тепловую карту распределения data shard'ов по нагрузке. Каждый data shard потребляет от 0% до 100% ядра CPU. Data shard'ы делятся на десять групп по занимаемой ими доле ядра CPU — 0-10%, 10-20% и т.д. Эта тепловая карта показывает количество data shard'ов в каждой группе.

График показывает только один data shard, нагрузка на который изменилась примерно в `10:19:30` — data shard перешёл в `Группу 70`, содержащую шарды, нагруженные на 60–70%.

</details>

![Overloaded shard](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-grafana-overloaded-shards.png)

<details>
<summary>См. описание графика</summary>

По аналогии с предыдущим графиком, **Overloaded shard count** — это тепловая карта распределения data shard'ов по нагрузке. Однако этот график отображает только data shard'ы с нагрузкой, превышающей 60%.

График показывает, что нагрузка на один data shard увеличилась до 70% примерно в `10:19:30`.

</details>

Чтобы определить, какую таблицу обслуживает перегруженный data shard, откроем вкладку **Diagnostics > Top shards** во встроенном UI:

![Diagnostics > shards](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-top-shards.png)

Мы видим, что один из data shard'ов, обслуживающих таблицу `kv_test`, нагружен на 67%.

Далее давайте взглянем на информацию о таблице `kv_test` на вкладке **Info**:

![stock table info](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/incident-ui-table-info.png)

> [!WARNING]
> Таблица `kv_test` была создана с отключённым партиционированием по нагрузке и содержит только одну партицию.
>
> Это означает, что все запросы к этой таблице обрабатывает один data shard. Учитывая, что data shard'ы — это однопоточные компоненты, обрабатывающие за раз только один запрос, такой подход неэффективен.

## Решение {#solution}

Нам необходимо включить партиционирование по нагрузке для таблицы `kv_test`:

1. Во встроенном UI выберите базу данных.

2. Откройте вкладку **Query**.

3. Выполните следующий запрос:

   ```yql
   ALTER TABLE kv_test SET (
       AUTO_PARTITIONING_BY_LOAD = ENABLED
   );
   ```

## Результат {#aftermath}

После включения автоматического партиционирования для таблицы `kv_test` перегруженный data shard разделился на два.

![Shard distribution by load](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-shard-distribution-by-workload.png)

<details>
<summary>См. описание графика</summary>

График показывает, что количество data shard'ов выросло примерно в `10:28:00`. Судя по цвету групп, их нагрузка не превышает 40%.

</details>

![Overloaded shard count](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-overloaded-shards.png)

<details>
<summary>См. описание графика</summary>

Перегруженный шард исчез с графика примерно в `10:28:00`.

</details>

Теперь два data shard'а обрабатывают запросы к таблице `kv_test`, и ни один из них не перегружен:

![Overloaded shard count](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-ui-top-shards.png)

Давайте убедимся, что задержки транзакций вернулись к прежним значениям:

![Final latency percentiles](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-latency-percentiles.png)

<details>
<summary>См. описание графика</summary>

Примерно в `10:28:00` процентили задержек p50, p75 и p95 упали практически до прежних значений. Задержки p99 сократились не настолько значительно, но всё же уменьшились в два раза.

</details>

![Final latencies](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/examples/schemas/_assets/overloaded-shard-simple-case/aftermath-grafana-latencies.png)

<details>
<summary>См. описание графика</summary>

Транзакции на этом графике теперь распределены по шести группам. Примерно половина транзакций вернулась в `Группу 1`, то есть их задержки не превышают одной миллисекунды. Более трети транзакций находятся в `Группе 2` с задержками от одной до двух миллисекунд. Одна шестая транзакций — в `Группе 4`. Размеры остальных групп незначительны.

</details>

Задержки практически вернулись к уровню до увеличения нагрузки. При этом мы не увеличили расходы на приобретение дополнительных аппаратных ресурсов, а просто включили автоматическое партиционирование по нагрузке, что позволило более эффективно использовать доступные ресурсы.

|  |  |  |  |
| --- | --- | --- | --- |
| Имя группы | Задержки, мс | Один перегруженный data shard,  <br> транзакций в секунду | Несколько data shard'ов,  <br> транзакций в секунду |
| 1 | 0-1 | 2110 | ▲ 16961 |
| 2 | 1-2 | 5472 | ▲ 13147 |
| 4 | 2-4 | 16437 | ▼ 6041 |
| 8 | 4-8 | 9430 | ▼ 432 |
| 16 | 8-16 | 98.8 | ▼ 52.4 |
| 32 | 16-32 | — | ▲ 0.578 |

## Тестовый стенд {#testbed}

### Топология {#topologiya}

Для этого примера мы использовали кластер YDB из трёх серверов на Ubuntu 22.04 LTS. На каждом сервере был запущен один [узел хранения](../../../concepts/glossary.md#storage-node) и три [узла баз данных](../../../concepts/glossary.md#database-node), обслуживающих одну и ту же базу данных.

### Аппаратная конфигурация {#apparatnaya-konfiguraciya}

Аппаратные ресурсы серверов (виртуальных машин) приведены ниже:

- Платформа: Intel Broadwell

- Гарантированный уровень производительности vCPU: 100%

- vCPU: 28

- Память: 32 GB

- Диски:

  - 3 × 93 GB SSD на каждом узле YDB
  - 20 GB HDD для операционной системы

### Тест {#test}

Нагрузка на кластер YDB была запущена с помощью команды CLI `ydb workload`. Дополнительную информацию см. в статье [Нагрузочное тестирование](../../../reference/ydb-cli/commands/workload/index.md).

Чтобы воспроизвести нагрузку, выполните следующие шаги:

1. Проинициализируйте таблицы для нагрузочного тестирования:

   ```shell
   ydb workload kv init --min-partitions 1 --auto-partition 0
   ```

   Мы намеренно отключаем автоматическое партиционирование для создаваемых таблиц используя опции `--min-partitions 1 --auto-partition 0`.

2. Воспроизведите стандартную нагрузку на кластер YDB:

   ```shell
   ydb workload kv run select -s 600 -t 100
   ```

   Мы запустили простую нагрузку, используя базу данных YDB как Key-Value хранилище. Точнее, мы использовали нагрузку `select` для выполнения `SELECT`-запросов, возвращающих строки по точному совпадению primary ключа.

   Параметр `-t 100` используется для запуска нагрузочного тестирования в 100 потоков.

3. Создайте перегрузку на кластере YDB:

   ```shell
   ydb workload kv run select -s 1200 -t 250
   ```

   Как только первый тест завершился, мы немедленно запустили тот же самый тест в 250 потоков, чтобы создать перегрузку.

## Смотрите также {#smotrite-takzhe}

- [Диагностика проблем с производительностью](../../performance/index.md)
- [Перегруженные таблетки data shard](../../performance/schemas/overloaded-shards.md)
- [Строковые таблицы](../../../concepts/datamodel/table.md#row-oriented-tables)
