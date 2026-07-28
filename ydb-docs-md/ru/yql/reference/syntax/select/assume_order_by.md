---
title: "ASSUME ORDER BY"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/assume_order_by?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/assume_order_by"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/assume_order_by.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/assume_order_by.md"
description: "Проверка сортированности результата SELECT по значению в указанном столбце или нескольких столбцах. Результат такого SELECT -а будет считаться сортированным, но"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ASSUME ORDER BY

Проверка сортированности результата `SELECT` по значению в указанном столбце или нескольких столбцах. Результат такого `SELECT`-а будет считаться сортированным, но без выполнения фактической сортировки. Проверка сортированности осуществляется на этапе исполнения запроса.

Как и для `ORDER BY`, поддерживается задание порядка сортировки с помощью ключевых слов `ASC` (по возрастанию) и `DESC` (по убыванию). Выражения в `ASSUME ORDER BY` не поддерживается.

## Примеры {#primery}

```yql
SELECT key || "suffix" as key, -CAST(subkey as Int32) as subkey
FROM my_table
ASSUME ORDER BY key, subkey DESC;
```
