---
title: "LIMIT и OFFSET"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/limit_offset?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/limit_offset"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/limit_offset.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/limit_offset.md"
description: "LIMIT ограничивает вывод указанным количеством строк. Если значение лимита равно NULL, или LIMIT не указан, то вывод не ограничен."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# LIMIT и OFFSET

`LIMIT` ограничивает вывод указанным количеством строк. Если значение лимита равно `NULL`, или `LIMIT` не указан, то вывод не ограничен.

`OFFSET` указывает отступ от начала (в строках). Если значение отступа равно `NULL`, или `OFFSET` не указан, то используется значение ноль.

## Примеры {#primery}

```yql
SELECT key FROM my_table
LIMIT 7;
```

```yql
SELECT key FROM my_table
LIMIT 7 OFFSET 3;
```

```yql
SELECT key FROM my_table
LIMIT 3, 7; -- эквивалентно предыдущему примеру
```

```yql
SELECT key FROM my_table
LIMIT NULL OFFSET NULL; -- эквивалентно SELECT key FROM my_table
```
