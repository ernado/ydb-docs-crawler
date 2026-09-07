---
title: "ALTER DATABASE"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_database/?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_database/"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_database/index.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_database/index.md"
description: "Изменяет настройки базы данных. Синтаксис. ALTER DATABASE path action; Параметры. path — путь к базе данных;"
revision: "be5a7d10b3ef95ed6c3f719d85a8cf83cd01dff2"
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
