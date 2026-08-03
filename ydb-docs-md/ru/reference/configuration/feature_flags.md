---
title: "feature_flags"
url: "https://ydb.tech/docs/ru/reference/configuration/feature_flags?version=v26.1"
doc_path: "ru/reference/configuration/feature_flags"
version: "v26.1"
lang: "ru"
source_path: "ru/core/reference/configuration/feature_flags.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/reference/configuration/feature_flags.md"
description: "Секция feature_flags включает или отключает определённые функции YDB с помощью булевых флагов. Для включения функции установите соответствующий функциональный ф"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# feature_flags

Секция `feature_flags` включает или отключает определённые функции YDB с помощью булевых флагов. Для включения функции установите соответствующий функциональный флаг в значение `true` в конфигурации кластера. Например, для включения поддержки автопартиционирования топиков в CDC, нужно добавить следующие строки в конфигурацию:

```yaml
feature_flags:
  enable_topic_autopartitioning_for_cdc: true
```

## Функциональные флаги {#funkcionalnye-flagi}

| Флаг | Функция |
| --- | --- |
| `enable_topic_autopartitioning_for_cdc` | [Автопартиционирование топиков](../../concepts/cdc.md#topic-partitions) в CDC для строковых таблиц |
| `enable_access_to_index_impl_tables` | Возможность [указания числа реплик](../../yql/reference/syntax/alter_table/indexes.md) для вторичного индекса |
| `enable_changefeeds_export`, `enable_changefeeds_import` | Поддержка потоков изменений (changefeed) в операциях резервного копирования и восстановления |
| `enable_view_export` | Поддержка представлений (`VIEW`) в операциях резервного копирования и восстановления |
| `enable_export_auto_dropping` | Автоудаление временных директорий и таблиц при экспорте в S3 |
| `enable_followers_stats` | Системные представления с информацией об [истории перегруженных партиций](../../dev/system-views.md#top-overload-partitions) |
| `enable_strict_acl_check` | Запрет на выдачу прав несуществующим пользователям и на удаление пользователей, которым выданы права |
| `enable_strict_user_management` | Строгие правила администрирования локальных пользователей (т.е. администрировать локальных пользователей может только администратор кластера или базы данных) |
| `enable_database_admin` | Добавление роли администратора базы данных |
| `enable_kafka_native_balancing` | Клиентская балансировка партиций при чтении по [протоколу Kafka](https://kafka.apache.org/documentation/#consumerconfigs_partition.assignment.strategy) |
| `enable_topic_compactification_by_key` | Включение компактификации топиков в [YDB Topics Kafka API](../kafka-api/index.md) |
| `enable_kafka_transactions` | Включение транзакций в [YDB Topics Kafka API](../kafka-api/index.md) |
| `enable_external_data_sources` | Включение [внешних источников данных](../../concepts/datamodel/external_data_source.md) |
