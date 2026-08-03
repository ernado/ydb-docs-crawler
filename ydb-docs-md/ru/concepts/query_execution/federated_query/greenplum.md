---
title: "Работа с базами данных Greenplum"
url: "https://ydb.tech/docs/ru/concepts/query_execution/federated_query/greenplum?version=v26.1"
doc_path: "ru/concepts/query_execution/federated_query/greenplum"
version: "v26.1"
lang: "ru"
source_path: "ru/core/concepts/query_execution/federated_query/greenplum.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/concepts/query_execution/federated_query/greenplum.md"
description: "В этом разделе описана основная информация про работу с внешней базой данных Greenplum. Поскольку Greenplum основан на PostgreSQL, интеграции с ними работают по"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Работа с базами данных Greenplum

В этом разделе описана основная информация про работу с внешней базой данных [Greenplum](https://greenplum.org). Поскольку Greenplum основан на [PostgreSQL](postgresql.md), интеграции с ними работают похожим образом, а некоторые ссылки ниже могут вести на документацию PostgreSQL.

Для работы с внешней базой данных Greenplum необходимо выполнить следующие шаги:

1. Создать [секрет](../../datamodel/secrets.md), содержащий пароль для подключения к базе данных.

   ```yql
   CREATE SECRET greenplum_datasource_user_password WITH (value = "<password>");
   ```

2. Создать [внешний источник данных](../../datamodel/external_data_source.md), описывающий определённую базу данных в составе кластера Greenplum. В параметр `LOCATION` нужно передать сетевой адрес [мастер-ноды](https://greenplum.org/introduction-to-greenplum-architecture/) Greenplum. При чтении по умолчанию используется [пространство имен](https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/ref_guide-system_catalogs-pg_namespace.html) `public`, но это значение можно изменить с помощью опционального параметра `SCHEMA`. Включить шифрование соединений к внешней базе данных можно с помощью параметра `USE_TLS="TRUE"`.

   ```yql
   CREATE EXTERNAL DATA SOURCE greenplum_datasource WITH (
       SOURCE_TYPE="Greenplum",
       LOCATION="<host>:<port>",
       DATABASE_NAME="<database>",
       AUTH_METHOD="BASIC",
       LOGIN="user",
       PASSWORD_SECRET_PATH="greenplum_datasource_user_password",
       USE_TLS="TRUE",
       SCHEMA="<schema>"
   );
   ```

3. Развернуть [коннектор](architecture.md#connectors) и [настроить](../../../devops/deployment-options/manual/federated-queries/index.md) динамические узлы YDB на взаимодействие с ним. Также необходимо обеспечить сетевой доступ с динамических узлов YDB к внешнему источнику данных (по адресу, указанному в параметре `LOCATION` запроса `CREATE EXTERNAL DATA SOURCE`). В случае, если на предыдущем шаге было включено шифрование сетевых соединений к внешнему источнику, коннектор будет использовать системные корневые сертификаты (более подробно о настройке TLS можно узнать в [инструкции](../../../devops/deployment-options/manual/federated-queries/connector-deployment.md) по разворачиванию коннектора).

4. [Выполнить запрос](greenplum.md#query) к базе данных.

## Синтаксис запросов {#query}

Для работы с Greenplum используется следующая форма SQL-запроса:

```yql
SELECT * FROM greenplum_datasource.<table_name>
```

где:

- `greenplum_datasource` - идентификатор внешнего источника данных;
- `<table_name>` - имя таблицы внутри внешнего источника данных.

## Ограничения {#limitations}

При работе с кластерами Greenplum существует ряд ограничений:

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

## Поддерживаемые типы данных {#podderzhivaemye-tipy-dannyh}

В базе данных Greenplum признак опциональности значений колонки (разрешено или запрещено колонке содержать значения `NULL`) не является частью системы типов данных. Ограничение (constraint) `NOT NULL` для каждой колонки реализуется в виде атрибута `attnotnull` в системном каталоге [pg_attribute](https://docs.vmware.com/en/VMware-Greenplum/6/greenplum-database/ref_guide-system_catalogs-pg_attribute.html), то есть на уровне метаданных таблицы. Следовательно, все базовые типы Greenplum по умолчанию могут содержать значения `NULL`, и в системе типов YDB они должны отображаться в [опциональные](../../../yql/reference/types/optional.md) типы.

Ниже приведена таблица соответствия типов Greenplum и YDB. Все остальные типы данных, за исключением перечисленных, не поддерживаются.

| Тип данных Greenplum | Тип данных YDB | Примечания |
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
| `json` | `Optional<Json>` |  |
| `date` | `Optional<Date>` | Допустимый диапазон дат с 1970-01-01 и до 2105-12-31. При выходе значения за границы диапазона возвращается `NULL`. |
| `timestamp` | `Optional<Timestamp>` | Допустимый диапазон времени с 1970-01-01 00:00:00 и до 2105-12-31 23:59:59. При выходе значения за границы диапазона возвращается значение `NULL`. |
| `bytea` | `Optional<String>` |  |
| `character` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию, строка дополняется пробелами до требуемой длины. |
| `character varying` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию. |
| `text` | `Optional<Utf8>` | [Правила сортировки](https://www.postgresql.org/docs/current/collation.html) по умолчанию. |
