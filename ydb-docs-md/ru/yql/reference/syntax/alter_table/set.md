---
title: "Изменение дополнительных параметров таблиц"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/alter_table/set?version=v26.1"
doc_path: "ru/yql/reference/syntax/alter_table/set"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/alter_table/set.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/alter_table/set.md"
description: "Большинство параметров строковых и колоночных таблиц в YDB, приведенных на странице описания таблицы, можно изменить командой ALTER."
revision: "e9f541853a7760e5c0d0babc071d86df7f523cf5"
---

# Изменение дополнительных параметров таблиц

Большинство параметров строковых и колоночных таблиц в YDB, приведенных на странице [описания таблицы](../../../../concepts/datamodel/table.md), можно изменить командой `ALTER`.

В общем случае команда для изменения любого параметра таблицы выглядит следующим образом:

```yql
ALTER TABLE table_name SET (key = value);
```

`key` — имя параметра, `value` — его новое значение.

Пример изменения параметра `TTL`, отвечающего за время жизни записей в таблицы:

```yql
ALTER TABLE series SET (TTL = Interval("PT0S") ON expire_at);
```

## Сброс дополнительных параметров таблицы {#additional-reset}

Некоторые параметры таблиц в YDB, приведенные на странице [описания таблицы](../../../../concepts/datamodel/table.md), можно сбросить командой `ALTER`. Команда для сброса параметра таблиц выглядит следующим образом:

```yql
ALTER TABLE table_name RESET (key);
```

`key` — имя параметра.

Например, такая команда сбросит (удалит) настройки TTL для строковых или колоночных таблиц:

```yql
ALTER TABLE series RESET (TTL);
```
