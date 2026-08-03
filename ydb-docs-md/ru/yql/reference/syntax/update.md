---
title: "UPDATE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/update?version=v26.1"
doc_path: "ru/yql/reference/syntax/update"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/update.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/update.md"
description: "Важно."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# UPDATE

> [!WARNING]
> В настоящее время одновременное использование [колоночных](../../../concepts/glossary.md#column-oriented-table) и [строковых](../../../concepts/glossary.md#row-oriented-table) таблиц поддерживается в транзакциях, в которых данные только читаются, но не изменяются. Поддержка транзакций с возможностью модификации данных при одновременном использовании строковых и колоночных таблиц находится в разработке.
>
> Если попытаться выполнить операцию записи в транзакции, в которой задействованы и колоночные, и строковые таблицы, транзакция завершится с ошибкой: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

Изменяет данные в таблице. После ключевого слова `SET` через запятую указываются столбцы, значение которых необходимо заменить, и сами новые значения. Список обновляемых строк задается с помощью условия `WHERE`. Если условие `WHERE` отсутствует, изменения будут применены ко всем строкам таблицы.

`UPDATE` не может менять значение колонок, входящих в состав первичного ключа.

## Пример {#primer}

```yql
UPDATE my_table
SET Value1 = YQL::ToString(Value2 + 1), Value2 = Value2 - 1
WHERE Key1 > 1;
```

## UPDATE ON

Используется для обновления данных на основе результатов подзапроса. Набор колонок, возвращаемых подзапросом, должен быть подмножеством колонок обновляемой таблицы. В составе возвращаемых подзапросом колонок обязательно должны присутствовать все колонки первичного ключа таблицы. Типы данных возвращаемых подзапросом колонок должны совпадать с типами данных соответствующих колонок таблицы.

Для поиска обновляемых записей используется значение первичного ключа. В каждой найденной записи при выполнении оператора изменяются значения неключевых колонок, указанных в подзапросе. Значения колонок таблицы, которые отсутствуют в возвращаемых колонках подзапроса, остаются неизменными.

### Пример {#primer1}

```yql
$to_update = (
    SELECT Key, SubKey, "Updated" AS Value FROM my_table
    WHERE Key = 1
);

UPDATE my_table ON
SELECT * FROM $to_update;
```

## UPDATE ... RETURNING {#update-returning-{update-returning}}

Используется для обновления строк и одновременного возврата их новых значений. Это позволяет получить информацию об обновленных записях за один запрос, избавляя от необходимости выполнять дополнительный SELECT.

### Примеры {#primery}

- Возврат всех значений обновленных строк

```yql
UPDATE orders
SET status = 'shipped'
WHERE order_date < '2023-01-01'
RETURNING *;
```

- Возврат конкретных столбцов

```yql
UPDATE products
SET price = price * 0.9
WHERE category = 'Electronics'
RETURNING product_id, name, price AS new_price;
```

## См. также {#sm-takzhe}

- [BATCH UPDATE](batch-update.md)
