---
title: "BATCH DELETE FROM"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/batch-delete?version=v26.1"
doc_path: "ru/yql/reference/syntax/batch-delete"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/batch-delete.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/batch-delete.md"
description: "Совет. Перед тем как изучать BATCH DELETE FROM, рекомендуется ознакомиться со стандартным DELETE FROM."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# BATCH DELETE FROM

> [!TIP]
> Перед тем как изучать `BATCH DELETE FROM`, рекомендуется ознакомиться со стандартным [DELETE FROM](delete.md).

`BATCH DELETE FROM` позволяет удалять записи в таблицах большого размера, минимизируя риск отмены блокировок и отката транзакций за счёт ослабления гарантий. Удаление данных выполняется в виде серии транзакций для каждой [партиции](../../../concepts/datamodel/table.md#partitioning_row_table) указанной таблицы отдельно, обрабатывая по 10 000 строк за итерацию. Каждый запрос обрабатывает не более 10 партиций одновременно.

Данный запрос, как и стандартный `DELETE FROM`, выполняется синхронно и завершается с некоторым статусом. В случае возникновения ошибки или отключения клиента удаление данных останавливается, применённые изменения не откатываются.

Семантика наследуется от стандартного `DELETE FROM` с ограничениями:

- Поддерживается только для [строковых таблиц](../../../concepts/glossary.md#row-oriented-table).
- Поддерживается только в режиме [неявного контроля транзакций](../../../concepts/transactions.md#implicit).
- Запрещено использование подзапросов и нескольких выражений в одном запросе.
- Недоступно ключевое слово `RETURNING`.

## Пример {#primer}

```yql
BATCH DELETE FROM my_table
WHERE Key1 > 1 AND Key2 >= "One";
```
