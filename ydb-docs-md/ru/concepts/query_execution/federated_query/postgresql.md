---
title: "Работа с базами данных PostgreSQL"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/postgresql?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/postgresql"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/postgresql.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/postgresql.md"
description: "В этом разделе описана основная информация про работу с внешней базой данных PostgreSQL."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Работа с базами данных PostgreSQL

В этом разделе описана основная информация про работу с внешней базой данных [PostgreSQL](http://postgresql.org).

Для работы с внешней базой данных PostgreSQL необходимо выполнить следующие шаги:

1. Создать [секрет](../../datamodel/secrets.md), содержащий пароль для подключения к базе данных.

   ```yql
   CREATE SECRET postgresql_datasource_user_password WITH (value = "<password>");
   ```

2. Создать [внешний источник данных](../../datamodel/external_data_source.md), описывающий определённую базу данных в составе кластера PostgreSQL. При чтении по умолчанию используется [пространство имен](https://www.postgresql.org/docs/current/catalog-pg-namespace.html) `public`, но это значение можно изменить с помощью опционального параметра `SCHEMA`. Сетевое подключение выполняется по стандартному ([Frontend/Backend Protocol](https://www.postgresql.org/docs/current/protocol.html)) по транспорту TCP (`PROTOCOL="NATIVE"`). Включить шифрование соединений к внешней базе данных можно с помощью параметра `USE_TLS="TRUE"`.

   ```yql
   CREATE EXTERNAL DATA SOURCE postgresql_datasource WITH (
       SOURCE_TYPE="PostgreSQL",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="postgresql_datasource_user_password",
       PROTOCOL="NATIVE",
       USE_TLS="TRUE",
       SCHEMA="<schema>"
   );
   ```

3. Развернуть [коннектор](architecture.md#connectors) и [настроить](../../../devops/deployment-options/manual/federated-queries/index.md) динамические узлы YDB на взаимодействие с ним. Также необходимо обеспечить сетевой доступ с динамических узлов YDB к внешнему источнику данных (по адресу, указанному в параметре `LOCATION` запроса `CREATE EXTERNAL DATA SOURCE`). В случае, если на предыдущем шаге было включено шифрование сетевых соединений к внешнему источнику, коннектор будет использовать системные корневые сертификаты (более подробно о настройке TLS можно узнать в [инструкции](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) по разворачиванию коннектора).

4. [Выполнить запрос](postgresql.md#query) к базе данных.

## Синтаксис запросов {#query}

Для работы с PostgreSQL используется следующая форма SQL-запроса:

```yql
SELECT * FROM postgresql_datasource.<table_name>
```

где:

- `postgresql_datasource` - идентификатор внешнего источника данных;
- `<table_name>` - имя таблицы внутри внешнего источника данных.

## Ограничения {#limitations}

При работе с кластерами PostgreSQL существует ряд ограничений:

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
   | `Int16` |
   | `Int32` |
   | `Int64` |
   | `Float` |
   | `Double` |
   | `Decimal` |

## Поддерживаемые типы данных {#podderzhivaemye-tipy-dannyh}

В базе данных PostgreSQL признак опциональности значений колонки (разрешено или запрещено колонке содержать значения `NULL`) не является частью системы типов данных. Ограничение (constraint) `NOT NULL` для каждой колонки реализуется в виде атрибута `attnotnull` в системном каталоге [pg_attribute](https://www.postgresql.org/docs/current/catalog-pg-attribute.html), то есть на уровне метаданных таблицы. Следовательно, все базовые типы PostgreSQL по умолчанию могут содержать значения `NULL`, и в системе типов YDB они должны отображаться в [опциональные](../../../yql/reference/types/optional.md) типы.

Ниже приведена таблица соответствия типов PostgreSQL и YDB. Все остальные типы данных, за исключением перечисленных, не поддерживаются.

| Тип данных PostgreSQL | Тип данных YDB | Примечания |
| --- | --- | --- |
| `boolean` | `Optional<Bool>` |  |
| `smallint` | `Optional<Int16>` |  |
| `int2` | `Optional<Int16>` |  |
| `integer` | `Optional<Int32>` |  |
| `int` | `Optional<Int32>` |  |
| `int4` | `Optional<Int32>` |  |
| `serial` | `Optional<Int32>` |  |
| `serial4` | `Optional<Int32>` |  |
| `bigint` | `Optional<Int64>` |  |
| `int8` | `Optional<Int64>` |  |
| `bigserial` | `Optional<Int64>` |  |
| `serial8` | `Optional<Int64>` |  |
| `real` | `Optional<Float>` |  |
| `float4` | `Optional<Float>` |  |
| `double precision` | `Optional<Double>` |  |
| `float8` | `Optional<Double>` |  |
| `date` | `Optional<Date>` | Допустимый диапазон дат с 1970-01-01 и до 2105-12-31. При выходе значения за границы диапазона возвращается `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `bytea` | `Optional<String>` |  |
| `character` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию, строка дополняется пробелами до требуемой длины. |
| `character varying` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию. |
| `text` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию. |
| `json` | `Optional<Json>` |  |
| `numeric(p,s)` | `Optional<Decimal(p,s)>` | `p` (precision) - общее количество знаков в числе, `s` (scale) - количество знаков после запятой. Типы `numeric` без указания параметров (так называемые «неограниченные», unconstrained) преобразуются в `Optional<Decimal(35, 0)>`. Типы `numeric`, у которых `p > 35` или `s < 0`, не поддерживаются. |
