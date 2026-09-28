---
title: "DROP EXTERNAL DATA SOURCE"
url: "https://ydb.tech/docs/en/yql/reference/syntax/drop-external-data-source?version=v26.1"
doc_path: "en/yql/reference/syntax/drop-external-data-source"
version: "v26.1"
lang: "en"
source_path: "en/core/yql/reference/syntax/drop-external-data-source.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/en/core/yql/reference/syntax/drop-external-data-source.md"
description: "Deletes the specified external data source. If no external data source with that name exists, an error is returned. Example."
revision: "8c7501e02fd7c6de0c7110aafa90f78948400f1e"
---

# DROP EXTERNAL DATA SOURCE

Deletes the specified [external data source](../../../concepts/datamodel/external_data_source.md).

If no external data source with that name exists, an error is returned.

## Example

```yql
DROP EXTERNAL DATA SOURCE my_external_data_source;
```
