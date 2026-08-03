---
title: "Федеративные запросы"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/index.md"
description: "Федеративные запросы - это способ получать информацию из различных источников данных без необходимости переноса данных этих источников внутрь YDB. В настоящее в"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Федеративные запросы

Федеративные запросы - это способ получать информацию из различных источников данных без необходимости переноса данных этих источников внутрь YDB. В настоящее время федеративные запросы поддерживают взаимодействие с базами данных ClickHouse, PostgreSQL и с S3-совместимыми объектными хранилищами. При помощи YQL запросов вы сможете обращаться к этим базам данных без необходимости дублирования данных между системами.

Для работы с данными, хранящимися во внешних СУБД, достаточно создать [внешний источник данных](../../datamodel/external_data_source.md). Для работы с несхематизированными данными, хранящимися в бакетах S3, нужно дополнительно создать [внешнюю таблицу](../../datamodel/external_table.md). В обоих случаях необходимо предварительно создать [секреты](../../datamodel/secrets.md), хранящие конфиденциальные данные, необходимые для аутентификации во внешних системах.

Вы сможете узнать о внутреннем устройстве системы обработки федеративных запросов в разделе об [архитектуре](architecture.md). Подробная информация про работу с различными источниками данных приведена в соответствующих разделах:

- [ClickHouse](clickhouse.md)
- [Greenplum](greenplum.md)
- [Microsoft SQL Server](ms_sql_server.md#query)
- [MySQL](mysql.md)
- [PostgreSQL](postgresql.md)
- [S3](s3/external_table.md)
- [YDB](ydb.md)
