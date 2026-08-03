---
title: "ORDER BY"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/order_by?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/order_by"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/order_by.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/order_by.md"
description: "Сортировка результата SELECT по разделенному запятыми перечню критериев сортировки. В качестве критерия может выступать значение столбца, или выражение над стол"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# ORDER BY

Сортировка результата `SELECT` по разделенному запятыми перечню критериев сортировки. В качестве критерия может выступать значение столбца, или выражение над столбцами. Не поддерживается указание порядкового номера колонки выборки (`ORDER BY N`, где `N` - номер).

Направление сортировки может быть указано после каждого критерия:

- `ASC` — по возрастанию. Применяется по умолчанию.
- `DESC` — по убыванию.

Несколько критериев сортировки будут применены слева направо.

## Пример {#primer}

```yql
SELECT key, string_column
FROM my_table
ORDER BY key DESC, LENGTH(string_column) ASC;
```

Ключевое слово `ORDER BY` также может использоваться в механизме [оконных функций](window.md).
