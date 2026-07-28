---
title: "Внешние источники данных"
url: "https://ydb.tech/docs/ru/concepts/datamodel/external_data_source?version=v26.1"
doc_path: "ru/concepts/datamodel/external_data_source"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/datamodel/external_data_source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/datamodel/external_data_source.md"
description: "Внешний источник (external data source) - это объект в YDB, описывающий параметры подключения к внешнему источнику данных. Например, в случае ClickHouse внешний"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Внешние источники данных

Внешний источник (external data source) - это объект в YDB, описывающий параметры подключения к внешнему источнику данных. Например, в случае ClickHouse внешний источник описывает сетевой адрес, логин и пароль для аутентификации в кластере ClickHouse, а в случае S3 (Object Storage) описывает реквизиты доступа и путь к бакету.

В следующем примере приведен пример создания внешнего источника, ведущего на кластер ClickHouse:

```yql
CREATE EXTERNAL DATA SOURCE test_data_source WITH (
  SOURCE_TYPE="ClickHouse",
  LOCATION="192.168.1.1:8123",
  DATABASE_NAME="default",
  AUTH_METHOD="BASIC",
  USE_TLS="TRUE",
  LOGIN="login",
  PASSWORD_SECRET_PATH="test_password_path",
  PROTOCOL="NATIVE"
);
```

После создания внешнего источника данных можно выполнять чтение данных из созданного объекта `EXTERNAL DATA SOURCE`. Пример ниже иллюстрирует чтение данных из таблицы `test_table` из базы данных `default` в кластере ClickHouse:

```yql
SELECT * FROM test_data_source.test_table;
```

С помощью внешних источников данных можно выполнять [федеративные запросы](../query_execution/federated_query/index.md) для задач межсистемной аналитики данных.

В качестве источников данных можно использовать:

- [ClickHouse](../query_execution/federated_query/clickhouse.md)
- [PostgreSQL](../query_execution/federated_query/postgresql.md)
- [Подключения к S3 (Object Storage)](../query_execution/federated_query/s3/external_data_source.md)
