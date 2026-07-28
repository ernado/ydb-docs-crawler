---
title: "Изменение владельца базы данных"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_database/owner?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_database/owner"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_database/owner.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_database/owner.md"
description: "Изменяет владельца базы данных. Выполнить операцию может только администратор базы данных. Синтаксис. ALTER DATABASE path OWNER TO user_name; Параметры."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Изменение владельца базы данных

Изменяет владельца базы данных. Выполнить операцию может только администратор базы данных.

## Синтаксис {#sintaksis}

```yql
ALTER DATABASE path OWNER TO user_name;
```

### Параметры {#parametry}

- `path` — путь к базе данных;
- `user_name` — имя пользователя, который станет владельцем базы данных.

## Примеры {#primery}

Владельцем базы данных `/Root/test` становится пользователь `user1`:

```yql
ALTER DATABASE `/Root/test` OWNER TO user1;
```
