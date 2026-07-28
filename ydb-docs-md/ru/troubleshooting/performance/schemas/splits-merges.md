---
title: "Избыточные разделения и слияния партиций таблиц"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/schemas/splits-merges?version=v26.1"
doc_path: "ru/troubleshooting/performance/schemas/splits-merges"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/schemas/splits-merges.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/schemas/splits-merges.md"
description: "Важно. Поддерживается только для строковых таблиц. Поддержка функциональности для колоночных таблиц находится в разработке."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Избыточные разделения и слияния партиций таблиц

> [!WARNING]
> Поддерживается только для [строковых](../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

Каждая партиция [строковой таблицы](../../../concepts/datamodel/table.md#row-oriented-tables) в YDB обрабатывается таблеткой [data shard](../../../concepts/glossary.md#data-shard). YDB поддерживает автоматическое [разделение и слияние](../../../concepts/datamodel/table.md#partitioning) таблеток data shard, что позволяет легко адаптироваться к изменениям в рабочих нагрузках. Однако эти операции не являются бесплатными и могут оказать кратковременное негативное влияние на задержки запросов.

Когда YDB разбивает партицию, исходная партиция заменяется двумя новыми партициями, охватывающими тот же диапазон первичных ключей. Теперь две таблетки data shard обрабатывают диапазон первичных ключей, который ранее обрабатывался одной таблеткой data shard, тем самым добавляя больше вычислительных ресурсов для таблицы.

По умолчанию YDB разделяет партицию таблицы, когда её размер достигает 2 ГБ. Однако рекомендуется также включить разделение по загрузке, что позволит YDB разделять перегруженные партиции, даже если их размер меньше 2 ГБ.

У [scheme shard](../../../concepts/glossary.md#scheme-shard) уходит примерно 15 секунд на принятие решения о разделении таблетки data shard. По умолчанию пороговое значение потребления процессора для разделения таблетки data shard установлено в 50%.

Когда YDB объединяет соседние партиции в строковой таблице, они заменяются одной партицией, которая охватывает их диапазон первичных ключей. Соответствующие таблетки data shard также объединяются в одну таблетку для управления новой партицией.

Для того чтобы произошло слияние, таблетки data shard должны существовать не менее 10 минут, а их загрузка процессора за последний час не должна превышать 35%.

При настройке [партиционирования таблицы](../../../concepts/datamodel/table.md#partitioning) вы можете также установить лимиты на [минимальное](../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) и [максимальное количество партиций](../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count). Если разница между минимальным и максимальным пределами превышает 20%, а загрузка таблицы значительно меняется с течением времени, [Hive](../../../concepts/glossary.md#hive) может начать разделять перегруженные таблицы, а затем объединять их обратно в периоды низкой загрузки.

## Диагностика {#diagnostika}

1. Посмотрите, есть ли всплески на графике **Split / Merge partitions** на панели мониторинга Grafana **[DB status](../../../reference/observability/metrics/grafana-dashboards.md#dbstatus)**.

   ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/schemas/_assets/splits-merges.png)

   На этой диаграмме отображаются временные ряды следующих данных:

   - количество разделений партиций таблиц в секунду (синий);
   - количество слияний партиций таблиц в секунду (зелёный).

2. Проверьте, не увеличилась ли пользовательская нагрузка, когда был замечен всплеск количества разделений и слияний таблеток.

   - Просмотрите диаграммы на панели мониторинга **DataShard** в Grafana на предмет любых изменений в объёме данных, считываемых или записываемых запросами.
   - Изучите диаграмму **Requests** на панели мониторинга **Query engine** в Grafana на предмет увеличения количества запросов.

3. Чтобы определить недавно разделённые или слитые таблетки, выполните следующие шаги:

   1. Во [Встроенном UI](../../../reference/embedded-ui/index.md) нажмите на ссылку **Developer UI** в правом верхнем углу.

   2. Перейдите на страницу **Node Table Monitor** > **All tablets of the cluster**.

   3. Для отображения только таблеток data shard в фильтре **TabletType** укажите `DataShard`.

      ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/schemas/_assets/node-tablet-monitor-data-shard.png)

   4. Отсортируйте таблетки по колонке **ChangeTime**. Обратите внимание на таблетки, значения времени изменения которых совпадают с пиковыми значениями на диаграмме **Split / Merge partitions**.

   5. Чтобы определить таблицу, связанную с таблеткой data shard, в строке data shard нажмите на ссылку в столбце **TabletID**.

   6. На странице **Tablets** откройте ссылку **App**.

      Информация о таблице отображается в секции **User table <имя таблицы>**.

4. Чтобы определить, связана ли проблема с неправильной схемой таблицы, выполните следующие шаги:

   1. Получите информацию о проблемной таблице с помощью [YDB CLI](../../../reference/ydb-cli/index.md). Выполните следующую команду:

      ```bash
      ydb scheme describe <имя_таблицы>
      ```

   2. В выводе команды проанализируйте **Auto partitioning settings**:

      - `Partitioning by load`
      - `Max partitions count`
      - `Min partitions count`

## Рекомендации {#rekomendacii}

Если пользовательская нагрузка на YDB не изменилась, рассмотрите возможность изменения интервала между минимальным и максимальным лимитами на количество партиций таблицы до рекомендуемой разницы в 20%. Используйте инструкцию YQL [`ALTER TABLE имя_таблицы SET (ключ = значение)`](../../../yql/reference/syntax/alter_table/set.md) для обновления параметров [`AUTO_PARTITIONING_MIN_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) и [`AUTO_PARTITIONING_MAX_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count).

Если вы хотите избежать разделения и слияния таблеток data shard, вы можете выставить одинаковые значения для параметров [`AUTO_PARTITIONING_MIN_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_min_partitions_count) и [`AUTO_PARTITIONING_MAX_PARTITIONS_COUNT`](../../../concepts/datamodel/table.md#auto_partitioning_max_partitions_count) или отключить разделение по загрузке.
