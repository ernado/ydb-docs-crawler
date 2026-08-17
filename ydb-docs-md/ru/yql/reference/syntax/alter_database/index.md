---
title: "ALTER DATABASE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_database/?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_database/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_database/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_database/index.md"
description: "Изменяет настройки базы данных. Синтаксис. ALTER DATABASE path action; Параметры. path — путь к базе данных;"
revision: "6cf79b202d43efced4776d730126c3952ec44c6d"
---

# ALTER DATABASE

Изменяет настройки базы данных.

## Синтаксис {#sintaksis}

```yql
ALTER DATABASE path action;
```

### Параметры {#parametry}

- `path` — путь к базе данных;

- `action` — любое действие по изменению базы данных, из описанных ниже:

  - [Изменение владельца базы данных](owner.md).
  - [Изменение настроек базы данных](settings.md).
