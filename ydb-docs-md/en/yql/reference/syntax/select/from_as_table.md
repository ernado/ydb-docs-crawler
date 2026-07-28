---
title: "FROM AS_TABLE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/select/from_as_table?version=v26.1"
doc_path: "en/yql/reference/syntax/select/from_as_table"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/select/from_as_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/select/from_as_table.md"
description: "Accessing named expressions as tables using the AS_TABLE function."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# FROM AS_TABLE

Accessing named expressions as tables using the `AS_TABLE` function.

`AS_TABLE($variable)` lets you use the value of `$variable` as the data source for the query. In this case, the variable `$variable` must have the type `List<Struct<...>>`.

## Example

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

SELECT Key, Value FROM AS_TABLE($data);
```

You should either explicitly specify the modifiable columns in both the source and the target when using expressions with modifying queries such as [UPSERT INTO](../upsert_into.md) or [INSERT INTO](../insert_into.md):

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

INSERT INTO `my_table` (Key, Value) SELECT Key, Value FROM AS_TABLE($data);
```

Or you should omit them completely:

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

INSERT INTO `my_table` SELECT * FROM AS_TABLE($data);
```
