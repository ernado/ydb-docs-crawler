---
title: "DISTINCT"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/distinct?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/distinct"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/distinct.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/distinct.md"
description: "Выбор уникальных строк. Примечание."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# DISTINCT

Выбор уникальных строк.

> [!NOTE]
> Применение `DISTINCT` к вычислимым значениям на данный момент не реализовано. С этой целью можно использовать подзапрос или выражение [`GROUP BY ... AS ...`](group-by.md).

## Пример {#primer}

```yql
SELECT DISTINCT value -- только уникальные значения из таблицы
FROM my_table;
```

Также ключевое слово `DISTINCT` может использоваться для применения [агрегатных функций](../../builtins/aggregation.md) только к уникальным значениям. Подробнее см. в документации по [GROUP BY](group-by.md).
