---
title: "VIEW (INDEX)"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/secondary_index?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/secondary_index"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/secondary_index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/secondary_index.md"
description: "Чтобы сделать запрос SELECT по вторичному индексу строковой таблицы, используйте конструкцию: SELECT * FROM TableName VIEW IndexName WHERE …. Важно."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# VIEW (INDEX)

Чтобы сделать запрос `SELECT` по вторичному индексу строковой таблицы, используйте конструкцию:

```yql
SELECT *
    FROM TableName VIEW IndexName
    WHERE …
```

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц. Поддержка функциональности для [колоночных](../../../../concepts/datamodel/table.md#column-oriented-tables) таблиц находится в разработке.

## Примеры {#primery}

Выбрать все поля из строковой таблицы `series` по индексу `views_index` с условием `views >= someValue`:

```yql
SELECT series_id, title, info, release_date, views, uploaded_user_id
    FROM series VIEW views_index
    WHERE views >= someValue
```

Сделать [`JOIN`](join.md) строковых таблиц `series` и `users` c заданным полем `userName` по индексам `users_index` и `name_index` соответственно:

```yql
SELECT t1.series_id, t1.title
    FROM series VIEW users_index AS t1
    INNER JOIN users VIEW name_index AS t2
    ON t1.uploaded_user_id == t2.user_id
    WHERE t2.name == userName;
```
