---
title: "Создание и заполнение таблицы на основе результатов запроса"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/as_select?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/as_select"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/as_select.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/as_select.md"
description: "Важно. Поддерживается только для колоночных таблиц. Поддержка функциональности для строковых таблиц находится в разработке."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# Создание и заполнение таблицы на основе результатов запроса

> [!WARNING]
> Поддерживается только для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц. Поддержка функциональности для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц находится в разработке.

Вызов `CREATE TABLE AS` создает новую [таблицу](../../../../concepts/datamodel/table.md), которая заполнена данными из результатов запроса.

```yql
CREATE TABLE table_name (
    PRIMARY KEY ( column, ... )
)
WITH ( key = value, ... )
AS SELECT ...
```

Имена и типы колонок будут соответствовать результатам `SELECT`.  
 Для колонок [неопционального типа](../../types/optional.md) также будет выставлен модификатор `NOT NULL`.

При создании таблицы через `CREATE TABLE AS` не поддерживается указание имен колонок, [вторичных индексов](secondary_index.md), [векторных индексов](vector_index.md), [групп колонок](family.md). Имена и типы данных для столбцов новой таблицы автоматически наследуются из результирующего набора запроса SELECT. Все вышеперечисленное можно изменять при помощи [`ALTER TABLE`](../alter_table/index.md) после создания таблицы. При этом поддерживаются [дополнительные параметры](with.md).

## Особенности {#osobennosti}

> [!WARNING]
> Запись строк производится с полной перезаписью строки, как при использовании [`REPLACE INTO`](../replace_into.md), но при этом отсутствуют гарантии на порядок записи строк в таблицу.
>
> Если `SELECT` вернул 2 или более строки с одним и тем же значением первичного ключа, то после завершения выполнения `CREATE TABLE AS` в созданной таблице будет только одна запись с таким значением первичного ключа. При этом какая именно из записей найденных в `SELECT` будет добавлена - в общем случае не определено.

- `CREATE TABLE AS` поддерживается только в режиме [неявного контроля транзакций](../../../../concepts/transactions.md#implicit). Таблица появится по указанному пути уже заполненной.
- `CREATE TABLE AS` может быть только единственным [DML](https://en.wikipedia.org/wiki/Data_manipulation_language)/[DDL](https://en.wikipedia.org/wiki/Data_definition_language) выражением в запросе. Допустимо использование [PRAGMA](../pragma.md), [DECLARE](../declare.md) и [именованных выражений](../expressions.md#named-nodes).
- `CREATE TABLE AS` не конфликтует с другими транзакциями. При выполнении запроса не используются блокировки, а все чтения производятся из консистентного снапшота. Балансировка или разделение [таблеток](../../../../concepts/glossary.md#tablet) не приводят к ошибкам.
- `CREATE TABLE AS` позволяет использовать в одном запросе и [колоночные таблицы](../../../../concepts/glossary.md#column-oriented-table), и [строковые таблицы](../../../../concepts/glossary.md#row-oriented-table).
- `CREATE TABLE AS` создаёт таблицу во временной директории `.tmp/sessions`, а после успешной записи данных перемещает её в указанное место. Если операция прервётся из-за ошибки, временная таблица не удаляется мгновенно, а остаётся в системе ещё на некоторое время.

## Примеры {#primery}

- Создание колоночной таблицы из результатов запроса

```yql
CREATE TABLE my_table (
    PRIMARY KEY (key1, key2)
) WITH (
    STORE=COLUMN
) AS SELECT 
    key AS key1,
    Unwrap(other_key) AS key2,
    value,
    String::Contains(value, "test") AS has_test
FROM other_table;
```
