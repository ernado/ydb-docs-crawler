---
title: "CREATE TOPIC"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create-topic?version=v26.1"
doc_path: "ru/yql/reference/syntax/create-topic"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create-topic.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create-topic.md"
description: "С помощью оператора CREATE TOPIC можно создать топик, а также читателей для него. Общий вид команды:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# CREATE TOPIC

С помощью оператора `CREATE TOPIC` можно создать [топик](../../../concepts/datamodel/topic.md), а также [читателей](../../../concepts/datamodel/topic.md#consumer) для него.

Общий вид команды:

```yql
CREATE TOPIC topic_path (
    CONSUMER consumer_name [WITH (consumer_option = value[, ...])]
    ) WITH (topic_option = value[, ...]);
```

- `consumer_option` — параметр читателя;
- `topic_option` — параметр топика.

Все параметры команды, кроме `topic_path` не обязательны. По умолчанию топик создается без читателей. Все  
 не указанные явно параметры также выставляются по умолчанию (и для топика, и для читателя).

Параметры читателя:

- `important` — определяет важного читателя. Никакие данные из топика не будут удалены, пока все важные читатели их не обработали. Тип значения — `boolean`, значение по умолчанию: `false`.
- `availability_period` — определяет время доступности сообщений для читателя. Опция позволяет продлить время хранения сообщений в топике с [retention_period](create-topic.md#topic-parameters) вплоть до `availability_period`, если читатель не подтверждает их обработку. Тип значения — `Interval`. Не совместим с параметром `important`. Значение по умолчанию отсутствует.
- `read_from` — определяет момент времени записи сообщений, начиная с которого читатель будет получать данные. Данные, записанные ранее этого момента, прочитаны не будут. Тип значения: `Datetime` ИЛИ `Timestamp` или `integer` (unix-timestamp в виде числа). Значение по умолчанию — `0` (чтение с самого раннего доступного в топике времени).

## Параметры топика {#topic-parameters}

- `metering_mode` — способ метеринга ресурсов (`RESERVED_CAPACITY` - по выделенным ресурсам или `REQUEST_UNITS` - по фактическому использованию). Актуально для топиков в serverless базах данных. Тип значения - `String`.

- `min_active_partitions` — минимальное количество активных партиций топика. [Автопартиционирование](../../../concepts/datamodel/topic.md#autopartitioning) не будет уменьшать количество активных партиций ниже этого количества. Тип значения — `integer`, значение по умолчанию — `1`.

- `max_active_partitions` — максимальное количество активных партиций топика. [Автопартиционирование](../../../concepts/datamodel/topic.md#autopartitioning) не будет увеличивать количество активных партиций выше этого количества. Тип значения — `integer`, по умолчанию равно `min_active_partitions`.

- `retention_period` — время хранения данных в топике. Тип значения — `Interval`, значение по умолчанию — `18h`.

- `retention_storage_mb` — ограничение на максимальное место на диске, занимаемое данными топика. При превышении этого значения старые данные будут удаляться, как по retention. При включенном автоматическом партиционировании потребляемое место может превышать установленное значение. Тип значения — `integer`, значение по умолчанию — `0` (не ограничено).

- `partition_write_burst_bytes` — размер запаса квоты на запись в партицию на случай всплесков записи. При выставлении в `0` фактическое значение write_burst принимается равным значению квоты (что позволяет всплески записи длительностью до 1 секунды). Тип значения — `integer`, значение по умолчанию: `0`.

- `partition_write_speed_bytes_per_second` — максимальная разрешенная скорость записи в 1 партицию. Если поток записи в партицию превысит это значение, запись будет квотироваться. Тип значения — `integer`, значение по умолчанию — `2097152` (2 МБ).

- `auto_partitioning_strategy` — [режим автопартиционирования](../../../concepts/datamodel/topic.md#autopartitioning_modes).
   Допустимые значения: `disabled`, `paused`, `scale_up`, значение по умолчанию — `disabled`.

- `auto_partitioning_up_utilization_percent` — определяет порог загрузки партиции в процентах от максимальной скорости записи, при достижении которого будет инициировано автоматическое **увеличение** числа партиций. Тип значения — `integer`, значение по умолчанию — `80`.

- `auto_partitioning_stabilization_window` — определяет временной интервал, в течение которого уровень нагрузки должен оставаться выше установленного порога (`auto_partitioning_up_utilization_percent`), прежде чем будет выполнено автоматическое увеличение количества партиций. Тип значения — `Interval`, значение по умолчанию — `5m`.

> [!NOTE]
> При выборе имени для топика учитывайте общие [правила именования схемных объектов](../../../concepts/datamodel/cluster-namespace.md#object-naming-rules).

Следующая команда создаст топик без читателей с настройками по умолчанию:

```yql
CREATE TOPIC `my_topic`;
```

Чтобы создать топик с важным читателем и временем хранения данных 1 сутки, выполните команду:

```yql
CREATE TOPIC `my_topic` (
    CONSUMER my_consumer WITH (important = true)
) WITH (
    retention_period = Interval('P1D')
);
```

Чтобы создать топик с временем хранения данных 1 сутки и двумя читателями, для одного из которых данные могут по необходимости храниться до 2-х суток, выполните команду:

```yql
CREATE TOPIC `my_topic` (
    CONSUMER my_consumer1,
    CONSUMER my_consumer2 WITH (availability_period = Interval('P2D'))
) WITH (
    retention_period = Interval('P1D')
);
```
