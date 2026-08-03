---
title: "FROM ... SELECT ..."
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/from_select?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/from_select"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/from_select.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/from_select.md"
description: "FROM... SELECT... Перевернутая форма записи, в которой сначала указывается источник данных, а затем — операция. Примеры. FROM my_table SELECT key, value;"
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# FROM ... SELECT ...

Перевернутая форма записи, в которой сначала указывается источник данных, а затем — операция.

## Примеры {#primery}

```yql
FROM my_table SELECT key, value;
```

```yql
FROM a_table AS a
JOIN b_table AS b
USING (key)
SELECT *;
```
