---
title: "DELETE FROM"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/delete?version=v26.1"
doc_path: "ru/yql/reference/syntax/delete"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/delete.md"
description: "Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DELETE FROM

> [!WARNING]
> В настоящее время одновременное использование [колоночных](../../../concepts/glossary.md#column-oriented-table) и [строковых](../../../concepts/glossary.md#row-oriented-table) таблиц поддерживается в транзакциях, в которых данные только читаются, но не изменяются. Поддержка транзакций с возможностью модификации данных при одновременном использовании строковых и колоночных таблиц находится в разработке.
>
> Если попытаться выполнить операцию записи в транзакции, в которой задействованы и колоночные, и строковые таблицы, транзакция завершится с ошибкой: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Удаляет строки из таблицы, подходящие под условия, заданные в `WHERE`.

## Пример {#primer}

```yql
DELETE FROM my_table
WHERE Key1 == 1 AND Key2 >= "One";
```

## DELETE FROM ... ON {#delete-on}

Используется для удаления данных на основе результатов подзапроса. Набор колонок, возвращаемых подзапросом, должен быть подмножеством колонок обновляемой таблицы, и в составе возвращаемых колонок обязательно должны присутствовать все колонки первичного ключа таблицы. Типы данных возвращаемых подзапросом колонок должны совпадать с типами данных соответствующих колонок таблицы.

Для поиска удаляемых из таблицы записей используется значение первичного ключа. Присутствие других (неключевых) колонок таблицы в составе выходных колонок подзапроса не влияет на результаты операции удаления.

### Пример {#primer1}

```yql
$to_delete = (
    SELECT Key, SubKey FROM my_table WHERE Value = "ToDelete" LIMIT 100
);

DELETE FROM my_table ON
SELECT * FROM $to_delete;
```

## DELETE FROM ... RETURNING {#delete-from-returning-{delete-from-returning}}

Используется для удаления строк и одновременного возврата значений из них. Это позволяет получить информацию об удаляемых записях за один запрос, избавляя от необходимости выполнять предварительный SELECT.

### Примеры {#primery}

- Возврат всех значений удаленных строк

```yql
DELETE FROM orders
WHERE status = 'cancelled'
RETURNING *;
```

- Возврат конкретных столбцов

```yql
DELETE FROM orders
WHERE status = 'cancelled'
RETURNING order_id, order_date;
```

## См. также {#sm-takzhe}

- [BATCH DELETE](batch-delete.md)
