---
title: "BATCH UPDATE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/batch-update?version=v26.1"
doc_path: "ru/yql/reference/syntax/batch-update"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/batch-update.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/batch-update.md"
description: "Совет. Перед тем как изучать BATCH UPDATE, рекомендуется ознакомиться со стандартным UPDATE."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# BATCH UPDATE

> [!TIP]
> Перед тем как изучать `BATCH UPDATE`, рекомендуется ознакомиться со стандартным [UPDATE](update.md).

`BATCH UPDATE` позволяет обновлять записи в таблицах большого размера, минимизируя риск отмены блокировок и отката транзакций за счёт ослабления гарантий. Обновление данных выполняется в виде серии транзакций для каждой [партиции](../../../concepts/datamodel/table.md#partitioning_row_table) указанной таблицы отдельно, обрабатывая по 10 000 строк за итерацию. Каждый запрос обрабатывает не более 10 партиций одновременно.

Данный запрос, как и стандартный `UPDATE`, выполняется синхронно и завершается с некоторым статусом. В случае возникновения ошибки или отключения клиента обновление данных останавливается, применённые изменения не откатываются.

Семантика наследуется от стандартного `UPDATE` с ограничениями:

- Поддерживается только для [строковых таблиц](../../../concepts/glossary.md#row-oriented-table).
- Поддерживается только в режиме [неявного контроля транзакций](../../../concepts/transactions.md#implicit).
- Поддерживаются только идемпотентные обновления: выражения после `SET` не должны зависеть от текущих значений изменяемых колонок.
- Запрещено использование подзапросов и нескольких выражений в одном запросе.
- Недоступно ключевое слово `RETURNING`.

## Пример {#primer}

```yql
BATCH UPDATE my_table
SET Value1 = "foo", Value2 = 0
WHERE Key1 > 1;
```
