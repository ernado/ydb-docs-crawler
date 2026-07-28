---
title: "Изменение настроек базы данных"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_database/settings?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_database/settings"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_database/settings.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_database/settings.md"
description: "Изменяет настройки базы данных. Выполнить операцию может только администратор базы данных. Синтаксис. ALTER DATABASE path SET ( key = value,...). Параметры."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Изменение настроек базы данных

Изменяет настройки базы данных. Выполнить операцию может только администратор базы данных.

## Синтаксис {#sintaksis}

```yql
ALTER DATABASE path SET (key = value, ...)
```

### Параметры {#parametry}

- `path` — путь к базе данных.

- `key` — имя изменяемой настройки:

  - `MAX_PATHS` — [максимальное количество путей](../../../../concepts/limits-ydb.md#schema-object) (объектов в схеме) в базе данных.
  - `MAX_SHARDS` — [максимальное количество таблеток](../../../../concepts/limits-ydb.md#schema-object) в базе данных.
  - `MAX_CHILDREN_IN_DIR` — [максимальное количество объектов в директории](../../../../concepts/limits-ydb.md#schema-object).
  - `MAX_SHARDS_IN_PATH` — [максимальное количество таблеток, ассоциированных с одним объектом схемы](../../../../concepts/limits-ydb.md#schema-object). Например, максимальное количество партиций одной таблицы.

- `value` — значение изменяемой настройки.

## Примеры {#primery}

Изменение ограничения на максимальное количество путей (объектов в схеме) в базе данных `/Root/test`:

```yql
ALTER DATABASE `/Root/test` SET (MAX_PATHS = 20000);
```
