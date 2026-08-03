---
title: "FROM AS_TABLE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/select/from_as_table?version=v26.1"
doc_path: "ru/yql/reference/syntax/select/from_as_table"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/select/from_as_table.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/select/from_as_table.md"
description: "Обращение к именованным выражениям как к таблицам с помощью функции AS_TABLE."
revision: "95f7629e80402dd261127ed00cdc781d2b8433de"
---

# FROM AS_TABLE

Обращение к именованным выражениям как к таблицам с помощью функции `AS_TABLE`.

`AS_TABLE($variable)` позволяет использовать значение `$variable` в качестве источника данных для запроса. При этом переменная `$variable` должна иметь тип `List<Struct<...>>`.

## Пример {#primer}

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

SELECT Key, Value FROM AS_TABLE($data);
```

При совместном использовании с другими операторами изменения данных, такими как [UPSERT INTO](../upsert_into.md) или [INSERT INTO](../insert_into.md), необходимо или указывать модифицируемые колонки и в источнике, и в приемнике:

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

INSERT INTO `my_table` (Key, Value) SELECT Key, Value FROM AS_TABLE($data);
```

Или не указывать их вовсе:

```yql
$data = AsList(
    AsStruct(1u AS Key, "v1" AS Value),
    AsStruct(2u AS Key, "v2" AS Value),
    AsStruct(3u AS Key, "v3" AS Value));

INSERT INTO `my_table` SELECT * FROM AS_TABLE($data);
```
