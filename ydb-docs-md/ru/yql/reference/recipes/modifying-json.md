---
title: "Изменение JSON с помощью YQL"
url: "https://ydb.tech/docs/ru/yql/reference/recipes/modifying-json?version=v26.1"
doc_path: "ru/yql/reference/recipes/modifying-json"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/recipes/modifying-json.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/recipes/modifying-json.md"
description: "В памяти YQL работает с неизменяемыми значениями. Таким образом, когда запросу нужно изменить что-то внутри значения JSON, следует думать об этом как о создании"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Изменение JSON с помощью YQL

В памяти YQL работает с неизменяемыми значениями. Таким образом, когда запросу нужно изменить что-то внутри значения JSON, следует думать об этом как о создании нового значения из частей старого.

Данный пример запроса принимает входной JSON названный `$fields`, парсит его, заменяет ключ `a` на 0, удаляет ключ `d` и добавляет ключ `c` со значением 3:

```yql
$fields = '{"a": 1, "b": 2, "d": 4}'j;
$pairs = DictItems(Yson::ConvertToInt64Dict($fields));
$result_pairs = ListExtend(ListNotNull(ListMap($pairs, ($item) -> {
    $item = if ($item.0 == "a", ("a", 0), $item);
    return if ($item.0 == "d", null, $item);
})), [("c", 3)]);
$result_dict = ToDict($result_pairs);
SELECT Yson::SerializeJson(Yson::From($result_dict));
```

## Смотрите также {#smotrite-takzhe}

- [Yson](../udf/list/yson.md)
- [Функции для работы со списками](../builtins/list.md)
- [Функции для работы со словарями](../builtins/dict.md)
- [Доступ к значениям в JSON с помощью YQL](accessing-json.md)
