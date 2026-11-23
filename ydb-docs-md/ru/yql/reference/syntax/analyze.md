---
title: "ANALYZE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/analyze?version=v26.1"
doc_path: "ru/yql/reference/syntax/analyze"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/analyze.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/analyze.md"
description: "ANALYZE принудительно запускает сбор статистики для стоимостного оптимизатора YDB. Синтаксис. ANALYZE <path_to_table> [ (<column_name> [,...]) ]."
revision: "5783baf4a26ccb796054e5b5f3109cb157158102"
---

# ANALYZE

`ANALYZE` принудительно запускает сбор статистики для [стоимостного оптимизатора YDB](../../../concepts/query_execution/optimizer.md).

## Синтаксис {#sintaksis}

```yql
ANALYZE <path_to_table> [ (<column_name> [, ...]) ]
```

Эта команда принудительно запускает синхронный сбор статистики таблицы и статистики столбцов для указанных столбцов или для всех столбцов, если столбцы не указаны. `ANALYZE` возвращает результат после сбора и обновления всей запрашиваемой статистики.

- `path_to_table` — путь к таблице, для которой должна быть собрана статистика.
- `column_name` — сбор статистики столбцов только для указанных столбцов таблицы.

Текущий набор статистики описан в [Статистики для стоимостного оптимизатора](../../../concepts/query_execution/optimizer.md#statistics).
