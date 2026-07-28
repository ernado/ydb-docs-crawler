---
title: "Работа с базами данных Microsoft SQL Server"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/ms_sql_server?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/ms_sql_server"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/ms_sql_server.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/ms_sql_server.md"
description: "В этом разделе описана основная информация про работу с внешней базой данных Microsoft SQL Server."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Работа с базами данных Microsoft SQL Server

В этом разделе описана основная информация про работу с внешней базой данных [Microsoft SQL Server](https://learn.microsoft.com/ru-ru/sql/?view=sql-server-ver16).

Для работы с внешней базой данных Microsoft SQL Server необходимо выполнить следующие шаги:

1. Создать [секрет](../../datamodel/secrets.md), содержащий пароль для подключения к базе данных.

   ```yql
   CREATE SECRET ms_sql_server_datasource_user_password WITH (value = "<password>");
   ```

2. Создать [внешний источник данных](../../datamodel/external_data_source.md), описывающий определённую базу данных Microsoft SQL Server. Параметр `LOCATION` содержит сетевой адрес экземпляра Microsoft SQL Server, к которому осуществляется подключение. В `DATABASE_NAME` указывается имя базы данных (например, `master`). Для аутентификации во внешнюю базу используются значения параметров `LOGIN` и `PASSWORD_SECRET_PATH`. Включить шифрование соединений к внешней базе данных можно с помощью параметра `USE_TLS="TRUE"`.

   ```yql
   CREATE EXTERNAL DATA SOURCE ms_sql_server_datasource WITH (
       SOURCE_TYPE="MsSQLServer",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="ms_sql_server_datasource_user_password",
       USE_TLS="TRUE"
   );
   ```

3. Развернуть [коннектор](architecture.md#connectors) и [настроить](../../../devops/deployment-options/manual/federated-queries/index.md) динамические узлы YDB на взаимодействие с ним. Также необходимо обеспечить сетевой доступ с динамических узлов YDB к внешнему источнику данных (по адресу, указанному в параметре `LOCATION` запроса `CREATE EXTERNAL DATA SOURCE`). В случае, если на предыдущем шаге было включено шифрование сетевых соединений к внешнему источнику, коннектор будет использовать системные корневые сертификаты (более подробно о настройке TLS можно узнать в [инструкции](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) по разворачиванию коннектора).

4. [Выполнить запрос](ms_sql_server.md#query) к базе данных.

## Синтаксис запросов {#query}

Для работы с Microsoft SQL Server используется следующая форма SQL-запроса:

```yql
SELECT * FROM ms_sql_server_datasource.<table_name>
```

где:

- `ms_sql_server_datasource` - идентификатор внешнего источника данных;
- `<table_name>` - имя таблицы внутри внешнего источника данных.

## Ограничения {#limitations}

При работе с кластерами Microsoft SQL Server существует ряд ограничений:

1. Внешние источники доступны только для чтения данных через запросы `SELECT`. Запросы, модифицирующие таблицы во внешних источниках, движком обработки федеративных запросов в настоящее время не поддерживаются.

2. Если значение даты, хранящейся во внешнем источнике данных, находится вне допустимого для YDB диапазона (все используемые даты должны быть позднее 1970-01-01, но ранее 2105-12-31), в YDB такое значение будет преобразовано в `NULL`.

3. Система обработки федеративных запросов YDB умеет передавать исполнение некоторых частей запроса системе, выступающей в качестве источника данных. Фрагменты запроса передаются сквозь YDB непосредственно во внешнюю систему и обрабатываются внутри неё. С помощью этой оптимизации, которая носит название «пушдауна предикатов» (predicate pushdown), удаётся значительно снизить объём данных, передаваемых от источника к движку обработки федеративных запросов. Благодаря этому снижается нагрузка на сеть и экономятся вычислительные ресурсы YDB.

   Частный случай пушдауна предикатов, при котором выполняется передача фильтрующих выражений, указанных после ключевого слова `WHERE`, называется «пушдауном фильтров» (filter pushdown). Пушдаун фильтров возможен при использовании:

   | Описание | Пример |
   | --- | --- |
   | Проверка на `NULL` | `WHERE column1 IS NULL` или `WHERE column1 IS NOT NULL` |
   | Логических условий `OR`, `NOT`, `AND` и круглых скобок для управление приоритетом вычислений. | `WHERE column1 IS NULL OR (column2 IS NOT NULL AND column3 > 10)`. |
   | [Операторов сравнения](../../../yql/reference/syntax/expressions.md#comparison-operators) c другими колонками или константами. | `WHERE column1 > column2 OR column3 <= 10`, `WHERE column1 + column2 > 10`, `WHERE column1 = (10 + 10)` |

   При использовании других видов фильтров пушдаун на источник не выполняется: фильтрация строк внешней таблицы будет выполнена на стороне федеративной YDB, что означает, что YDB выполнит полное чтение (full scan) внешней таблицы в момент обработки запроса.

   | Тип данных YDB |
   | --- |
   | `Bool` |
   | `Int8` |
   | `Int16` |
   | `Int32` |
   | `Int64` |
   | `Float` |
   | `Double` |

## Поддерживаемые типы данных {#podderzhivaemye-tipy-dannyh}

В базе данных Microsoft SQL Server признак опциональности значений колонки (разрешено или запрещено колонке содержать значения `NULL`) не является частью системы типов данных. Ограничение (constraint) `NOT NULL` для любой колонки любой таблицы хранится в виде значения столбца `IS_NULLABLE` системной таблицы [INFORMATION_SCHEMA.COLUMNS](https://learn.microsoft.com/ru-ru/sql/relational-databases/system-information-schema-views/columns-transact-sql?view=sql-server-ver16), то есть на уровне метаданных таблицы. Следовательно, все базовые типы Microsoft SQL Server по умолчанию могут содержать значения `NULL`, и в системе типов YDB они должны отображаться в [опциональные](../../../yql/reference/types/optional.md) типы.

Ниже приведена таблица соответствия типов Microsoft SQL Server и YDB. Все остальные типы данных, за исключением перечисленных, не поддерживаются.

| Тип данных Microsoft SQL Server | Тип данных YDB | Примечания |
| --- | --- | --- |
| `bit` | `Optional<Bool>` |  |
| `tinyint` | `Optional<Int8>` |  |
| `smallint` | `Optional<Int16>` |  |
| `int` | `Optional<Int32>` |  |
| `bigint` | `Optional<Int64>` |  |
| `real` | `Optional<Float>` |  |
| `float` | `Optional<Double>` |  |
| `date` | `Optional<Date>` | Допустимый диапазон дат с 1970-01-01 и до 2105-12-31. При выходе значения за границы диапазона возвращается `NULL`. |
| `smalldatetime` | `Optional<Datetime>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `datetime` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `datetime2` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `binary` | `Optional<String>` |  |
| `varbinary` | `Optional<String>` |  |
| `image` | `Optional<String>` |  |
| `char` | `Optional<Utf8>` |  |
| `varchar` | `Optional<Utf8>` |  |
| `text` | `Optional<Utf8>` |  |
| `nchar` | `Optional<Utf8>` |  |
| `nvarchar` | `Optional<Utf8>` |  |
| `ntext` | `Optional<Utf8>` |  |
