---
title: "Modifying JSON with YQL"
url: "https://ydb.tech/docs/en/yql/reference/recipes/modifying-json?version=v26.1"
doc_path: "en/yql/reference/recipes/modifying-json"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/recipes/modifying-json.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/recipes/modifying-json.md"
description: "In memory, YQL operates on immutable values. Thus, when a query needs to change something inside a JSON value, the mindset should be about constructing a new va"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Modifying JSON with YQL

In memory, YQL operates on immutable values. Thus, when a query needs to change something inside a JSON value, the mindset should be about constructing a new value from pieces of the old one.

This example query takes an input JSON named `$fields`, parses it, substitutes key `a` with 0, drops key `d`, and adds a key `c` with value 3:

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

## See also

- [Yson](../udf/list/yson.md)
- [Functions for lists](../builtins/list.md)
- [Functions for dictionaries](../builtins/dict.md)
- [Accessing values inside JSON with YQL](accessing-json.md)
