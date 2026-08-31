---
title: "Группы колонок"
url: "https://ydb.tech/docs/ru/yql/reference/syntax/create_table/family?version=v26.1"
doc_path: "ru/yql/reference/syntax/create_table/family"
version: "v26.1"
lang: "ru"
source_path: "ru/core/yql/reference/syntax/create_table/family.md"
vcs_url: "https://github.com/ydb-platform/ydb/tree/main/ydb/docs/ru/core/yql/reference/syntax/create_table/family.md"
description: "Важно. Поддерживается только для строковых таблиц. Колонки одной таблицы можно объединять в группы, чтобы задать следующие параметры:"
revision: "7580679a5c9e32c15be9989745f34e270cb4e4f1"
---

# Группы колонок

> [!WARNING]
> Поддерживается только для [строковых](../../../../concepts/datamodel/table.md#row-oriented-tables) таблиц.

Колонки одной таблицы можно объединять в группы, чтобы задать следующие параметры:

- `DATA` — тип устройства хранения для данных колонок этой группы. Допустимые значения: `"ssd"`, `"rot"`.
- `COMPRESSION` — кодек сжатия данных. Допустимые значения: `"off"`, `"lz4"`.
- `CACHE_MODE` — [режим кэширования](../../../../concepts/datamodel/table.md#cache-modes). Допустимые значения: `"in_memory"`, `"regular"`.

По умолчанию все колонки находятся в одной группе с именем `default`. При необходимости параметры этой группы тоже можно переопределить. В противном случае применяются предопределённые значения.

## Пример {#primer}

В примере ниже для создаваемой таблицы добавляется группа колонок `family_large`, которая устанавливается для колонки `series_info`, а также переопределяются параметры для группы `default`, которая по умолчанию применяется ко всем остальным колонкам:

```yql
CREATE TABLE series_with_families (
    series_id Uint64,
    title Utf8,
    series_info Utf8 FAMILY family_large,
    release_date Uint64,
    PRIMARY KEY (series_id),
    FAMILY default (
        DATA = "ssd",
        COMPRESSION = "off",
        CACHE_MODE = "in_memory"
    ),
    FAMILY family_large (
        DATA = "rot",
        COMPRESSION = "lz4",
        CACHE_MODE = "regular"
    )
);
```

> [!NOTE]
> Доступные типы устройств хранения зависят от конфигурации кластера YDB.
