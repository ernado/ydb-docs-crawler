---
title: "ALTER VIEW"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter-view?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter-view"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter-view.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter-view.md"
description: "ALTER VIEW изменяет определение представления. Важно. Это команда не поддерживается в текущей версии YDB."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# ALTER VIEW

`ALTER VIEW` изменяет определение [представления](../../../concepts/datamodel/view.md).

> [!WARNING]
> Это команда не поддерживается в текущей версии YDB.

Для переопределения представления можно его удалить и воссоздать с другим определением:

```yql
DROP VIEW redefined_view;
CREATE VIEW redefined_view ...;
```

Обратите внимание, что эти две инструкции выполняются отдельно, в отличие от одной инструкции `ALTER VIEW`. При изменении представления таким образом его может быть видно в удалённом состоянии на короткий момент.

## См. также {#sm-takzhe}

- [CREATE VIEW](create-view.md)
- [DROP VIEW](drop-view.md)
