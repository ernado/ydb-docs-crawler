---
title: "Импорт и экспорт данных с использованием федеративных запросов"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/import_and_export?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/import_and_export"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/import_and_export.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/import_and_export.md"
description: "Примечание. При импорте/экспорте данных из/в S3 в формате Parquet необходимо учитывать маппинг типов YQL и Apache Arrow. Импорт данных."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Импорт и экспорт данных с использованием федеративных запросов

> [!NOTE]
> При импорте/экспорте данных из/в S3 в формате Parquet необходимо учитывать [маппинг типов YQL и Apache Arrow](s3/arrow_types_mapping.md).

## Импорт данных {#import}

Федеративные запросы позволяют импортировать данные из подключенных внешних источников в таблицы базы данных YDB. Для импорта данных нужно использовать запрос чтения из [внешнего источника данных](../../datamodel/external_data_source.md) или [внешней таблицы](../../datamodel/external_table.md) и записи в YDB таблицу.

Для колоночных таблиц поддерживается массивно-параллельный импорт из внешнего источника при использовании конструкций UPSERT и INSERT — несколько рабочих потоков параллельно читают данные из внешнего источника и пишут в таблицу. Для строковых таблиц функциональность в разработке.

| Операция | Запись в [строковые таблицы](../../datamodel/table.md#row-oriented-tables) | Запись в [колоночные таблицы](../../datamodel/table.md#column-oriented-tables) |
| --- | --- | --- |
| [UPSERT](../../../yql/reference/syntax/upsert_into.md) | однопоточная | параллельная |
| [REPLACE](../../../yql/reference/syntax/replace_into.md) | однопоточная | параллельная |
| [INSERT](../../../yql/reference/syntax/insert_into.md) | однопоточная | параллельная |

> [!TIP]
> Рекомендованными вариантами импорта с использованием федеративных запросов являются операции `UPSERT` и `REPLACE` — для них значительно оптимизирован сценарий импорта данных.

Пример импорта данных из PostgreSQL таблицы в YDB таблицу:

```yql
UPSERT INTO target_table
SELECT * FROM postgresql_datasource.source_table
```

Подробнее про создание внешних источников данных и внешних таблиц, а также про запросы чтения данных из них можно прочитать в статьях:

- [ClickHouse](clickhouse.md#query)
- [Greenplum](greenplum.md#query)
- [Microsoft SQL Server](ms_sql_server.md#query)
- [MySQL](mysql.md#query)
- [PostgreSQL](postgresql.md#query)
- [S3](s3/external_table.md)
- [YDB](ydb.md#query)

## Экспорт данных {#export}

На данный момент экспорт данных с использованием федеративных запросов поддержан только для S3-совместимых хранилищ, подробнее смотреть в статье [Экспорт данных в объектное хранилище S3](s3/write_data.md#export-to-s3).
