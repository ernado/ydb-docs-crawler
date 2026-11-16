---
title: "DROP EXTERNAL DATA SOURCE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-external-data-source?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-external-data-source"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-external-data-source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-external-data-source.md"
description: "Deletes the specified external data source. If no external data source with that name exists, an error is returned. Example."
revision: "7d1701f96bbb0c1cd62ff0890f67a9b86caf1d5e"
---

# DROP EXTERNAL DATA SOURCE

Deletes the specified [external data source](../../../concepts/datamodel/external_data_source.md).

If no external data source with that name exists, an error is returned.

## Example

```yql
DROP EXTERNAL DATA SOURCE my_external_data_source;
```
