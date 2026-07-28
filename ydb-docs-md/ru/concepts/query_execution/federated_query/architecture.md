---
title: "Архитектура системы обработки федеративных запросов"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/architecture?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/architecture"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/architecture.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/architecture.md"
description: "Внешние источники данных и внешние таблицы."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Архитектура системы обработки федеративных запросов

## Внешние источники данных и внешние таблицы {#vneshnie-istochniki-dannyh-i-vneshnie-tablicy}

Ключевым элементом системы обработки федеративных запросов YDB является понятие [внешнего источника данных](../../datamodel/external_data_source.md) (external data source). В качестве таких источников могут выступать реляционные СУБД, объектные хранилища и другие системы хранения данных. При обработке федеративного запроса YDB потоково вычитывает данные из внешних систем и позволяет выполнять над ними точно такой же спектр операций, что и для локальных данных.

Для того, чтобы работать с данными, размещёнными во внешних системах, YDB должна располагать информацией о внутренней структуре этих данных (например, о количестве, названиях и типах столбцов в таблицах). Некоторые источники предоставляют подобную метаинформацию о данных вместе с самими данными, тогда как для работы с другими, несхематизированными источниками требуется задание этой метаинформации извне. Последней цели служат [внешние таблицы](../../datamodel/external_table.md) (external tables).

Зарегистрировав в YDB внешние источники данных и (в случае необходимости) внешние таблицы, клиент может приступать к описанию федеративных запросов.

## Коннекторы {#connectors}

В ходе выполнения федеративных запросов YDB необходимо обращаться по сети к сторонним системам хранения данных, для чего приходится использовать их клиентские библиотеки. Появление таких зависимостей негативно сказывается на объёме кодовой базы, времени компиляции и размере бинарных файлов YDB, а также на стабильности всего продукта в целом.

Перечень поддерживаемых источников данных для федеративных запросов постоянно расширяется.  
 Наиболее популярные источники, такие как S3, поддерживаются YDB нативно. Однако не всем пользователям требуется поддержка одновременно всех источников. Её можно включить опционально с помощью *коннекторов* - специальных микросервисов, реализующих унифицированный интерфейс доступа к внешним источникам данных.

В функции коннекторов входят:

- Трансляция YQL-запросов в запросы на языке, специфичном для внешнего источника (например, в запросы на другом диалекте SQL или в обращения к HTTP API).
- Организация сетевых соединений с источниками данных.
- Конвертация данных, извлечённых из внешних источников, в колоночное представление в формате [Arrow IPC Stream](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc), поддерживаемом YDB.

![Архитектура YDB Federated Query](https://raw.githubusercontent.com/ydb-platform/ydb/main/ydb/docs/ru/core/concepts/query_execution/federated_query/_assets/architecture.png "Архитектура YDB Federated Query")

Таким образом, благодаря коннекторам формируется слой абстракции, скрывающий от YDB специфику внешних источников данных. Лаконичность интерфейса коннектора позволяет легко расширять перечень поддерживаемых источников, внося минимальные изменения в код YDB.

Пользователи могут развернуть [один из готовых коннекторов](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) или написать свою реализацию на любом языке программирования по [gRPC спецификации](https://github.com/ydb-platform/ydb/tree/main/ydb/library/yql/providers/generic/connector/api).

## Перечень поддерживаемых внешних источников данных {#supported-datasources}

| Источник | Поддержка |
| --- | --- |
| [ClickHouse](https://clickhouse.com/) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [Greenplum](https://greenplum.org/) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [Microsoft SQL Server](https://learn.microsoft.com/ru-ru/sql/?view=sql-server-ver16) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [MySQL](https://www.mysql.org/) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [PostgreSQL](https://www.postgresql.org/) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
| [S3](https://aws.amazon.com/ru/s3/) | Встроенная в `ydbd` |
| [YDB](https://ydb.tech/) | Через коннектор [fq-connector-go](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md#fq-connector-go) |
