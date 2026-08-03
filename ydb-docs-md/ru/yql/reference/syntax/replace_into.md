---
title: "REPLACE INTO"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/replace_into?version=v26.1"
doc_path: "ru/yql/reference/syntax/replace_into"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/replace_into.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/replace_into.md"
description: "Важно."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# REPLACE INTO

> [!WARNING]
> В настоящее время одновременное использование [колоночных](../../../concepts/glossary.md#column-oriented-table) и [строковых](../../../concepts/glossary.md#row-oriented-table) таблиц поддерживается в транзакциях, в которых данные только читаются, но не изменяются. Поддержка транзакций с возможностью модификации данных при одновременном использовании строковых и колоночных таблиц находится в разработке.
>
> Если попытаться выполнить операцию записи в транзакции, в которой задействованы и колоночные, и строковые таблицы, транзакция завершится с ошибкой: `Write transactions that use both row-oriented and column-oriented tables are disabled at current time`.

В отличие от [`INSERT INTO`](insert_into.md) и [`UPDATE`](update.md), запросы [`UPSERT INTO`](upsert_into.md) и `REPLACE INTO` не требуют предварительного чтения данных, поэтому выполняются быстрее. `REPLACE INTO` сохраняет данные в таблицу с перезаписью строк по первичному ключу. Если заданный первичный ключ отсутствует, в таблицу будет добавлена новая строка. Если задан существующий первичный ключ, строка будет перезаписана. При этом значения столбцов, не определенных в операции `REPLACE INTO`, заменяются на значения по умолчанию.

## Примеры {#primery}

- Задание значений для `REPLACE INTO` c помощью `VALUES`:

```yql
  REPLACE INTO my_table (Key1, Key2, Value2) VALUES
      (1u, "One", 101),
      (2u, "Two", 102);
  COMMIT;
```

- Получение значений для `REPLACE INTO` с помощью выборки `SELECT`:

```yql
  REPLACE INTO my_table
  SELECT Key AS Key1, "Empty" AS Key2, Value AS Value1
  FROM my_table1;
  COMMIT;
```
