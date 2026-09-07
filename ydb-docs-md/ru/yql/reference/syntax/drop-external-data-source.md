---
title: "DROP EXTERNAL DATA SOURCE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-external-data-source?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-external-data-source"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-external-data-source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-external-data-source.md"
description: "Удаляет указанный внешний источник данных. Если внешнего источника данных с таким именем не существует, возвращается ошибка. Пример."
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
---

# DROP EXTERNAL DATA SOURCE

Удаляет указанный [внешний источник данных](../../../concepts/datamodel/external_data_source.md).

Если внешнего источника данных с таким именем не существует, возвращается ошибка.

## Пример {#primer}

```yql
DROP EXTERNAL DATA SOURCE my_external_data_source;
```
