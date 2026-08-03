---
title: "Добавление или удаление потока изменений"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/changefeed?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/changefeed"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/changefeed.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/changefeed.md"
description: "Важно. Поддерживается только для строковых таблиц. Поддержка функциональности для колоночных таблиц находится в разработке."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Добавление или удаление потока изменений

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

`ADD CHANGEFEED <name> WITH (option = value[, ...])` — добавляет [поток изменений (changefeed)](../../../../concepts/cdc.md) с указанным именем и параметрами.

## Параметры потока изменений {#changefeed-options}

- `MODE` — режим работы. Указывает, что именно будет записано в поток при каждом изменении данных в таблице:

  - `KEYS_ONLY` — будут записаны только компоненты первичного ключа и признак изменения.
  - `UPDATES` — будут записаны значения изменившихся столбцов, получившиеся в результате изменения.
  - `NEW_IMAGE` — будут записаны значения всех столбцов, получившиеся в результате изменения.
  - `OLD_IMAGE` — будут записаны значения всех столбцов, предшествующие изменению.
  - `NEW_AND_OLD_IMAGES` - комбинация режимов `NEW_IMAGE` и `OLD_IMAGE`. Будут записаны значения всех столбцов *до* и *в результате* изменения.

- `FORMAT` — формат данных, в котором будут записаны данные:

  - `JSON` — записывать данные в формате [JSON](../../../../concepts/cdc.md#json-record-structure).
  - `DEBEZIUM_JSON` — записывать данные в [JSON-формате, аналогичном Debezium формату](../../../../concepts/cdc.md#debezium-json-record-structure).

- `VIRTUAL_TIMESTAMPS` — включение-выключение [виртуальных меток времени](../../../../concepts/cdc.md#virtual-timestamps).

- `BARRIERS_INTERVAL` — периодичность выгрузки [барьеров](../../../../concepts/cdc.md#barriers). Тип значения — `Interval`. По умолчанию выключено.

- `RETENTION_PERIOD` — [время хранения записей](../../../../concepts/cdc.md#retention-period). Тип значения — `Interval`, значение по умолчанию — 24 часа (`Interval('PT24H')`).

- `TOPIC_AUTO_PARTITIONING` — [режим автопартиционирования топика](../../../../concepts/cdc.md#topic-partitions):

  - `ENABLED` — для потока изменений будет создан [автопартиционированный топик](../../../../concepts/datamodel/topic.md#autopartitioning). Количество партиций в таком топике увеличивается автоматически по мере роста скорости обновления таблицы. Параметры автопартиционирования топика можно [настроить](../alter-topic.md#alter-topic).
  - `DISABLED` — для потока изменений будет создан топик без [автопартиционирования](../../../../concepts/datamodel/topic.md#autopartitioning). Это значение по умолчанию.

- `TOPIC_MIN_ACTIVE_PARTITIONS` — [количество партиций топика](../../../../concepts/cdc.md#topic-partitions). По умолчанию количество партиций топика равно количеству партиций таблицы. Для автопартиционированных топиков количество партиций увеличивается по мере роста скорости обновления таблицы. Если при создании ченджфида опция `TOPIC_AUTO_PARTITIONING` была отключена (`DISABLED`), то число партиций в топике, связанном с таким ченджфидом, впоследствии изменить нельзя.

- `INITIAL_SCAN` — включение-выключение [первоначального сканирования](../../../../concepts/cdc.md#initial-scan) таблицы. По умолчанию выключено.

Приведенный ниже код добавит поток изменений с именем `updates_feed`, в который будут выгружаться значения изменившихся столбцов таблицы в формате JSON:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES'
);
```

Записи в таком потоке изменений будут храниться в течение 24 часов (значение по умолчанию). Код из следующего примера создаст поток изменений с хранением записей в течение 12 часов:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    RETENTION_PERIOD = Interval('PT12H')
);
```

Пример создания потока изменений с включенными виртуальными метками времени:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    VIRTUAL_TIMESTAMPS = TRUE
);
```

Пример создания потока изменений с виртуальными метками времени и барьерами раз в 10 секунд:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    VIRTUAL_TIMESTAMPS = TRUE,
    BARRIERS_INTERVAL = Interval('PT10S')
);
```

Пример создания потока изменений с первоначальным сканированием:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    INITIAL_SCAN = TRUE
);
```

Пример создания потока изменений с автопартиционированием:

```yql
ALTER TABLE `series` ADD CHANGEFEED `updates_feed` WITH (
    FORMAT = 'JSON',
    MODE = 'UPDATES',
    TOPIC_AUTO_PARTITIONING = 'ENABLED',
    TOPIC_MIN_ACTIVE_PARTITIONS = 2
);
```

`DROP CHANGEFEED` — удаляет поток изменений с указанным именем. Приведенный ниже код удалит changefeed с именем `updates_feed`:

```yql
ALTER TABLE `series` DROP CHANGEFEED `updates_feed`;
```
