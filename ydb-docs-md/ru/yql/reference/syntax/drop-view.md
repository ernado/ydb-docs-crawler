---
title: "DROP VIEW"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/drop-view?version=v26.1"
doc_path: "ru/yql/reference/syntax/drop-view"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/drop-view.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/drop-view.md"
description: "DROP VIEW удаляет представление. Синтаксис. DROP VIEW [ IF EXISTS ] <имя>. Параметры."
revision: "610144200e326713a5926ef40527cb973f94a519"
---

# DROP VIEW

`DROP VIEW` удаляет [представление](../../../concepts/datamodel/view.md).

## Синтаксис {#sintaksis}

```yql
DROP VIEW [IF EXISTS] <имя>
```

### Параметры {#parametry}

- `IF EXISTS` - при использовании этой конструкции, выражение не возвращает ошибку, если представления с указанным именем не существует.
- `имя` - имя представления, подлежащего удалению.

## Примеры {#primery}

Следующая команда удалит представление со списком современных сериалов:

```yql
DROP VIEW recent_series;
```

## См. также {#sm-takzhe}

- [CREATE VIEW](create-view.md)
- [ALTER VIEW](alter-view.md)
