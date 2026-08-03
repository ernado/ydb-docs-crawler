---
title: "Работа с базами данных MySQL"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/mysql?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/mysql"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/mysql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/mysql.md"
description: "В этом разделе описана основная информация про работу с внешней базой данных MySQL. Для работы с внешней базой данных MySQL необходимо выполнить следующие шаги:"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Работа с базами данных MySQL

В этом разделе описана основная информация про работу с внешней базой данных [MySQL](https://www.mysql.com/).

Для работы с внешней базой данных MySQL необходимо выполнить следующие шаги:

1. Создать [секрет](../../datamodel/secrets.md), содержащий пароль для подключения к базе данных.

   ```yql
   CREATE SECRET mysql_datasource_user_password WITH (value = "<password>");
   ```

2. Создать [внешний источник данных](../../datamodel/external_data_source.md), описывающий определённую базу данных MySQL. Параметр `LOCATION` содержит сетевой адрес экземпляра MySQL, к которому осуществляется подключение. В `DATABASE_NAME` указывается имя базы данных (например, `mysql`). Для аутентификации во внешнюю базу используются значения параметров `LOGIN` и `PASSWORD_SECRET_PATH`. Включить шифрование соединений к внешней базе данных можно с помощью параметра `USE_TLS="TRUE"`.

   ```yql
   CREATE EXTERNAL DATA SOURCE mysql_datasource WITH (
       SOURCE_TYPE="MySQL",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="mysql_datasource_user_password",
       USE_TLS="TRUE"
   );
   ```

3. Развернуть [коннектор](architecture.md#connectors) и [настроить](../../../devops/deployment-options/manual/federated-queries/index.md) динамические узлы YDB на взаимодействие с ним. Также необходимо обеспечить сетевой доступ с динамических узлов YDB к внешнему источнику данных (по адресу, указанному в параметре `LOCATION` запроса `CREATE EXTERNAL DATA SOURCE`). В случае, если на предыдущем шаге было включено шифрование сетевых соединений к внешнему источнику, коннектор будет использовать системные корневые сертификаты (более подробно о настройке TLS можно узнать в [инструкции](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) по разворачиванию коннектора).

4. [Выполнить запрос](mysql.md#query) к базе данных.

## Синтаксис запросов {#query}

Для работы с MySQL используется следующая форма SQL-запроса:

```yql
SELECT * FROM mysql_datasource.<table_name>
```

где:

- `mysql_datasource` - идентификатор внешнего источника данных;
- `<table_name>` - имя таблицы внутри внешнего источника данных.

## Ограничения {#limitations}

При работе с кластерами MySQL существует ряд ограничений:

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

   Поддерживаемые типы данных для пушдауна фильтров:

   | Тип данных YDB |
   | --- |
   | `Bool` |
   | `Int8` |
   | `Uint8` |
   | `Int16` |
   | `Uint16` |
   | `Int32` |
   | `Uint32` |
   | `Int64` |
   | `Uint64` |
   | `Float` |
   | `Double` |

## Поддерживаемые типы данных {#podderzhivaemye-tipy-dannyh}

В базе данных MySQL признак опциональности значений колонки (разрешено или запрещено колонке содержать значения `NULL`) не является частью системы типов данных. Ограничение (constraint) `NOT NULL` для любой колонки любой таблицы хранится в виде значения столбца `IS_NULLABLE` системной таблицы [INFORMATION_SCHEMA.COLUMNS](https://dev.mysql.com/doc/refman/8.4/en/information-schema-columns-table.html), то есть на уровне метаданных таблицы. Следовательно, все базовые типы MySQL по умолчанию могут содержать значения `NULL`, и в системе типов YDB они должны отображаться в [опциональные](../../../yql/reference/types/optional.md) типы.

Ниже приведена таблица соответствия типов MySQL и YDB. Все остальные типы данных, за исключением перечисленных, не поддерживаются.

| Тип данных MySQL | Тип данных YDB | Примечания |
| --- | --- | --- |
| `bool` | `Optional<Bool>` |  |
| `tinyint` | `Optional<Int8>` |  |
| `tinyint unsigned` | `Optional<Uint8>` |  |
| `smallint` | `Optional<Int16>` |  |
| `smallint unsigned` | `Optional<Uint16>` |  |
| `mediumint` | `Optional<Int32>` |  |
| `mediumint unsigned` | `Optional<Uint32>` |  |
| `int` | `Optional<Int32>` |  |
| `int unsigned` | `Optional<Uint32>` |  |
| `bigint` | `Optional<Int64>` |  |
| `bigint unsigned` | `Optional<Uint64>` |  |
| `float` | `Optional<Float>` |  |
| `real` | `Optional<Float>` |  |
| `double` | `Optional<Double>` |  |
| `date` | `Optional<Date>` | Допустимый диапазон дат с 1970-01-01 и до 2105-12-31. При выходе значения за границы диапазона возвращается `NULL`. |
| `datetime` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `tinyblob` | `Optional<String>` |  |
| `blob` | `Optional<String>` |  |
| `mediumblob` | `Optional<String>` |  |
| `longblob` | `Optional<String>` |  |
| `tinytext` | `Optional<String>` |  |
| `text` | `Optional<String>` |  |
| `mediumtext` | `Optional<String>` |  |
| `longtext` | `Optional<String>` |  |
| `char` | `Optional<Utf8>` |  |
| `varchar` | `Optional<Utf8>` |  |
| `binary` | `Optional<String>` |  |
| `varbinary` | `Optional<String>` |  |
| `json` | `Optional<Json>` |  |
