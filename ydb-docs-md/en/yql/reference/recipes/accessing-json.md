---
title: "Accessing values inside JSON with YQL"
url: "https://ydb.tech/docs/en/yql/reference/recipes/accessing-json?version=v26.1"
doc_path: "en/yql/reference/recipes/accessing-json"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/recipes/accessing-json.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/recipes/accessing-json.md"
description: "YQL provides two main ways to retrieve values from JSON:"
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Accessing values inside JSON with YQL

YQL provides two main ways to retrieve values from JSON:

- Using [**JSON functions from the SQL standard**](../builtins/json.md). This approach is recommended for simple cases and for teams that are familiar with them from other DBMSs.
- Using [**Yson UDF**](../udf/list/yson.md), [list](../builtins/list.md) and [dict](../builtins/dict.md) builtins, and [lambdas](../syntax/expressions.md#lambda). This approach is more flexible and tightly integrated with YDB's data type system, thus recommended for complex cases.

Below are the recipes that will use the same input JSON to demonstrate how to use each option to check whether a key exists, get a specific value, and retrieve a subtree.

## JSON functions

```yql
$json = @@{
    "friends": [
        {
            "name": "James Holden",
            "age": 35
        },
        {
            "name": "Naomi Nagata",
            "age": 30
        }
    ]
}@@j;

SELECT
    JSON_EXISTS($json, "$.friends[*].name"), -- True
    CAST(JSON_VALUE($json, "$.friends[0].age") AS Int32), -- 35
    JSON_QUERY($json, "$.friends[0]"); -- {"name": "James Holden", "age": 35}
```

`JSON_*` functions expect the `Json` data type as an input to run. In this example, the string literal has the suffix `j`, marking it as `Json`. In tables, data could be stored in either JSON format or as a string representation. To convert data from `String` to `JSON` data type, use the `CAST` function, such as `CAST(my_string AS JSON)`.

## Yson UDF

This approach typically combines multiple functions and expressions, so a query might leverage different specific strategies.

### Convert the whole JSON to YQL containers

```yql
$json = @@{
    "friends": [
        {
            "name": "James Holden",
            "age": 35
        },
        {
            "name": "Naomi Nagata",
            "age": 30
        }
    ]
}@@j;

$containers = Yson::ConvertTo($json, Struct<friends:List<Struct<name:String?,age:Int32?>>>);
$has_name = ListAny(
    ListMap($containers.friends, ($friend) -> {
        return $friend.name IS NOT NULL;
    })
);
$get_age = $containers.friends[0].age;
$get_first_friend = Yson::SerializeJson(Yson::From($containers.friends[0]));

SELECT
    $has_name, -- True
    $get_age, -- 35
    $get_first_friend; -- {"name": "James Holden", "age": 35}
```

It is **not** necessary to convert the whole JSON object to a structured combination of containers. Some fields can be omitted if not used, while some subtrees could be left in an unstructured data type like `Json`.

### Work with in-memory representation

```yql
$json = @@{
    "friends": [
        {
            "name": "James Holden",
            "age": 35
        },
        {
            "name": "Naomi Nagata",
            "age": 30
        }
    ]
}@@j;

$has_name = ListAny(
    ListMap(Yson::ConvertToList($json.friends), ($friend) -> {
        return Yson::Contains($friend, "name");
    })
);
$get_age = Yson::ConvertToInt64($json.friends[0].age);
$get_first_friend = Yson::SerializeJson($json.friends[0]);

SELECT
    $has_name, -- True
    $get_age, -- 35
    $get_first_friend; -- {"name": "James Holden", "age": 35}
```

## See also

- [Modifying JSON with YQL](modifying-json.md)
