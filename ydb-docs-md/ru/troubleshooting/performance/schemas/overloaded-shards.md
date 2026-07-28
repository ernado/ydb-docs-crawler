---
title: "Перегруженные таблетки data shard"
url: "https://ydb.tech/docs/ru/troubleshooting/performance/schemas/overloaded-shards?version=v26.1"
doc_path: "ru/troubleshooting/performance/schemas/overloaded-shards"
version: "v26.1"
lang: "ru"
source_path: "ru/core/troubleshooting/performance/schemas/overloaded-shards.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/troubleshooting/performance/schemas/overloaded-shards.md"
description: "Таблетки data shard, обслуживающие строковые таблицы, могут быть перегружены по следующим причинам:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Перегруженные таблетки data shard

Таблетки [data shard](../../../concepts/glossary.md#data-shard), обслуживающие [строковые таблицы](../../../concepts/datamodel/table.md#row-oriented-tables), могут быть перегружены по следующим причинам:

- Таблица создана без указания параметра [AUTO_PARTITIONING_BY_LOAD](../../../concepts/datamodel/table.md#AUTO_PARTITIONING_BY_LOAD).

  В этом случае YDB не разбивает перегруженные таблетки data shard.

  Таблетки data shard являются однопоточными и обрабатывают запросы последовательно. Каждая таблетка data shard может принимать на выполнение до 10000 операций. Принятые запросы ожидают своей очереди на выполнение. Таким образом, чем длиннее очередь, тем выше задержка.

  Если таблетка data shard уже содержит 10000 операций в своей очереди, новые запросы будут возвращать ошибку «overloaded». Повторите такие запросы, используя экспоненциально растущий перерыв, см. [Ошибки «overloaded»](../queries/overloaded-errors.md).

- Таблица создана с параметром [AUTO_PARTITIONING_MAX_PARTITIONS_COUNT](../../../concepts/datamodel/table.md#AUTO_PARTITIONING_MAX_PARTITIONS_COUNT) и уже достигла лимита на число партиций.

- Неэффективный [первичный ключ](../../../concepts/glossary.md#primary-key), который вызывает дисбаланс в распределении запросов по таблеткам data shard. Типичным примером является использование монотонно увеличивающегося первичного ключа при загрузке данных, что может привести к перегрузке «последней» партиции. Например, это может произойти с автоматически увеличивающимся первичным ключом, использующим тип данных [Serial](../../../yql/reference/types/serial.md).

## Диагностика {#diagnostika}

1. Используйте Встроенный UI или Grafana, чтобы проверить, не перегружены ли узлы YDB:

   - На панели мониторинга Grafana **[DB overview](../../../reference/observability/metrics/grafana-dashboards.md#dboverview)** проанализируйте диаграмму **Overloaded shard count**.

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/schemas/_assets/overloaded-shards-dashboard.png)

     Диаграмма отображает перегруженные таблетки data shard в кластере YDB, но она не показывает таблицы, в которых есть перегруженные таблетки.

     > [!TIP]
     > Настройте уведомления в Grafana о перегрузках таблеток data shard.

   - Во [Встроенном UI](../../../reference/embedded-ui/index.md):

     1. Перейдите на вкладку **Databases** и выберите базу данных.
     2. На вкладке **Navigation** убедитесь, что база данных выбрана.
     3. Откройте вкладку **Diagnostics**.
     4. Откройте вкладку **Top shards**.
     5. На вкладках **Immediate** и **Historical** отсортируйте таблетки по колонке **CPUCores** и проанализируйте информацию.

     ![](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/schemas/_assets/partitions-by-cpu.png)

     Кроме того, информация о перегруженных таблетках представлена в виде системной таблицы. Дополнительные сведения см. в разделе [История перегруженных партиций](../../../dev/system-views.md#top-overload-partitions).

2. Чтобы точно определить проблему со схемой, используйте [Встроенный UI](../../../reference/embedded-ui/index.md) или [YDB CLI](../../../reference/ydb-cli/index.md):

   - Во [Встроенном UI](../../../reference/embedded-ui/index.md):

     1. На вкладке **Databases** нажмите на базу данных.

     2. На вкладке **Navigation** выберите требуемую базу данных.

     3. Откройте вкладку **Diagnostics**.

     4. На вкладке **Describe** перейдите на страницу `root > PathDescription > Table > PartitionConfig > PartitioningPolicy`.

        ![Describe](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/troubleshooting/performance/schemas/_assets/describe.png)

     5. Проанализируйте значения **PartitioningPolicy**:

        - `SizeToSplit`
        - `SplitByLoadSettings`
        - `MaxPartitionsCount`

        Если в таблице не отображаются вышеперечисленные параметры, см. [Рекомендации по конфигурации таблиц](overloaded-shards.md#table-config).

     > [!NOTE]
     > Эта информация также отображается на вкладке **Diagnostics > Info**.

   - В [YDB CLI](../../../reference/ydb-cli/index.md):

     1. Чтобы получить информацию о проблемной таблице, выполните следующую команду:

        ```bash
        ydb scheme describe <table_name>
        ```

     2. В выводе команды проанализируйте **Auto partitioning settings**:

        - `Partitioning by size`
        - `Partitioning by load`
        - `Max partitions count`

        Если в таблице не указаны эти параметры, см. [Рекомендации по конфигурации таблиц](overloaded-shards.md#table-config).

3. Проанализируйте, монотонно ли увеличиваются значения первичного ключа:

   - Проверьте тип данных столбца первичного ключа. Типы данных `Serial` используются для автоматического увеличения значений.
   - Проверьте логику приложения.
   - Вычислите разницу между минимальным и максимальным значениями столбца первичного ключа. Затем сравните это значение с количеством строк в данной таблице. Если эти значения совпадают, возможно первичный ключ в этой таблице увеличивается монотонно.

   Если значения первичного ключа действительно увеличиваются монотонно, см. [Рекомендации для несбалансированного первичного ключа](overloaded-shards.md#pk-recommendations).

## Рекомендации {#rekomendacii}

### Для конфигурации таблиц {#table-config}

Рассмотрите следующие решения для устранения перегрузки таблеток data shard:

- Если в проблемной таблице не включено партиционирование по нагрузке, включите его.

  > [!TIP]
  > Партиционирование по нагрузке отключено, если на вкладке **Diagnostics > Info** во **Встроенном UI** или в выводе команды `ydb scheme describe` отображается строка `Partitioning by load: false`.

- Если количество партиций в таблице достигло максимального лимита, увеличьте максимальный лимит партиций таблицы.

  > [!TIP]
  > Чтобы определить количество партиций в таблице, см. значение `PartCount` на вкладке **Diagnostics > Info** во **Встроенном UI**.

Обе операции можно выполнить с помощью запроса [`ALTER TABLE ... SET`](../../../yql/reference/syntax/alter_table/set.md).

### Для несбалансированного первичного ключа {#pk-recommendations}

Рассмотрите возможность изменения первичного ключа, чтобы равномерно распределить нагрузку по партициям таблицы. Вы не можете изменить первичный ключ существующей таблицы. Для этого вам нужно будет создать новую таблицу с изменённым первичным ключом, а затем перенести данные в новую таблицу.

> [!NOTE]
> Также рассмотрите возможность изменения логики вашего приложения для генерации значений первичного ключа для новых строк. Например, используйте хэши значений вместо самих значений.
